The package provides the function ``use_zope_exception_log_format``.
When called, it overrides ``logging.Formatter.formatException`` with
the effect that later log entries use Zope's format for exceptions rather
than Python's. The former contains additional hints from
``__traceback_info__`` and ``__traceback_supplement__`` found in the
traceback frames.

``__traceback_info__`` and/or ``__traceback_supplement__``
are often used by the Zope infrastructure or application code
to provide additional information for the analysis of exception
causes. For example, Zope's page templates use this mechanism
to make available at what position in the template an exception occurred.
