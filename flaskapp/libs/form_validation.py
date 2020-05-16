import re
from flaskapp import db

class Validate:
  def execute(self, payload, rules):
    self.errors = []
    for key, string in rules.items():
      checks = string.split("|")
      try:
        field = payload[key][0]
      except:
        for check in checks:
          rule = check.split(":")
          name = rule[0]
          if name == 'required':
            self.errors.append({
              "rule": "required",
              "field": key
            })
      else:
        for check in checks:
          rule = check.split(":")
          name = rule[0]
          if len(rule) >= 2:
            value = rule[1]
          if name == 'required' or (field and len(str(field)) > 0):
            if name == 'required' and not field or len(str(field)) == 0:
              self.errors.append({
                "rule": "required",
                "field": key
              })
            else:
              if name == "max" and len(str(field)) > int(value):
                self.errors.append({
                  "rule": "max",
                  "field": key,
                  "value": value
                })
              if name == "min" and len(str(field)) < int(value):
                self.errors.append({
                  "rule": "min",
                  "field": key,
                  "value": value
                })
              if name == "max_value" and int(field) > int(value):
                self.errors.append({
                  "rule": "max_value",
                  "field": key,
                  "value": value
                })
              if name == "min_value" and int(field) < int(value):
                self.errors.append({
                  "rule": "min_value",
                  "field": key,
                  "value": value
                })
              if name == "numeric" and not str(field).isnumeric():
                self.errors.append({
                  "rule": "numeric",
                  "field": key
                })
              if name == "email":
                regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
                match = re.fullmatch(regex, field)
                if not match:
                  self.errors.append({
                    "rule": "email",
                    "field": key
                  })
              if name == "unique":
                unique = self.isUnique(rule[1], rule[2], field)
                if not unique:
                  self.errors.append({
                    "rule": "unique",
                    "field": key
                  })
    return self.errors
    
  def isUnique(self, table, field, value):
    cur = db.connection.cursor()
    cur.execute("SELECT COUNT(*) rows FROM " + table + " WHERE " + field + " = '" + str(value) + "'")
    result = cur.fetchone()
    if(result["rows"] > 0):
      return False
    else:
      return True