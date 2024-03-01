from typing import Callable, Union
import math
import customtkinter
import constants
import utils
from state import state


class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 min_value: Union[int, float] = 1,
                 max_value: Union[int, float] = 10,
                 key: str = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.step_size = step_size
        self.command = command
        self.min_value = min_value
        self.max_value = max_value
        self.key = key
        self.value = state.get(key)

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=28,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(0, 0), pady=0)

        self.label_var = customtkinter.IntVar(value=self.value) if isinstance(
            step_size, int) else customtkinter.DoubleVar(value=self.value)
        self.label = customtkinter.CTkLabel(
            self, width=60, textvariable=self.label_var)
        self.label.grid(row=0, column=1, columnspan=1,
                        padx=0, pady=0, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=28,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 0), pady=0)

    def add_button_callback(self):
        try:
            if isinstance(self.step_size, int):
                new_value = self.label_var.get() + self.step_size
            else:
                new_value = round(self.label_var.get() +
                                  self.step_size, 2)
            new_value = new_value if new_value <= self.max_value else self.max_value
            self.label_var.set(new_value if isinstance(
                self.step_size, int) else f"{new_value:.2f}")

            if self.command is not None:
                self.command(self.label_var.get(), self.key)
        except ValueError:
            return

    def subtract_button_callback(self):
        try:
            if isinstance(self.step_size, int):
                new_value = self.label_var.get() - self.step_size
            else:
                new_value = round(self.label_var.get() -
                                  self.step_size, 2)
            new_value = new_value if new_value >= self.min_value else self.min_value
            self.label_var.set(new_value if isinstance(
                self.step_size, int) else f"{new_value:.2f}")

            if self.command is not None:
                self.command(self.label_var.get(), self.key)
        except ValueError:
            return


class LoadingFrame(customtkinter.CTkFrame):
    def __init__(self, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.angle = 0
        self.animation_id = None

        self.configure(fg_color=("#FFFFFF", "#0C0A09"))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.settings_label = customtkinter.CTkLabel(self, justify="left")

        self.circle_1 = customtkinter.CTkButton(self,
                                                text="",
                                                state="disabled",
                                                width=28,
                                                height=28,
                                                hover="disable",
                                                )
        self.circle_2 = customtkinter.CTkButton(self,
                                                text="",
                                                state="disabled",
                                                width=28,
                                                height=28,
                                                hover="disable",
                                                )
        self.circle_3 = customtkinter.CTkButton(self,
                                                text="",
                                                state="disabled",
                                                width=28,
                                                height=28,
                                                hover="disable",
                                                )

        self.progressbar = customtkinter.CTkProgressBar(
            self, height=18, width=constants.WINDOW_WIDTH / 2)
        self.progressbar.grid(row=2, column=0)

        self.label = customtkinter.CTkLabel(
            self, text="Audio Demuxer is working. Please wait...", font=("Roboto", 24))
        self.label.grid(row=3, column=0, columnspan=3, sticky="ew")

    def show(self, text: str):
        self.settings_label.configure(text=text)
        self.settings_label.grid(
            row=0, column=0, columnspan=3, sticky="new")
        self.place(relwidth=1, relheight=1)
        self.animation_id = "after#01"
        self.animate_btns()

    def hide(self):
        self.progressbar.set(0)
        utils.progress_tracker.reset_all()
        self.after_cancel(self.animation_id)
        self.animation_id = None
        self.place_forget()

    def animate_btns(self):
        self.angle += constants.ANIMATION["angular_velocity"]

        self.circle_1.place(
            x=constants.ANIMATION["center_x"] + constants.ANIMATION["radious"] *
            math.cos(self.angle + 0),
            y=constants.ANIMATION["center_y"] + constants.ANIMATION["radious"] *
            math.sin(self.angle + 0),
            anchor="center")
        self.circle_2.place(
            x=constants.ANIMATION["center_x"] + constants.ANIMATION["radious"] *
            math.cos(self.angle + 2),
            y=constants.ANIMATION["center_y"] + constants.ANIMATION["radious"] *
            math.sin(self.angle + 2),
            anchor="center")
        self.circle_3.place(
            x=constants.ANIMATION["center_x"] + constants.ANIMATION["radious"] *
            math.cos(self.angle + 4),
            y=constants.ANIMATION["center_y"] + constants.ANIMATION["radious"] *
            math.sin(self.angle + 4),
            anchor="center")
        self.progressbar.set(utils.progress_tracker.get_progress())

        # To avoid after_cancel bug, after gets called only when animation_id is not None
        self.animation_id = self.after(
            20, self.animate_btns) if self.animation_id is not None else None
        # print("animating", self.animation_id)


class Label(customtkinter.CTkFrame):
    def __init__(self, *args,
                 text: str = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self, text=self.text, justify="left")
        self.label.grid(row=0, column=0, padx=10, pady=1, sticky="w")

    def set_text(self, text: str):
        self.label.configure(text=text)
