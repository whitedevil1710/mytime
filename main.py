#!/bin/python3
import os
import time
from datetime import datetime, timedelta
from tkinter import Tk, messagebox
import sqlite3
from lock import check_screen
from banner import banner

conn = sqlite3.connect('work_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS work_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        start_time TIMESTAMP,
        accurate_work_time TEXT,
        total_break_time TEXT,
        last_locked_time TEXT,
        num_times_locked INTEGER,
        total_num_breaks INTEGER
    )
''')
conn.commit()

last_updated_date = None  

def parse_time_string_to_timedelta(time_str):
    hours, minutes, seconds = map(float, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def get_existing_data():
    cursor.execute('SELECT * FROM work_logs ORDER BY date DESC LIMIT 1')
    row = cursor.fetchone()

    if row:
        date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks = row[1:]
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            elapsed_work_time = parse_time_string_to_timedelta(elapsed_work_time)
            total_break_time = parse_time_string_to_timedelta(total_break_time)
            
            if last_locked_time and last_locked_time != 'None':
                last_locked_time = datetime.strptime(last_locked_time, '%Y-%m-%d %H:%M:%S.%f')
            else:
                last_locked_time = None

            return date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks
        except ValueError as e:
            print(f"Error converting date/time string: {e}")
            return None
    else:
        return None


def insert_or_update_work_data(date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks):
    cursor.execute('SELECT * FROM work_logs WHERE date = ?', (date,))
    existing_record = cursor.fetchone()

    if existing_record:
        cursor.execute('''
            UPDATE work_logs
            SET start_time = ?, accurate_work_time = ?, total_break_time = ?,
                last_locked_time = ?, num_times_locked = ?, total_num_breaks = ?
            WHERE date = ?
        ''', (start_time, str(elapsed_work_time), str(total_break_time), last_locked_time.strftime('%Y-%m-%d %H:%M:%S') if last_locked_time else None, num_times_locked, total_num_breaks, date))
    else:
        cursor.execute('''
            INSERT INTO work_logs (date, start_time, accurate_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, start_time, str(elapsed_work_time), str(total_break_time), last_locked_time.strftime('%Y-%m-%d %H:%M:%S') if last_locked_time else None, num_times_locked, total_num_breaks))
    
    conn.commit()

def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def update_database(start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks):
    current_date = datetime.now().date()

    existing_data = get_existing_data()
    if existing_data:
        last_updated_date, _, _, _, _, _, _ = existing_data
        if last_updated_date != current_date:
            insert_or_update_work_data(current_date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks)
    else:
        insert_or_update_work_data(current_date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks)

def calculate_work_time(start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks):
    fmt = '%Y-%m-%d %H:%M:%S'
    screen_locked_time = None
    work_start_time = start_time
    last_elapsed = timedelta(0)
    count = num_times_locked
    lock = last_locked_time
    num = total_num_breaks

    while True:
        current_time = datetime.now()
        screen_locked = check_screen() 

        elapsed_since_last_iteration = current_time - start_time
        if screen_locked:
            if screen_locked_time is None:
                screen_locked_time = current_time
                print("Screen locked. Work paused.")
                count += 1
                lock = current_time
        else:
            if screen_locked_time is not None:
                screen_unlocked_time = current_time
                screen_locked_duration = screen_unlocked_time - screen_locked_time
                response = show_break_popup()
                if response:
                    total_break_time += screen_locked_duration
                    num += 1
                else:
                    locked_during_work_time = screen_locked_time - work_start_time
                    work_start_time += locked_during_work_time
                    elapsed_since_last_iteration -= locked_during_work_time

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

        predicted_end_time = current_time + remaining_work_time
        os.system('cls' if os.name == 'nt' else 'clear')

        update_database(start_time, elapsed_work_time, total_break_time, lock, count, num)

        elapsed_work_time_str = format_timedelta(elapsed_work_time)
        total_break_time_str = format_timedelta(total_break_time)
        lock_time_str = lock.strftime('%Y-%m-%d %H:%M:%S') if lock else "N/A"

        banner()
        print("\n" * 5)
        print(f"{' ' * 20}Start Time:              {start_time.strftime(fmt)}")
        print(f"{' ' * 20}Current Time:            {current_time.strftime(fmt)}")
        print(f"{' ' * 20}Accurate Work Time:      {elapsed_work_time_str}")
        print(f"{' ' * 20}Total Break Time:        {total_break_time_str}")
        print(f"{' ' * 20}Last locked Time:        {lock_time_str}")
        print(f"{' ' * 20}Number of times locked:  {count}")
        print(f"{' ' * 20}Total number of breaks:  {num}")
        print(f"{' ' * 20}Predicted end time:      {predicted_end_time.strftime(fmt)}")

        time.sleep(1)

def show_break_popup():
    root = Tk()
    root.withdraw()
    response = messagebox.askquestion("Tester Break Time", "Have you been on a break?")
    root.update_idletasks()
    root.destroy()

    return response.lower() == "yes"

if __name__ == "__main__":
    try:

        existing_data = get_existing_data()
        if existing_data:
            last_updated_date, start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks = existing_data
        else:
            last_updated_date = None
            start_time = datetime.now()
            elapsed_work_time = timedelta(0)
            total_break_time = timedelta(0)
            last_locked_time = None
            num_times_locked = 0
            total_num_breaks = 0

        calculate_work_time(start_time, elapsed_work_time, total_break_time, last_locked_time, num_times_locked, total_num_breaks)
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            conn.close()
        except Exception as e:
            print(f"Error while closing the database connection: {e}")
