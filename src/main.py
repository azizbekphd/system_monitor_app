import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QSpinBox
)
from PyQt6.QtCore import QTimer

from core.database_manager import DatabaseManager
from core.system_stats import SystemStats
from utils.string_formatter import StringFormatter


class SystemMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.initUI()
        self.timer.timeout.connect(self.update_stats)

        self.recording = False
        self.start_time = None
        self.db_manager = DatabaseManager(Path.home() / 'Desktop' / 'system_stats.db')

    def initUI(self):
        self.setWindowTitle('System Monitor')

        # Widgets
        self.cpu_label = QLabel('CPU Usage:')
        self.ram_label = QLabel('RAM Usage:')
        self.disk_label = QLabel('Disk Usage:')

        self.interval_label = QLabel('Update Interval (seconds):')
        self.interval_spinner = QSpinBox()
        self.interval_spinner.setMinimum(1)
        self.interval_spinner.setValue(1)
        self.interval_spinner.valueChanged.connect(self.set_interval)

        self.start_button = QPushButton('Start Recording')
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton('Stop Recording')
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setVisible(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_spinner)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Start the monitoring timer
        self.timer.start(1000)

    def set_interval(self):
        interval = self.interval_spinner.value()
        self.timer.setInterval(interval * 1000)

    def update_stats(self):
        stats = SystemStats()
        formatted_stats = StringFormatter.format_stats(stats)

        self.cpu_label.setText(f"CPU Usage: {formatted_stats['cpu']}")
        self.ram_label.setText(f"RAM Usage: {formatted_stats['ram']}")
        self.disk_label.setText(f"Disk Usage: {formatted_stats['disk']}")

        if self.recording:
            elapsed_time = time.time() - self.start_time
            self.stop_button.setText(f'Stop Recording ({StringFormatter.format_time(int(elapsed_time))})')
            self.db_manager.insert_record(stats)

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)

    def stop_recording(self):
        self.recording = False
        self.start_time = None
        self.stop_button.setVisible(False)
        self.start_button.setVisible(True)
        self.stop_button.setText('Stop Recording')

    def closeEvent(self, event):
        self.db_manager.close()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SystemMonitorApp()
    mainWin.show()
    sys.exit(app.exec())
