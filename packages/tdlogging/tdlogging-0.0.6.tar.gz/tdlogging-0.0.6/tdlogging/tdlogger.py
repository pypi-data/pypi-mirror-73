import os
import re
import threading
import traceback
import time

from tdlogging.tdprinter import TDPrinter, BoxPrinter
from tdlogging.tdreader import TDReader


def __user_prompt(question: str) -> bool:
    """
    A yes or no prompt I copied from stackoverflow
    :param question: Input Question
    :return: True or False
    """
    from distutils.util import strtobool

    while True:
        user_input = input(question + " [y/n]: ").lower()
        try:
            result = strtobool(user_input)
            return result
        except ValueError:
            print("Please use y/n or yes/no.\n")


def __verbose_print(message, verbose):
    if verbose:
        print(message)


def ApplyDecorators(target_dir, import_root, var_name="troppydash_logger", force=False, verbose=True):
    """
    DANGEROUS, use with caution\n
    Apply decorators to every python file in the Directory, and also marking the file\n
    :param verbose: Whether to log changes
    :param target_dir: Directory that is affected
    :param import_root: Python import name of your tdlogger instance, e.p. tdlogging.tdprinter
    :param var_name: Variable name of the TDLogger instance in your file
    :param force: Apply Changes without confirmation
    :return:
    """
    comment = "## Edited by TDLogger"
    import_line = "from {} import {}".format(import_root, var_name)
    dec_line = "@{}".format(var_name)

    file_names_to_modify = []
    files_to_modify = []

    # Check target_dir
    if target_dir == os.getcwd() and not force:
        raise Exception("It is dangerous to apply decorators at the current file level, \n"
                        "Overwrite this error with 'force=True'")

    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if name.endswith('.py') and not name.startswith('__init__'):
                files_to_modify.append(os.path.join(root, name))
                file_names_to_modify.append(name)

    if not force:
        if not __user_prompt("The following files will be modified .\n"
                             "{}\n"
                             "Continue ?:".format(files_to_modify)):
            print("Crisis diverted")
            return

    lines_modified = 0
    files_modified = 0
    for index, file in enumerate(files_to_modify):

        data = None
        with open(file, 'r') as f:
            data = f.readlines()

        # File Open Failure
        if data is None:
            __verbose_print("File '{}' failed to open, skipping...".format(files_to_modify[index]), verbose)
            continue

        if len(data) > 0 and data[0].find(comment) != -1:
            __verbose_print("File '{}' has already been marked, skipping...".format(files_to_modify[index]), verbose)
            continue

        lines_modified += 2
        files_modified += 1
        data.insert(0, import_line + "\n")
        data.insert(0, comment + "\n")

        for i, line in enumerate(data):
            if re.search("class\\s\\w*:", line):
                if data[i - 1].find(dec_line) == -1:
                    data.insert(i, dec_line + "\n")
                    lines_modified += 1
        with open(file, 'w') as f:
            f.writelines(data)

    __verbose_print("Added {} lines to {} file(s) .".format(lines_modified, files_modified), True)


def RemoveDecorators(target_dir, import_root, var_name="troppydash_logger", force=False, verbose=True):
    """
    DANGEROUS, use with caution\n
    Remove decorators to every python file in the Directory, and also removing the mark headings\n
    :param verbose: Whether to log changes
    :param target_dir: Directory that is affected
    :param import_root: Python import name of your tdlogger instance, e.p. tdlogging.tdprinter
    :param var_name: Variable name of the TDLogger instance in your file
    :param force: Apply Changes without confirmation
    :return:
    """
    comment = "## Edited by TDLogger"
    import_line = "from {} import {}".format(import_root, var_name)
    dec_line = "@{}".format(var_name)

    file_names_to_modify = []
    files_to_modify = []

    if target_dir == os.getcwd() and not force:
        raise Exception("It is dangerous to remove decorators at the current file level, \n"
                        "Overwrite this error with 'force=True'")

    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if name.endswith('.py') and not name.startswith('__init__'):
                files_to_modify.append(os.path.join(root, name))
                file_names_to_modify.append(name)

    if not force:
        if not __user_prompt("The following files will be modified .\n"
                             "{}\n"
                             "Continue ?:".format(files_to_modify)):
            print("Crisis diverted")
            return

    lines_modified = 0
    files_modified = 0
    # Loop through all detected files
    for index, file in enumerate(files_to_modify):

        data = None
        with open(file, 'r') as f:
            data = f.readlines()

        # File Open Failure
        if data is None:
            __verbose_print("File '{}' failed to open, skipping...".format(files_to_modify[index]), verbose)
            continue

        # Continue if the file does not have the comment
        if len(data) > 0 and data[0].find(comment) == -1:
            __verbose_print("File '{}' is unmarked, skipping...".format(files_to_modify[index]), verbose)
            continue

        lines_modified += 1
        files_modified += 1
        # Remove the comment
        data.pop(0)

        for i, line in enumerate(data):
            if line.find(dec_line) != -1 or line.find(import_line) != -1:
                data.pop(i)
                lines_modified += 1

        with open(file, 'w') as f:
            f.writelines(data)

    __verbose_print("Removed {} lines from {} file(s) .".format(lines_modified, files_modified), True)


class TDLogger:
    __default_config = {
        "exception": False,
        "count": True,
        "exec": False,
        "time": False,
        "return": False,
        "poll": False,
        "poll_period": 5
    }

    current_config = __default_config.copy()
    alias = ""

    """
    information: {
        "class_name": {
            "method_name": {
                "execcount": 1,
                "elapsed_time:" -1
            }
        }
    }
    """
    __information = {}

    def __init__(self, file_path="tdlogger.txt", config: dict = None, alias="", printer=TDPrinter()):
        """
        Construct an instance of TDLogger
        :param file_path: config file path - optional
        :param config: config dict - optional
        :param alias: alias
        """
        self.printer = printer
        self.alias = alias

        if config is not None:
            self.__set_config(config)
        else:
            file_content = TDReader.read_from_file(file_path)
            result_config = TDLogger.__parse_config(file_content)
            self.__set_config(result_config)

        if self.current_config["poll"] and config is None:
            self.__file_path = file_path
            self.__start_polling()

    def get_information(self):
        return self.__information

    @staticmethod
    def __parse_config(string: str) -> dict:
        """
        Parse the string into a config
        :param string: input string
        :return: a config dict
        """
        updated_config = TDLogger.__default_config
        if string:
            # Set configs
            for line in string.split('\n'):
                key_value = re.findall("\w+", line)

                if len(key_value) == 2:
                    if key_value[0] == "poll_period":
                        if re.match("\d", key_value[1]):
                            updated_config[key_value[0]] = int(key_value[1])
                    else:
                        updated_config[key_value[0]] = key_value[1].lower() == "true"

        return updated_config

    def __set_config(self, new_config: dict = None) -> dict:
        """
        Set current config from string and return it
        :param new_config: input string - usually from a file read
        :return: current_config
        """

        if new_config != self.current_config:
            self.printer.set_title("Configuration")
            self.printer.add_message("Alias", self.alias)
            self.printer.add_dict_message("New Configuration", new_config)
            self.printer.log_message()
            self.current_config.update(new_config)

        return new_config

    def __start_polling(self):
        if not self.current_config['poll']:
            return

        delay = float(self.current_config['poll_period'])
        threading.Timer(delay, self.__start_polling).start()

        ### Update config ###
        file_content = TDReader.read_from_file(self.__file_path)
        result_config = TDLogger.__parse_config(file_content)
        self.__set_config(result_config)

    @staticmethod
    def __get_arguments(func, argv):
        f_code = func.__code__
        func_parameter = f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]
        arguments = {}
        for i in range(len(func_parameter)):
            if i >= len(argv):
                arguments[func_parameter[i]] = "Undefined"
            else:
                arguments[func_parameter[i]] = argv[i]
        return arguments

    def __start_timer(self, func_name, class_name):
        self.__information[class_name][func_name]['elapsed_time'] = time.time()

    def __end_timer(self, func_name, class_name):
        start_time = self.__information[class_name][func_name]['elapsed_time']
        if start_time != -1:
            total_time = time.time() - start_time
            self.__information[class_name][func_name]['elapsed_time'] = -1
            return total_time

        return None

    def config(self):
        """
        Gets the logger from a TDLogger Instance that is using config
        :return: logger
        """

        def class_logger(cls):
            def innerLogger(func):
                def wrapper(*argv, **kwargs):
                    # Return Value
                    result = None

                    function_name = func.__name__
                    class_name = cls.__name__

                    log_exception = self.current_config['exec'] or self.current_config['exception']
                    log_time = self.current_config['exec'] or self.current_config['time']
                    log_count = self.current_config['exec'] or self.current_config['count']
                    log_return = self.current_config['exec'] or self.current_config['return']
                    log_any = self.current_config['exec'] or self.current_config['count'] \
                              or self.current_config['time'] or self.current_config['return']

                    self.__information[class_name][function_name]['execcount'] += 1
                    arguments = self.__get_arguments(func, argv)

                    if log_time:
                        self.__start_timer(function_name, class_name)

                    # TODO: Make a new decorator for this
                    if log_exception:
                        try:
                            result = func(*argv, **kwargs)
                        except Exception:
                            self.printer.set_title("Exception")
                            if self.alias:
                                self.printer.add_message("Alias", self.alias)
                            self.printer.add_message("Class Name", class_name)
                            self.printer.add_message("Method Name", function_name)
                            self.printer.add_message(
                                "Run Count", self.__information[class_name][function_name]['execcount'])
                            if log_time:
                                total_time = self.__end_timer(function_name, class_name)
                                self.printer.add_message("Run Time", "{:.3f}s".format(total_time))
                            self.printer.add_dict_message("Run Time Arguments", arguments)

                            self.printer.log_message(level='error')
                            print(str(traceback.format_exc()))

                            # Re-throw Exception
                            raise
                    else:
                        result = func(*argv, **kwargs)

                    total_time = None
                    if log_time:
                        total_time = self.__end_timer(function_name, class_name)

                    if log_any:
                        # Log Arguments
                        self.printer.set_title("Method \"{}\"".format(function_name))
                        if self.alias:
                            self.printer.add_message("Alias", self.alias)
                        self.printer.add_message("Class Name", class_name)
                        self.printer.add_message("Method Name", function_name)

                        # Log Count
                        if log_count:
                            self.printer.add_message(
                                "Run Count", self.__information[class_name][function_name]['execcount'])

                        # Log Time
                        if log_time:
                            self.printer.add_message("Run Time", "{:.3f}s".format(total_time))

                        # Log Return
                        if log_return:
                            self.printer.add_message("Return Value", result)
                            self.printer.add_message("Return Type", str(type(result)))

                        self.printer.add_dict_message("Run Time Arguments", arguments)

                        self.printer.log_message()

                    return result

                return wrapper

            # Apply inside logger to every method
            self.__information[cls.__name__] = {}
            for attr in cls.__dict__:
                if callable(getattr(cls, attr)):
                    func = getattr(cls, attr)

                    # init methods
                    self.__information[cls.__name__][func.__name__] = {
                        "execcount": 0,
                        "elapsed_time": -1.0,
                    }

                    setattr(cls, attr, innerLogger(func))
            return cls

        return class_logger
