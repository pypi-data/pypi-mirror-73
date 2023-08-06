from ursina import *

app = Ursina()

Text('''
F5: reload starting script
F6: reload textures
F7: reload models
F8: toggle hotreloading

F9: reset display mode
F10: cycle display mode (default, wireframe, colliders, normals)
F11: fullscreen/windowed


''',
position=(-.5,.5),
background=True

)



app.run()
