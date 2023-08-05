import unittest
import os
from gradio import inputs

BASE64_IMG = "data:image/jpeg;base64,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"
BASE64_SKETCH = "data:image/png;base64,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"
RAND_STRING = "2wBDAAYEBQYFBAYGBQYHBwYIC"
PACKAGE_NAME = 'gradio'


class TestSketchpad(unittest.TestCase):
    def test_path_exists(self):
        inp = inputs.Sketchpad()
        path = inputs.BASE_INPUT_INTERFACE_JS_PATH.format(inp.__class__.__name__.lower())
        self.assertTrue(os.path.exists(os.path.join(PACKAGE_NAME, path)))

    def test_preprocessing(self):
        inp = inputs.Sketchpad()
        array = inp.preprocess(BASE64_SKETCH)
        self.assertEqual(array.shape, (1, 28, 28))


class TestWebcam(unittest.TestCase):
    def test_path_exists(self):
        inp = inputs.Webcam()
        path = inputs.BASE_INPUT_INTERFACE_JS_PATH.format(inp.__class__.__name__.lower())
        self.assertTrue(os.path.exists(os.path.join(PACKAGE_NAME, path)))

    def test_preprocessing(self):
        inp = inputs.Webcam()
        array = inp.preprocess(BASE64_IMG)
        self.assertEqual(array.shape, (224, 224, 3))


class TestTextbox(unittest.TestCase):
    def test_path_exists(self):
        inp = inputs.Textbox()
        path = inputs.BASE_INPUT_INTERFACE_JS_PATH.format(
            inp.__class__.__name__.lower())
        self.assertTrue(os.path.exists(os.path.join(PACKAGE_NAME, path)))

    def test_preprocessing(self):
        inp = inputs.Textbox()
        string = inp.preprocess(RAND_STRING)
        self.assertEqual(string, RAND_STRING)


class TestImageUpload(unittest.TestCase):
    def test_path_exists(self):
        inp = inputs.Image()
        path = inputs.BASE_INPUT_INTERFACE_JS_PATH.format(inp.__class__.__name__.lower())
        self.assertTrue(os.path.exists(os.path.join(PACKAGE_NAME, path)))

    def test_preprocessing(self):
        inp = inputs.Image()
        array = inp.preprocess(BASE64_IMG)
        self.assertEqual(array.shape, (224, 224, 3))

    def test_preprocessing(self):
        inp = inputs.Image()
        inp.image_height = 48
        inp.image_width = 48
        array = inp.preprocess(BASE64_IMG)
        self.assertEqual(array.shape, (48, 48, 3))

if __name__ == '__main__':
    unittest.main()