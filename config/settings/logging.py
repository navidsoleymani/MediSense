"""
Logging Configuration for Django Project

This logging setup is designed to capture detailed debug-level logs
specifically for MongoDB queries executed by Django's database backend.
It uses Python's built-in logging framework with the following features:

- Version: 1 (standard for logging configuration dictionaries)
- Existing loggers are kept enabled to avoid disabling default Django logging
- Formatter 'verbose' formats logs with level, timestamp, module name,
  process ID, thread ID, and the log message, using the '{' style formatting
- Handler 'mongo_debug' writes logs to a rotating file located at
  '/var/log/django/mongo_queries.log'
    - Logs are rotated when the file reaches 5 MB in size
    - Up to 5 backup files are retained to preserve recent log history
    - Uses the 'verbose' formatter for detailed log entries
- Logger for 'django.db.backends' is configured to use the 'mongo_debug' handler,
  capturing all DEBUG level logs related to database backend activity
- Propagation is disabled to prevent duplicate logging of the same events

This configuration enables effective monitoring and debugging of MongoDB
query activity within the Django application by persisting detailed logs
in a managed file with rotation to avoid unbounded growth.

Note: Ensure the directory '/var/log/django/' exists and has appropriate
write permissions for the Django process to avoid logging errors.

"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Keep Django's default loggers active
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'mongo_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/mongo_queries.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB max file size before rotation
            'backupCount': 5,  # Keep up to 5 backup log files
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['mongo_debug'],
            'level': 'DEBUG',
            'propagate': False,  # Prevent duplicate logs in ancestor loggers
        },
    }
}
