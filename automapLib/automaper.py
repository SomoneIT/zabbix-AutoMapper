import json
import logging

from automapLib.Models.Host import Host
from automapLib.Models.Map import Map
from automapLib.network_graph import NetworkGraph
from automapLib.zabbix import Zabbix


class Automaper:
    zabbix: Zabbix = None
    graph: NetworkGraph = None
    map_info: Map = None
    logger = logging.getLogger("Automaper")
    host_group_name: str = None
    map_name: str = None
    map_height: int = None
    map_width: int = None
    map_sysmapid: str = None
    list_hosts: list[Host] = None
    config: any = None
    map_layout: str = None

    def __init__(
            self,
            zabbix_token,
            zabbix_host,
            zabbix_port,
            zabbix_scheme,
            zabbix_folder,
            host_group_name,
            map_name,
            map_layout,
    ):


        self.logger.info(f"initialize Automaper class")
        self.read_config("config.json")
        self.logger.info(f"create zabbix object")
        self.zabbix = Zabbix(
            zabbix_token=zabbix_token,
            zabbix_host=zabbix_host,
            zabbix_port=zabbix_port,
            zabbix_scheme=zabbix_scheme,
            zabbix_folder=zabbix_folder,
        )
        self.zabbix.create_api()
        self.host_group_name = host_group_name
        self.map_name = map_name
        self.map_layout = map_layout
        self.logger.info(f"getting information for map {map_name}")
        self.get_zabbix_map_informations()
        self.logger.info(f"getting information for hostgroup {host_group_name}")
        self.get_zabbix_host_in_hostgroups()
        self.logger.info(f"create graph object")
        self.graph = NetworkGraph(
            height=self.map_height,
            width=self.map_width,
            border=100,
            config=self.config,
            layout_type=self.map_layout,
        )
        self.logger.info(f"adding hosts to graph")
        self.insert_zabbix_map_in_graph()

    def read_config(self, config_file):
        # Lire le fichier config.json
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def get_zabbix_map_informations(self):
        self.map_info = self.zabbix.get_map_by_name(self.map_name)
        self.map_width = self.map_info.width
        self.map_height = self.map_info.height
        self.map_sysmapid = self.map_info.sysmapid
        self.logger.info(f"got map informations : {self.map_width}x{self.map_height}")

    def insert_zabbix_map_in_graph(self):
        self.graph.add_hosts_from_list(self.list_hosts)

    def get_zabbix_host_in_hostgroups(self):
        self.list_hosts = self.zabbix.get_hosts_in_host_group_name(self.host_group_name)

    def update_zabbix_map_from_graph(self):
        list_host = list()
        list_link = list()

        for vertice in self.graph.get_vertices():
            list_host.append(
                {
                    "selementid": vertice["name"],
                    "elements": [{"hostid": vertice["hostid"]}],
                    "x": vertice["x"],
                    "y": vertice["y"],
                    "elementtype": 0,  # 0 = host
                    "iconid_off": vertice["iconid_off"],
                    "label": vertice["label"],
                }
            )
        logging.debug(f"list host : {list_host}")
        for edge in self.graph.get_edges():
            logging.debug(f"{edge}")
            list_link.append(
                {
                    "linkid": edge["name"],
                    "label": edge["label"],
                    "selementid1": edge["host1"],
                    "selementid2": edge["host2"],
                    "color": edge["color"],
                    "drawtype": edge["draw_type"],
                }
            )
        logging.debug(f"list link : {list_link}")

        self.zabbix.update_map(
            sysmapid=self.map_sysmapid, list_selements=list_host, list_links=list_link
        )
