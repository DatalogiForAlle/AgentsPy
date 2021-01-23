import sys
import os
import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtChart import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
    QBarSet,
    QBarSeries,
    QBarCategoryAxis,
)
from PyQt5.QtCore import QPointF, QLineF, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPolygonF

from agents.model import (
    Agent,
    Tile,
    Model,
    get_quickstart_model,
    active_model_exists,
    set_active_model,
    AgentShape,
    ButtonSpec,
    ToggleSpec,
    SliderSpec,
    CheckboxSpec,
    LineChartSpec,
    BarChartSpec,
    HistogramSpec,
    AgentGraphSpec,
    MonitorSpec,
    EllipseStruct,
    RectStruct,
)

from multiprocessing import Process, Queue

from random import randint

import cProfile

class UIAgent():
    def __init__(self, x, y, direction, size, shape, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.shape = shape
        self.color = color
        self.selected = False
        self.drawn_paths = []
        self.enable_draw_path = False

    def move(self, new_x, new_y, continue_path):
        if not self.enable_draw_path and continue_path:
            self.drawn_paths.append([])
        self.enable_draw_path = continue_path
        if self.enable_draw_path:
            self.drawn_paths[-1].append(QLineF(self.x,self.y,new_x,new_y))
        self.x = new_x
        self.y = new_y

class UITile():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class SimulationArea(QtWidgets.QWidget):

    output_count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui_agents = {}
        self.__ui_tiles = {}
        self.model_width = 100
        self.model_height = 100
        self.model_tile_size = 8
        self.enable_rendering = True

    """
    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model
        #self.setFixedSize(model.width, model.height)
        self.setFixedSize(500, 500)
        self.enable_rendering = True
    """

    def reset(self):
        self.__ui_agents = {}

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Default to a black background
        white = QtGui.QColor("white")
        painter.setBrush(white)
        painter.drawRect(
            0, 0, painter.device().width()/2, painter.device().height()/2
        )

        # Load/update all simulation area elements (agents/tiles):
        i = 0
        while not Agent._queue.empty():
            msg = Agent._queue.get()
            sender = msg[0]
            command = msg[1]
            if command == "create":
                self.__ui_agents[sender] = UIAgent(msg[2],msg[3],msg[4],
                                                   msg[5],msg[6],msg[7])
            elif command == "update_pos":
                self.__ui_agents[sender].move(msg[2],msg[3],msg[4])
            elif command == "update_dir":
                self.__ui_agents[sender].direction = msg[2]
            elif command == "update_size":
                self.__ui_agents[sender].size = msg[2]
            elif command == "update_shape":
                self.__ui_agents[sender].shape = msg[2]
            elif command == "update_color":
                self.__ui_agents[sender].color = msg[2]
            elif command == "select":
                self.__ui_agents[sender].selected = True
            elif command == "deselect":
                self.__ui_agents[sender].selected = False
            elif command == "reset":
                self.reset()

        while not Tile._queue.empty():
            msg = Tile._queue.get()
            sender = msg[0]
            command = msg[1]
            if command == "create":
                self.__ui_tiles[sender] = UITile(msg[2],msg[3],msg[4])
            elif command == "update_color":
                self.__ui_tiles[sender].color = msg[2]

        # Draw tiles
        for tile in self.__ui_tiles.values():
            self.paintTile(painter, tile)

        # Draw shapes
        """
        for shape in self.model.get_shapes():
            c = shape.color
            painter.setBrush(QtGui.QColor(c[0], c[1], c[2]))
            if type(shape) is EllipseStruct:
                painter.drawEllipse(shape.x, shape.y, shape.w, shape.h)
            elif type(shape) is RectStruct:
                painter.drawRect(shape.x, shape.y, shape.w, shape.h)
        """

        # Draw lines
        for agent in self.__ui_agents.values():
            painter.setPen(QColor(agent.color[0], agent.color[1], agent.color[2]))
            for path in agent.drawn_paths:
                painter.drawLines(path)

        # Draw agents
        select = None
        for agent in self.__ui_agents.values():
            self.paintAgent(painter, agent)
            if agent.selected:
                select = agent

        if select:
            path = QPainterPath()
            path.addRect(0, 0, self.model.width, self.model.height)
            path.addEllipse(
                select.x - select.size * 1.5,
                select.y - select.size * 1.5,
                select.size * 3,
                select.size * 3,
            )
            painter.setBrush(QColor(0, 0, 0, 150))
            painter.drawPath(path)

        painter.setBrush(QColor(255, 255, 255, 200))
        painter.end()


    def paintAgent(self, painter, agent):
        r, g, b = agent.color
        painter.setBrush(QtGui.QColor(r, g, b))
        if agent.shape == AgentShape.CIRCLE:
            painter.drawEllipse(
                agent.x - agent.size / 2,
                agent.y - agent.size / 2,
                agent.size,
                agent.size,
            )
        elif agent.shape == AgentShape.ARROW:
            x = agent.x
            y = agent.y
            d = math.radians(agent.direction)
            s = agent.size
            point_list = [
                QPointF(x + math.cos(d) * s, y + math.sin(d) * s),
                QPointF(x + math.cos(d + 2.3) * s, y + math.sin(d + 2.3) * s),
                QPointF(
                    x + math.cos(d + math.pi) * s / 2,
                    y + math.sin(d + math.pi) * s / 2,
                ),
                QPointF(x + math.cos(d - 2.3) * s, y + math.sin(d - 2.3) * s),
            ]
            painter.drawPolygon(QPolygonF(point_list))
        elif agent.shape == AgentShape.PERSON:
            x = agent.x - agent.size / 2
            y = agent.y - agent.size / 2
            size = agent.size
            point_list = [
                QPointF(x + 0.4 * size, y + 0.4 * size),
                QPointF(x + 0.2 * size, y + 0.5 * size),
                QPointF(x + 0.2 * size, y + 0.6 * size),
                QPointF(x + 0.4 * size, y + 0.5 * size),
                QPointF(x + 0.4 * size, y + 0.8 * size),
                QPointF(x + 0.2 * size, y + size),
                QPointF(x + 0.3 * size, y + size),
                QPointF(x + 0.5 * size, y + 0.85 * size),
                QPointF(x + 0.7 * size, y + size),
                QPointF(x + 0.8 * size, y + size),
                QPointF(x + 0.6 * size, y + 0.8 * size),
                QPointF(x + 0.6 * size, y + 0.5 * size),
                QPointF(x + 0.8 * size, y + 0.6 * size),
                QPointF(x + 0.8 * size, y + 0.5 * size),
                QPointF(x + 0.6 * size, y + 0.4 * size),
            ]
            painter.drawPolygon(QPolygonF(point_list))
            painter.drawEllipse(x + 0.3 * size, y, 0.4 * size, 0.4 * size)
        elif agent.shape == AgentShape.HOUSE:
            x = agent.x - agent.size / 2
            y = agent.y - agent.size / 2
            size = agent.size
            point_list = [
                QPointF(x + 0.5 * size, y),
                QPointF(x, y + 0.5 * size),
                QPointF(x + 0.2 * size, y + 0.5 * size),
                QPointF(x + 0.2 * size, y + size),
                QPointF(x + 0.40 * size, y + size),
                QPointF(x + 0.40 * size, y + 0.7 * size),
                QPointF(x + 0.60 * size, y + 0.7 * size),
                QPointF(x + 0.60 * size, y + size),
                QPointF(x + 0.8 * size, y + size),
                QPointF(x + 0.8 * size, y + 0.5 * size),
                QPointF(x + size, y + 0.5 * size),
            ]
            painter.drawPolygon(QPolygonF(point_list))

    def paintTile(self, painter, tile):
        r, g, b = tile.color
        color = QtGui.QColor(r, g, b)
        painter.setBrush(color)
        x = self.model_tile_size * tile.x
        y = self.model_tile_size * tile.y
        painter.drawRect(x, y, self.model_tile_size, self.model_tile_size)

    def mousePressEvent(self, e):
        x = e.localPos().x()
        y = e.localPos().y()
        self.model.mouse_click(x, y)

    def contextMenuEvent(self, event):
        # Create menu
        menu = QtWidgets.QMenu(self)
        if self.enable_rendering:
            pause_action = menu.addAction("Pause rendering")
        else:
            pause_action = menu.addAction("Start rendering")
        # Open menu
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # Handle user choice
        if action == pause_action:
            self.enable_rendering = not self.enable_rendering


class QtGraph(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        # self.chart.setTitle(str(self.spec.variables))
        # self.chart.legend().hide()

        for i in range(len(self.spec.variables)):
            series = QLineSeries()
            series.setColor(
                QColor(
                    self.spec.colors[i][0],
                    self.spec.colors[i][1],
                    self.spec.colors[i][2],
                )
            )
            series.setName(self.spec.variables[i])
            self.chart.addSeries(series)

        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.chart.createDefaultAxes()
        self.autoscale_y_axis = True
        if self.spec.min_y and self.spec.max_y:
            self.autoscale_y_axis = False
            self.chart.axes()[1].setRange(self.spec.min_y, self.spec.max_y)

        self._updates_per_second = 60
        self._data = []
        self._min = 0
        self._max = 0

    def clear(self):
        for chart in self.chart.series():
            chart.clear()
        self._data = []

    def add_data(self, data):
        self._data.append(data)

    def redraw(self):
        if len(self._data) > 0:
            for i in range(len(self.spec.variables)):
                data = [datapoint[i] for datapoint in self._data]
                datapoint = sum(data) / len(data)
                self.chart.series()[i].append(
                    QPointF(
                        self.chart.series()[i].count()
                        / self._updates_per_second,
                        datapoint,
                    )
                )
                self._min = min(self._min, datapoint)
                self._max = max(self._max, datapoint)
        self.chart.axes()[0].setRange(
            0, (self.chart.series()[0].count() - 1) / self._updates_per_second
        )
        diff = self._max - self._min
        if self.autoscale_y_axis:
            if diff > 0:
                self.chart.axes()[1].setRange(self._min, self._max)
            else:
                self.chart.axes()[1].setRange(self._min - 0.5, self._max + 0.5)
        self._data = []


class QtBarChart(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        # self.chart.setTitle(str(self.spec.variables))
        self.chart.legend().hide()
        self.mainset = QBarSet("")
        self.mainset.append([0 for i in range(len(spec.variables))])
        self.mainset.setColor(
            QColor(spec.color[0], spec.color[1], spec.color[2])
        )
        self.series = QBarSeries()
        self.series.append(self.mainset)

        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.axis_x = QBarCategoryAxis()
        self.axis_y = QValueAxis()
        self.axis_x.append(spec.variables)
        self.chart.addSeries(self.series)
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

        self._updates_per_second = 10
        self._dataset = []

    def clear(self):
        self._dataset = []

    def update_data(self, dataset):
        data = []
        for d in dataset:
            data.append(d)
        self._dataset = data

    def redraw(self):
        if len(self._dataset) > 0:
            for i in range(len(self._dataset)):
                self.mainset.replace(i, self._dataset[i])
            self.axis_y.setRange(0, max(self._dataset))


class QtHistogram(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.setTitle(self.spec.variable)
        self.chart.legend().hide()

        self.mainset = QBarSet("")
        self.mainset.append([0 for i in range(len(spec.bins))])
        self.mainset.setColor(
            QColor(spec.color[0], spec.color[1], spec.color[2])
        )
        self.series = QBarSeries()
        self.series.append(self.mainset)

        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.axis_x = QBarCategoryAxis()
        self.axis_y = QValueAxis()
        self.axis_x.append(map(str, spec.bins))
        self.chart.addSeries(self.series)
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

        self._updates_per_second = 10
        self._dataset = []

    def clear(self):
        self._dataset = []

    def update_data(self, dataset):
        data = []
        for d in dataset:
            data.append(d)
        self._dataset = data

    def redraw(self):
        if len(self._dataset) > 0:
            for i in range(len(self._dataset)):
                self.mainset.replace(i, self._dataset[i])
            self.axis_y.setRange(0, max(self._dataset))


class QtAgentGraph(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.setTitle(str(self.spec.variable))
        self.chart.legend().hide()

        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.chart.createDefaultAxes()
        self.autoscale_y_axis = True
        if self.spec.min_y and self.spec.max_y:
            self.autoscale_y_axis = False
            self.chart.axes()[1].setRange(self.spec.min_y, self.spec.max_y)

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self._updates_per_second = 60
        self._data = []
        self._min = 0
        self._max = 0

    def clear(self):
        for chart in self.chart.series():
            chart.clear()
        self._data = []

    def update_data(self, dataset):
        for ag in dataset:
            agent_id = ag[0]
            agent_data = ag[1]
            agent_color = ag[2]
            if agent_id not in self.spec.agents.keys():
                self.spec.agents[agent_id] = (QLineSeries(), [agent_data])
                self.spec.agents[agent_id][0].setColor(
                    QColor(agent_color[0], agent_color[1], agent_color[2])
                )
                self.chart.addSeries(self.spec.agents[agent_id][0])
                self.spec.agents[agent_id][0].attachAxis(self.chart.axisX())
                self.spec.agents[agent_id][0].attachAxis(self.chart.axisY())
            else:
                self.spec.agents[agent_id][0].setColor(
                    QColor(agent_color[0], agent_color[1], agent_color[2])
                )
                self.spec.agents[agent_id][1].append(agent_data)

    def redraw(self):
        for ag in self.spec.agents.keys():
            ag_tuple = self.spec.agents[ag]
            ag_series = ag_tuple[0]
            ag_data = ag_tuple[1]
            if len(ag_data) > 0:
                datapoint = sum(ag_data) / len(ag_data)
                ag_series.append(
                    QPointF(
                        ag_series.count() / self._updates_per_second,
                        datapoint,
                    )
                )
                self._min = min(self._min, datapoint)
                self._max = max(self._max, datapoint)
            ag_data = []
        if len(self.spec.agents) > 0:
            first_agent_tuple = list(self.spec.agents.values())[0]
            if len(first_agent_tuple[1]):
                first_series = first_agent_tuple[0]
                self.chart.axes()[0].setRange(
                    0, (first_series.count() - 1) / self._updates_per_second
                )
                diff = self._max - self._min
                if self.autoscale_y_axis:
                    if diff > 0:
                        self.chart.axes()[1].setRange(self._min, self._max)
                    else:
                        self.chart.axes()[1].setRange(
                            self._min - 0.5, self._max + 0.5
                        )


class ToggleButton(QtWidgets.QPushButton):
    def __init__(self, text, button_id):
        super().__init__(text)
        self.button_id = button_id
        self.setCheckable(True)


# Based on https://stackoverflow.com/a/50300848/
class Slider(QtWidgets.QHBoxLayout):
    def __init__(self, variable, minval, maxval, initial):
        super().__init__()
        label = QtWidgets.QLabel()
        label.setText(variable)
        self.addWidget(label)
        self.sliderBar = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sliderBar.factor = 1000
        self.sliderBar.setMinimum(minval * self.sliderBar.factor)
        self.sliderBar.setMaximum(maxval * self.sliderBar.factor)
        self.sliderBar.setValue(initial * self.sliderBar.factor)
        self.sliderBar.setMinimumWidth(150)
        self.addWidget(self.sliderBar)
        self.indicator = QtWidgets.QLabel()
        self.indicator.setText(str(initial))
        self.addWidget(self.indicator)


class Monitor(QtWidgets.QLabel):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable
        self.setText(variable + ": -")
        self.data = None

    def update_label(self, data):
        self.data = data
        self.setText(self.variable + ": " + str(self.data))


class Checkbox(QtWidgets.QCheckBox):
    def __init__(self, variable):
        super().__init__(variable)
        self.setText(variable)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def closeEvent(self, event):
        Model._input_queue.put(["close"])
        super().closeEvent(event)


class Application:
    def __init__(self, model):
        self.model = model
        self.plots = {}
        self.logic_timer = QtCore.QTimer()
        self.logic_timer.timeout.connect(self.update_logic)
        self.graphics_timer = QtCore.QTimer()
        self.graphics_timer.timeout.connect(self.update_graphics)
        self.panel_timer = QtCore.QTimer()
        self.panel_timer.timeout.connect(self.add_elements)
        self.initializeUI()

    def initializeUI(self):
        # Initialize main window and central widget
        self.mainwindow = MainWindow(self.model)
        self.mainwindow.setWindowTitle("")
        self.centralwidget = QtWidgets.QWidget(self.mainwindow)
        self.mainwindow.setCentralWidget(self.centralwidget)

        # Add horizontal divider
        self.horizontal_divider = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.horizontal_divider)

        # Box for left side (simulation area + controllers)
        self.left_box = QtWidgets.QVBoxLayout()
        self.horizontal_divider.addLayout(self.left_box)
        self.controllers = []

        # Box for right side (plots)
        self.right_box = QtWidgets.QVBoxLayout()
        self.plots_box = QtWidgets.QVBoxLayout()
        self.horizontal_divider.addLayout(self.right_box)
        self.right_box.addLayout(self.plots_box)
        # self.right_box.addStretch(1)

        # Simulation area
        self.simulation_area = SimulationArea()
        self.simulation_area.model = self.model
        self.left_box.addWidget(self.simulation_area)

        # Controller box (bottom left)
        self.row_empty = True
        self.controller_box = QtWidgets.QVBoxLayout()
        self.left_box.addLayout(self.controller_box)
        self.left_box.addStretch(1)

        self.mainwindow.show()

        # For some reason best to add matplotlib plots after the
        # MainWindow is shown, otherwise the plot size isn't adjusted
        # to the window size
        #self.add_plots(self.model.plot_specs, self.plots_box)

        # Start timers
        self.logic_timer.start(1000 / 30)
        self.graphics_timer.start(1000 / 30)
        self.panel_timer.start(1000 / 10)

    def update_logic(self):
        #if not self.model.is_paused():
        for controller in self.controllers:
            if (
                isinstance(controller, ToggleButton)
                and controller.isChecked()
            ):
                Model._input_queue.put(["toggle_button",
                                        controller.button_id])
            elif isinstance(controller, Monitor):
                controller.update_label()

    def update_graphics(self):
        if self.simulation_area.enable_rendering:
            self.simulation_area.update()
        while not Model._data_queue.empty():
            msg = Model._data_queue.get()
            plot_id = msg[0]
            dataset = msg[1]
            if plot_id in self.plots.keys():
                plot = self.plots[plot_id]
                if type(plot) is QtGraph:
                    plot.add_data(dataset)
                elif type(plot) is QtBarChart:
                    plot.update_data(dataset)
                elif type(plot) is QtHistogram:
                    plot.update_data(dataset)
                elif type(plot) is QtAgentGraph:
                    plot.update_data(dataset)
                elif type(plot) is Monitor:
                    plot.update_data(dataset)
        for plot in self.plots.values():
            if type(plot) is not Monitor:
                plot.redraw()

    def add_button(self, button_id, label, row):
        btn = QtWidgets.QPushButton(label)
        btn.clicked.connect(lambda x: Model._input_queue.put(["single_button",
                                                              button_id]))
        row.addWidget(btn)
        self.controllers.append(btn)

    def add_toggle(self, button_id, label, row):
        btn = ToggleButton(label, button_id)
        row.addWidget(btn)
        self.controllers.append(btn)

    def add_slider(self, slider_id, variable, initial, minval, maxval, row):
        slider = Slider(
            variable,
            minval,
            maxval,
            initial,
        )

        def update_variable(v):
            value = v / slider.sliderBar.factor
            Model._input_queue.put(["slider_change",
                                    slider_id,variable,v/1000])
            slider.indicator.setText(str(value))

        slider.sliderBar.valueChanged.connect(update_variable)
        row.addLayout(slider)
        self.controllers.append(slider)

    def add_checkbox(self, checkbox_id, variable, row):
        checkbox = Checkbox(variable)

        def update_variable(v):
            Model._input_queue.put(["checkbox_check",
                                    checkbox_id, checkbox.isChecked()])

        checkbox.stateChanged.connect(update_variable)
        row.addWidget(checkbox)
        self.controllers.append(checkbox)

    def add_monitor(self, monitor_id, variable, row):
        monitor = Monitor(variable)
        row.addWidget(monitor)
        self.plots[monitor_id] = monitor

    def add_line_chart(self, graph_id, variables, colors, min_y, max_y):
        chart = QtGraph(LineChartSpec(variables, colors, min_y, max_y))
        self.plots[graph_id] = chart
        self.plots_box.addWidget(chart)

    def add_bar_chart(self, graph_id, variables, color):
        chart = QtBarChart(BarChartSpec(variables, color))
        self.plots[graph_id] = chart
        self.plots_box.addWidget(chart)

    def add_histogram(self, graph_id, variable, minimum, maximum, bins, color):
        histogram = QtHistogram(HistogramSpec(variable, minimum, maximum, bins, color))
        self.plots[graph_id] = chart
        self.plots_box.addWidget(histogram)

    def add_agent_graph(self, graph_id, variable, min_y, max_y):
        chart = QtAgentGraph(AgentGraphSpec({}, variable, min_y, max_y))
        self.plots[graph_id] = chart
        self.plots_box.addWidget(chart)

    def add_elements(self):
        rowbox = QtWidgets.QHBoxLayout()
        self.controller_box.addLayout(rowbox)
        while not Model._ui_queue.empty():
            msg = Model._ui_queue.get()
            command = msg[0]
            if command == "add_row" and not self.row_empty:
                self.row_empty = True
                rowbox = QtWidgets.QHBoxLayout()
                self.controller_box.addLayout(rowbox)
                continue
            elif command == "clear_all":
                for plot in self.plots.values():
                    plot.clear()
            elif command == "add_button":
                self.add_button(msg[1], msg[2], rowbox)
            elif command == "add_toggle":
                self.add_toggle(msg[1], msg[2], rowbox)
            elif command == "add_slider":
                self.add_slider(msg[1], msg[2], msg[3], msg[4], msg[5], rowbox)
            elif command == "add_checkbox":
                self.add_checkbox(msg[1], msg[2], rowbox)
            elif command == "add_monitor":
                self.add_monitor(msg[1], msg[2], rowbox)
            elif command == "add_line_chart":
                self.add_line_chart(msg[1], msg[2], msg[3], msg[4], msg[5])
            elif command == "add_bar_chart":
                self.add_bar_chart(msg[1], msg[2], msg[3])
            elif command == "add_histogram":
                self.add_histogram(msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
            elif command == "add_agent_graph":
                self.add_agent_graph(msg[1], msg[2], msg[3], msg[4])
            elif command == "add_ellipse"
            elif command == "new_model":
                self.simulation_area.setFixedSize(msg[1],msg[2])
                self.simulation_area.model_width = msg[1]
                self.simulation_area.model_height = msg[2]
                self.simulation_area.model_tile_size = msg[3]
                self.simulation_area.reset()
                continue
            elif command == "reset_model":
                self.simulation_area.reset()
                continue
            self.row_empty = False
            rowbox.addStretch(1)

    def add_plots(self, plot_specs, plots_box):
        for plot_spec in plot_specs:
            if type(plot_spec) is LineChartSpec:
                self.add_line_chart(plot_spec, plots_box)
            elif type(plot_spec) is BarChartSpec:
                self.add_bar_chart(plot_spec, plots_box)
            elif type(plot_spec) is HistogramSpec:
                self.add_histogram(plot_spec, plots_box)
            elif type(plot_spec) is AgentGraphSpec:
                self.add_agent_graph(plot_spec, plots_box)

pid = os.getpid()

def run(model):
    global pid
    if pid == os.getpid():
        if model:
            set_active_model(model)
            Model._ui_queue.put(["new_model",
                                 model.width,
                                 model.height,
                                 model.tile_size])
        return
    # Initialize application
    qapp = QtWidgets.QApplication(sys.argv)

    # We need to store a reference to the application, even though we are not
    # using it, as otherwise it will be garbage-collected and the UI will get
    # some very weird behavior.
    app = Application(model)  # noqa: F841

    # Launch the application
    qapp.exec_()

    # Application was closed, clean up and exit
    sys.exit(0)


def quick_run():
    run(None)

process = Process(target=quick_run)
process.start()
