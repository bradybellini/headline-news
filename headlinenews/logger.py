import logging
import logging.handlers

rogger = logging.getLogger("rogger_logger")
rogger.setLevel(logging.DEBUG)

fh = logging.handlers.TimedRotatingFileHandler(
    filename="logs/warning/headlinenews.log",
    when="midnight",
    utc=True,
    backupCount=14,
    encoding="utf-8",
)
fh.setLevel(logging.WARNING)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

nfo = logging.handlers.TimedRotatingFileHandler(
    filename="logs/info/headlinenews_info.log",
    when="midnight",
    utc=True,
    backupCount=7,
    encoding="utf-8",
)
nfo.setLevel(logging.INFO)

dbug = logging.handlers.TimedRotatingFileHandler(
    filename="logs/debug/headlinenews_debug.log",
    when="midnight",
    utc=True,
    backupCount=3,
    encoding="utf-8",
)
dbug.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh.setFormatter(formatter)
ch.setFormatter(formatter)
nfo.setFormatter(formatter)
dbug.setFormatter(formatter)

rogger.addHandler(fh)
rogger.addHandler(ch)
rogger.addHandler(nfo)
rogger.addHandler(dbug)
