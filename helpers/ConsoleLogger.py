import logging


class ConsoleLogger(logging.getLoggerClass()):
    def __init__(self):
        super().__init__("ConsoleLogger")
        self.setup_console_logger()

    def setup_console_logger(self):
        self.setLevel(logging.DEBUG)

        # remove all default handlers
        for handler in self.handlers:
            self.removeHandler(handler)

        # create console handler and set level to debug
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(fmt="%(levelname)-9s %(message)s")
        console_handler.setFormatter(formatter)

        # now add new handler to logger
        self.addHandler(console_handler)
