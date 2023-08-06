from thompcoutils.log_utils import get_logger
from thompcoutils.test_utils import assert_test
from thompcoutils.cron_time import CronTime
import thompcoutils.file_utils as file_utils
import datetime
import sys
from builtins import staticmethod
import ast
from configparser import ConfigParser, NoOptionError, NoSectionError, DuplicateSectionError
import os
import logging
from dateutil import parser


class ConfigException(Exception):
    pass


class EmailConnectionConfig:
    def __init__(self, cfg_mgr=None, username=None, password=None, from_user=None, smtp_host="smtp.gmail.com",
                 smtp_port=587, application_name="Application Name", section_heading="email connection",
                 username_tag="username", password_tag="password", from_tag="from", smtp_host_tag="smtp_host",
                 smtp_port_tag="smtp_port"):

        if cfg_mgr is None:
            self.username = username
            self.password = password
            self.from_user = from_user
            self.smtp_host = smtp_host
            self.smtp_port = smtp_port
        else:
            self.username = cfg_mgr.read_entry(section_heading, username_tag, "myname@google.com")
            self.password = cfg_mgr.read_entry(section_heading, password_tag, "mySecretPassword")
            self.from_user = cfg_mgr.read_entry(section_heading, from_tag, application_name,
                                                "Where the email will come from")
            self.smtp_host = cfg_mgr.read_entry(section_heading, smtp_host_tag, smtp_host)
            self.smtp_port = cfg_mgr.read_entry(section_heading, smtp_port_tag, smtp_port)


class HiLow:
    """
    HiLow class provides a config file to store low and hi values.  If a low value for a tag/entry is lower than the
    existing value, it will be updated.  Similarly, if a hi value for is higher than the existing hi value, it will be
    updated.
    """
    smallest = -sys.maxsize-1
    biggest = sys.maxsize
    hi_tag = "hi"
    low_tag = "low"
    last_tag = "last"
    low_changed_tag = "low_changed"
    hi_changed_tag = "hi_changed"
    last_changed_tag = "last_changed"
    direction_tag = "direction"
    change_amount_tag = "change_amount"

    class Direction(enumerate):
        Up = "up"
        Down = "down"
        NoChange = "no change"

        @staticmethod
        def validate(string):
            if string == str(HiLow.Direction.Up):
                return HiLow.Direction.Up
            elif string == str(HiLow.Direction.Down):
                return HiLow.Direction.Down
            elif string == str(HiLow.Direction.NoChange):
                return HiLow.Direction.NoChange
            else:
                raise ConfigException("{} not recognized as a HiLow.Direction".format(string))

    def __init__(self, file_name):
        """
        :param file_name: name of the file to store values
        """
        self.file_name = file_name
        if not os.path.exists(file_name):
            file_utils.touch(file_name)
        self.cfg_mgr = ConfigManager(file_name)

    def read_values(self, entry):
        """
        gets the current values for a tag/entry
        :param entry: tag/entry`
        :return: a dictionary of values (i.e. {"hi": 10, "low": 2} )
        """
        try:
            hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, default_value=self.smallest)
        except ValueError:
            hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, default_value=self.smallest + .01)
        try:
            low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, default_value=self.biggest)
        except ValueError:
            low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, default_value=self.biggest - .01)
        hi_changed_time = self.cfg_mgr.read_entry(section=entry, entry=self.hi_changed_tag,
                                                  default_value=datetime.datetime.now())
        low_changed_time = self.cfg_mgr.read_entry(section=entry, entry=self.low_changed_tag,
                                                   default_value=datetime.datetime.now())

        direction = self.cfg_mgr.read_entry(section=entry, entry=self.direction_tag,
                                            default_value=str(self.Direction.NoChange))
        direction = self.Direction.validate(direction)

        try:
            last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, default_value=0)
        except ValueError:
            last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, default_value=0.01)

        try:
            changed_amount = self.cfg_mgr.read_entry(section=entry, entry=self.change_amount_tag, default_value=0)
        except ValueError:
            changed_amount = self.cfg_mgr.read_entry(section=entry, entry=self.change_amount_tag, default_value=0.01)
        last_changed = self.cfg_mgr.read_entry(section=entry, entry=self.last_changed_tag,
                                               default_value=datetime.datetime.now())
        return {self.hi_tag: hi, self.low_tag: low,
                self.low_changed_tag: low_changed_time, self.hi_changed_tag: hi_changed_time,
                self.last_tag: last, self.last_changed_tag: last_changed, self.direction_tag: direction,
                self.change_amount_tag: changed_amount}

    def write_value(self, entry, value):
        try:
            self.cfg_mgr.config.add_section(entry)
        except DuplicateSectionError:
            pass

        try:
            cfg_last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, default_value=0)
        except ValueError:
            cfg_last = self.cfg_mgr.read_entry(section=entry, entry=self.last_tag, default_value=.01)
        if value < cfg_last:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=cfg_last-value)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.Down)
            try:
                cfg_low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, default_value=self.biggest)
            except ValueError:
                cfg_low = self.cfg_mgr.read_entry(section=entry, entry=self.low_tag, default_value=self.biggest - .01)
            if value < cfg_low:
                self.cfg_mgr.write_entry(section=entry, entry=self.low_changed_tag, value=datetime.datetime.now())
                self.cfg_mgr.write_entry(section=entry, entry=self.low_tag, value=value)
        elif value > cfg_last:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=value-cfg_last)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.Up)
            try:
                cfg_hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, default_value=self.smallest)
            except ValueError:
                cfg_hi = self.cfg_mgr.read_entry(section=entry, entry=self.hi_tag, default_value=self.smallest + .01)
            if value > cfg_hi:
                self.cfg_mgr.write_entry(section=entry, entry=self.hi_changed_tag, value=datetime.datetime.now())
                self.cfg_mgr.write_entry(section=entry, entry=self.hi_tag, value=value)
        else:
            self.cfg_mgr.write_entry(section=entry, entry=self.change_amount_tag, value=0)
            self.cfg_mgr.write_entry(section=entry, entry=self.direction_tag, value=self.Direction.NoChange)
        self.cfg_mgr.write_entry(section=entry, entry=self.last_tag, value=value)
        self.cfg_mgr.write_entry(section=entry, entry=self.last_changed_tag, value=datetime.datetime.now())
        self.cfg_mgr.write(out_file=self.file_name, stop=False, overwrite=True)
        return self.read_values(entry)


class ConfigManager:
    def __init__(self, file_name, title=None, create=False):
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.create = create
        if not create:
            if os.path.exists(file_name):
                self.config.read(file_name)
            else:
                raise FileNotFoundError("File {} does not exist!".format(file_name))
        self.notes = []
        self.title = title
        self.values = {}

    @staticmethod
    def missing_entry(section, entry, file_name, default_value=None):
        logger = get_logger()
        logger.debug("starting")
        if default_value is None:
            log_fn = logger.critical
            message = "Required entry"
            default_value = ""
        else:
            log_fn = logger.debug
            message = "Entry"
            if default_value == "":
                default_value = "Ignoring."
            else:
                default_value = "Using default value of (" + str(default_value) + ")"
        log_fn(message + " \"" + entry + "\" in section [" + section + "] in file: " + file_name
               + " is malformed or missing.  " + str(default_value))
        if default_value == "":
            log_fn("Exiting now")
            sys.exit()

    @staticmethod
    def _insert_note(lines, line_number, note):
        if "\n" in note:
            message = note.split("\n")
        else:
            message = note
        if message is None:
            pass
        elif type(message) == str:
            lines.insert(line_number, "# " + message + ":\n")
        else:
            for line in message[:-1]:
                lines.insert(line_number, "# " + line + "\n")
                line_number += 1
            lines.insert(line_number, "# " + message[-1] + ":\n")

    def read_entry(self, section, entry, default_value, notes=None, value_type=None, use_default_if_missing=True):
        logger = get_logger()
        value = default_value
        if self.create:
            try:
                self.config.add_section(section)
            except DuplicateSectionError:
                pass
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": entry,
                                   "notes": notes})
            self.config.set(section, entry, str(default_value))
        else:
            if default_value is None:
                if value_type is None:
                    raise ConfigException("if default_value=None, value_type must be set")
                default_value = value_type
            try:
                if isinstance(default_value, str):
                    value = self.config.get(section, entry)
                elif isinstance(default_value, bool):
                    value = self.config.getboolean(section, entry)
                elif isinstance(default_value, int):
                    value = self.config.getint(section, entry)
                elif isinstance(default_value, float):
                    value = self.config.getfloat(section, entry)
                elif isinstance(default_value, dict):
                    value = ast.literal_eval(self.config.get(section, entry))
                elif isinstance(default_value, list):
                    value = ast.literal_eval(self.config.get(section, entry))
                elif isinstance(default_value, datetime.datetime):
                    value = parser.parse(self.config.get(section, entry))
                elif isinstance(default_value, CronTime):
                    format_entry = '{}_format'.format(entry)
                    time_entry = '{}_time'.format(entry)
                    try:
                        time_format = self.config.get(section, format_entry)
                    except NoOptionError:
                        raise ConfigException('{} missing for entry {} under section {}', format_entry, entry, section)
                    try:
                        value = self.config.get(section, time_entry)
                    except NoOptionError:
                        raise ConfigException('{} missing for entry {} under section {}', time_entry, entry, section)
                    value = CronTime.strfpcrontime(value, time_format)
                else:
                    raise ConfigException("type {} not handled for ()".format(type(default_value), default_value))
            except NoOptionError:
                logger.debug("Entry {} in section [{}] is missing.  Using default value of {}".format(entry, section,
                                                                                                      default_value))
                if not use_default_if_missing:
                    value = None
            except NoSectionError:
                logger.debug("section [{}] is missing.  Using default value of {}".format(section, default_value))
                if not use_default_if_missing:
                    value = None
        return value

    def write_entry(self, section, entry, value, note=None, format_string=None):
        try:
            if isinstance(value, CronTime):
                self.config.set(section, '{}_format'.format(entry), format_string.replace('%', '%%'))
                self.config.set(section, '{}_time'.format(entry), value.strfcrontime(format_string))
            else:
                self.config.set(section, str(entry), str(value))
        except DuplicateSectionError:
            self.config.add_section(section)
            self.config.set(section, str(entry), str(value))

        if note is not None:
            self.notes.append({"section": section,
                               "entry": entry,
                               "notes": note})

    def read_section(self, section, default_entries, notes=None):
        key_values = default_entries
        if self.create:
            try:
                self.config.add_section(section)
            except DuplicateSectionError:
                pass
            for entry in default_entries:
                self.config.set(section, str(entry), str(default_entries[entry]))
            if notes is not None:
                self.notes.append({"section": section,
                                   "entry": None,
                                   "notes": notes})
        else:
            key_values = dict()
            for (key, val) in self.config.items(section):
                key_values[key] = val
        return key_values

    def write(self, out_file, stop=True, overwrite=False):
        if os.path.isfile(out_file) and not overwrite:
            raise ConfigException("File {} exists!  You must remove it before running this".format(out_file))
        f = open(out_file, "w")
        self.config.write(f)
        f.close()
        f = open(out_file)
        lines = f.readlines()
        f.close()
        if self.title is not None:
            ConfigManager._insert_note(lines, 0, self.title)
        for note in self.notes:
            in_section = False
            line_number = 0
            for line in lines:
                if "[" + note["section"] + "]" in line:
                    if note["entry"] is None:
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                    else:
                        in_section = True
                elif line.startswith("[") and line.endswith("]"):
                    in_section = False
                if in_section:
                    if line.startswith(note["entry"]):
                        ConfigManager._insert_note(lines, line_number, note["notes"])
                        break
                line_number += 1
        f = open(out_file, "w")
        contents = "".join(lines)
        f.write(contents)
        f.close()
        if stop:
            print("Done writing {} configuration file.  Stopping execution, please re-run".format(out_file))
            sys.exit()


def _test_replace(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    try:
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        # Safely write the changed content, if found in the file
        with open(filename, 'w') as f:
            print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)
    except Exception as e:
        raise e


def _test_email_connection_config(path):
    file_name = os.path.join(path, "test_email.ini")
    for write in [True, False]:
        if write:
            if os.path.isfile(file_name):
                os.remove(file_name)
        else:
            pass
        cfg_mgr = ConfigManager(file_name,
                                "This is the title of the ini file\n"
                                "You can have multiple lines if you use line breaks", write)
        email_connection = EmailConnectionConfig(cfg_mgr)
        print(email_connection.username)
        print(email_connection.password)
        print(email_connection.from_user)
        print(email_connection.smtp_host)
        print(email_connection.smtp_port)
        if write:
            test_file = file_name
            cfg_mgr.write(test_file, stop=False)
            contents = open(test_file, "r")
            print("File contents are:")
            print("====================================================")
            print(contents.read())
            print("====================================================")
            contents.close()


def _test_config_mgr(path):
    file_name = os.path.join(path, "test_config.ini")
    for write in [True, False]:
        if write:
            if os.path.isfile(file_name):
                os.remove(file_name)
        else:
            _test_replace(file_name, "Rover", "Baily")
        cfg_mgr = ConfigManager(file_name,
                                "This is the title of the ini file\n"
                                "You can have multiple lines if you use line breaks", write)
        first = cfg_mgr.read_entry("User 1", "date_time", datetime.datetime.now())
        second = cfg_mgr.read_entry("User 1", "first name", "Joe", "This is the first name")
        last = cfg_mgr.read_entry("User 1", "last name", "Brown", "This is the last name")
        age = cfg_mgr.read_entry("User 1", "age", 12)
        is_male = cfg_mgr.read_entry("User 1", "male", True)
        weight = cfg_mgr.read_entry("User 1", "weight", 23.5)
        values = cfg_mgr.read_entry("User 1", "values", {"height": 7.5, "weight": 10, "name": "Fred"})
        weights = cfg_mgr.read_entry("User 1", "weights", [23.5, 22])
        names = cfg_mgr.read_entry("User 1", "names", ["Joe", "Fred"])
        cfg_mgr.write_entry("User 1", "male", False)
        cfg_mgr.write_entry("User 1", "parent", "Fred")
        cfg_mgr.write_entry("User 1", "date_time", datetime.datetime.now())
        cfg_mgr.write_entry("User 1", "cron_time", CronTime(day_of_month=1, hour=2, minute=3), format_string='%d %H %M')
        section = cfg_mgr.read_section("user 2", {"first name": "Sally",
                                                  "last name": "Jones",
                                                  "age": 15,
                                                  "is_male": False,
                                                  "weight": 41.3},
                                       "You only get to add notes at the top of the section using this method")
        if write:
            test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
            assert_test(test1 == "Rover", "value should be Rover")
        else:
            test1 = cfg_mgr.read_entry("User 1", "dog name", "Rover")
            assert_test(test1 == "Baily", "value should be Rover")
            test2 = cfg_mgr.read_entry("User 1", "cat name", "Tinkerbell", use_default_if_missing=False)
            assert_test(test2 is None, "missing value should be none")
            val = cfg_mgr.read_entry("User 1", "cron_time", CronTime(day_of_month=1, hour=2, minute=3))
            assert_test(val.day_of_month == 1)
            assert_test(val.day_of_week == 0)
            assert_test(val.month == 0)
            assert_test(val.hour == 2)
            assert_test(val.minute == 3)

        print(first)
        print(second)
        print(last)
        print(age)
        print(is_male)
        print(weight)
        print(values)
        print(weights)
        print(names)
        print(section)
        if write:
            test_file = file_name
            cfg_mgr.write(test_file, stop=False)
            contents = open(test_file, "r")
            print("File contents are:")
            print("====================================================")
            print(contents.read())
            print("====================================================")
            contents.close()


def _test_hi_low_vals(file_name, section, value):
    hi_low = HiLow(file_name=file_name)
    hi_value = value
    places = 10
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(values[HiLow.change_amount_tag] > 1, "value should be large")

    diff = 1
    value -= diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Down, "Should be moving Down")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.hi_tag] == hi_value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.NoChange, "Should not be moving")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.hi_tag] == hi_value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(values[HiLow.change_amount_tag] == 0, "value has not changed")

    diff = 2
    value += diff
    values = hi_low.write_value(entry=section, value=value)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    diff = 1.1
    value += diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Up, "Should be moving Up")
    assert_test(values[HiLow.hi_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    diff = 10.1
    value -= diff
    hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(values[HiLow.direction_tag] == HiLow.Direction.Down, "Should be moving Down")
    assert_test(values[HiLow.low_tag] == value, "value should match")
    assert_test(values[HiLow.last_tag] == value, "value should match")
    assert_test(round(values[HiLow.change_amount_tag], places) == diff, "value should be {}".format(diff))

    value = 14
    vals = hi_low.write_value(entry=section, value=value)
    values = hi_low.read_values(entry=section)
    assert_test(vals == values, "values should match")


def _test_hi_low(path):
    file_name = os.path.join(path, "test_hi_low.ini")
    if os.path.isfile(file_name):
        os.remove(file_name)
    value = 50
    _test_hi_low_vals(file_name, "first", value)
    value = 60
    _test_hi_low_vals(file_name, "second", value)
    value = 40
    _test_hi_low_vals(file_name, "third", value)


if __name__ == "__main__":
    test_path = 'test'
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    log_configuration_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.ini')
    logging.config.fileConfig(log_configuration_file)
    _test_config_mgr(test_path)
    _test_email_connection_config(test_path)
    _test_hi_low(test_path)
    print("Done!")
