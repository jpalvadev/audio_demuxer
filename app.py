import shlex
from threading import Thread
import shutil
import os
import demucs.separate
import customtkinter
from customtkinter import filedialog
from PIL import Image
import constants
import custom_widgets
import utils


# Set FFMPEG temporal ENV PATH
os.environ["PATH"] += os.pathsep + utils.resource("ffmpeg")


# App Configuration
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme(utils.resource("themes/theme.json"))


global_vars = {
    "source": "",
    "output": "",
    "model": "Hybrid Transformer Demucs v4",
    "output_format": "MP3",
    "mp3_bitrate": "320",
    "split_mode": "Separate all tracks",
    "device": "GPU (CUDA)" if constants.CUDA_VERSION >= constants.MIN_CUDA_VERSION else "CPU",
    "shifts": 1,
    "clip_mode": "Rescale",
    "jobs": 1,
    "overlap": 0.25,
}


app = customtkinter.CTk()
app.title("Audio Demuxer")
app.geometry(f"{constants.WINDOW_WIDTH}x{constants.WINDOW_HEIGHT}")
app.resizable(False, False)

app.wm_iconbitmap(utils.resource("images/icon.ico"))

app.grid_columnconfigure(0, weight=1, uniform="x")
app.grid_columnconfigure(13, weight=1, uniform="x")
for i in range(1, 13):
    app.grid_columnconfigure(i, weight=2, uniform="x")

app.grid_rowconfigure(0, weight=2, uniform="x")
for i in range(1, 12):
    app.grid_rowconfigure(i, weight=1, uniform="x")


def change_appearance_mode():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("Light")
    else:
        customtkinter.set_appearance_mode("Dark")


def separate_worker():
    # pylint: disable=broad-except
    try:
        demucs.separate.main(shlex.split(
            f'{constants.OUTPUT_FORMATS[global_vars["output_format"]]} '
            f'{"--mp3-bitrate " + global_vars["mp3_bitrate"] if global_vars["output_format"] == "MP3" else ""} '
            f'{constants.SPLIT_MODES[global_vars["split_mode"]]} '
            f'-n {constants.MODELS[global_vars["model"]]} '
            f'--shifts {global_vars["shifts"]} '
            f'--clip-mode {constants.CLIP_MODES[global_vars["clip_mode"]]} '
            f'--overlap {global_vars["overlap"]} '
            f'-d {constants.DEVICES[global_vars["device"]]} '
            f'-o "{global_vars["output"]}" '
            f'-j {global_vars["jobs"]} '
            f'"{global_vars["source"]}"'))

        # Removing temp files
        file_folder_name = os.path.splitext(
            os.path.basename(global_vars["source"]))[0]
        model_folder_name = constants.MODELS[global_vars["model"]]
        shutil.copytree(
            f"{global_vars['output']}/{model_folder_name}/{file_folder_name}", global_vars["output"], dirs_exist_ok=True)
        shutil.rmtree(f"{global_vars['output']}/{model_folder_name}", True)
        utils.show_notification(master=app, title="Success",
                                message="Audio separated successfully.",
                                icon="check")

    except Exception as e:
        utils.show_notification(
            master=app,
            title="Error",
            message=str(e),
            icon="cancel")

    finally:
        loading_frame.hide()


def separate():
    settings = f'''
    Selected Audio File: {global_vars["source"]}
    Files will be saved in: {global_vars["output"]}
    Selected Model: {global_vars["model"]}
    Split Mode: {global_vars["split_mode"]}
    Output Format: {global_vars["output_format"]} 
    Shifts set to: {global_vars["shifts"]}
    Overlap set to: {global_vars["overlap"]}
    Clip Mode: {global_vars["clip_mode"]}
    Selected Device for Separation: {global_vars["device"]} 
    '''

    loading_frame.show(settings)

    t = Thread(target=separate_worker)
    t.start()


def set_source():
    source = filedialog.askopenfilename(
        title="Select audio file",
        filetypes=constants.FILETYPES,
    )
    if not source:
        return
    global_vars["source"] = source
    source_selected_label.set_text(global_vars["source"])
    check_paths()


def set_output():
    output = filedialog.askdirectory(
        title="Select output directory")
    if not output:
        return
    global_vars["output"] = output
    output_selected_label.set_text(global_vars["output"])
    check_paths()


def show_bitrate_menu():
    mp3_bitrate_title_label.grid(row=8, column=5, columnspan=2, sticky="ew")
    mp3_bitrate_menu.grid(row=8, column=7, columnspan=1, sticky="ew")


def hide_bitrate_menu():
    mp3_bitrate_title_label.grid_forget()
    mp3_bitrate_menu.grid_forget()


def show_jobs_spinbox():
    jobs_title_label.grid(row=9, column=10, columnspan=1, sticky="w")
    jobs_spinbox.grid(row=9, column=11, columnspan=2, sticky="ew")


def hide_jobs_spinbox():
    jobs_title_label.grid_forget()
    jobs_spinbox.grid_forget()


def check_paths():
    if not global_vars["source"] or not global_vars["output"]:
        separate_btn.configure(**constants.DISABLED_BTN_STYLE)
    else:
        separate_btn.configure(**constants.DEFAULT_BTN_STYLE)


def update_gui():
    if global_vars["output_format"] == "MP3":
        show_bitrate_menu()
    else:
        hide_bitrate_menu()

    if global_vars["device"] == "CPU":
        show_jobs_spinbox()
    else:
        hide_jobs_spinbox()


def update_global_vars(choice, key):
    global_vars[key] = choice
    update_gui()


# Title and subtitle
app_title_label = customtkinter.CTkLabel(
    app, text="Audio Demuxer", font=("Roboto", 36), justify="center")
app_title_label.grid(row=0, column=1, columnspan=12, sticky="ew")

app_subtitle_label = customtkinter.CTkLabel(
    app, text="Made with ❤ by: @jpalvadev, using Demucs from Meta, Inc.", font=("Roboto", 16), justify="center")
app_subtitle_label.grid(row=1, column=1, columnspan=12, sticky="new")

# Dark/Light btn
theme_icons = customtkinter.CTkImage(light_image=Image.open(utils.resource("images/light.png")),
                                     dark_image=Image.open(
                                         utils.resource("images/dark.png")),
                                     size=(20, 20))

togle_theme_btn = customtkinter.CTkButton(
    app, image=theme_icons, text="", width=28, height=28, command=change_appearance_mode)
togle_theme_btn.grid(row=0, column=12, sticky="e")


# Source Selection Section
source_title_label = customtkinter.CTkLabel(
    app, text="Audio File", justify="left")
source_title_label.grid(row=3, column=1, columnspan=2, sticky="w")
source_selected_label = custom_widgets.Label(
    app, text=constants.PLACEHOLDERS["source"])
source_selected_label.grid(
    row=3, column=2, columnspan=10, sticky="ew", padx=15)
source_btn = customtkinter.CTkButton(
    app, text="Select", command=set_source)
source_btn.grid(row=3, column=12)

# Output Selection Section
output_title_label = customtkinter.CTkLabel(
    app, text="Directory", justify="left")
output_title_label.grid(row=4, column=1, columnspan=2, sticky="w")
output_selected_label = custom_widgets.Label(
    app, text=constants.PLACEHOLDERS["output"])
output_selected_label.grid(
    row=4, column=2, columnspan=10, sticky="ew", padx=15)
output_btn = customtkinter.CTkButton(
    app, text="Select", command=set_output)
output_btn.grid(row=4, column=12)

# Model Selection Section
model_title_label = customtkinter.CTkLabel(
    app, text="Demucs Model", justify="left")
model_title_label.grid(row=6, column=1, columnspan=2, sticky="w")
model_menu = customtkinter.CTkOptionMenu(
    app,
    values=list(constants.MODELS.keys()),
    command=lambda choice: update_global_vars(choice, "model")
)
model_menu.grid(row=6, column=3, columnspan=5, sticky="ew")

# Split Mode Selection Section
split_mode_title_label = customtkinter.CTkLabel(
    app, text="Audio Split Mode", justify="left")
split_mode_title_label.grid(row=7, column=1, columnspan=2, sticky="w")
split_mode_menu = customtkinter.CTkOptionMenu(
    app,
    values=list(constants.SPLIT_MODES.keys()),
    command=lambda choice: update_global_vars(choice, "split_mode"),
)
split_mode_menu.grid(row=7, column=3, columnspan=3, sticky="ew")

# Format Selection Section
format_title_label = customtkinter.CTkLabel(
    app, text="Output Format", justify="left")
format_title_label.grid(row=8, column=1, columnspan=2, sticky="w")
format_menu = customtkinter.CTkOptionMenu(
    app,
    values=list(constants.OUTPUT_FORMATS.keys()),
    command=lambda choice: update_global_vars(choice, "output_format"),
)
format_menu.grid(row=8, column=3, columnspan=2, sticky="ew")

# Mp3 bitrate Selection Section
mp3_bitrate_title_label = customtkinter.CTkLabel(
    app, text="MP3 bitrate", anchor="center")
mp3_bitrate_title_label.grid(row=8, column=5, columnspan=2, sticky="ew")
mp3_bitrate_menu = customtkinter.CTkOptionMenu(
    app,
    values=constants.MP3_BITRATES,
    command=lambda choice: update_global_vars(choice, "mp3_bitrate"),
)
mp3_bitrate_menu.grid(row=8, column=7, columnspan=1, sticky="ew")

# Clip Mode Selection Section
clip_title_label = customtkinter.CTkLabel(
    app, text="Clip Mode", justify="left")
clip_title_label.grid(row=9, column=1, columnspan=2, sticky="w")
clip_menu = customtkinter.CTkOptionMenu(
    app,
    values=list(constants.CLIP_MODES.keys()),
    command=lambda choice: update_global_vars(choice, "clip_mode"),
)
clip_menu.grid(row=9, column=3, columnspan=2, sticky="ew")

# Device Selection Section
device_title_label = customtkinter.CTkLabel(
    app, text="Device", justify="left")
device_title_label.grid(row=6, column=10, columnspan=1, sticky="w")
device_menu = customtkinter.CTkOptionMenu(
    app,
    values=list(constants.DEVICES.keys()),
    command=lambda choice: update_global_vars(choice, "device"),
)
device_cpuonly_label = custom_widgets.Label(app, text="CPU")
if constants.CUDA_VERSION >= constants.MIN_CUDA_VERSION:
    device_menu.grid(row=6, column=11, columnspan=2, sticky="ew")
else:
    device_cpuonly_label.grid(
        row=6, column=11, columnspan=2, padx=0, sticky="ew")

# Overlap Selection Section
overlap_title_label = customtkinter.CTkLabel(
    app, text="Overlap", justify="left")
overlap_title_label.grid(row=7, column=10, columnspan=1, sticky="w")
overlap_spinbox = custom_widgets.Spinbox(app,
                                         command=update_global_vars,
                                         step_size=constants.OVERLAP_STEP_SIZE,
                                         min_value=constants.OVERLAP_MIN_VALUE,
                                         max_value=constants.OVERLAP_MAX_VALUE,
                                         initial_value=global_vars["overlap"],
                                         key="overlap"
                                         )
overlap_spinbox.grid(row=7, column=11, columnspan=2, sticky="ew")

# Shifts Selection Section
shifts_title_label = customtkinter.CTkLabel(
    app, text="Shifts", justify="left")
shifts_title_label.grid(row=8, column=10, columnspan=1, sticky="w")
shifts_spinbox = custom_widgets.Spinbox(app,
                                        command=update_global_vars,
                                        step_size=constants.SHIFTS_STEP_SIZE,
                                        min_value=constants.SHIFTS_MIN_VALUE,
                                        max_value=constants.SHIFTS_MAX_VALUE,
                                        initial_value=global_vars["shifts"],
                                        key="shifts"
                                        )
shifts_spinbox.grid(row=8, column=11, columnspan=2, sticky="ew")

# Jobs Selection Section
jobs_title_label = customtkinter.CTkLabel(
    app, text="Jobs", justify="left")
jobs_spinbox = custom_widgets.Spinbox(app,
                                      command=update_global_vars,
                                      step_size=constants.JOBS_STEP_SIZE,
                                      min_value=constants.JOBS_MIN_VALUE,
                                      max_value=constants.JOBS_MAX_VALUE,
                                      initial_value=global_vars["jobs"],
                                      key="jobs"
                                      )

# Run demucs btn
separate_btn = customtkinter.CTkButton(
    master=app, text="Separate", command=separate, **constants.DISABLED_BTN_STYLE)
separate_btn.grid(row=10, column=11, columnspan=2,
                  rowspan=2, sticky="ew", pady=(10, 0))


DEBUG = False
if DEBUG:
    def show_no():
        utils.show_notification(
            master=app,
            title="Error",
            message="Something went wrong",
            icon="cancel")

    def show_yes():
        utils.show_notification(
            master=app,
            title="Success",
            message="Everything is working fine",
            icon="check")

    def separatin():
        global_vars["source"] = "C:/tmp/bas.ta_fuerte.mp3"
        global_vars["output"] = "C:/tmp"
        separate()

    def print_state():
        print(global_vars)

    no_btn = customtkinter.CTkButton(master=app, text="No", command=show_no)
    no_btn.grid(row=10, column=7, columnspan=2,
                rowspan=2, sticky="ew", pady=(10, 0))
    yes_btn = customtkinter.CTkButton(master=app, text="Yes", command=show_yes)
    yes_btn.grid(row=10, column=9, columnspan=2,
                 rowspan=2, sticky="ew", pady=(10, 0))
    print_state_btn = customtkinter.CTkButton(
        master=app, text="Print_state", command=print_state)
    print_state_btn.grid(row=10, column=5, columnspan=2,
                         rowspan=2, sticky="ew", pady=(10, 0))
    separate_debug_btn = customtkinter.CTkButton(
        master=app, text="Sparate", command=separatin)
    separate_debug_btn.grid(row=10, column=3, columnspan=2,
                            rowspan=2, sticky="ew", pady=(10, 0))

    bags_label = customtkinter.CTkLabel(
        app, text="Bags", justify="left")
    bags_label.grid(row=10, column=2, sticky="w")


# Loading Frame
loading_frame = custom_widgets.LoadingFrame(app)

update_gui()
app.mainloop()