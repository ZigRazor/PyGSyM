import traceback

from qtpy.QtCore import QObject, Signal
import psutil


class CpuDataGrabber(QObject):
    finished = Signal()

    results = Signal(dict)  # set the type of object you are sending

    def __init__(self):
        super().__init__()
        self.cpu_count = psutil.cpu_count()
        self.value_x_cpu = 0
        self.value_total = 0.0
        self.frequency = 1000
        self.count = 0

    @staticmethod
    def calculate_usage_x_cpu(cpu_interval):
        return psutil.cpu_percent(interval=cpu_interval, percpu=True)

    def run(self):
        while True:
            try:
                self.value_x_cpu = self.calculate_usage_x_cpu(self.frequency / 1000)
                for i in range(self.cpu_count):
                    self.value_total += self.value_x_cpu[i]
                self.value_total /= self.cpu_count
                self.send_results()  # when done, send the results
            except:
                traceback.print_exc()

        self.finished.emit()

    def send_results(self):
        results = {'value_total': self.value_total, 'value_x_cpu': self.value_x_cpu, 'cpu_count': self.cpu_count}
        self.results.emit(results)
