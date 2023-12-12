from ui.sys_info_python import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QValidator
import time
import sys
import threading
import datetime
import PyQt5.QtWidgets
import platform
import os
import psutil
import GPUtil  # Ekran kartı bilgileri için

from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import json
from PyQt5.QtWidgets import QApplication, QWidget
class dataThread(QThread):
    dataChanged = pyqtSignal(str,str,str,str,str,str,str,str,str,str,str,str,str,str,
                             str,str,str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):

        while True:
            # Sistem bilgilerini al
            system_info = platform.uname()
            system = str(system_info.system)
            node = str(system_info.node)
            release = str(system_info.release)
            version = system_info.version
            machine = system_info.machine

            # İşlemci bilgilerini al
            cpu_info = platform.processor()

            # Bellek bilgilerini al
            ram = psutil.virtual_memory()
            total_memory = str(int((ram.total)/(1024*1024)))
            available_memory = str(int((ram.available)/(1024*1024)))
            used_memory_percent = str(ram.percent)

            # İşlemci yükünü al
            cpu_percent = str(psutil.cpu_percent(percpu=False))

            # İşlemci sayısı
            cpu_count = str(psutil.cpu_count(logical=False))
            logical_cpu_count = str(psutil.cpu_count(logical=True))

            # Batarya bilgilerini al (sadece dizüstü bilgisayarlar için geçerlidir)
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = str(battery.percent)
            else:
                battery_percent = "Bilinmiyor"

            # Ekran kartı bilgilerini al
            try:
                gpu_info = GPUtil.getGPUs()
                gpu = gpu_info[0]
                gpu_name = str(gpu.name)
                gpu_driver = str(gpu.driver)
                gpu_memory_total = str(gpu.memoryTotal)
                gpu_memory_free = str(gpu.memoryFree)
                gpu_memory_used = str(gpu.memoryUsed)
                gpu_utilization = str(gpu.load)
            except Exception as e:
                gpu_name = "Bilinmiyor"
                gpu_driver = "Bilinmiyor"
                gpu_memory_total = "Bilinmiyor"
                gpu_memory_free = "Bilinmiyor"
                gpu_memory_used = "Bilinmiyor"
                gpu_utilization = "Bilinmiyor"

            # İşlemci sıcaklığını al (Windows için)
            if os.name == 'nt':
                try:
                    import wmi
                    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
                    temperature_infos = str(w.Sensor())
                    for sensor in temperature_infos:
                        if "CPU Package" in sensor.SensorType:
                            cpu_temperature = str(sensor.Value)
                            break
                except Exception as e:
                    cpu_temperature = "Bilinmiyor"
            else:
                cpu_temperature = "Sadece Windows'ta desteklenmektedir."

            # Elde edilen bilgileri yazdır
            print(f"Sistem: {system}")
            print(f"Bilgisayar Adı: {node}")
            print(f"Sistem Sürümü: {release}")
            print(f"İşlemci: {cpu_info}")
            print(f"Toplam Bellek: {total_memory} bytes")
            print(f"Kullanılabilir Bellek: {available_memory} bytes")
            print(f"Bellek Kullanım Oranı: {used_memory_percent}%")
            print(f"İşlemci Yükü: {cpu_percent}%")
            print(f"İşlemci Sayısı: {cpu_count} (Toplam), {logical_cpu_count} (Mantıksal)")
            print(f"İşlemci Sıcaklığı: {cpu_temperature}°C")
            print(f"Batarya Yüzdesi: {battery_percent}%")
            print(f"Ekran Kartı Adı: {gpu_name}")
            print(f"Ekran Kartı Sürücüsü: {gpu_driver}")
            print(f"Toplam GPU Belleği: {gpu_memory_total} MB")
            print(f"Kullanılabilir GPU Belleği: {gpu_memory_free} MB")
            print(f"Kullanılan GPU Belleği: {gpu_memory_used} MB")
            print(f"GPU Kullanım Oranı: {gpu_utilization}%")

            self.dataChanged.emit(system,node,release,cpu_info,total_memory,available_memory,used_memory_percent,
                                  cpu_percent,cpu_count,cpu_temperature,battery_percent,gpu_name,
                                  gpu_driver,gpu_memory_total,gpu_memory_free,gpu_memory_used,gpu_utilization
            )
            time.sleep(1)