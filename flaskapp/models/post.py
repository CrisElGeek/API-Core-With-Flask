from flaskapp import db

class PostModel:
  def execute(self, database, payload):
    fields = ""
    keys = ""
    valueList = []
    for key, item in payload.items():
      fields = fields + item[1] + ","
      keys = keys + "%s,"
      valueList.append(item[0])
    fields = fields.rstrip(",")
    keys = keys.rstrip(",")
    values = tuple(valueList)
    qry = "INSERT INTO " + database + "(" + fields + ") VALUES(" + keys + ")"
    cur = db.connection.cursor()
    try:
      cur.execute(qry, values)
    except Exception as e:
      err = str(e)
      return {
        "message": "Database query error",
        "code": 500,
        "response": err
      }
    finally:
      id = db.connection.insert_id()
      cur.close()
      db.connection.commit()
      return {
        "message": "Data insert",
        "code": 200,
        "data": {
          "id": id
        }
      }