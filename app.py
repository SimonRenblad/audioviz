import numpy as np
import ctypes
import sys

import soundcard as sc
import scipy as sp

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox, QLabel, QHBoxLayout, QWidget
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal, QThread, QObject

# normalizes it to be between 0 and 1 instead of -1, 1
vertex_shader = """
#version 330

// we can assume the z axis here is 0, but requires vec attri
layout(location = 0) in vec3 aPos;

out vec2 fragCoord;

void main()
{
    gl_Position =  vec4(aPos,1);
    fragCoord  = (aPos.xy+vec2(1,1))/2.0;
}"""

fragment_shader = """
#version 330 core

in vec2 fragCoord;
out vec4 fragColor;

// below are stolen from cava as they turn out to be useful shaders
// use uniforms / uniform buffers to alter the visualization every draw call
// bar values. defaults to left channels first (low to high), then right (high to low).
uniform float bars[512];

// uniform int bars_count;  // number of bars (left + right) (configurable)
// uniform int bar_width;   // bar width (configurable), not used here
// uniform int bar_spacing; // space between bars (configurable)

void main() {
    if (fragCoord.x > 0.5) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
}
"""

class MainCanvas(QOpenGLWidget):
    def __init__(self):
        QOpenGLWidget.__init__(self)

    def initializeGL(self):
        # compile the shader program
        self.shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
                            compileShader(fragment_shader, GL_FRAGMENT_SHADER))


        # define the widget to use this program
        glUseProgram(self.shader)

        self.bar_location = glGetUniformLocation(self.shader, "bars")

        # define buffers
        # input data (x, y, z) (monocolor)
        vertices = [
             -1.0, -1.0,
             1.0, -1.0,
             1.0, 1.0,
             -1.0, 1.0,
        ]
        self.vertices = np.array(vertices, dtype=np.float32)

        # indices define elements based on connecting vertices (reuse)
        indices = [
            0, 1, 2, 3
        ]
        self.indices = np.array(indices, dtype=np.int32)

        # vertex buffer object
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0))
        
        # set background color
        glClearColor(0.2, 0.3, 0.3, 1.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.shader)
        # triangle fan sets one as a hub and then the rest connect to it (hence FAN)
        glDrawElements(GL_TRIANGLE_FAN, 4, GL_UNSIGNED_INT, ctypes.c_void_p(0))

    # buffer slot
    def set_data(self, data):
        # process fft data here for now
        yf = sp.fft.fft(data)
        N = 512
        mag = 2/512 * np.abs(yf)
        # change uniform data here
        glUniform1fv(self.bar_location, 512, mag)
        self.update()


class AudioWorker(QObject):
    # define signals that emit info to be displayed in the frame buffer
    buffer = pyqtSignal(np.ndarray)
    ping = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    # what will be run by the thread
    def run(self):
        self.ping.emit()
        mic = sc.get_microphone(str(sc.default_speaker().name), include_loopback=True)
        # -1 -> mono mix of all channels on linux
        with mic.recorder(44100, channels=[-1]) as r:
            while not QThread.currentThread().isInterruptionRequested():
                data = r.record(numframes=512)
                self.buffer.emit(data.ravel())




class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("audioviz")
        layout = QHBoxLayout()
        self.canvas = MainCanvas()
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #run the main thread
        self._audio_thread = QThread()
        self._audio_thread.setObjectName("AudioThread")
        self._audio_worker = AudioWorker()
        self._audio_worker.moveToThread(self._audio_thread)

        self._audio_worker.buffer.connect(self.canvas.set_data)
        self._audio_thread.started.connect(self._audio_worker.run)
        self._audio_thread.start()

    def closeEvent(self, ev):
        self._audio_thread.requestInterruption()
        ev.accept()


if __name__ == "__main__":
    app = QApplication(["Audio Visualizer"])
    main_window = MainWindow()
    main_window.show()
    app.exec()
