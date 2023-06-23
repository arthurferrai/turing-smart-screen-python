import time
import unittest
from threading import Thread

from provider import Provider
from utils import spy_call


class DummyProvider(Provider):
    def __init__(self, trigger=None):
        super().__init__(trigger)
        self.data = 0

    def change_data(self):
        self.data += 1


class TestDataProvider(unittest.TestCase):
    def test_when_provider_has_no_data_then_return_None(self):
        provider = Provider()
        assert provider.data is None

    def test_when_provider_updates_data_then_data_must_be_updated(self):
        provider = DummyProvider()
        last_data = provider.data
        provider.change_data()
        assert provider.data != last_data

    def test_when_user_updates_provider_data_then_trigger_must_be_called(self):
        data = None

        @spy_call
        def t(value):
            nonlocal data
            data = value

        provider = Provider(trigger=t)
        assert t.called is False

        provider.data = 1
        assert data == 1
        assert t.called is True

    def test_when_provider_updates_data_then_trigger_must_be_called(self):
        data = None

        def t(value):
            nonlocal data
            data = value

        provider = DummyProvider(trigger=t)
        provider.change_data()
        assert provider.data == data

    def test_trigger_must_be_called_even_if_data_does_not_change(self):

        @spy_call
        def t(_): ...

        provider = Provider(trigger=t)
        assert t.called is False
        provider.data = provider.data
        assert t.called is True


if __name__ == '__main__':
    unittest.main()
