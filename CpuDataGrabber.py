import traceback

from qtpy.QtCore import QObject, Signal
import psutil


class CpuPercentGrabber(QObject):
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
            self.value_total = 0.0
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

class CpuTimesGrabber(QObject):
    finished = Signal()

    results = Signal(dict)  # set the type of object you are sending

    def __init__(self):
        super().__init__()
        self.cpu_count = psutil.cpu_count()
        self.value_x_cpu = {}
        self.value_total = {}
        self.frequency = 1000
        self.count = 0

    @staticmethod
    def calculate_times_x_cpu(cpu_interval):
        return psutil.cpu_times_percent(interval=cpu_interval, percpu=True)

    def run(self):        
        while True:
            self.value_total["user"]  = 0.0
            self.value_total["system"]  = 0.0
            self.value_total["idle"]  = 0.0
            self.value_total["interrupt"]  = 0.0
            self.value_total["dpc"]  = 0.0
            try:
                self.value_x_cpu = self.calculate_times_x_cpu(self.frequency / 1000)
                for i in range(self.cpu_count):
                    self.value_total["user"]  += self.value_x_cpu[i].user
                    self.value_total["system"]  += self.value_x_cpu[i].system
                    self.value_total["idle"]  += self.value_x_cpu[i].idle
                    self.value_total["interrupt"]  += self.value_x_cpu[i].interrupt
                    self.value_total["dpc"]  += self.value_x_cpu[i].dpc
                self.value_total["user"]  /= self.cpu_count
                self.value_total["system"]  /= self.cpu_count
                self.value_total["idle"] /= self.cpu_count
                self.value_total["interrupt"]  /= self.cpu_count
                self.value_total["dpc"]  /= self.cpu_count
                self.send_results()  # when done, send the results
            except:
                traceback.print_exc()

        self.finished.emit()

    def send_results(self):
        results = {'value_total': self.value_total, 'value_x_cpu': self.value_x_cpu, 'cpu_count': self.cpu_count}
        self.results.emit(results)

