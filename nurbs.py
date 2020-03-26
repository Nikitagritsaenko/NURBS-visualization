import sys
import math

from PyQt5 import QtGui, QtCore, QtWidgets, QtTest, uic
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

import numpy as np

width = 800
height = 600

class NurbsDrawer(QtWidgets.QMainWindow):
    qp = QtGui.QPainter() 

    # define all NURBS params
    points = [ 
              (-240, -220, 1),
              (-330, -40, 1),
              (-230, 250, 1),
              (40, 270, 1),
              (190, 80, 1),
              (-60, -270, 1),
              (170, -60, 1),
            ]
    weights = [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]
    knots = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    degree = 6

    # define visualizator params
    draw_step = 0.001
    visualize_step = 0.01
    curr_x = 0.5
    colors = [Qt.green, Qt.magenta, Qt.cyan, Qt.darkYellow, Qt.blue, Qt.darkGreen]

    def paintEvent(self, e):
        self.qp.begin(self)

        for p in self.points:
            self.draw_circle(p[0], p[1], 3, Qt.green)

        for i in range(1, len(self.points)):
            x1 = self.points[i-1][0]
            y1 = self.points[i-1][1]
            x2 = self.points[i][0]
            y2 = self.points[i][1]
            self.draw_line(x1, y1, x2, y2)

        self.draw_deBoor(self.points, self.curr_x)

        t = float("{0:.3f}".format(self.curr_x))
        text = "t = " + str(t)
        self.qp.drawText(400, 25, text)

        self.qp.end()

    def mouseMoveEvent(self, e):
        print(e.x(), e.y())
        min_dist = (width ** 2 + height ** 2) ** 0.5
        touched_point_idx = 0

        for i in range(0, len(self.points)):
            point = self.points[i]
            px = point[0] + width/2
            py = -point[1] + height/2
            dist = ((px - e.x()) ** 2 + (py - e.y()) ** 2) ** 0.5 
            if min_dist > dist:
                min_dist = dist
                touched_point_idx = i

        if (min_dist < 75):
            self.points[touched_point_idx] = (e.x() - width/2, -e.y() + height/2, 1)
            self.update()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Left:
             if (self.curr_x - self.visualize_step >= 0):
                 self.curr_x -= self.visualize_step
             event.accept()
         elif event.key() == Qt.Key_Right:
             if (self.curr_x + self.visualize_step <= 1):
                 self.curr_x += self.visualize_step
             event.accept() 
         else:
             event.ignore()

    def draw_line(self, x1, y1, x2, y2):
        self.qp.setPen(QPen(Qt.gray, 1))
        x1 = x1 + width/2
        y1 = -y1 + height/2
        x2 = x2 + width/2
        y2 = -y2 + height/2
        self.qp.drawLine(x1, y1, x2, y2)

    def draw_pixel(self, x, y):
        self.qp.setPen(QPen(Qt.black,  2))
        x = x + width/2
        y = -y + height/2
        self.qp.drawPoint(x,y)

    def draw_circle(self, x, y, r, color):
        self.qp.setPen(QPen(color, 9))
        x0 = x + width/2
        y0 = -y + height/2
        self.qp.drawEllipse(x0, y0, r, r)


    def deBoor(self, r, p, i, x, t, c, visualize):
        if r == 0:
            return c[i]
        else:
            alpha = (x - t[i]) / (t[i+p+1-r] - t[i])
            p1 = self.deBoor(r - 1, p, i - 1, x, t, c, visualize)
            p2 = self.deBoor(r - 1, p, i, x, t, c, visualize)
            if visualize:
                self.draw_line(p1[0] / p1[2], 
                               p1[1] / p1[2], 
                               p2[0] / p2[2], 
                               p2[1] / p2[2])

                self.draw_circle(p1[0] / p1[2],
                                 p1[1] / p1[2], 
                                 3,
                                 self.colors[r-1])

                self.draw_circle(p2[0] / p2[2],
                                 p2[1] / p2[2], 
                                 3,
                                 self.colors[r-1])
            return p1 * (1 - alpha) + p2 * alpha

    def draw_deBoor(self, points, x_visual):
        points = np.asarray(points)

        nurbs_points = [point for point in points]

        for i in range(0, len(points)):
            nurbs_points[i] = (int(nurbs_points[i][0] * self.weights[i]), 
                               int(nurbs_points[i][1] * self.weights[i]), 
                               int(nurbs_points[i][2] * self.weights[i]))

        nurbs_points = np.asarray(nurbs_points)

        for x in np.arange(0, 1, self.draw_step):
            k = 0
            for i in range(1, len(self.knots)):
                if (x < self.knots[i] and x >= self.knots[i-1]):
                    k = i-1
                    break

            visualize = False
            if np.abs(x - x_visual) < self.draw_step:
                visualize = True
        
            new_point = self.deBoor(self.degree, self.degree, k, x, self.knots, nurbs_points, visualize)

            if visualize:
                self.draw_circle(new_point[0] / new_point[2], 
                                 new_point[1] / new_point[2], 
                                 3, 
                                 Qt.red)
                self.update()

            self.draw_pixel(new_point[0] // new_point[2], 
                            new_point[1] // new_point[2])

def main(args):
    app = QtWidgets.QApplication(sys.argv)
    ex = NurbsDrawer()
    ex.resize(width, height)
    ex.show()
    app.exec_()

if __name__=='__main__':
    main(sys.argv[1:])
