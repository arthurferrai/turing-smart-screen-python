class Provider:
    def __init__(self, trigger=None):
        self.trigger = trigger
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        if self.trigger:
            self.trigger(value)
