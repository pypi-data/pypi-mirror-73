from pi_json import json_encode


@json_encode(mapping="to_dict")
class Example:
    def __init__(self,ex, name="", value=10):
        self.name = name
        self.value = value
        self.other = ex

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "other": self.other
        }


@json_encode(mapping="to_dict")
class Example1:

    def __init__(self, address="", ignored=False, ex=None):
        self.address = address
        self.ignored = ignored
        self.example = ex

    def to_dict(self):
        return {
            "address": self.address,
            "ignored": self.ignored,
            "example": self.example
        }