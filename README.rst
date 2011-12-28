`glglue` provide boilerplate codes that glue OpenGL with some GUI.
it is handling mouse event, keyboard event, window resize event and draw event. 

Requirements
============
* Python 2.7

Features
========
* glut window
* tkinter's togl widget
* pyQt4's qgl widget
* wxPython's GLCanvas widget

Usage
=====

glut
----
::

    #!/usr/bin/python
    # coding: utf8

    import glglue.sample
    import glglue.glut

    if __name__=="__main__":
        controller=glglue.sample.SampleController()
        glglue.glut.mainloop(controller)

