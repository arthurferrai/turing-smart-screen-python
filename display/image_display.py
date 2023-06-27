from PIL import Image

from display import DisplayBase


class ImageDisplay(DisplayBase):
    def __init__(self, width: int, height: int, rotation: int = 0):
        self.width = width
        self.height = height
        self.rotation = rotation
        self._current_image = None  # type: Image.Image | None

    def initialize(self):
        super().initialize()
        self._current_image = Image.new('RGB', (self.width, self.height))

    def get_image(self):
        return self._current_image.copy().rotate(self.rotation)

    def draw(self, x, y, image):
        super().draw(x, y, image)
        self._current_image.paste(image, (x, y))
