from ursina import *
from ursina.color import *
from math import floor

class PixelEditor(Entity):
    def __init__(self, texture, **kwargs):
        super().__init__(
            parent=camera.ui,
            model='quad',
            texture=texture,
            collider='box',
            )
        self.texture.filtering = False

        self.cursor = Entity(parent=self, model='quad', origin=(-.5,-.5), scale=(1/self.texture.width, 1/self.texture.height), color=red, z=-.1)
        self.cursor.model.mode = 'line'
        self.cursor.model.generate()

        self.selected_color = black
        self.selected_color_indicator = Entity(parent=self, model='quad', scale=.05, color=self.selected_color, x=-.75)
        self.palette = Entity(parent=self, position=(-.75,-.05))
        for col in (
            white, light_gray, gray, black,
            red, orange, yellow, lime,
            green, turquoise, cyan, azure,
            blue, violet, magenta, pink
        ):

            b = Button(parent=self.palette, scale=.05, model='quad', color=col)
            b.on_click = Func(setattr, self, 'selected_color', col)

        grid_layout(self.palette.children, max_x=4)

        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        self.cursor.enabled = self.hovered
        if self.hovered:
            self.cursor.position = mouse.point
            self.cursor.x = floor(self.cursor.x * self.texture.width) / self.texture.width
            self.cursor.y = floor(self.cursor.y * self.texture.height) / self.texture.height

            if mouse.left:
                x, y = int((self.cursor.x+.5) * self.texture.width), int((self.cursor.y+.5) * self.texture.height)

                if held_keys['alt']:
                    self.selected_color = self.texture.get_pixel(x, y)
                    print('-----', self.selected_color)
                else:
                    self.texture.set_pixel(x, y, self.selected_color)
                    self.texture.apply()
    # def on_click(self):
    #     print(x, y)


if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov =3
    PixelEditor('brick')
    app.run()
