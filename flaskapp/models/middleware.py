from flask import jsonify, request
from flaskapp.models.get import GetModel
from flaskapp.models.post import PostModel
from flaskapp.models.put import PutModel

class Models:
  def __init__(self, params, payload = None):
    self.request = request.args
    self.fields = params["fields"]
    self.filters = []
    self.joins = []
    if 'filters' in params:
      self.filters = params["filters"]
    if 'joins' in params:
      self.joins = params["joins"]
    self.payload = payload
    self.params = {
      "database": params["database"],
      "fields": [],
      "filters": [],
      "sort": [],
      "joins": []
    }
  # GET
  def Get(self, id = None):
    self.params["fields"] = self.SetFields()
    self.params["filters"] = self.SetParms()
    if id:
      filter = self.setFilters("eq:{}".format(id), "id")
      self.params["filters"].append(filter)
    return GetModel().execute(self.params)

  def SetParms(self):
    filters = []
    for key, value in self.request.items():
      if key == "limit":
        pass
      elif key == "sort":
        pass
      elif key != "fields":
        filter = self.setFilters(value, key)
        if filter:
          filters.append(filter)
    if self.filters:
      for f in self.filters:
        exist = False
        for value in filters:
          if value == f:
            exist = True
            return
        if not exist:
          filter = self.SetLocalFilters(f)
          filters.append(filter)
    return filters

 # Crea una lista (Array) de todos los campos de la base de datos a consultar
  def SetFields(self):
    db_fields = []
    def allFields():
      for key, value in self.fields.items():
        secured = value.get("secured")
        if not secured:
          db_fields.append(value["field"] + " " + key)
    try:
      fields = self.request['fields']
    except:
      allFields()
    else:
      field_list = fields.split(',')
      for key, value in self.fields.items():
        secured = value.get("secured")
        if key in field_list and not secured:
          db_fields.append(value["field"] + " " + key)
      if len(db_fields) == 0:
        allFields()
    return db_fields

  #POST
  def Post(self, payload):
    database = self.params["database"].split(" ")[0]
    return PostModel().execute(database, payload)

  def Params(self, insert = False):
    fields = {}
    for key, value in self.payload.items():
      for index, field in self.fields.items():
        protected = field.get("protected") #Handle KeyError
        if key == index and not protected:
          if insert:
            f = field["field"].split(".")[1]
          else:
            f = field["field"]
          fields.update({key: [value, f]})
    return fields

  def SetLocalFilters(self, item):
    return {
      "field": item["field"],
      "value": item["value"],
      "operator": item["operator"]
    }

  def setFilters(self, filter, field):
    params = filter.split(":")
    value = params[1]
    op = params[0]

    operators = {
      "eq": "=",
      "ne": "!=",
      "in": "IN",
      "like": "LIKE",
      "gt": ">",
      "lt": "<",
      "gte": ">=",
      "lte": "<=",
      "isn": "IS NULL",
      "non": "IS NOT NULL",
      "nin": "NOT IN",
      "is": "IS",
      "nis": "IS NOT"
    }

    for key, param in self.fields.items():
      if key == field:
        operator = operators[op]
        return {
          "field": param["field"],
          "value": value,
          "operator": operator
        }

  # PUT
  def Put(self, id, payload):
    filter = self.setFilters("eq:{}".format(id), "id")
    self.params["filters"].append(filter)
    return PutModel().execute(self.params, payload)