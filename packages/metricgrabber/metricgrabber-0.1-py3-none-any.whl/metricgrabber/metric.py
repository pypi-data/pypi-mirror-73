class Metric():
    def __init__(self, params={}, value=0):
        self.params = params
        self.value = value

    def to_dict(self):
        return {
            'params': self.params,
            'value': self.value,
        }