import re
import math
import random
import networkx as nx
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsEllipseItem, QGraphicsLineItem,
                               QGraphicsPolygonItem, QGraphicsTextItem)
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPen, QBrush, QPolygonF, QPainter, QFont
from pathlib import Path

__all__ = ['Graph']

def parse_graph(base_path, path=None):
    base_path = Path(base_path)


    def get_links(_path):
        with open(_path, 'r', encoding='utf-8') as f:
            text = f.read()
        pattern = r'\[\[(.*?)\]\]'
        raw = re.findall(pattern, text)
        return [Path(f"{base_path}\\{e}") for e in raw]

    graph = nx.DiGraph()


    for path_ in base_path.rglob('*'):
        if path_.is_file():
            graph.add_node(path_.resolve(), name=path_.name)

    for path_ in base_path.rglob('*'):
        if path_.is_file():
            name1 = path_.resolve()
            names = get_links(path_.resolve())
            names = [t for t in names if t.exists()]
            [graph.add_edge(name1, name) for name in names]

    if path is not None:
        return graph.subgraph(nx.node_connected_component(graph.to_undirected(), Path(path)))
    else:
        return graph

class NodeItem(QGraphicsEllipseItem):
    """Узел графа (круг + текстовая метка)."""
    def __init__(self, path, name, x, y, parent,  radius=14):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.parent = parent
        self.path = path
        self.name = name
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.fx = 0.0
        self.fy = 0.0
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.blue))
        self.setPen(QPen(Qt.black, 1))
        self.setZValue(2)

        # Текстовая
        self.label = QGraphicsTextItem(name, self)
        self.label.setFont(QFont("Arial", 8))
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, -rect.height() / 2 - radius - 5)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setZValue(2.1)


    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.parent.ww.on_md_opened(str(self.path), False)


class Edge:
    """Ориентированное ребро: линия + треугольная стрелка."""
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.line = QGraphicsLineItem()
        self.line.setPen(QPen(Qt.gray, 1))
        self.line.setZValue(0)
        self.arrow = QGraphicsPolygonItem()
        self.arrow.setPen(QPen(Qt.NoPen))
        self.arrow.setBrush(QBrush(Qt.gray))
        self.arrow.setZValue(1)
        self.update_positions()

    def shrink_source(self):
        dx = self.dest.x - self.source.x
        dy = self.dest.y - self.source.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return self.source.x, self.source.y
        r = self.source.radius
        return (self.source.x + dx / dist * r,
                self.source.y + dy / dist * r)

    def shrink_dest(self):
        dx = self.dest.x - self.source.x
        dy = self.dest.y - self.source.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return self.dest.x, self.dest.y
        r = self.dest.radius + 6
        return (self.dest.x - dx / dist * r,
                self.dest.y - dy / dist * r)

    def update_positions(self):
        dx = self.dest.x - self.source.x
        dy = self.dest.y - self.source.y
        angle = math.atan2(dy, dx)

        sx, sy = self.shrink_source()
        dx2, dy2 = self.shrink_dest()
        self.line.setLine(sx, sy, dx2, dy2)

        r = self.dest.radius + 6
        ax = self.dest.x - math.cos(angle) * r
        ay = self.dest.y - math.sin(angle) * r
        arrow_size = 10
        poly = QPolygonF()
        poly.append(QPointF(0, 0))
        poly.append(QPointF(-arrow_size, -arrow_size / 2))
        poly.append(QPointF(-arrow_size, arrow_size / 2))
        self.arrow.setPolygon(poly)
        self.arrow.setPos(ax, ay)
        self.arrow.setRotation(math.degrees(angle))


class Graph(QGraphicsView):
    """Интерактивное представление ориентированного графа с физической симуляцией."""
    def __init__(self, base_path, path, ww):
        self.base_path = base_path
        self.ww = ww
        self.path = path

        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        self.node_map = {}
        self.nodes = []
        self.edges = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_physics)
        self.timer.start(30)

        self.dragged_node = None
        self._panning = False
        self._pan_start = QPointF()

        graph = parse_graph(self.base_path, self.path)
        self.set_graph(graph)

    def set_graph(self, G):
        """Принимает networkx.DiGraph и строит сцену."""
        self.scene.clear()
        self.node_map.clear()
        self.nodes.clear()
        self.edges.clear()

        if G is None:
            return

        self.scene.setSceneRect(-2000, -2000, 4000, 4000)

        for n, data in G.nodes(data=True):
            x = random.uniform(-600, 600)
            y = random.uniform(-400, 400)
            name = data.get('name')
            node = NodeItem(n, name, x, y, self, radius=14)
            self.scene.addItem(node)
            self.node_map[n] = node
            self.nodes.append(node)

        for u, v in G.edges():
            if u in self.node_map and v in self.node_map:
                src = self.node_map[u]
                dst = self.node_map[v]
                edge = Edge(src, dst)
                self.scene.addItem(edge.line)
                self.scene.addItem(edge.arrow)
                self.edges.append(edge)

    def _update_physics(self):
        if not self.nodes:
            return

        repulsion = 5000.0
        attraction = 0.005
        gravity = 0.003
        damping = 0.85
        max_vel = 8.0
        rest_length = 120.0
        cx, cy = 0, 0

        for node in self.nodes:
            node.fx = node.fy = 0.0

        # Отталкивание
        for i in range(len(self.nodes)):
            a = self.nodes[i]
            for j in range(i + 1, len(self.nodes)):
                b = self.nodes[j]
                dx = a.x - b.x
                dy = a.y - b.y
                dist_sq = dx * dx + dy * dy
                if dist_sq < 1.0:
                    dist_sq = 1.0
                force = repulsion / dist_sq
                dist = math.sqrt(dist_sq)
                fx = force * dx / dist
                fy = force * dy / dist
                a.fx += fx
                a.fy += fy
                b.fx -= fx
                b.fy -= fy

        # Притяжение вдоль рёбер
        for edge in self.edges:
            src = edge.source
            dst = edge.dest
            dx = dst.x - src.x
            dy = dst.y - src.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            force = attraction * (dist - rest_length)
            fx = force * dx / dist
            fy = force * dy / dist
            src.fx += fx
            src.fy += fy
            dst.fx -= fx
            dst.fy -= fy

        # Гравитация
        for node in self.nodes:
            node.fx += gravity * (cx - node.x)
            node.fy += gravity * (cy - node.y)

        # Обновление скоростей и позиций
        for node in self.nodes:
            if node is self.dragged_node:
                node.vx = node.vy = 0.0
                continue
            node.vx = (node.vx + node.fx) * damping
            node.vy = (node.vy + node.fy) * damping
            speed = math.hypot(node.vx, node.vy)
            if speed > max_vel:
                node.vx = node.vx / speed * max_vel
                node.vy = node.vy / speed * max_vel
            node.x += node.vx
            node.y += node.vy
            node.setPos(node.x, node.y)

        for edge in self.edges:
            edge.update_positions()

    # ---- Мышь ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(pos, self.transform())
            if isinstance(item, NodeItem):
                self.dragged_node = item
                item.vx = item.vy = 0.0
                self.setCursor(Qt.ClosedHandCursor)
                event.accept()
                return
        elif event.button() == Qt.RightButton:
            # Начинаем панорамирование
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning:
            # Вычисляем смещение в координатах viewport и сдвигаем полосы прокрутки
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return
        if self.dragged_node:
            pos = self.mapToScene(event.pos())
            self.dragged_node.x = pos.x()
            self.dragged_node.y = pos.y()
            self.dragged_node.setPos(pos.x(), pos.y())
            for edge in self.edges:
                if edge.source is self.dragged_node or edge.dest is self.dragged_node:
                    edge.update_positions()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self._panning:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        if event.button() == Qt.LeftButton and self.dragged_node:
            self.dragged_node = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1 / factor, 1 / factor)
