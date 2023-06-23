from PIL import Image

from display import DisplayBase


class ImageDisplay(DisplayBase):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._current_image = None  # type: Image.Image

    def initialize(self):
        self._current_image = Image.new('RGB', (self.width, self.height))

    def get_image(self):
        return self._current_image.copy()

    def draw(self, x, y, image):
        super().draw(x, y, image)
        self._current_image.paste(image, (x, y))
