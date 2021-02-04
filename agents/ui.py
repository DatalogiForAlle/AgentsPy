import sys
import math
import bisect
from collections import deque
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
    get_quickstart_model,
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


class SimulationArea(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__model = None

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model
        self.setFixedSize(model.width, model.height)
        self.enable_rendering = True

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Default to a black background
        white = QtGui.QColor("black")
        painter.setBrush(white)
        painter.drawRect(
            0, 0, painter.device().width(), painter.device().height()
        )

        if self.model:
            # Draw tiles
            for tile in self.model.tiles:
                self.paintTile(painter, tile)

            # Draw shapes
            for shape in self.model.get_shapes():
                c = shape.color
                painter.setBrush(QtGui.QColor(c[0], c[1], c[2]))
                if type(shape) is EllipseStruct:
                    painter.drawEllipse(shape.x, shape.y, shape.w, shape.h)
                elif type(shape) is RectStruct:
                    painter.drawRect(shape.x, shape.y, shape.w, shape.h)

            # Draw lines
            for agent in self.model.agents:
                painter.setPen(
                    QColor(agent.color[0], agent.color[1], agent.color[2])
                )
                # Pretty terrible code here
                # Replaces line-tuples in agent.__paths with QLineF's
                for path in agent.get_paths():
                    for i in range(len(path)):
                        if type(path[i]) is tuple:
                            path[i] = QLineF(
                                path[i][0][0],
                                path[i][0][1],
                                path[i][1][0],
                                path[i][1][1],
                            )
                    painter.drawLines(path)

            # Draw agents
            select = None
            for agent in self.model.agents:
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
        painter.end()

    def paintAgent(self, painter, agent):
        r, g, b = agent.color
        painter.setBrush(QColor(r, g, b))
        painter.setPen(QColor(r, g, b))
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
        x = self.model.tile_size * tile.x
        y = self.model.tile_size * tile.y
        painter.drawRect(x, y, self.model.tile_size, self.model.tile_size)

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
        self.mainset.append([0] * len(spec.bins))
        self.mainset.setColor(
            QColor(spec.color[0], spec.color[1], spec.color[2])
        )
        self.series = QBarSeries()
        self.series.append(self.mainset)

        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.y_ranges = [0, 1, 5, 10, 25, 50, 100, 250, 500, 1000]
        self.max_y = 1000
        self.max_y_range = 1000
        self.lookback = 30
        self.recent_max_y = deque([self.max_y_range] * self.lookback)

        font = QtGui.QFont()
        font.setPixelSize(10)

        self.axis_x = QBarCategoryAxis()
        self.axis_x.setLabelsAngle(-90)
        self.axis_x.setLabelsFont(font)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, self.max_y)
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

            # Calculate max of current values
            max_y_range = max(self._dataset)

            # Store max value
            self.recent_max_y.appendleft(max_y_range)
            if len(self.recent_max_y) > self.lookback:
                self.recent_max_y.pop()

            # Set max based on the last 30 max values,
            # to avoid flickering
            self.max_y_range = max(self.recent_max_y)

            y_range = bisect.bisect_left(self.y_ranges, self.max_y_range)
            if y_range < len(self.y_ranges):
                self.max_y = self.y_ranges[y_range]
            elif max_y_range > self.max_y:
                self.max_y += self.max_y
            elif max_y_range < self.max_y / 2:
                self.max_y = self.max_y / 2

            self.axis_y.setRange(0, self.max_y)


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

    def update_data(self):
        for a in self.spec.agents:
            if not hasattr(a, "_agent_series"):
                a._agent_series = QLineSeries()
                a._agent_series.setColor(
                    QColor(a.color[0], a.color[1], a.color[2])
                )
                a._agent_series_data = [getattr(a, self.spec.variable)]
                self.chart.addSeries(a._agent_series)
                a._agent_series.attachAxis(self.chart.axisX())
                a._agent_series.attachAxis(self.chart.axisY())
            else:
                a._agent_series_data.append(getattr(a, self.spec.variable))

    def redraw(self):
        for a in self.spec.agents:
            if hasattr(a, "_agent_series") and len(a._agent_series_data) > 0:
                datapoint = sum(a._agent_series_data) / len(
                    a._agent_series_data
                )
                a._agent_series.append(
                    QPointF(
                        a._agent_series.count() / self._updates_per_second,
                        datapoint,
                    )
                )
                self._min = min(self._min, datapoint)
                self._max = max(self._max, datapoint)
                a._agent_series.setColor(
                    QColor(a.color[0], a.color[1], a.color[2])
                )
            a._agent_series_data = []
        if len(self.spec.agents) > 0:
            first_agent = self.spec.agents[0]
            if hasattr(first_agent, "_agent_series"):
                first_series = first_agent._agent_series
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
    def __init__(self, text, func, model):
        super().__init__(text)
        self.setCheckable(True)
        self.model = model
        self.func = func


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
    def __init__(self, variable, model):
        super().__init__()
        self.variable = variable
        self.setText(variable + ": -")
        self.model = model

    def update_label(self):
        if self.variable in self.model.variables:
            self.setText(self.variable + ": " + str(self.model[self.variable]))


class Checkbox(QtWidgets.QCheckBox):
    def __init__(self, variable):
        super().__init__(variable)
        self.setText(variable)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def closeEvent(self, event):
        self.model.close()
        super().closeEvent(event)


class Application:
    def __init__(self, model):
        self.model = model
        self.logic_timer = QtCore.QTimer()
        self.logic_timer.timeout.connect(self.update_logic)
        self.graphics_timer = QtCore.QTimer()
        self.graphics_timer.timeout.connect(self.update_graphics)
        self.initializeUI()

    def initializeUI(self):
        # Initialize main window and central widget
        self.mainwindow = MainWindow(self.model)
        self.mainwindow.setWindowTitle(self.model.title)
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
        self.controller_box = QtWidgets.QVBoxLayout()
        self.left_box.addLayout(self.controller_box)
        self.left_box.addStretch(1)

        self.add_controllers(self.model.controller_rows, self.controller_box)
        self.mainwindow.show()

        # For some reason best to add matplotlib plots after the
        # MainWindow is shown, otherwise the plot size isn't adjusted
        # to the window size
        self.add_plots(self.model.plot_specs, self.plots_box)

        # Start timers
        self.logic_timer.start(1000 / 60)
        self.graphics_timer.start(1000 / 30)

    def update_logic(self):
        if not self.model.is_paused():
            for controller in self.controllers:
                if (
                    isinstance(controller, ToggleButton)
                    and controller.isChecked()
                ):
                    controller.func(controller.model)
                elif isinstance(controller, Monitor):
                    controller.update_label()

    def update_graphics(self):
        if self.simulation_area.enable_rendering:
            self.simulation_area.update()
        for p in self.model.plots:
            p.redraw()

    def add_button(self, button_spec, row):
        btn = QtWidgets.QPushButton(button_spec.label)
        btn.clicked.connect(lambda x: button_spec.function(self.model))
        row.addWidget(btn)
        self.controllers.append(btn)

    def add_toggle(self, toggle_spec, row):
        btn = ToggleButton(toggle_spec.label, toggle_spec.function, self.model)
        row.addWidget(btn)
        self.controllers.append(btn)

    def add_slider(self, slider_spec, row):
        slider = Slider(
            slider_spec.variable,
            slider_spec.minval,
            slider_spec.maxval,
            slider_spec.initial,
        )

        def update_variable(v):
            value = v / slider.sliderBar.factor
            setattr(self.model, slider_spec.variable, value)
            slider.indicator.setText(str(value))

        slider.sliderBar.valueChanged.connect(update_variable)
        row.addLayout(slider)
        self.controllers.append(slider)

    def add_checkbox(self, checkbox_spec, row):
        checkbox = Checkbox(checkbox_spec.variable)

        def update_variable(v):
            setattr(self.model, checkbox_spec.variable, checkbox.isChecked())

        checkbox.stateChanged.connect(update_variable)
        row.addWidget(checkbox)
        self.controllers.append(checkbox)

    def add_monitor(self, monitor_spec, plots_box):
        monitor = Monitor(monitor_spec.variable, self.model)
        plots_box.addWidget(monitor)
        self.controllers.append(monitor)

    def add_line_chart(self, line_chart_spec, plots_box):
        chart = QtGraph(line_chart_spec)
        plots_box.addWidget(chart)
        self.model.plots.add(chart)

    def add_bar_chart(self, bar_chart_spec, plots_box):
        chart = QtBarChart(bar_chart_spec)
        plots_box.addWidget(chart)
        self.model.plots.add(chart)

    def add_histogram(self, histogram_spec, plots_box):
        histogram = QtHistogram(histogram_spec)
        plots_box.addWidget(histogram)
        self.model.plots.add(histogram)

    def add_agent_graph(self, agent_graph_spec, plots_box):
        chart = QtAgentGraph(agent_graph_spec)
        plots_box.addWidget(chart)
        self.model.plots.add(chart)

    def add_controllers(self, rows, controller_box):
        first_row = True
        for row in rows:
            # Create a horizontal box layout for this row
            rowbox = QtWidgets.QHBoxLayout()
            controller_box.addLayout(rowbox)
            if first_row:
                first_row = False

            # Add controllers
            for controller in row:
                if isinstance(controller, ButtonSpec):
                    self.add_button(controller, rowbox)
                elif isinstance(controller, ToggleSpec):
                    self.add_toggle(controller, rowbox)
                elif isinstance(controller, SliderSpec):
                    self.add_slider(controller, rowbox)
                elif isinstance(controller, CheckboxSpec):
                    self.add_checkbox(controller, rowbox)
                elif isinstance(controller, MonitorSpec):
                    self.add_monitor(controller, rowbox)
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


def run(model):
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
    run(get_quickstart_model())
