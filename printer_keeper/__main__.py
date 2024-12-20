import logging

import click

from printer_keeper.fortune import logger, main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("printer_keeper.log", encoding="utf8"),
        logging.StreamHandler(),
    ],
)

logger.info("Started")


@click.command
def cli():
    try:
        main()
        logger.info("Done")
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("Application failed")


cli()
