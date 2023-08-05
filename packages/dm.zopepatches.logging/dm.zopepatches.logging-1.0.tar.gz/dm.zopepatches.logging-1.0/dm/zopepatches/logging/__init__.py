from logging import Formatter, getLogger

from zExceptions.ExceptionFormatter import format_exception

logger = getLogger(__name__)

def zope_format_exception(self, ei):
  """Use ``Zope``'s ``format_exception`` to format *ei*."""
  return "".join(format_exception(*ei, as_html=False))

def use_zope_exception_log_format():
  Formatter.formatException = zope_format_exception
  logger.info("patched `logging.Formatter.formatException`` to get exception "
              "info in (the more informative) Zope format")
