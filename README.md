# zabbix-AutoMapper

Generate automatic map placement for Zabbix hosts using zabbix  API.

### Prerequisites
install the required python packages

`pip install -r requirements.txt`

### How to run the script
`python automap.py`

`python automap.py --help` to get help 

### tags used by the script
- am.host.type => type of the host, should be defined in config.json
- am.host.label => label of the host
- am.link.connect_to => the host to connect to
- am.link.label => the label to show on the link
- am.link.color => the color of the link
- am.link.draw_type => the type of the link (0: line, 2: bold line, 3: dotted line, 4: dashed line)

## *Author*

Pascal de JESSEY [pjessey@gmail.com](mailto:pjessey@gmail.com)
