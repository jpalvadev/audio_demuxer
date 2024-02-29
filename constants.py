import torch
# pylint: disable=broad-except
try:
    CUDA_VERSION = torch.cuda.get_device_properties(0).major
except Exception:
    CUDA_VERSION = 0

MIN_CUDA_VERSION = 6
OVERLAP_STEP_SIZE = 0.05
OVERLAP_MIN_VALUE = 0.01
OVERLAP_MAX_VALUE = 0.99

SHIFTS_STEP_SIZE = 1
SHIFTS_MIN_VALUE = 1
SHIFTS_MAX_VALUE = 10

JOBS_STEP_SIZE = 1
JOBS_MIN_VALUE = 1
JOBS_MAX_VALUE = 20

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

DISABLED_BTN_STYLE = {
    "fg_color": ["#e5e5e5", "#292524"],
    "border_color": ["#e5e5e5", "#292524"],
    "text_color_disabled": ["#0C0A09", "#f8fafc"],
    "state": "disabled"
}


DEFAULT_BTN_STYLE = {
    "fg_color": ["#4338ca", "#f2dd78"],
    "border_color": ["#4338ca", "#f2dd78"],
    "state": "normal"
}

MODELS = {
    "Hybrid Transformer Demucs v4": "htdemucs",
    "Hybrid Transformer Demucs v4 Fine-Tuned": "htdemucs_ft",
    "Hybrid Transformer Demucs v4 6 Sources": "htdemucs_6s",
    "Hybrid Demucs v3": "hdemucs_mmi",
    "Demucs trained with MusDB HQ": "mdx",
    "Demucs trained with MusDB HQ + sources": "mdx_extra",
    "MDX quantized": "mdx_q",
    "MDX + extra sources quantized": "mdx_extra_q"
}

FILETYPES = [
    ("MP3 Files", "*.mp3"),
    ("WAV Files", "*.wav"),
    ("OGG Files", "*.ogg"),
    ("FLAC Files", "*.flac"),
]

OUTPUT_FORMATS = {
    "MP3": "--mp3",
    "WAV": "",
    "FLAC": "--flac"
}

PLACEHOLDERS = {
    "source": "Select Audio File",
    "output": "Select Output Folder",
}

MP3_BITRATES = ("320", "256", "192", "128")


SPLIT_MODES = {
    "Separate all tracks": "",
    "Karaoke": "--two-stems vocals",
    "Drumless": "--two-stems drums",
    "Bassless": "--two-stems bass",
    "Other sources only": "--two-stems other"
}

CLIP_MODES = {
    "Rescale": "rescale",
    "Clamp": "clamp",

}


DEVICES = {"GPU (CUDA)": "cuda", "CPU": "cpu"} if CUDA_VERSION >= MIN_CUDA_VERSION else {
    "CPU": "cpu"}

ANIMATION = {
    "radious": 50,
    "angular_velocity": 0.08,
    "center_x": WINDOW_WIDTH / 2,
    "center_y": WINDOW_HEIGHT / 2,
}
