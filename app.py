import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox
from PyQt6.QtGui import QAction, QKeySequence

vertex_shader = """
#version 330 core

void main() {
    
}
"""

fragment_shader = """
#version 330 core

in vec2 fragCoord;
out vec4 fragColor;

// below are stolen from cava as they turn out to be useful shaders
// use uniforms / uniform buffers to alter the visualization every draw call
// bar values. defaults to left channels first (low to high), then right (high to low).
uniform float bars[512];

uniform int bars_count;  // number of bars (left + right) (configurable)
uniform int bar_width;   // bar width (configurable), not used here
uniform int bar_spacing; // space between bars (configurable)

void main() {
    
}
"""

class MainCanvas(QOpenGLWidget):
    def __init__(self):
        QOpenGLWidget.__init__(self)

    def initializeGL(self):
        # compile the shader program
        # self.shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
        #                     compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        # define the widget to use this program
        # glUseProgram(self.shader)

        # set background color
        glClearColor(0.2, 0.3, 0.3, 1.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("audioviz")
        self.setCentralWidget(MainCanvas())

    def closeEvent(self, ev):
        ev.accept()


if __name__ == "__main__":
    app = QApplication(["Audio Visualizer"])
    main_window = MainWindow()
    main_window.show()
    app.exec()
