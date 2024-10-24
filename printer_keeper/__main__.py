import logging

import click

from printer_keeper.fortune import logger, main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


@click.command
def cli():
    try:
        main()
        logger.info("Done")
    except:
        logger.exception("Application failed")


cli()
