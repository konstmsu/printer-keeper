import logging

from printer_keeper.fortune import main, logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("printer_keeper.log", encoding="utf8"),
        logging.StreamHandler(),
    ],
)

try:
    main()
except:
    logger.exception("Application failed")

logger.info("Done")
