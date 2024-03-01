import constants
import shlex


class State:
    def __init__(self):
        self.source = ""
        self.output = ""
        self.model = "Hybrid Transformer Demucs v4"
        self.output_format = "MP3"
        self.mp3_bitrate = "320"
        self.split_mode = "Separate all tracks"
        self.device = "GPU (CUDA)" if constants.CUDA_VERSION >= constants.MIN_CUDA_VERSION else "CPU"
        self.shifts = 1
        self.clip_mode = "Rescale"
        self.jobs = 1
        self.overlap = 0.25

    def get(self, key):
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)

    def reset(self, key):
        setattr(self, key, "")

    def get_separate_settings(self):
        return shlex.split(
            f'{constants.OUTPUT_FORMATS[self.output_format]} '
            f'{"--mp3-bitrate " + self.mp3_bitrate if self.output_format == "MP3" else ""} '
            f'{constants.SPLIT_MODES[self.split_mode]} '
            f'-n {constants.MODELS[self.model]} '
            f'--shifts {self.shifts} '
            f'--clip-mode {constants.CLIP_MODES[self.clip_mode]} '
            f'--overlap {self.overlap} '
            f'-d {constants.DEVICES[self.device]} '
            f'-o "{self.output}" '
            f'-j {self.jobs} '
            f'"{self.source}"')

    def get_separate_text(self):
        return f'''
          Selected Audio File: {state.source}
          Files will be saved in: {state.output}
          Selected Model: {state.model}
          Split Mode: {state.split_mode}
          Output Format: {state.output_format} 
          Shifts set to: {state.shifts}
          Overlap set to: {state.overlap}
          Clip Mode: {state.clip_mode}
          Selected Device for Separation: {state.device} 
          '''


state = State()
