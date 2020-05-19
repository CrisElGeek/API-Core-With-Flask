from flaskapp import db
from flaskapp.models.shared import SharedComponents

class GetModel:
  def execute(self, _params):
    self.params = _params
    fields = self.fields()
    self.parameters = ()
    response = SharedComponents().filters(self.params["filters"], self.parameters)
    filters = response["filters"]
    joins = self.joins()
    self.parameters = response["parameters"]
    self.qry = "SELECT " + fields + " FROM " + self.params["database"] + joins + filters
    return self.Query()

  def Query(self):
    cur = db.connection.cursor()
    cur.execute(self.qry, self.parameters)
    results = cur.fetchall()
    if len(results) > 0:
      return {
        "data": results,
        "code": 200
      }
    else:
      return {
        "message": "No results",
        "code": 404
      }

  def fields(self):
    string = ""
    for field in self.params["fields"]:
      string = string + field + ","
    string = string.rstrip(",")
    if len(string) == 0:
      string = "*"
    return string

  def joins(self):
    # NOTE: CONTINUAR AQUI EXISTE ALGUN PROBLEMA CON LA CREACION DEL STRING DE JOINS
    print(self.params["joins"])
    string = ""
    for join in self.params["joins"]:
      string +=  "JOIN " + join["table"] + " ON" + join["match"][0] + " = " + join["match"][1] + " "
    return string