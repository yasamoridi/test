import os
import platform
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox


def schedule_shutdown(target_time: datetime):
    """Schedule a system shutdown at the given datetime."""
    now = datetime.now()
    if target_time <= now:
        # if target time already passed today, assume next day
        target_time += timedelta(days=1)
    delta = target_time - now
    total_seconds = int(delta.total_seconds())

    system = platform.system().lower()
    try:
        if 'windows' in system:
            os.system(f"shutdown /s /t {total_seconds}")
        elif 'linux' in system or 'darwin' in system:
            minutes = max(1, total_seconds // 60)
            os.system(f"shutdown -h +{minutes}")
        else:
            messagebox.showerror("Unsupported OS", f"Shutdown not supported on {system}.")
            return
        messagebox.showinfo("Scheduled", f"Shutdown scheduled for {target_time.strftime('%Y-%m-%d %H:%M')}")
    except Exception as exc:
        messagebox.showerror("Error", str(exc))


def on_schedule(entry: tk.Entry):
    time_str = entry.get().strip()
    try:
        target = datetime.strptime(time_str, "%H:%M")
        now = datetime.now()
        target = target.replace(year=now.year, month=now.month, day=now.day)
    except ValueError:
        messagebox.showerror("Invalid time", "Please enter time in HH:MM format.")
        return
    schedule_shutdown(target)


def main():
    root = tk.Tk()
    root.title("Shutdown Scheduler")

    tk.Label(root, text="Enter shutdown time (HH:MM):").pack(padx=10, pady=5)
    time_entry = tk.Entry(root)
    time_entry.pack(padx=10, pady=5)

    schedule_button = tk.Button(root, text="Schedule Shutdown", command=lambda: on_schedule(time_entry))
    schedule_button.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
