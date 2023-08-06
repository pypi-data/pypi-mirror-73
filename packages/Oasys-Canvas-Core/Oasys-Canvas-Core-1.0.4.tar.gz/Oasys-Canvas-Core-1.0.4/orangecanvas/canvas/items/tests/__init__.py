"""
Tests for items
"""
import sys
import traceback
import unittest


class TestItems(unittest.TestCase):
    def setUp(self):
        import logging

        from PyQt5.QtGui import QApplication, QGraphicsScene, QGraphicsView, \
                                QPainter

        from PyQt5.QtCore import QTimer

        logging.basicConfig()

        self.app = QApplication([])
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(
            QPainter.Antialiasing | \
            QPainter.SmoothPixmapTransform | \
            QPainter.TextAntialiasing
            )
        self.view.resize(500, 300)
        self.view.show()
        QTimer.singleShot(10000, self.app.exit)

        def my_excepthook(etype, value, tb):
            sys.setrecursionlimit(1010)
            traceback.print_exception(etype, value, tb)

        self._orig_excepthook = sys.excepthook
        sys.excepthook = my_excepthook
        self.singleShot = QTimer.singleShot

    def tearDown(self):
        self.scene.clear()
        self.scene.deleteLater()
        self.view.deleteLater()
        del self.scene
        del self.view
        self.app.processEvents()
        del self.app
        sys.excepthook = self._orig_excepthook
