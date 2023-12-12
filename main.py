import sys
from functions.get_data import dataThread
from ui.sys_info_python import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread

class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.datathread = dataThread()
        self.datathread.dataChanged.connect(self.set)
        self.datathread.start()

    def set(self, system, node, release, cpu_info, total_memory, available_memory, used_memory_percent, cpu_percent,
            cpu_count, cpu_temperature, battery_percent, gpu_name, gpu_driver, gpu_memory_total, gpu_memory_free,
            gpu_memory_used, gpu_utilization):
        self.ui.lbl_dev_name.setText(node)
        self.ui.lbl_sys_name.setText(system)
        self.ui.lbl_sys_ver.setText(release)
        self.ui.lbl_cpu_family.setText(cpu_info)
        self.ui.lbl_total_ram.setText(total_memory)
        self.ui.lbl_av_ram.setText(available_memory)
        self.ui.lbl_ram_usage.setText(used_memory_percent)
        self.ui.lbl_cpu_usage.setText(cpu_percent)
        self.ui.lbl_cpu_count.setText(cpu_count)
        self.ui.lbl_cpu_temp.setText(cpu_temperature)
        self.ui.lbl_battery_per.setText(battery_percent)
        self.ui.lbl_gpu_name.setText(gpu_name)
        self.ui.lbl_gpu_driver.setText(gpu_driver)
        self.ui.lbl_vram.setText(gpu_memory_total)
        self.ui.lbl_av_ram.setText(gpu_memory_free)
        self.ui.lbl_vram_usage.setText(gpu_memory_used)
        self.ui.lbl_usage_vram_per.setText(gpu_utilization)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
