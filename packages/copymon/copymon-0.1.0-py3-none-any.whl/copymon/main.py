from nuclear import CliBuilder, flag

from .copymon import action_monitor_meminfo
from .version import __version__


def main():
    CliBuilder('copymon', version=__version__, run=action_monitor_meminfo,
               help='Dirty-Writeback memory stream monitor,\nType [s], [Enter] to force sync when monitoring memory',
               ).has(
        flag('--sync', help='run sync continuously'),
    ).run()
