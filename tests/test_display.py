import unittest

from PIL import Image, ImageChops

from display import DisplayBase, ImageDisplay, AlreadyInitialized, InvalidImage

DUMMY_IMAGE = Image.new('1', (0, 0))


class DummyDisplay(DisplayBase):

    def draw(self, x, y, image):
        super().draw(x, y, image)


class SpyDisplay(DummyDisplay):
    def __init__(self):
        self.called_funcs = []

    def initialize(self):
        super().initialize()
        self.called_funcs.append("initialize")

    def finalize(self):
        super().finalize()
        self.called_funcs.append("finalize")


class TestDisplay(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy = DummyDisplay()
        self.spy = SpyDisplay()

    def test_display_must_be_initializable(self):
        self.dummy.initialize()

    def test_display_must_be_initialized_before_draw_image(self):
        self.spy.draw(0, 0, DUMMY_IMAGE)
        assert "initialize" in self.spy.called_funcs

    def test_dont_let_display_initialize_more_than_once(self):
        self.dummy.initialize()

        with self.assertRaises(AlreadyInitialized):
            self.dummy.initialize()

    def test_after_finalize_display_can_initialize_again(self):
        self.dummy.initialize()
        self.dummy.finalize()
        self.dummy.initialize()

    def test_restart_display_must_finalize_then_initialize(self):
        self.spy.initialize()

        self.spy.restart()

        assert tuple(self.spy.called_funcs) == ("initialize", "finalize", "initialize")


class TestDisplayDraw(unittest.TestCase):
    def setUp(self) -> None:
        self.d = DummyDisplay()

    def test_when_invalid_image_is_sent_then_raise_exception(self):
        with self.assertRaises(InvalidImage):
            self.d.draw(0, 0, None)

    def test_when_valid_image_is_sent_then_no_exception(self):
        self.d.draw(0, 0, DUMMY_IMAGE)


def images_are_equal(img1: Image.Image, img2: Image.Image):
    if img1.width != img2.width or img1.height != img2.height:
        return False
    return not ImageChops.difference(img1.convert('RGB'), img2.convert('RGB')).getbbox()


class TestImageDisplay(unittest.TestCase):
    def setUp(self) -> None:
        self.d = ImageDisplay(10, 10)

    def test_when_image_is_drawn_out_of_limits_then_nothing_is_drawn(self):
        image = Image.new('RGB', (10, 10), 'rgb(255,0,0)')
        self.d.initialize()
        current = self.d.get_image()
        self.d.draw(20, 20, image)

        assert images_are_equal(current, self.d.get_image())

    def test_when_image_is_drawn_inside_limits_then_image_is_drawn(self):
        image = Image.new('RGB', (10, 10), 'rgb(255,0,0)')
        self.d.initialize()
        current = self.d.get_image()

        result_image = current.copy()
        result_image.paste(image, (0, 0))

        self.d.draw(0, 0, image)

        assert images_are_equal(result_image, self.d.get_image())

    def test_when_display_is_restarted_then_image_must_reset(self):
        image = Image.new('RGB', (10, 10), 'rgb(255,0,0)')

        self.d.initialize()
        initial_image = self.d.get_image()
        self.d.draw(0, 0, image)
        self.d.restart()

        assert images_are_equal(initial_image, self.d.get_image())


class Rotation:
    Clockwise = -90
    CounterClockwise = 90
    UpsideDown = 180


class TestImageDisplayRotated(unittest.TestCase):
    def setUp(self) -> None:
        self.lamp_post = Image.new('RGB', (10, 20), 'rgb(255,0,0)')
        self.lamp_post.paste(Image.new('RGB', (10, 10), 'rgb(0,255,0)'), (0, 0))

    def test_when_display_is_not_rotated_then_result_image_must_not_be_rotated(self):
        expected_image = Image.new('RGB', (20, 20))
        expected_image.paste(self.lamp_post, (0, 0))

        d = ImageDisplay(20, 20)
        d.draw(0, 0, self.lamp_post)

        assert images_are_equal(expected_image, d.get_image())

    def test_when_display_is_rotated_then_result_image_must_be_rotated(self):
        expected_image = Image.new('RGB', (20, 20))
        expected_image.paste(self.lamp_post, (0, 0))

        d = ImageDisplay(20, 20, Rotation.Clockwise)
        d.draw(0, 0, self.lamp_post)

        assert images_are_equal(expected_image.rotate(-90), d.get_image())

        d = ImageDisplay(20, 20, Rotation.CounterClockwise)
        d.draw(0, 0, self.lamp_post)

        assert images_are_equal(expected_image.rotate(90), d.get_image())

        d = ImageDisplay(20, 20, Rotation.UpsideDown)
        d.draw(0, 0, self.lamp_post)

        assert images_are_equal(expected_image.rotate(180), d.get_image())


class DummySerialDevice:
    ...


class SerialDisplay(DisplayBase):
    def __init__(self, s):
        super().__init__()
        self.s = s
        ...

    def initialize(self):
        super().initialize()
        self.s.open()

    def finalize(self):
        super().finalize()
        self.s.close()

    def draw(self, x, y, image):
        super().draw(x, y, image)


class SpySerialDevice:
    def __init__(self):
        self.called_funcs = []

    def open(self):
        self.called_funcs.append("open")

    def close(self):
        self.called_funcs.append("close")


class TestSerialDisplay(unittest.TestCase):
    def test_create_serial_display(self):
        s = DummySerialDevice()
        SerialDisplay(s)

    def test_when_serial_display_is_initialized_a_serial_connection_must_be_opened(self):
        s = SpySerialDevice()
        d = SerialDisplay(s)
        d.initialize()

        assert "open" in s.called_funcs

    def test_when_serial_display_is_finalized_the_serial_connection_must_be_closed(self):
        s = SpySerialDevice()
        d = SerialDisplay(s)
        d.initialize()
        d.finalize()

        print(s.called_funcs)
        assert tuple(s.called_funcs) == ('open', 'close')


if __name__ == '__main__':
    unittest.main()
