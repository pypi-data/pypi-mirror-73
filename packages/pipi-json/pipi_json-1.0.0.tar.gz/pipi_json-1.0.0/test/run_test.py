import json
from pi_json import _encode_classes, PiJsonEncoder
from test.clz import Example1, Example


if __name__ == '__main__':
  ex2 = Example1("address1", True)
  ex1 = Example1("address", False, ex2)
  ex = Example(ex1, "test", 10)
  print(_encode_classes)
  jex = json.dumps(ex, indent=2, cls=PiJsonEncoder)
  print(jex)
