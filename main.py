#!/bin/python3
import os
import time
from datetime import datetime, timedelta
from tkinter import Tk, messagebox
from lock import check_screen
from banner import banner

def show_break_popup():
    root = Tk()
    root.withdraw()
    response = messagebox.askquestion("Break Time", "Have you been on a break?")
    root.update_idletasks()
    root.destroy()

    return response.lower() == "yes"


def format_timedelta(td):
    seconds = td.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"

def predict_work_end(break_hours=0):
    current_time = datetime.now()
    work_duration = timedelta(hours=8) + timedelta(hours=break_hours)
    predicted_end_time = current_time + work_duration

    return predicted_end_time

def calculate_work_time(start_time):
    fmt = '%Y-%m-%d %H:%M:%S'  
    screen_locked_time = None
    work_start_time = start_time
    total_break_time = timedelta(0)
    last_elapsed = timedelta(0)
    count = 0

    while True:
        current_time = datetime.now()

        screen_locked = check_screen()

        elapsed_since_last_iteration = current_time - start_time

        if screen_locked:
            if screen_locked_time is None:
                screen_locked_time = current_time
                print("Screen locked. Work paused.")
                count+=1

        else:  
            if screen_locked_time is not None:
                screen_unlocked_time = current_time
                screen_locked_duration = screen_unlocked_time - screen_locked_time
                response = show_break_popup()
                if response:
                    total_break_time += screen_locked_duration
                else:
                    locked_during_work_time = screen_locked_time - work_start_time
                    work_start_time += locked_during_work_time
                    elapsed_since_last_iteration -= screen_locked_duration

                screen_locked_time = None
                print("Screen unlocked. Work resumed.")

        elapsed_work_time = elapsed_since_last_iteration - total_break_time

        if elapsed_work_time < timedelta(0):
            elapsed_work_time = last_elapsed
            work_start_time = current_time - last_elapsed

        last_elapsed = elapsed_work_time
        remaining_work_time = timedelta(hours=8) - elapsed_work_time
        if remaining_work_time < timedelta(0):
            remaining_work_time = timedelta(0)

        predicted_end_time = current_time + remaining_work_time + total_break_time
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        print("\n"*5)
        print(f"{' '*20}Start Time:              {start_time.strftime(fmt)}")
        print(f"{' '*20}Current Time:            {current_time.strftime(fmt)}")
        print(f"{' '*20}Accurate Work Time:      {format_timedelta(elapsed_work_time)}")
        print(f"{' '*20}Total Break Time:        {format_timedelta(total_break_time)}")
        print(f"{' '*20}Last locked Time:        {screen_locked_time}")
        print(f"{' '*20}Number of times locked:  {count}")
        print(f"{' '*20}Predicted end time:      {predicted_end_time.strftime(fmt)}")
     


        time.sleep(1)

start_time = datetime.now()
calculate_work_time(start_time)
