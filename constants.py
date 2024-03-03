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

TOOLTIP_SETTINGS = {
    "delay": 0.6,
    "corner_radius": 3,
    "alpha": 0.85,
    "bg_color": ["#0C0A09", "#f8fafc"],
    "text_color": ["#f8fafc", "#0C0A09"],
    "x_offset": -100,
    "y_offset": 30,
}

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

TOOLTIPS = {
    "toggle_theme": "Switch between light mode and dark mode.",
    "source": "Select an audio file to separate.",
    "output": "Folder where to put extracted tracks.",
    "model": "Select a Demucs model for audio source separation.",
    "split_mode": "Select how to separate audio source.",
    "format": "Select the output format.",
    "mp3_bitrate": "Select the bitrate for the MP3 output.",
    "clip": "Strategy for avoiding clipping: rescaling entire signal if necessary (rescale) or hard clipping (clamp).",
    "device": "Device to use for audio separation.",
    "overlap": "Overlap between the splits.",
    "shifts": "Number of random shifts for equivariant stabilization. Increase separation time but improves quality",
    "jobs": "Number of jobs. Increase when RAM and multiple cores are available.",
    "separate": "Start the separation process.",

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
