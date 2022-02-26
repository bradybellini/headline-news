import logging
from headlinenews import SupaPSQL


def main():
    logger = logging.getLogger("rogger_logger.run.main")
    logger.info("Pull Started")
    supa = SupaPSQL()
    supa.run()
    logger.info("Pull Ended")


if __name__ == "__main__":
    main()
