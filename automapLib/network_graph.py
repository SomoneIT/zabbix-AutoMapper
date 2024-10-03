import logging
from dataclasses import dataclass
from typing import Optional

import igraph
import igraph as ig
from matplotlib import pyplot as plt

from automapLib.Models.GraphHost import GraphHost
from automapLib.Models.GraphLink import GraphLink
from automapLib.Models.Host import Host, Tag


@dataclass
class NetworkGraph:
    graph: ig.Graph
    logger: logging.Logger = logging.getLogger("NetworkGraph")
    layout_type: str = ""
    height: Optional[int] = None
    width: Optional[int] = None
    border: Optional[int] = None
    config: Optional[any] = None

    def __init__(self, height: int, width: int, border: int, config: any = None,layout_type: str = ""):
        self.logger.info(f"create graph object")
        self.graph = ig.Graph()
        self.height = height
        self.width = width
        self.border = border
        self.config = config
        self.layout_type = layout_type

    def __repr__(self):
        return ig.summary(self.graph)

    def __str__(self):
        return self.graph.__str__()

    def insert_layout(self):
        bbox = (self.width - (self.border * 2), self.height - (self.border * 2))
        # Create the layout with the specified bounding box
        self.logger.info(f"inserting layout {self.layout_type}")
        layout = self.graph.layout(self.layout_type)
        layout.fit_into(bbox=bbox)
        self.graph.vs["x"] = [
            int(coord[0]) + (self.border / 2) for coord in layout.coords
        ]
        self.graph.vs["y"] = [
            int(coord[1]) + (self.border / 2) for coord in layout.coords
        ]

    def plot_graph(self):
        fig, ax = plt.subplots()
        # Define the bounding box (width, height)
        bbox = (self.width - self.border, self.height - self.border)
        # Create the layout with the specified bounding box
        layout = self.graph.layout(self.layout_type)
        layout.fit_into(bbox=bbox)
        self.logger.info(
            f"plotting graph with layout {self.layout_type}, {layout.coords}"
        )

        ig.plot(
            self.graph,
            target=ax,
            layout=layout,
            vertex_size=30,
            vertex_color=["steelblue"],
            vertex_frame_width=4.0,
            vertex_frame_color="white",
            vertex_label=self.graph.vs["name"],
            vertex_label_size=7.0,
            edge_width=4,
            edge_color=self.graph.es["color"],
            edge_label=self.graph.es["label"],
        )
        plt.show()

    def add_hosts_from_list(self, list_hosts: list[Host]):

        list_graph_hosts = self.get_list_graph_host_in_host_group(list_hosts)

        attributes = {
            "hostid": [host.hostid for host in list_graph_hosts],
            "label": [host.label for host in list_graph_hosts],
            "iconid_off": [host.iconid_off for host in list_graph_hosts],
        }

        self.graph.add_vertices(
            n=[host.name for host in list_hosts], attributes=attributes
        )

        list_links = self.get_list_links_in_host_group(list_hosts)
        self.graph.add_edges(
            es=[[link.host1, link.host2] for link in list_links],
            attributes={
                "name": [f"{link.host1}-{link.host2}" for link in list_links],
                "host1": [link.host1 for link in list_links],
                "host2": [link.host2 for link in list_links],
                "label": [link.label for link in list_links],
                "color": [link.color for link in list_links],
                "link_type": [link.link_type for link in list_links],
                "draw_type": [link.draw_type for link in list_links],
            },
        )
        self.insert_layout()

    def get_list_graph_host_in_host_group(
        self, list_hosts: list[Host]
    ) -> list[GraphHost]:
        _return_list: list[GraphHost] = []
        for host in list_hosts:
            _graph_host: GraphHost = self.get_graph_host_from_host_data(host)
            _return_list.append(_graph_host)
        return _return_list

    def get_graph_host_from_host_data(self, host: Host) -> GraphHost:

        label: Optional[str] = None
        host_type: Optional[str] = None

        for tag in host.tags:
            if tag.tag == "am.host.type":
                host_type = tag.value
            if tag.tag == "am.host.label":
                label = tag.value
                label = label.replace("\\n", "\n")

        if host_type is None:
            host_type = self.config["default_host_type"]
        if label is None:
            label = self.config["host_type"][host_type]["label"]

        _result = GraphHost(
            name=host.host,
            hostid=host.hostid,
            label=label,
            iconid_off=self.config["host_type"][host_type]["iconid_off"],
        )
        return _result

    def get_list_links_in_host_group(self, list_hosts: list[Host]) -> list[GraphLink]:
        _return_list: list[GraphLink] = []
        for host in list_hosts:
            linkto: Optional[GraphLink] = self.get_links_to_from_host_data(host)
            if linkto is not None:
                _return_list.append(linkto)
        return _return_list

    def get_links_to_from_host_data(self, host: Host) -> Optional[GraphLink]:

        linkid: Optional[str] = None
        sysmapid: Optional[str] = None
        draw_type: int = 0
        color: str = "00CC00"
        label: Optional[str] = None
        linkto: Optional[str] = None
        link_type: Optional[int] = None

        tags: list[Tag] = host.tags

        for tag in tags:
            if tag.tag == "am.link.connect_to":
                linkto = tag.value
            if tag.tag == "am.link.label":
                label = tag.value
            if tag.tag == "am.link.type":
                link_type = int(tag.value)
            if tag.tag == "am.link.color":
                color = tag.value
            if tag.tag == "am.link.draw_type":
                draw_type = int(tag.value)

        if linkto is None:
            _result = None
        else:
            _result = GraphLink(
                host1=host.host,
                host2=linkto,
                label=label,
                color=color,
                link_type=link_type,
                draw_type=draw_type,
            )
        return _result

    def get_vertices(self) -> list[igraph.Vertex]:
        return self.graph.vs

    def get_edges(self) -> list[igraph.Edge]:
        return self.graph.es
