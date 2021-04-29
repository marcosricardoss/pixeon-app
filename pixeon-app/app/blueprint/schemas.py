user = {
  "required": ["username", "password"],
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "maxLength": 50
    },
    "password": {
      "type": "string",
      "maxLength": 256
    }
  }
}