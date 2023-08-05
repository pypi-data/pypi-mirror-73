class IOTInternal(object):
  def __init__(self, internal):
    self.internal = internal
  def get_id(self):
    return self.internal['id']

class IOTDevice(IOTInternal):
  def __init__(self, internal):
    super().__init__(internal)
    self.data = None

class IOTDataField(IOTInternal):
  def __init__(self, internal):
    super().__init__(internal)
  def get_unit(self):
    return self.internal

class IOTDataEntries(object):
  def __init__(self, data, device, field):
    self.data = data
    self.field = field
    print (field)
    self.device = device
  def get_data(self):
    X = []
    Y = []
    for x in self.data:
      Y.append(x["value"])
      X.append(x["created_at"])
    return {"X" : X, "Y" : Y}

  def get_unit(self):
    return self.field.get_unit();
