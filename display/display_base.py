from abc import ABC, abstractmethod

from PIL.Image import Image

from display.exceptions import AlreadyInitialized, InvalidImage


class DisplayBase(ABC):
    _initialized = False

    def initialize(self):
        if self._initialized:
            raise AlreadyInitialized()
        self._initialized = True

    @abstractmethod
    def draw(self, x, y, image):
        if not isinstance(image, Image):
            raise InvalidImage()
        if not self._initialized:
            self.initialize()

    def finalize(self):
        self._initialized = False

    def restart(self):
        self.finalize()
        self.initialize()
