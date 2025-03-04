import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

# Create logs directory
log_dir = os.path.join(os.getcwd(), "storage/logs")
os.makedirs(log_dir, exist_ok=True)

# Define log files
app_log_file = os.path.join(log_dir, "app.log")
system_log_file = os.path.join(log_dir, "system.log")

# Define log format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

# Set up app logger
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.DEBUG)
app_handler = RotatingFileHandler(app_log_file, maxBytes=10485760, backupCount=5)
app_handler.setFormatter(formatter)
app_logger.addHandler(app_handler)


class ExecutableFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "pathname"):
            return True
        return not (
            os.path.exists(record.pathname) and os.access(record.pathname, os.X_OK)
        )


# Set up root logger for system logs (using INFO level to reduce noise)
root_logger = logging.getLogger()
root_logger.setLevel(logging.WARNING)
system_handler = RotatingFileHandler(system_log_file, maxBytes=10485760, backupCount=5)
system_handler.setFormatter(formatter)
system_handler.addFilter(ExecutableFilter())
root_logger.addHandler(system_handler)

app_logger.propagate = False

app_logger.info("App logging initialized. Logs will be stored in: %s", app_log_file)
root_logger.info(
    "System logging initialized. Logs will be stored in: %s", system_log_file
)


def prune_old_logs(log_file, days_to_keep=30):
    """Prune log files older than specified days"""
    if not os.path.exists(log_file):
        return

    directory = os.path.dirname(log_file)
    base_name = os.path.basename(log_file)
    current_time = datetime.now()
    logger = logging.getLogger("log_pruner")

    for filename in os.listdir(directory):
        if filename.startswith(base_name):
            file_path = os.path.join(directory, filename)
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            if current_time - file_modified > timedelta(days=days_to_keep):
                try:
                    os.remove(file_path)
                    logger.info(f"Removed old log file: {file_path}")
                except OSError as e:
                    logger.error(f"Error removing {file_path}: {e}")


prune_old_logs(system_log_file, days_to_keep=7)
prune_old_logs(app_log_file, days_to_keep=30)
