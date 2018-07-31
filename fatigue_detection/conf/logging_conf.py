import logging
import logging.handlers
import structlog
from structlog.stdlib import LoggerFactory

from .experiment_conf import exp_conf


class ProcessorFormatter(logging.Formatter):
	"""Custom stdlib logging formatter for structlog ``event_dict`` messages.
	Apply a structlog processor to the ``event_dict`` passed as
	``LogRecord.msg`` to convert it to loggable format (a string).
	"""

	def __init__(self, processor, fmt=None, datefmt=None, style='%'):
		""""""
		super().__init__(fmt=fmt, datefmt=datefmt, style=style)
		self.processor = processor

	def format(self, record):
		"""Extract structlog's ``event_dict`` from ``record.msg``.
		Process a copy of ``record.msg`` since the some processors modify the
		``event_dict`` and the ``LogRecord`` will be used for multiple
		formatting runs.
		"""
		if isinstance(record.msg, dict):
			msg_repr = self.processor(
				record._logger, record._name, record.msg.copy())
		return msg_repr


class LogConf:

	def event_dict_to_message(logger, name, event_dict):
		"""Passes the event_dict to stdlib handler for special formatting."""
		return ((event_dict,), {'extra': {'_logger': logger, '_name': name}})

	# https://gist.github.com/fabianbuechler/414a8322089e5e43b024fdf08c750c1a
	structlog.configure(
		processors=[
			structlog.stdlib.filter_by_level,
			structlog.stdlib.add_logger_name,
			structlog.stdlib.add_log_level,
			structlog.stdlib.PositionalArgumentsFormatter(),
			structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
			structlog.processors.StackInfoRenderer(),
			structlog.processors.format_exc_info,
			# Do not include last processor that converts to a string for stdlib
			# since we leave that to the handler's formatter.
			event_dict_to_message,
		],
		context_class=dict,
		logger_factory=structlog.stdlib.LoggerFactory(),
		wrapper_class=structlog.stdlib.BoundLogger,
		cache_logger_on_first_use=True,
	)

	exp_logger = structlog.get_logger(exp_conf.LOGGER_NAME)
	exp_logger.setLevel(logging.DEBUG)
	exph = logging.handlers.TimedRotatingFileHandler("%sdt_experiment.log" % (exp_conf.LOG_DIR), encoding='utf-8')
	exph.setFormatter(ProcessorFormatter(processor=structlog.processors.JSONRenderer()))
	exp_logger.addHandler(exph)
	
	#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	formatter = logging.Formatter('%(message)s')

	f_logger = logging.getLogger("file")
	f_logger.setLevel(logging.DEBUG)
	fh = logging.handlers.TimedRotatingFileHandler("%sdt_experiment.csv" % (exp_conf.LOG_DIR), encoding='utf-8')
	fh.setFormatter(formatter)
	f_logger.addHandler(fh)
