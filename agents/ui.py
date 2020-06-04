import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from agents.model import ButtonSpec, ToggleSpec, SliderSpec, PlotSpec

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
            for agent in self.model.agents:
                self.paintAgent(painter, agent)

    def paintAgent(self, painter, agent):
        r, g, b = agent.color
        painter.setBrush(QtGui.QColor(r, g, b))
        painter.drawEllipse(agent.x, agent.y, agent.size, agent.size)

    def paintTile(self, painter, tile):
        r, g, b = tile.color
        color = QtGui.QColor(r, g, b)
        painter.setBrush(color)
        x = self.model.tile_size * tile.x
        y = self.model.tile_size * tile.y
        painter.drawRect(x, y, self.model.tile_size, self.model.tile_size)

class Plot(FigureCanvasQTAgg):
    # TODO: Connect with data, just shows random data
    def __init__(self, parent=None):
        self.figure = Figure()
        super(Plot, self).__init__(self.figure)
        self.setParent(parent)
        self.setMinimumWidth(400)
        self.setMinimumHeight(230)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.draw()


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

class Slider(QtWidgets.QSlider):
    def __init__(self, variable, minval, maxval, initial):
        super().__init__(QtCore.Qt.Horizontal)
        self.setMinimum(minval)
        self.setMaximum(maxval)
        self.setValue(initial)
        self.setMinimumWidth(150)

    # TODO: Support floats. See https://stackoverflow.com/a/50300848/


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
        self.right_box.addStretch(1)

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
        self.add_plots(self.model.plots, self.plots_box)

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
            self.model[slider_spec.variable] = v
        slider.valueChanged.connect(update_variable)
        row.addWidget(slider)

    def add_plot(self, plot_spec, plots_box):
        # TODO Record data and display
        plot = Plot()
        plot.plot()
        plots_box.addWidget(plot)

    def add_controllers(self, rows, controller_box):
        for row in rows:
            # Create a horizontal box layout for this row
            rowbox = QtWidgets.QHBoxLayout()
            controller_box.addLayout(rowbox)

            # Add controllers
            for controller in row:
                if isinstance(controller, ButtonSpec):
                    self.add_button(controller, rowbox)
                elif isinstance(controller, ToggleSpec):
                    self.add_toggle(controller, rowbox)
                elif isinstance(controller, SliderSpec):
                    self.add_slider(controller, rowbox)
            rowbox.addStretch(1)

    def add_plots(self, plots, plots_box):
        for plot_spec in plots:
            self.add_plot(plot_spec, plots_box)

def run(model):
    # Initialize application
    qapp = QtWidgets.QApplication(sys.argv)
    myapp = Application(model)

    # Launch the application
    qapp.exec_()

    # Application was closed, clean up and exit
    sys.exit(0)
