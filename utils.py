import sys
import os
from CTkMessagebox import CTkMessagebox


def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def show_notification(master, title, message, icon="check"):
    CTkMessagebox(master=master,
                  title=title,
                  message=message,
                  icon=icon,
                  corner_radius=3,
                  fg_color=["#f8fafc", "#0C0A09"],
                  bg_color=["#f8fafc", "#0C0A09"],
                  header=True,
                  )


class ProgressTracker:
    def __init__(self):
        self.bags_count = 0
        self.current_count = 0
        self.progress = 0
        self.total_steps = 0
        self.shifts = 1

    def get_progress(self):
        return self.progress

    def set_bags_count(self, bags_count):
        self.bags_count = bags_count

    def set_progress(self):
        p = (self.current_count / (self.bags_count * self.shifts)) / \
            self.total_steps
        self.progress = round(p, 2)

    def increment_current_count(self):
        self.current_count += 1
        self.set_progress()

    def set_total_steps(self, total_steps):
        self.total_steps = total_steps

    def set_shifts(self, shifts):
        self.shifts = shifts

    def reset_current_count(self):
        self.current_count = 0

    def reset_progress(self):
        self.progress = 0

    def reset_all(self):
        self.bags_count = 0
        self.current_count = 0
        self.progress = 0
        self.total_steps = 0


progress_tracker = ProgressTracker()
