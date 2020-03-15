import sys
import math

from PyQt5 import QtGui, QtCore,  QtWidgets, uic
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5.QtCore import Qt
from PyQt5 import QtTest

import numpy as np

width = 800
height = 600

def rotate(l, n):
    return l[n:] + l[:n]

class NurbsDrawer(QtWidgets.QMainWindow):
    qp = QtGui.QPainter() 
    points = [(250, -250, 1), 
              (-250, 100, 1), 
              (-100, 250, 1), 
              (0, 100, 1), 
              (100, 250, 1), 
              (250, 100, 1), 
              (-250, -250, 1)]

    points = rotate(points, 1)
    weights = [1.0, 1.0, 1.0, 10.0, 1.0, 1.0, 1.0]
    weights = rotate(weights, 1)

    def paintEvent(self, e):
        self.qp.begin(self)
        
        for p in self.points:
            self.draw_circle(p[0], p[1], 3)

        for i in range(1, len(self.points)):
            x1 = self.points[i-1][0]
            y1 = self.points[i-1][1]
            x2 = self.points[i][0]
            y2 = self.points[i][1]
            self.draw_line(x1, y1, x2, y2)

        self.draw_deBoor(self.points)

        self.qp.end()

    def mouseMoveEvent(self, e):
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

        if (min_dist < 50):
            self.points[touched_point_idx] = (e.x() - width/2, -e.y() + height/2, 1)
            self.update()
                

    def draw_line(self, x1, y1, x2, y2):
        self.qp.setPen(QPen(Qt.gray, 1))
        x1 = x1 + width/2
        y1 = -y1 + height/2
        x2 = x2 + width/2
        y2 = -y2 + height/2
        self.qp.drawLine(x1, y1, x2, y2)

    def draw_pixel(self, x, y):
        self.qp.setPen(QPen(Qt.black,  1))
        x = x + width/2
        y = -y + height/2
        self.qp.drawPoint(x,y)

    def draw_circle(self, x, y, r):
        self.qp.setPen(QPen(Qt.green,  6))
        x0 = x + width/2
        y0 = -y + height/2
        self.qp.drawEllipse(x0, y0, r, r)
        
    def deBoor(self, k: int, x: int, t, c, p: int):
        
        d = [c[j + k - p] for j in range(0, p+1)]

        for r in range(1, p+1):
            for j in range(p, r-1, -1):
                alpha = (x - t[j+k-p]) / (t[j+1+k-r] - t[j+k-p])
                d[j] = (1.0 - alpha) * d[j-1] + alpha * d[j]

        return d[p]

    def draw_deBoor(self, points):
        px = [point[0] for point in points]
        px = np.sort(px)
        px = np.asarray(px)

        points = np.asarray(points)
        degree = 2
        
        t = np.linspace(px[0], px[len(px)-1], num = len(points) + degree + 1)
        x = px[0]
        
        while (x <= px[len(px)-1]):
            k = 0
            for i in range(1, len(points) + 1):
                if (x < t[i] and x >= t[i-1]):
                    k = i-1
                    break
           
            nurbs_points = [point for point in points]
            for i in range(0, len(points)):
                nurbs_points[i] = (int(nurbs_points[i][0] * self.weights[i]), 
                                   int(nurbs_points[i][1] * self.weights[i]), 
                                   int(nurbs_points[i][2] * self.weights[i]))

            nurbs_points = np.asarray(nurbs_points)
                
            new_point = self.deBoor(k, x, t, nurbs_points, degree)
            self.draw_pixel(new_point[0] // new_point[2], 
                            new_point[1] // new_point[2])
            x += 0.1

def main(args):
    app = QtWidgets.QApplication(sys.argv)
    
    ex = NurbsDrawer()
    ex.resize(width, height)
    ex.show()
    app.exec_()
    
if __name__=='__main__':
    main(sys.argv[1:])