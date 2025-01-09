from core.system_stats import SystemStats


class StringFormatter:
    @staticmethod
    def format_stats(stats: SystemStats):
        return {
            'cpu': f'{stats.cpu_percent}%',
            'ram': f"""{StringFormatter.format_memory(stats.ram_used)}/{
                StringFormatter.format_memory(stats.ram_total)} ({
                stats.ram_percent}%) — {
                StringFormatter.format_memory(stats.ram_free)} free""",
            'disk': f"""{StringFormatter.format_memory(stats.disk_used)}/{
                StringFormatter.format_memory(stats.disk_total)} ({
                stats.disk_percent}%) — {
                StringFormatter.format_memory(stats.disk_free)} free"""
        }

    @staticmethod
    def format_memory(bits: int):
        if bits < 1024:
            return f'{bits} B'
        elif bits < 1024 ** 2:
            return f'{bits / 1024:.2f} KB'
        elif bits < 1024 ** 3:
            return f'{bits / 1024 ** 2:.2f} MB'
        elif bits < 1024 ** 4:
            return f'{bits / 1024 ** 3:.2f} GB'
        else:
            return f'{bits / 1024 ** 4:.2f} TB'
