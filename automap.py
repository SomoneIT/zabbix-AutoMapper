import logging
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from automapLib.automaper import Automaper

sys.path.append(str(Path(".").resolve()))

__version__ = "0.1.0"
__program_name__ = "automap"


class type_scheme(str, Enum):
    http = "http"
    https = "https"


class type_layout(str, Enum):
    circle = "circle"
    grid = "grid"
    tree = "tree"
    drl = "drl"
    dh = "dh"
    fr = "fr"
    kk = "kk"
    lgl = "lgl"
    random = "random"
    rt = "rt"
    rt_circular = "rt_circular"



class type_log_level(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


def version_callback(value: bool):
    if value:
        print(f"{__program_name__} Version {__version__}")
        raise typer.Exit()


def configure_logging(log_file, log_level, verbose):
    handlers = []
    if log_file is not None:
        file_handler = logging.FileHandler(filename=log_file)
        handlers.append(file_handler)
    if verbose:
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        handlers.append(stdout_handler)

    numeric_level = getattr(logging, log_level.value.upper(), None)



    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level.value}')

    logging.basicConfig(
        level=numeric_level,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers
    )

    logging.info(f"Logging is set to {log_level.value.upper()}")


def main(
        zabbix_token: Annotated[
            str, typer.Option("--token", "-t", help="token for accessing zabbix api")
        ],
        zabbix_map_name: Annotated[
            str, typer.Option("--map", "-m", help="map name we want to use")
        ] = "automap",
        zabbix_host_group_name: Annotated[
            str, typer.Option("--group", "-g", help="group we want to sync in the map")
        ] = "automap",
        zabbix_port: Annotated[
            int, typer.Option("--zabbix_port", "-p", help="zabbix port")
        ] = 80,
        zabbix_host: Annotated[
            str,
            typer.Option("--zabbix_host", "-z", help="zabbix addess"),
        ] = "127.0.0.1",
        zabbix_scheme: Annotated[
            type_scheme,
            typer.Option("--zabbix_scheme", "-s", help="zabbix scheme"),
        ] = type_scheme.http,
        zabbix_folder: Annotated[
            str,
            typer.Option(
                "--zabbix_folder",
                "-f",
                help="zabbix folder (where the api_jsonrpc.php file resides, normally /zabbix or /)",
            ),
        ] = "/zabbix",
        map_layout: Annotated[
            type_layout,
            typer.Option("--map_layout", "-L", help="Map layout to use"),
        ] = type_layout.kk,
        log_level: Annotated[
            type_log_level,
            typer.Option(
                "--log_level",
                "-l",
                help="log level",
            ),
        ] = type_log_level.warning,
        log_file: Annotated[
            Path,
            typer.Option(
                "--log_path",
                "-P",
                help="log file to use",
            ),
        ] = None,
        verbose: Annotated[
            bool,
            typer.Option(
                "--verbose",
                "-v",
                help="print logs on stdout",
            ),
        ] = False,
        version: Annotated[
            Optional[bool],
            typer.Option("--version", callback=version_callback, is_eager=True),
        ] = None,
):

    configure_logging(log_file, log_level, verbose)
    logger = logging.getLogger()

    logger.info(f"program starting ...")

    logger.info(f"map layout {map_layout.value}")
    # create client for zabbix
    automaper = Automaper(
        zabbix_token=zabbix_token,
        zabbix_host=zabbix_host,
        zabbix_port=zabbix_port,
        zabbix_scheme=zabbix_scheme.value,
        zabbix_folder=zabbix_folder,
        map_name=zabbix_map_name,
        map_layout=map_layout.value,
        host_group_name=zabbix_host_group_name,
    )

    logger.debug(f"{automaper.graph.graph.vs.attribute_names()}")
    logger.debug(f"{automaper.graph.graph.vs["x"]}")
    logger.debug(f"{automaper.graph.graph.vs["y"]}")
    automaper.update_zabbix_map_from_graph()


if __name__ == "__main__":
    typer.run(main)
    os._exit(0)
