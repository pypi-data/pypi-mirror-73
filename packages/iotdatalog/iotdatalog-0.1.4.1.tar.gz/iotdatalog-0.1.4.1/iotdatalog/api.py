import requests
from iotdatalog.models import IOTDevice, IOTDataField, IOTDataEntries

class Api(object):
  def __init__(self, key, https=True):
    self.key = key
    self.https = https
    self.api_domain = "datalog.anglebrackets.co.za"
    self.auth_header = {"Authorization" : "Bearer " + self.key}
    self.devices = []
    self.fields = []

  def _get_base_url(self):
    if self.https:
      base_url = "https://"
    else:
      base_url = "http://"
    return base_url + self.api_domain + "/api/"

  def _get_fields_url(self):
    return self._get_base_url() + 'fields'

  def _get_devices_url(self):
    return self._get_base_url() + 'devices'

  def _get_entries_url(self, device_id, field_id):
    return self._get_base_url() + 'entries/' + device_id + '/' + field_id
  
  def set_key(self, key):
    self.key = key

  def get_devices(self):
   datalog_response = requests.get(self._get_devices_url(), headers=self.auth_header)
   datalog_response.raise_for_status()
   for d in datalog_response.json():
     self.devices.append(IOTDevice(d));
   return self.devices

  def get_fields(self):
   datalog_response = requests.get(self._get_devices_url(), headers=self.auth_header)
   datalog_response.raise_for_status()
   for d in datalog_response.json():
     self.fields.append(IOTDataField(d));
   return self.fields

  def get_entries(self, device, field):
   datalog_response = requests.get(self._get_entries_url(str(device.get_id()), str(field.get_id())), headers=self.auth_header)
   datalog_response.raise_for_status()
   return IOTDataEntries(datalog_response.json(), device, field)


  
