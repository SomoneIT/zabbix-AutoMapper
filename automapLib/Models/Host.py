# generated by datamodel-codegen:
#   filename:  host.json
#   timestamp: 2024-09-11T14:15:47+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Inventory(BaseModel):
    type: str
    type_full: str
    name: str
    alias: str
    os: str
    os_full: str
    os_short: str
    serialno_a: str
    serialno_b: str
    tag: str
    asset_tag: str
    macaddress_a: str
    macaddress_b: str
    hardware: str
    hardware_full: str
    software: str
    software_full: str
    software_app_a: str
    software_app_b: str
    software_app_c: str
    software_app_d: str
    software_app_e: str
    contact: str
    location: str
    location_lat: str
    location_lon: str
    notes: str
    chassis: str
    model: str
    hw_arch: str
    vendor: str
    contract_number: str
    installer_name: str
    deployment_status: str
    url_a: str
    url_b: str
    url_c: str
    host_networks: str
    host_netmask: str
    host_router: str
    oob_ip: str
    oob_netmask: str
    oob_router: str
    date_hw_purchase: str
    date_hw_install: str
    date_hw_expiry: str
    date_hw_decomm: str
    site_address_a: str
    site_address_b: str
    site_address_c: str
    site_city: str
    site_state: str
    site_country: str
    site_zip: str
    site_rack: str
    site_notes: str
    poc_1_name: str
    poc_1_email: str
    poc_1_phone_a: str
    poc_1_phone_b: str
    poc_1_cell: str
    poc_1_screen: str
    poc_1_notes: str
    poc_2_name: str
    poc_2_email: str
    poc_2_phone_a: str
    poc_2_phone_b: str
    poc_2_cell: str
    poc_2_screen: str
    poc_2_notes: str


class Tag(BaseModel):
    tag: str
    value: str
    automatic: str


class Host(BaseModel):
    hostid: str
    proxyid: str
    host: str
    status: str
    ipmi_authtype: str
    ipmi_privilege: str
    ipmi_username: str
    ipmi_password: str
    maintenanceid: str
    maintenance_status: str
    maintenance_type: str
    maintenance_from: str
    name: str
    flags: str
    templateid: str
    description: str
    tls_connect: str
    tls_accept: str
    tls_issuer: str
    tls_subject: str
    custom_interfaces: str
    uuid: str
    vendor_name: str
    vendor_version: str
    proxy_groupid: str
    monitored_by: str
    inventory_mode: str
    active_available: str
    assigned_proxyid: str
    tags: List[Tag]
