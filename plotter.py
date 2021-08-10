from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from multiprocessing import Queue


class MainWindow2(QtWidgets.QMainWindow):
    def __init__(self, communication_queue=None, *args, **kwargs):
        super(MainWindow2, self).__init__(*args, **kwargs)

        self.window = pg.GraphicsWindow()
        self.window.show()

        # To do: Set num channels automatically based on length of data intake
        self.num_channels = 8
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = 100

        self._init_timeseries()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(lambda: self.update_plot_data(communication_queue))
        self.timer.start()


    def _init_timeseries(self):
        self.plots = list()
        self.parameters = list()
        self.times = list()
        self.times.append(0)
        for i in range(self.num_channels):
            # To do: create better layout
            p = self.window.addPlot(row=i, col=0)
            p.showAxis('left', True)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', True)
            p.setMenuEnabled('bottom', False)
            # To do: Create list of titles
            if i == 0:
                p.setTitle('Torque Plot')
            self.plots.append(p)
            self.parameters.append([1])

    def update_plot_data(self, comm_queue):
        data = []

        while not comm_queue.empty():
            val = comm_queue.get_nowait()

            if val == "EXIT":
                sys.exit(QtWidgets.QApplication(sys.argv).exec_())

            data = val
        
        if not data:
            return

        # First value will be time, next 8 will be datapoints 
        current_time = data[0]
        data_sensors = data[1:]

        self.times = self.times[-self.num_points:]
        self.times.append(current_time)

        for count, datum in enumerate(data_sensors):
            self.parameters[count] = self.parameters[count][-self.num_points:]
            self.parameters[count].append(datum)
            self.plots[count].plot(self.times, self.parameters[count])
            self.plots[count].setXRange(self.times[0], self.times[-1])
        
def animation_control(comm_queue):
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow2(comm_queue)
    w.show()
    sys.exit(app.exec_())
