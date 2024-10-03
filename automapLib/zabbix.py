import logging
from dataclasses import dataclass

from zabbix_utils import ZabbixAPI

from automapLib.Models.Host import Host
from automapLib.Models.Map import Map


@dataclass
class Zabbix:
    zabbix_token: str
    zabbix_host: str = "localhost"
    zabbix_port: int = 80
    zabbix_scheme: str = "http"
    zabbix_folder: str = "/zabbix"
    api: ZabbixAPI = None
    logger: logging = logging.getLogger("Zabbix")

    def __post_init__(self):
        self.zabbix_url = f"{self.zabbix_scheme}://{self.zabbix_host}:{self.zabbix_port}{self.zabbix_folder}"
        self.logger.info(f"url zabbix : {self.zabbix_url}")

    def create_api(self):
        self.logger.info(f"create zabbix api")
        self.api = ZabbixAPI(url=self.zabbix_url, token=self.zabbix_token)

    def get_hosts_in_host_group_name(self, host_group_name) -> list[Host]:
        groupid = self.get_host_group_from_name(host_group_name)
        result_host: list[Host] = []
        try:
            _hosts: dict = self.api.host.get(  # type: ignore
                output="extend",
                groupids=[groupid],
                selectTags="extend",
            )
            # self.logger.info(f"got response : {_hosts}")
            result_host = [Host(**_host) for _host in _hosts]
        except Exception as e:
            self.logger.error(f"got error : {e}")
        return result_host

    def get_host_group_from_name(self, host_group_name: str) -> int:
        try:
            groupid = self.api.hostgroup.get(
                output=["groupid"],
                filter={"name": [host_group_name]},
            )[0]["groupid"]
        except IndexError:
            groupid = 0
        return groupid

    def get_map_by_name(self, map_name: str) -> Map:
        self.logger.info(f"get informations for map {map_name}")

        result_map: Map = None

        try:
            _map: dict = self.api.map.get(
                output="extend",
                selectSelements="extend",
                selectLinks="extend",
                selectUsers="extend",
                selectUserGroups="extend",
                selectShapes="extend",
                selectLines="extend",
                filter={"name": [map_name]},
            )
            # self.logger.info(f"got response : {_map}")
            result_map = Map(**_map[0])
        except Exception as e:
            self.logger.error(f"error during get_map_by_name : {e}")

        # self.logger.debug(f"{result_map}")

        return result_map

    def update_map(self, sysmapid, list_selements, list_links):
        try:
            _response = self.api.map.update(
                sysmapid=sysmapid,
                selements=list_selements,
                links=list_links,
            )  # type: ignore
            self.logger.info(f"got response : {_response}")

        except Exception as e:
            self.logger.error(f"got error : {e}")
