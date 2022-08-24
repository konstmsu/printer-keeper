import logging

from printer_keeper.fortune import logger, main

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
    logger.info("Done")
except:
    logger.exception("Application failed")
