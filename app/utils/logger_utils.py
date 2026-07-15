# app/utils/logger_utils.py
import logging
import os

LOG_FILE = "chatbot_diagnostics.log"
HEADER_LINE = "timestamp,session_id,cache_mode,cache_status,cache_hits,db_hits,latency_ms,query\n"

# Ensure log file exists and has the latest CSV header
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r+") as f:
        lines = f.readlines()
        if not lines:
            f.write(HEADER_LINE)
        elif lines[0] != HEADER_LINE:
            lines[0] = HEADER_LINE
            f.seek(0)
            f.writelines(lines)
            f.truncate()
else:
    with open(LOG_FILE, "w") as f:
        f.write(HEADER_LINE)

# Set up raw logging
logging.basicConfig(level=logging.INFO)
diagnostics_logger = logging.getLogger("diagnostics")

file_handler = logging.FileHandler(LOG_FILE)
# Simple, raw format to write our CSV lines clean
file_handler.setFormatter(logging.Formatter('%(message)s'))
diagnostics_logger.addHandler(file_handler)
diagnostics_logger.propagate = False  # Avoid cluttering console out