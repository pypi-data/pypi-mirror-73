import json

class PiJsonEncoder(json.JSONEncoder):

  def default(self, o):
    for cls, f_ in _encode_classes.items():
      if isinstance(o, cls):
        if callable(f_):
          return f_()
        elif hasattr(o, f_):
          return getattr(o, f_)()
        else:
          return f_
    return json.JSONEncoder.default(self, o)

def json_encode(_cls=None, *, mapping=None):
  def decorator_encode(cls):
    if cls and mapping:
      _encode_classes.update({cls: mapping})
    return cls

  if _cls is None:
    return decorator_encode
  else:
    return decorator_encode(_cls)

_default_json_encoder = PiJsonEncoder
_encode_classes = {}
