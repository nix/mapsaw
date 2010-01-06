# Copyright (c) 2010 Nick Thompson
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
interactive view of a dataset.

currently uses glumpy.

glumpy is totally awesome but sometimes it freaks out.

"""

import numpy as N

def glumpy_loop(raster):
    import glumpy
    import pyglet
    import pyglet.gl as gl

    if raster.dtype == N.float64:
        raster = N.array(raster, N.float32)

    img = glumpy.Image(raster,
                       #np.array(cloudlum,dtype=np.float32), cmap=glumpy.colormap.Grey,
                       #np.array(image, np.float32),  #image,
                       interpolation='nearest')
    sy,sx = raster.shape[:2]

    window = pyglet.window.Window(sx, sy, resizable=True)

    cmap = glumpy.colormap.Colormap((0.,   (0.,0.,0.,1.)),
                                    (0.5,  (1.,1.,1.,1.)),
                                    (1.,   (0.,0.,0.,1.)))
    #(1.,   (1.,1.,1.,1.)))
    #cmap.set_alpha(0.3)

    @window.event
    def on_draw():
        gl.glClearColor(255, 255, 255, 255)
        window.clear()

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        #print marble.shape, clouds.shape, I.shape

        gl.glColor4f(1,1,1,1)
        img.blit(0, 0, window.width, window.height)

    def update(dt):
        pass

    pyglet.clock.schedule(update)
    pyglet.clock.set_fps_limit(30)
    pyglet.app.run()


