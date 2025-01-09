import sqlite3
import time

from core.system_stats import SystemStats


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                timestamp TEXT,
                cpu_percent REAL,
                ram_used REAL,
                ram_total REAL,
                ram_free REAL,
                disk_used REAL,
                disk_total REAL,
                disk_free REAL
            )
        ''')
        self.conn.commit()

    def insert_record(self, stats: SystemStats):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO system_stats (
                timestamp,
                cpu_percent,
                ram_used,
                ram_total,
                ram_free,
                disk_used,
                disk_total,
                disk_free
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (
            time.strftime('%Y-%m-%d %H:%M:%S'),
            stats.cpu_percent,
            stats.ram_used,
            stats.ram_total,
            stats.ram_free,
            stats.disk_used,
            stats.disk_total,
            stats.disk_free
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()
