Logging
=======

Most events will be logged to the logger named :code:`rolumns`.

When a column is bound to a value that doesn't exist during rendering, that warning will be logged to :code:`rolumns.missing-value`.

If you don't care about missing values, feel free to set the log level of :code:`rolumns.missing-value` to :code:`logging.NOTSET`.
