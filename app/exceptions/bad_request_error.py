class BadRequestError(Exception):
  
  def __init__(self, message: str, data=None):
    self.message = message
    self.data = data or {}
    super().__init__(message)

  def to_dict(self):
    return {"erro": self.message, "data": self.data}
  