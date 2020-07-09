import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import QPointF, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen

from agents.model import ButtonSpec, ToggleSpec, SliderSpec, GraphSpec, HistogramSpec

class SimulationArea(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__model = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/60)

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
        white = QtGui.QColor('white')
        painter.setBrush(white)
        painter.drawRect(0, 0, painter.device().width(), painter.device().height())

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
                path.addEllipse(select.x-select.size*1.5,
                                select.y-select.size*1.5,
                                select.size*3,
                                select.size*3)
                painter.setBrush(QColor(0, 0, 0, 150))
                painter.drawPath(path)

    def paintAgent(self, painter, agent):
        r, g, b = agent.color
        painter.setBrush(QtGui.QColor(r, g, b))
        painter.drawEllipse(agent.x-agent.size/2, agent.y-agent.size/2, agent.size, agent.size)

    def paintTile(self, painter, tile):
        r, g, b = tile.color
        color = QtGui.QColor(r, g, b)
        painter.setBrush(color)
        x = self.model.tile_size * tile.x
        y = self.model.tile_size * tile.y
        painter.drawRect(x, y, self.model.tile_size, self.model.tile_size)

    def mousePressEvent(self,e):
        self.model.mouse_click(e.localPos().x(),e.localPos().y())

class QtGraph(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.series = QLineSeries()
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
        self.timer.start(1000/5)
        self._data = []

    def clear(self):
        self.series.clear()
        self._data = []

    def add_data(self,data):
        self._data.append(data)

    def redraw(self):
        if len(self._data) > 0:
            self.series.clear()
            for i in range(len(self._data)):
                self.series.append(QPointF(i, self._data[i]))
            self.axis_x.setRange(0,self.series.count())
            self.axis_y.setRange(min(self._data), max(self._data))

class QtHistogram(QChartView):
    def __init__(self, spec):
        super().__init__(None)
        self.spec = spec
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.mainset = QBarSet('MainSet')
        self.mainset.append([0 for i in range(len(spec.variables))])
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
        self.timer.start(1000/10)
        self._dataset = []

    def clear(self):
        self._dataset = []

    def update_data(self,dataset):
        data = []
        for d in dataset:
            data.append(d)
        self._dataset = data

    def redraw(self):
        if len(self._dataset) > 0:
            for i in range(len(self._dataset)):
                self.mainset.replace(i,self._dataset[i])
            self.axis_y.setRange(0, max(self._dataset))

class ToggleButton(QtWidgets.QPushButton):
    def __init__(self, text, func, model):
        super().__init__(text)
        self.toggled.connect(self.on_toggle)
        self.setCheckable(True)
        self.model = model
        self.func = func
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.func(model))

    def on_toggle(self, checked):
        if checked:
            self.timer.start(1000/60)
        else:
            self.timer.stop()

 # Based on https://stackoverflow.com/a/50300848/
class Slider(QtWidgets.QSlider):

    def __init__(self, variable, minval, maxval, initial):
        super().__init__(QtCore.Qt.Horizontal)
        self.factor = 1000
        self.setMinimum(minval * self.factor)
        self.setMaximum(maxval * self.factor)
        self.setValue(initial * self.factor)
        self.setMinimumWidth(150)

class Application():
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
        #self.right_box.addStretch(1)

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
        slider = Slider(slider_spec.variable, slider_spec.minval, slider_spec.maxval, slider_spec.initial)
        def update_variable(v):
            self.model[slider_spec.variable] = v/slider.factor
        slider.valueChanged.connect(update_variable)
        row.addWidget(slider)

    def add_graph(self, graph_spec, plots_box):
        # TODO Record data and display
        graph = QtGraph(graph_spec)
        plots_box.addWidget(graph)
        self.model.plots.add(graph)

    def add_histogram(self, histogram_spec, plots_box):
        histogram = QtHistogram(histogram_spec)
        plots_box.addWidget(histogram)
        self.model.plots.add(histogram)

    def add_controllers(self, rows, controller_box):
        for row in rows:
            # Create a horizontal box layout for this row
            rowbox = QtWidgets.QHBoxLayout()
            controller_box.addLayout(rowbox)
            toggle_render_btn = QtWidgets.QPushButton("Disable rendering")
            def toggle(checked):
                if checked:
                    self.simulation_area.timer.stop()
                else:
                    self.simulation_area.timer.start(1000/60)
            toggle_render_btn.toggled.connect(toggle)
            toggle_render_btn.setCheckable(True)
            rowbox.addWidget(toggle_render_btn)

            # Add controllers
            for controller in row:
                if isinstance(controller, ButtonSpec):
                    self.add_button(controller, rowbox)
                elif isinstance(controller, ToggleSpec):
                    self.add_toggle(controller, rowbox)
                elif isinstance(controller, SliderSpec):
                    self.add_slider(controller, rowbox)
            rowbox.addStretch(1)

    def add_plots(self, plot_specs, plots_box):
        for plot_spec in plot_specs:
            if type(plot_spec) is GraphSpec:
                self.add_graph(plot_spec, plots_box)
            elif type(plot_spec) is HistogramSpec:
                self.add_histogram(plot_spec, plots_box)

def run(model):
    # Initialize application
    qapp = QtWidgets.QApplication(sys.argv)
    myapp = Application(model)

    # Launch the application
    qapp.exec_()

    # Application was closed, clean up and exit
    sys.exit(0)
