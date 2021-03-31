from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import numpy as np
from matplotlib import cm
from PIL import Image
from scipy.ndimage import gaussian_filter
import random


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
        image = np.asarray(Image.open("maxresdefault.jpg"))
        image_resolution = image.shape[:-1]
        ccd_frame = np.zeros(image_resolution)
        ccd_frame = generate_random_points(ccd_frame, 3)
        ccd_frame = gaussian_filter(ccd_frame, sigma=75.0)
        ccd_frame = cm.inferno(normalise_matrix(ccd_frame))[:, :, :-1]
        self.tex = Texture.create(size=(image_resolution[1], image_resolution[0]))
        self.image = image * ccd_frame
        self.image = np.flipud(self.image)
        self.image = self.image.astype(np.ubyte)

        self.tex.blit_buffer(self.image.tobytes(), colorfmt='rgb')

        # Arranging Canvas
        with self.canvas:
            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.),
                                  texture=self.tex,
                                  color=Color(1, 1, 1, mode='rgb'))

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
