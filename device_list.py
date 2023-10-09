import requests
import xml.etree.ElementTree as ET
import pandas as pd
from enum import Enum


# Choose categories from:
class Options(Enum):
    device = "asset.device"
    asset_tag = "asset.device.ncentralassettag"
    asset_os = "asset.os"
    computer_system = "asset.computersystem"
    processor = "asset.processor"
    motherboard = "asset.motherboard"
    raid_controller = "asset.raidcontroller"
    memory = "asset.memory"
    video_controller = "asset.videocontroller"
    logical_device = "asset.logicaldevice"
    physical_drive = "asset.physicaldrive"
    mapped_drive = "asset.mappeddrive"
    media_access_device = "asset.mediaaccessdevice"
    network_adapter = "asset.networkadapter"
    usb_device = "asset.usbdevice"
    printer = "asset.printer"
    port = "asset.port"
    service = "asset.service"
    application = "asset.application"
    patch = "asset.patch"
    customer = "asset.customer"
    so_customer = "asset.socustomer"

    def __init__(self, include_category):
        self.include_category = include_category

    def __str__(self):
        return f"{self.include_category}"

    def __repr__(self):
        return f"{self.include_category}"


categories = [Options.network_adapter, Options.device]

# add your username
username = 'YOUR USERNAME'

# add your JWT
jwt = 'YOUR JWT'

# add the uri for your N-central server
nc_uri = 'YOUR SERVER FQDN'
headers = {'content-type': 'text/xml'}
# 0.0 for N-central as the source
version = '0.0'


category_string = ''
for category in categories:
    category_string += f'<ei2:value>{category}</ei2:value>\n'

body = f"""
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ei2="http://ei2.nobj.nable.com/">
<soap:Header/>
<soap:Body>
<ei2:deviceAssetInfoExportDeviceWithSettings>
<ei2:version>{version}</ei2:version>
<ei2:username>{username}</ei2:username>
<ei2:password>{jwt}</ei2:password>
<ei2:settings>
<ei2:key>InformationCategoriesInclusion</ei2:key>
{category_string}
</ei2:settings>
</ei2:deviceAssetInfoExportDeviceWithSettings>
</soap:Body>
</soap:Envelope>
"""

response = requests.post(url=f'{nc_uri}/dms2/services2/ServerEI2', headers=headers, data=body)
xml_response = response.content
xml_response = ET.ElementTree(ET.fromstring(xml_response))
root = xml_response.getroot()
tree = root.findall('.//{http://ei2.nobj.nable.com/}return')

device_list = []
for device in tree:
    device_info = {}
    for attribute in device:
        key = attribute.find('{http://ei2.nobj.nable.com/}key')
        value = attribute.find('{http://ei2.nobj.nable.com/}value')
        if value is not None:
            device_info[key.text] = value.text
    device_list.append(device_info)

df = pd.DataFrame(device_list)

df.to_csv('device_list.csv', index=False)
