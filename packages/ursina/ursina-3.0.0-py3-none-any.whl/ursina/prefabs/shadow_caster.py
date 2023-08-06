from ursina import *


app = Ursina()

for i in range(4):
    wall = Entity(model='cube', origin=(-.5,-.5,0), scale=(4,2,.5), rotation_y=90*i)
    cube = Entity(model='cube', world_parent=wall, world_scale=.5, position=(.5,0,-5), origin_y=-.5, scale_y=3)

EditorCamera()

light = Entity(model='cube', color=color.yellow, position=(2,3,-2), scale=.25)

ground = Entity(model='plane', scale=10, color=color.brown)

for e in [e for e in scene.entities if not e.eternal and e.model]:
    print(e)
    c = duplicate(e)
    # print(c)

    c.model.mode = 'line'
    c.model.thickness = 2
    c.model.generate()
    c.color = color.azure



app.run()
