import psutil


class SystemStats:
    cpu_percent = None
    ram_percent = None
    ram_used = None
    ram_total = None
    ram_free = None
    disk_percent = None
    disk_used = None
    disk_total = None
    disk_free = None

    def __init__(self):
        self.cpu_percent = psutil.cpu_percent()
        self.ram_percent = psutil.virtual_memory().percent
        self.ram_total = psutil.virtual_memory().total
        self.ram_free = psutil.virtual_memory().available
        self.ram_used = self.ram_total - self.ram_free
        self.disk_total = psutil.disk_usage('/').total
        self.disk_free = psutil.disk_usage('/').free
        self.disk_used = self.disk_total - self.disk_free
        self.disk_percent = round(self.disk_used / self.disk_total * 100, 1)
