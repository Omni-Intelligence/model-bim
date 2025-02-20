import logging
import os
from logging.handlers import RotatingFileHandler

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
app_handler = RotatingFileHandler(
    app_log_file, maxBytes=10485760, backupCount=5
)  # 10MB per file, keep 5 backups
app_handler.setFormatter(formatter)
app_logger.addHandler(app_handler)

# Set up root logger for system logs
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
system_handler = RotatingFileHandler(system_log_file, maxBytes=10485760, backupCount=5)
system_handler.setFormatter(formatter)
root_logger.addHandler(system_handler)

# Prevent app logs from being written to system.log
app_logger.propagate = False

# Initial log messages
app_logger.info("App logging initialized. Logs will be stored in: %s", app_log_file)
root_logger.info(
    "System logging initialized. Logs will be stored in: %s", system_log_file
)
