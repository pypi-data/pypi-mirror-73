#!/usr/bin/python3
import argparse
import platform
import sys

from time import sleep
from datetime import datetime
from os import system, getpid, path
from multiprocessing import Process

WELCOME_PAGE = """
  ____                                  _  ___
 ♂  _ \                                ♂ |/ (_)
 ♂ |_) | __ _ _ __   __ _ _ __   __ _  ♂ ' / _ _ __   __ _
 ♂  _ < / _` | '_ \ / _` | '_ \ / _` | ♂  < | | '_ \ / _` ♂
 ♂ |_) | (_| | | | | (_| | | | | (_| | ♂ . \| | | | | (_| ♂
 ♂____/ \__,_|_| |_|\__,_|_| |_|\__,_| ♂_|\_\_|_| |_|\__, ♂
                                                      __/ ♂
                                                     |___/

"""

is_windows =  platform.system() == 'Windows'
PROGRESS_BAR_SIZE = 40 if not is_windows else 30
LB = [
    "老铁们啊,只有你们想不到的,没有老八做不到的.还是那句话,今天老八,挑战一把吃粑粑",
    "老铁们啊,虽然不是同一时间,但是同一个撤shuoer~.老八我再次挑战一把吃粑粑",
    "老铁们啊,只有你们想不到的,永远没有我老八做不到的.你们不要笑我狼狈不堪,我也可以笑你,离开你的父母,比我吃屎都难",
    "奥利给! 干了兄弟们! 呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~呕~",
]


def run(program, time_str, show_progress=True):
    replace_time_dict = dict(second=0, minute=0)
    current_time = datetime.now()

    def check(index, value):
        if value is None:
            return
        value = int(value)
        if index == 0:
            replace_time_dict["hour"] = None if value > 24 or value < 0 else value
        elif index == 1:
            replace_time_dict["minute"] = None if value > 60 or value < 0 else value
        elif index == 2:
            replace_time_dict["second"] = None if value > 60 or value < 0 else value

    if time_str:
        for i, v in enumerate(time_str.replace(" ", "").split(":")):
            if i > 2:
                break
            check(i, v)

        run_time = current_time.replace(**replace_time_dict)
        run_time = current_time if run_time < current_time else run_time
        print(
            'Execute Time: {}\tExecute Program: "{}"'.format(
                run_time.strftime("%H:%M:%S"), program
            )
        )
        total_seconds = None
        if show_progress:
            total_seconds = (run_time - current_time).total_seconds()
        else:
            print("Run in backgroud, and will print Killed.")
         
        while True:
            current_time = datetime.now()
            if run_time <= current_time:
                break
            if not show_progress:
                sleep(1)
                continue

            if current_time.second % 9 == 0:
                sys.stdout.write(LB[current_time.second % 4] + "\r")
                sleep(1)
                sys.stdout.flush()
            else:
                time_difference = run_time - current_time
                last_progress = time_difference.total_seconds() / total_seconds

                show_last_progress = int(last_progress * PROGRESS_BAR_SIZE)
                sys.stdout.write(
                    "Time Remaining: {} |{} {}% {}|\r".format(
                        str(time_difference).split('.')[0],
                        "♂" * int(PROGRESS_BAR_SIZE - show_last_progress),
                        round((1 - last_progress) * 100, 2),
                        "-" * show_last_progress,
                    )
                )
                sleep(1)
                sys.stdout.flush()
            sys.stdout.write(
                "                                                                                                             \r"
            )
            sys.stdout.flush()
    print('\n\t\t蕉!      迟!      但!      到!\n\n\t\tBanana King Is Never! Absent!\n')
    if not is_windows and path.exists(program):
        return system('./' + program)
    return system(program)


class MyParse(argparse.ArgumentParser):
    def print_help(self, file=None):
        example_str = """
Example: 
  1. banana-king -p "ls /"
  2. banana-king -p "ls /" -t 22:23
  3. banana-king -p "ls /" -t 22:23 -b
"""
        print(WELCOME_PAGE)
        super().print_help(file)
        print(example_str)


def main():
    parser = MyParse()
    parser.add_argument("-t", "--time", help='set time to execute, format: "H:M:S"')
    parser.add_argument(
        "-f",
        "--foreground",
        help="execute this program foreground",
        action="store_true",
    )
    parser.add_argument(
        "-b",
        "--background",
        help="execute this program background",
        action="store_true",
    )
    parser.add_argument("-p", "--program", help="program path")

    args = parser.parse_args()
    if args.program:
        print(WELCOME_PAGE)
        if args.background:
            Process(target=run, args=(args.program, args.time, False)).start()
            
            if platform.system() == 'Windows':
                system('taskkill /pid {} /f'.format(getpid()))
            else:
                system("kill -KILL {}".format(getpid(), getpid()))
        else:
            run(args.program, args.time)
    else:
        parser.print_help()