import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from typing import Tuple, List, Optional

import select
from dataclasses import dataclass
from nuclear.sublog import log
from nuclear.utils.regex import regex_filter_list, regex_replace_list
from nuclear.utils.shell import shell_output
from nuclear.utils.strings import nonempty_lines
from nuclear.utils.time import time2str


def get_mem_dirty_writeback() -> Tuple[int, int]:
    meminfo = nonempty_lines(shell_output('cat /proc/meminfo'))
    dirty = regex_filter_list(meminfo, r'Dirty: +([0-9]+) kB')
    dirty = regex_replace_list(dirty, r'Dirty: +([0-9]+) kB', '\\1')
    writeback = regex_filter_list(meminfo, r'Writeback: +([0-9]+) kB')
    writeback = regex_replace_list(writeback, r'Writeback: +([0-9]+) kB', '\\1')
    return int(dirty[0]), int(writeback[0])


def kill_process(proc):
    if proc is not None:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            proc.terminate()


class BackgroundExecuteThread(threading.Thread):
    def __init__(self, cmd: str):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__cmd: str = cmd
        self.__proc = None

    def run(self):
        self.__proc = subprocess.Popen(self.__cmd, stdout=None, shell=True, preexec_fn=os.setsid)
        if self.__proc is not None:
            self.__proc.wait()
            self.__proc = None

    def stop(self):
        kill_process(self.__proc)
        self.__proc = None


def run_sync_background() -> BackgroundExecuteThread:
    background_thread = BackgroundExecuteThread('nohup sync > /dev/null 2>&1 &')
    background_thread.start()
    return background_thread


@dataclass
class MemDataPoint(object):
    timestamp: float  # [s]
    dirty_kb: int  # [kB]
    writeback_kb: int  # [kB]

    @property
    def remaining_kb(self) -> int:
        return self.dirty_kb + self.writeback_kb


def kb_to_human(kbs: int) -> str:
    if kbs < 0:
        return '-' + kb_to_human(-kbs)
    if kbs < 1024:
        return f'{kbs} kB'
    mbs: float = kbs / 1024.0
    if mbs < 1024:
        return f'{mbs:.2f} MB'
    gbs = mbs / 1024.0
    return f'{gbs:.2f} GB'


def kb_to_human_just(kbs: int) -> str:
    return kb_to_human(kbs).rjust(10)


def kb_to_speed_human_just(kbps: float) -> str:
    kb_human = kb_to_human(int(kbps)) + '/s'
    if kbps > 0:
        kb_human = '+' + kb_human
    return kb_human.rjust(13)


def calc_avg_speed(mem_infos: List[MemDataPoint]) -> float:
    if len(mem_infos) < 2:
        return 0
    first = mem_infos[0]
    last = mem_infos[-1]
    remaining_delta = last.remaining_kb - first.remaining_kb
    time_delta = last.timestamp - first.timestamp
    return remaining_delta / time_delta


def calc_temporary_speed(mem_infos: List[MemDataPoint]) -> float:
    if len(mem_infos) < 2:
        return 0
    last = mem_infos[-1]
    prelast = mem_infos[-2]
    remaining_delta = last.remaining_kb - prelast.remaining_kb
    time_delta = last.timestamp - prelast.timestamp
    return remaining_delta / time_delta


def calc_eta(remaining_kb: int, speed: float) -> Optional[float]:
    if speed >= 0:
        return None
    return remaining_kb / -speed


def seconds_to_human(seconds: Optional[float]) -> str:
    if not seconds:
        return 'Infinity'
    strout: str = f'{int(seconds) % 60}s'
    minutes: int = int(seconds) // 60
    if minutes > 0:
        strout = f'{minutes}m {strout}'
    return strout


def current_time() -> str:
    return time2str(datetime.now(), '%H:%M:%S')


CHAR_BOLD = '\033[1m'
CHAR_RESET = '\033[0m'
CHAR_GREEN = '\033[32m'
CHAR_BLUE = '\033[34m'
CHAR_YELLOW = '\033[33m'
CHAR_RED = '\033[31m'


def input_or_timeout(timeout: int) -> Optional[str]:
    i, o, e = select.select([sys.stdin], [], [], timeout)
    if i:
        return sys.stdin.readline().strip()
    else:
        return None


def action_monitor_meminfo(sync: bool):
    background_thread: Optional[BackgroundExecuteThread] = None
    if sync:
        background_thread = run_sync_background()

    mem_sizes_buffer: List[MemDataPoint] = []

    try:
        while True:
            # rerun sync
            if sync and background_thread and not background_thread.is_alive():
                log.info('running sync in background...')
                background_thread.stop()
                background_thread = run_sync_background()

            timestamp: float = time.time()
            dirty_kb, writeback_kb = get_mem_dirty_writeback()
            remaining_kb: int = dirty_kb + writeback_kb

            mem_sizes_buffer.append(MemDataPoint(timestamp, dirty_kb, writeback_kb))
            # max buffer size
            if len(mem_sizes_buffer) > 10:
                mem_sizes_buffer.pop(0)

            speed_temp: float = calc_temporary_speed(mem_sizes_buffer)
            speed_avg: float = calc_avg_speed(mem_sizes_buffer)
            eta_s: float = calc_eta(remaining_kb, speed_avg)

            # output values
            print_timestamp = CHAR_BOLD + current_time() + CHAR_RESET
            print_remaining = CHAR_BOLD + kb_to_human_just(remaining_kb) + CHAR_RESET
            print_temporary_speed = CHAR_BOLD + kb_to_speed_human_just(speed_temp) + CHAR_RESET
            print_avg_speed = CHAR_BOLD + kb_to_speed_human_just(speed_avg) + CHAR_RESET
            print_eta = CHAR_BOLD + seconds_to_human(eta_s).rjust(8) + CHAR_RESET

            # output formatting
            if remaining_kb < 100:
                print_remaining = CHAR_GREEN + print_remaining

            if speed_temp > 0:
                print_temporary_speed = CHAR_RED + print_temporary_speed
            elif speed_temp == 0:
                print_temporary_speed = CHAR_YELLOW + print_temporary_speed
            else:
                print_temporary_speed = CHAR_GREEN + print_temporary_speed

            if speed_avg > 0:
                print_avg_speed = CHAR_RED + print_avg_speed
            elif speed_avg == 0:
                print_avg_speed = CHAR_YELLOW + print_avg_speed
            else:
                print_avg_speed = CHAR_GREEN + print_avg_speed

            if not eta_s:
                print_eta = CHAR_YELLOW + print_eta
            elif eta_s < 60:
                print_eta = CHAR_GREEN + print_eta
            elif eta_s > 600:
                print_eta = CHAR_RED + print_eta

            print(f'[{print_timestamp}] Remaining:{print_remaining}, '
                  f'Speed:{print_temporary_speed}, '
                  f'AVG:{print_avg_speed}, '
                  f'ETA: {print_eta}')

            # delay before next loop
            inp = input_or_timeout(1)
            # sync command
            if inp == 's':
                if background_thread and background_thread.is_alive():
                    log.info('already syncing.')
                else:
                    log.info('running sync in background...')
                    background_thread = run_sync_background()
            elif inp == 'q':
                return

    except KeyboardInterrupt:
        # Ctrl + C handling without printing stack trace
        print()  # new line)
    finally:
        # cleanup_thread
        if background_thread is not None:
            background_thread.stop()
