import re

class Functions:

  def strToSlug(self, string, subst = "-"):
    regex = r"([\s]+)"
    result = re.sub(regex, subst, string, 0)
    result = result.lower()
    result = list(result)

    vocals = {
      "á": "a",
      "é": "e",
      "í": "i",
      "ó": "o",
      "ú": "u",
      "ü": "u",
      "ñ": "n"
    }
    str = ""
    for word in result:
      match = False
      for key, vocal in vocals.items():
        if key == word:
          match = vocal
      if match:
        str += match
      else:
        str += word
    
    regex = r"([^a-z0-9\-]+)"
    result = re.sub(regex, subst, str, 0)
    return result