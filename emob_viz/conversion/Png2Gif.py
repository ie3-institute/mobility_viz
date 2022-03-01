import os.path
from pathlib import Path

import imageio


class Png2Gif:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def build_gif(self, file_name: str, fps: int = 2):
        input_files = list(Path(self.input_dir).glob('*.png'))
        frames = [imageio.imread(img) for img in input_files]
        imageio.mimwrite(os.path.join(self.output_dir, file_name + ".gif"), frames, fps=fps)
