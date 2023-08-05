import logging
from . import util


class Plugin:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.logger = PluginLoggerAdapter(util.get_class_logger(self), self.pipeline)


class Input(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
    
    def input(self, rows_prev=None, num_rows_prev=None):
        raise NotImplementedError


class Output(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)

    def output(self, rows, num_rows):
        raise NotImplementedError


class Processor(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)

    def process(self, rows):
        raise NotImplementedError


class Trigger(Plugin):
    def __init__(self, pipeline):
        super().__init__(pipeline)
    
    def run(self):
        raise NotImplementedError


class PluginLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, pipeline):
        super(PluginLoggerAdapter, self).__init__(logger, {})
        self.pipeline = pipeline

    def process(self, msg, kwargs):
        return f'[{self.pipeline}] {msg}', kwargs
