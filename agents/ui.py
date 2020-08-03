import sys
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
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPolygonF

from agents.model import (
    ButtonSpec,
    ToggleSpec,
    SliderSpec,
    CheckboxSpec,
    LineChartSpec,
    BarChartSpec,
    HistogramSpec,
    MonitorSpec,
)


class SimulationArea(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__model = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 60)

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model
        self.setFixedSize(model.width, model.height)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Default to a white background
        white = QtGui.QColor("white")
        painter.setBrush(white)
        painter.drawRect(0, 0,
                         painter.device().width(),
                         painter.device().height())

        if self.model:
            # Draw tiles
            for tile in self.model.tiles:
                self.paintTile(painter, tile)
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

    def paintAgent(self, painter, agent):
        r, g, b = agent.color
        painter.setBrush(QtGui.QColor(r, g, b))
        if self.model.show_direction:
            x = agent.x
            y = agent.y
            d = math.radians(agent.direction)
            s = agent.size
            point_list = [
                QPointF(x + math.cos(d) * s, y + math.sin(d) * s),
                QPointF(x + math.cos(d + 2.3) * s, y + math.sin(d + 2.3) * s),
                QPointF(
                    x + math.cos(d + math.pi) * s / 2,
                    y + math.sin(d + math.pi) * s / 2
                ),
                QPointF(x + math.cos(d - 2.3) * s, y + math.sin(d - 2.3) * s),
            ]
            painter.drawPolygon(QPolygonF(point_list))
        else:
            painter.drawEllipse(
                agent.x - agent.size / 2,
                agent.y - agent.size / 2,
                agent.size,
                agent.size,
            )

    def paintTile(self, painter, tile):
        r, g, b = tile.color
        color = QtGui.QColor(r, g, b)
        painter.setBrush(color)
        x = self.model.tile_size * tile.x
        y = self.model.tile_size * tile.y
        painter.drawRect(x, y, self.model.tile_size, self.model.tile_size)

    def mousePressEvent(self, e):
        self.model.mouse_click(e.localPos().x(), e.localPos().y())


class QtGraph(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.createDefaultAxes()
        self.chart.setTitle(self.spec.variable)
        self.chart.legend().hide()
        self.series = QLineSeries()
        self.series.setColor(QColor(spec.color[0],
                                    spec.color[1],
                                    spec.color[2]))
        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addSeries(self.series)
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.redraw())
        self.timer.start(1000 / 20)
        self._data = []
        self._min = 0
        self._max = 0

    def clear(self):
        self.series.clear()
        self._data = []

    def add_data(self, data):
        self._data.append(data)

    def redraw(self):
        if len(self._data) > 0:
            datapoint = sum(self._data) / len(self._data)
            self.series.append(QPointF(self.series.count() / 2, datapoint))
            self.axis_x.setRange(0, (self.series.count() - 1) / 2)
            self._min = min(self._min, datapoint)
            self._max = max(self._max, datapoint)
            diff = self._max - self._min
            if diff > 0:
                self.axis_y.setRange(self._min, self._max)
            else:
                self.axis_y.setRange(self._min-0.5, self._max+0.5)
            self._data = []


class QtBarChart(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.setTitle(str(self.spec.variables))
        self.chart.legend().hide()
        self.mainset = QBarSet("")
        self.mainset.append([0 for i in range(len(spec.variables))])
        self.mainset.setColor(QColor(spec.color[0],
                                     spec.color[1],
                                     spec.color[2]))
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

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.redraw())
        self.timer.start(1000 / 5)
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
        self.mainset.setColor(QColor(spec.color[0],
                                     spec.color[1],
                                     spec.color[2]))
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

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.redraw())
        self.timer.start(1000 / 5)
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


class ToggleButton(QtWidgets.QPushButton):
    def __init__(self, text, func, model):
        super().__init__(text)
        self.toggled.connect(self.on_toggle)
        self.setCheckable(True)
        self.model = model
        self.func = func
        self.timer = QtCore.QTimer()

        def call_func():
            if not model.is_paused():
                self.func(model)

        self.timer.timeout.connect(call_func)

    def on_toggle(self, checked):
        if checked:
            self.timer.start(1000 / 60)
        else:
            self.timer.stop()


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
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.update_label())
        self.timer.start(1000 / 60)

    def update_label(self):
        if self.variable in self.model.variables:
            self.setText(self.variable + ": " + str(self.model[self.variable]))


class Checkbox(QtWidgets.QCheckBox):
    def __init__(self, variable):
        super().__init__(variable)
        self.setText(variable)


class Application:
    def __init__(self, model):
        # self.controller_rows = []
        # self.plots = []
        self.model = model
        self.initializeUI()

    def initializeUI(self):
        # Initialize main window and central widget
        self.mainwindow = QtWidgets.QMainWindow()
        self.mainwindow.setWindowTitle(self.model.title)
        self.centralwidget = QtWidgets.QWidget(self.mainwindow)
        self.mainwindow.setCentralWidget(self.centralwidget)

        # Add horizontal divider
        self.horizontal_divider = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.horizontal_divider)

        # Box for left side (simulation area + controllers)
        self.left_box = QtWidgets.QVBoxLayout()
        self.horizontal_divider.addLayout(self.left_box)

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

    def add_button(self, button_spec, row):
        btn = QtWidgets.QPushButton(button_spec.label)
        btn.clicked.connect(lambda x: button_spec.function(self.model))
        row.addWidget(btn)

    def add_toggle(self, toggle_spec, row):
        btn = ToggleButton(toggle_spec.label, toggle_spec.function, self.model)
        row.addWidget(btn)

    def add_slider(self, slider_spec, row):
        slider = Slider(
            slider_spec.variable,
            slider_spec.minval,
            slider_spec.maxval,
            slider_spec.initial,
        )

        def update_variable(v):
            value = v / slider.sliderBar.factor
            self.model[slider_spec.variable] = value
            slider.indicator.setText(str(value))

        slider.sliderBar.valueChanged.connect(update_variable)
        row.addLayout(slider)

    def add_checkbox(self, checkbox_spec, row):
        checkbox = Checkbox(checkbox_spec.variable)

        def update_variable(v):
            self.model[checkbox_spec.variable] = checkbox.isChecked()

        checkbox.stateChanged.connect(update_variable)
        row.addWidget(checkbox)

    def add_line_chart(self, line_chart_spec, plots_box):
        # TODO Record data and display
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

    def add_monitor(self, monitor_spec, plots_box):
        monitor = Monitor(monitor_spec.variable, self.model)
        plots_box.addWidget(monitor)

    def add_render_toggle(self, rowbox):
        toggle_render_btn = QtWidgets.QPushButton("Disable rendering")

        def toggle(checked):
            if checked:
                self.simulation_area.timer.stop()
            else:
                self.simulation_area.timer.start(1000 / 60)

        toggle_render_btn.toggled.connect(toggle)
        toggle_render_btn.setCheckable(True)
        rowbox.addWidget(toggle_render_btn)

    def add_controllers(self, rows, controller_box):
        first_row = True
        for row in rows:
            # Create a horizontal box layout for this row
            rowbox = QtWidgets.QHBoxLayout()
            controller_box.addLayout(rowbox)
            if first_row:
                self.add_render_toggle(rowbox)
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


def run(model):
    # Initialize application
    qapp = QtWidgets.QApplication(sys.argv)
    Application(model)

    # Launch the application
    qapp.exec_()

    # Application was closed, clean up and exit
    sys.exit(0)
