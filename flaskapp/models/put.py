from flaskapp import db
from flaskapp.models.shared import SharedComponents


class PutModel:
    def execute(self, _params, payload):
        columns = ""
        self.params = _params
        self.parameters = ()
        valueList = []
        for key, item in payload.items():
            columns += item[1] + " = %s, "
            valueList.append(item[0])
        columns = columns.rstrip(", ")
        self.values = tuple(valueList)
        response = SharedComponents().filters(
            self.params["filters"], self.parameters)
        filters = response["filters"]
        self.parameters = response["parameters"]
        self.data = self.values + self.parameters
        self.qry = "UPDATE " + \
            self.params["database"] + " SET " + columns + filters
        return self.Query()

    def Query(self):
        cur = db.connection.cursor()
        try:
            cur.execute(self.qry, self.data)
        except Exception as e:
            err = str(e)
            return {
                "message": "Database query error",
                "code": 500,
                "response": err
            }
        finally:
          cur.close()
          db.connection.commit()
          return {
            "message": "Data updated",
            "code": 200
          }
