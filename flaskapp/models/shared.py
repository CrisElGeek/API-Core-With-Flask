class SharedComponents:
  def filters(self, filters, parameters = ()):
    string = ""
    for filter in filters:
      if filter["operator"] == "IS NULL" or filter["operator"] == "IS NOT NULL":
        f = filter["field"] + " " + filter["operator"]
      elif filter["operator"] in ["=", ">", "<", ">=", "<=", "!=", "IS", "IS NOT", "IN", "NOT IN"]:
        f = filter["field"] + " " + filter["operator"] + " %s"
        parameters = parameters + (filter["value"], )
      elif filter["operator"] == "LIKE" or filter["operator"] == "NOT LIKE":
        f = filter["field"] + " " + filter["operator"] + " %s"
        parameters = parameters + ("%" + filter["value"] + "%" )
      string = string + f + " AND "
    if len(string) > 0:
      string = " WHERE " + string.rstrip(" AND ")
    return {
      'filters': string,
      'parameters': parameters
    }