from flaskapp import db

class GetModel:
  def execute(self, params):
    self.params = params
    fields = self.fields()
    self.parameters = ()
    filters = self.filters()
    self.qry = "SELECT " + fields + " FROM " + self.params["database"] + filters
    print(self.qry)
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
  
  def filters(self):
    string = ""
    for filter in self.params["filters"]:
      if filter["operator"] == "IS NULL" or filter["operator"] == "IS NOT NULL":
        f = filter["field"] + " " + filter["operator"]
      elif filter["operator"] in ["=", ">", "<", ">=", "<=", "!=", "IS", "IS NOT", "IN", "NOT IN"]:
        f = filter["field"] + " " + filter["operator"] + " %s"
        self.parameters = self.parameters + (filter["value"], )
      elif filter["operator"] == "LIKE" or filter["operator"] == "NOT LIKE":
        f = filter["field"] + " " + filter["operator"] + " %s"
        self.parameters = self.parameters + ("%" + filter["value"] + "%", )
      string = string + f + " AND "
    if len(string) > 0:
      string = " WHERE " + string.rstrip(" AND ")
    return string