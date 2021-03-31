from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import numpy as np
from matplotlib import cm
from PIL import Image
from scipy.ndimage import gaussian_filter
import random
import time


#  class in which we are creating the canvas
def generate_random_points(frame, number_of_points):
    for _ in range(number_of_points):
        frame[random.randrange(1, 720), random.randrange(1, 1280)] = 1
    return frame


def normalise_matrix(frame: np.ndarray):
    return (frame - frame.min()) / (frame.max() - frame.min())


class CanvasWidget(Widget):

    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        self.fps = 10
        self.image = np.asarray(Image.open("maxresdefault.jpg"))
        self.image_resolution = self.image.shape[:-1]
        self.tex = Texture.create(size=(self.image_resolution[1], self.image_resolution[0]))
        self.update()

    def update(self):
        ccd_frame = np.zeros(self.image_resolution)
        ccd_frame = generate_random_points(ccd_frame, 20)
        ccd_frame = gaussian_filter(ccd_frame, sigma=25.0)
        ccd_frame = normalise_matrix(ccd_frame)
        ccd_frame = np.repeat(ccd_frame[:, :, np.newaxis], 4, axis=2)
        # ccd_frame = cm.inferno(ccd_frame)
        self.image = np.array(ccd_frame * 255).astype(np.uint8)
        self.image = np.flipud(self.image)
        self.image = self.image.astype(np.ubyte)

        self.tex.blit_buffer(self.image.tobytes(), colorfmt='rgba')

        # Arranging Canvas
        with self.canvas:
            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.),
                                  texture=self.tex,
                                  color=Color(1, 1, 1, mode='rgba'))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

            # update function which makes the canvas adjustable.

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # Create the App Class


class CanvasApp(App):
    def build(self):
        return CanvasWidget()

    # run the App


CanvasApp().run()
