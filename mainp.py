import pyglet

window = pyglet.window.Window()
image = pyglet.resource.image('logo.png')
sprite = pyglet.sprite.Sprite(img=image)
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    sprite.draw()
    
def update(dt):
    # Move 10 pixels per second
    sprite.x += dt * 10
pyglet.clock.schedule_interval(update, 1/60.)
pyglet.app.run()