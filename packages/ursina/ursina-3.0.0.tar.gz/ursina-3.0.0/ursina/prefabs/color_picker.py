from ursina import *


class ColorPicker(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui)
        # self.model='quad'
        # self.y = .3
        # self.scale *= .25
        self.color_field = None
        self.enabled = True
        self.z = -10
        # self.origin=(-.5,-.5)
        # self.color_field = Panel(parent=self.model, model='quad', scale=.75, z=-.01, color=color.white, collider='box')
        for i, name in enumerate(('r', 'g', 'b')):
            slider = Slider(min=0, max=255, step=1, text=name, dynamic=True,
                world_parent=self, scale=(2/4, 1), position=(0,.035+(i*.03),-1))
            # slider.world_scale = (7.5, 16)
            # slider.model = 'quad'
            # slider.knob.model.mode = 'line'
            # slider.knob.model.thickness = 2
            # slider.knob.model.generate()
            slider.knob.world_scale_x = slider.knob.world_scale_y
            # slider.knob.text_entity.position = (0,-.015)

            slider.label.world_scale_x = slider.label.world_scale_y
            # slider.label.x = -.06
            slider.label.x = .56
            # slider.on_value_changed = self.on_rgb_slider_changed
            setattr(self, name+'_slider', slider)

        self.bg = Panel(parent=self, origin=(-.4,-.3), scale=(slider.scale_x*.6, 4*.125), color=color.gray)
        self.apply_button = Button(parent=self, model=Quad(radius=.5, aspect=.25/.03/1), text='select', color=color.azure,
            scale=(.235,.03), origin=(-.5,0), x=.02)
        self.cancel = Button(parent=self, model=Quad(radius=.5), text='<gray>x', color=color.red,
            scale=(.03,.03), x=slider.x, on_click=Func(setattr, self, 'enabled', False), highlight_color=color.blue)
        # self.scale /= 4
        # self.r = Slider(parent=self)
        #
        # for i, c in enumerate(('rgb')):
        #     s = Slider(world_parent=self, text=c, min=0, max=255, y=-i*.05)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def input(self, key):
        if key == 'left mouse down':
            if not mouse.hovered_entity:
                self.enabled = False
                return
            if mouse.hovered_entity.has_ancestor(self) or mouse.hovered_entity == self.color_field:
                return

            self.enabled = False


class ColorField(Button):

    color_picker = None

    def __init__(self, text='', **kwargs):
        super().__init__(
            scale = (Text.size*4, Text.size*2),
        )
        if not ColorField.color_picker:
            ColorField.color_picker = ColorPicker()

        if text:
            self.text = text
            self.text_entity.origin = (-.5, 0)
            self.text_entity.x = .6

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def on_click(self):
        ColorField.color_picker.color_field = self
        invoke(setattr, ColorField.color_picker, 'enabled', True, delay=.1)
        ColorField.color_picker.position = mouse.position
        ColorField.color_picker.z = -10

        # print(self.color.r, self.color.g, self.color.b)
        ColorField.color_picker.r_slider.value = self.color.r * 255
        ColorField.color_picker.g_slider.value = self.color.g * 255
        ColorField.color_picker.b_slider.value = self.color.b * 255












if __name__ == '__main__':
    app = Ursina()

    ColorField(text='primary')
    ColorField(y=-Text.size*2.1, text='secondary_color', color=color.orange)

    app.run()
