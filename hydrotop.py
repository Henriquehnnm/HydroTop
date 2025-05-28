#!/usr/bin/env python3
import curses
import psutil
import time

TITLE = r"""

██╗  ██╗██╗   ██╗██████╗ ██████╗  ██████╗ ████████╗ ██████╗ ██████╗ 
██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████║ ╚████╔╝ ██║  ██║██████╔╝██║   ██║   ██║   ██║   ██║██████╔╝
██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██║   ██║   ██║   ██║   ██║██╔═══╝ 
██║  ██║   ██║   ██████╔╝██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     
                                                                    
"""

# Nerd Fonts Symbols
CPU_SYM = " "
MEM_SYM = " "
DISK_SYM = " "
NET_SYM = " "

# Box-drawing chars
TL = '╭'
TR = '╮'
BL = '╰'
BR = '╯'
H  = '─'
V  = '│'

# Minimal terminal dimensions
MIN_WIDTH = 45
MIN_HEIGHT = 30

# Draw a rectangular box at (y,x) with given h,w, safely
def draw_box(stdscr, y, x, h, w):
    try:
        stdscr.addstr(y, x, TL + H*(w-2) + TR)
        for i in range(1, h-1):
            stdscr.addstr(y+i, x, V)
            stdscr.addstr(y+i, x+w-1, V)
        stdscr.addstr(y+h-1, x, BL + H*(w-2) + BR)
    except curses.error:
        # ignore drawing errors when viewport is small
        pass

# Draw a colored bar
def draw_bar(stdscr, y, x, width, percent, color):
    fill = int(width * percent / 100)
    bar = '█'*fill + '░'*(width-fill)
    try:
        stdscr.addstr(y, x, bar, curses.color_pair(color))
    except curses.error:
        pass

# Main TUI loop
def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)  # non-blocking input

    # init color pairs
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)

    # For network rate calculation
    last_net = psutil.net_io_counters()
    last_time = time.time()

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # Check minimal size
        if h < MIN_HEIGHT or w < MIN_WIDTH:
            msg = f"Resize terminal to at least {MIN_WIDTH}x{MIN_HEIGHT}"
            try:
                stdscr.addstr(h//2, max(0, (w - len(msg))//2), msg, curses.color_pair(2) | curses.A_BOLD)
            except curses.error:
                pass
            stdscr.refresh()
            time.sleep(1.0)
            continue

        # Calculate box sizes
        box_w = min(80, w-4)
        metrics_h = len(TITLE.strip().splitlines()) + 10  # title + barras + linha de rede
        proc_h = 1 + 5 + 2
        total_h = metrics_h + proc_h + 3
        start_y = max((h-total_h)//2, 1)
        start_x = max((w-box_w)//2, 2)

        # Draw metrics box
        draw_box(stdscr, start_y, start_x, metrics_h, box_w)
        for idx, line in enumerate(TITLE.strip().splitlines()):
            try:
                stdscr.addstr(start_y+1+idx, start_x+2, line, curses.color_pair(3) | curses.A_BOLD)
            except curses.error:
                pass

        # Bars inside metrics box
        inner_x = start_x + 2
        inner_w = box_w - 4

        # CPU
        cpu = psutil.cpu_percent(interval=None)
        try:
            stdscr.addstr(start_y+metrics_h-8, inner_x, f"{CPU_SYM} CPU: {cpu:5.1f}%", curses.color_pair(4))
        except curses.error:
            pass
        draw_bar(stdscr, start_y+metrics_h-8, inner_x+20, inner_w-20, cpu, 1 if cpu<70 else 2)

        # MEM
        mem = psutil.virtual_memory().percent
        try:
            stdscr.addstr(start_y+metrics_h-6, inner_x, f"{MEM_SYM} Mem: {mem:5.1f}%", curses.color_pair(4))
        except curses.error:
            pass
        draw_bar(stdscr, start_y+metrics_h-6, inner_x+20, inner_w-20, mem, 1 if mem<70 else 2)

        # DISK
        disk = psutil.disk_usage('/').percent
        try:
            stdscr.addstr(start_y+metrics_h-4, inner_x, f"{DISK_SYM} Disk: {disk:5.1f}%", curses.color_pair(4))
        except curses.error:
            pass
        draw_bar(stdscr, start_y+metrics_h-4, inner_x+20, inner_w-20, disk, 1 if disk<70 else 2)

        # NET (agora dentro da caixa de métricas)
        now = time.time()
        net = psutil.net_io_counters()
        elapsed = now - last_time
        down = (net.bytes_recv - last_net.bytes_recv) / 1024 / elapsed
        up = (net.bytes_sent - last_net.bytes_sent) / 1024 / elapsed
        last_net, last_time = net, now
        try:
            stdscr.addstr(start_y+metrics_h-2, inner_x, f"{NET_SYM} ↓{down:6.1f}KB/s ↑{up:6.1f}KB/s", curses.color_pair(5))
        except curses.error:
            pass

        # Draw processes box below
        proc_y = start_y + metrics_h + 1
        draw_box(stdscr, proc_y, start_x, proc_h, box_w)
        try:
            stdscr.addstr(proc_y+1, start_x+2, "PID   CPU%   MEM%   Name", curses.A_BOLD)
        except curses.error:
            pass
        procs = sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
        for i, p in enumerate(procs[:5]):
            info = p.info
            line = f"{info['pid']:5d} {info['cpu_percent']:6.1f} {info['memory_percent']:6.1f} {info['name'][:box_w-20]}"
            try:
                stdscr.addstr(proc_y+2+i, start_x+2, line)
            except curses.error:
                pass

        # Footer
        try:
            stdscr.addstr(start_y+total_h, start_x+2, "Press 'q' to exit", curses.color_pair(3))
        except curses.error:
            pass
        stdscr.refresh()

        # Delay for update
        time.sleep(1.0)
        # non-blocking key check
        if stdscr.getch() == ord('q'):
            break

if __name__ == '__main__':
    curses.wrapper(main)
