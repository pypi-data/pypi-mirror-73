import os

LOG_LEVEL = os.environ.get("TRIBUTORS_LOG_LEVEL", "INFO")
LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "QUIET", "FATAL"]
if LOG_LEVEL not in LOG_LEVELS:
    LOG_LEVEL = "INFO"
