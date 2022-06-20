import asyncio
import subprocess

import ffmpeg
import math
import os
from pathlib import Path


def time_formatter(duration: int) -> str:
    """
    :param duration: (duration of file for formatting to this 00:00:00 type)
    :return: string of time in this format 00:00:00
    """
    if duration >= 3600:
        return f"{duration // 60 // 60}:00:00"
    if duration == 0:
        return "00:00:00"

    return f"00:{duration // 60}:00"


class Main:
    """
    split file by size
    """
    def __init__(self, file: str, split_size: int, file_duration: int):
        """
        :param file: (file_name) if conditions incorrect, return false
        :param split_size: (file_size for split in MB) if conditions incorrect, return error text
        """
        self.file = file
        self.file_name = os.path.join(Path(__file__).resolve().parent.parent.parent, file)
        self.split_size = split_size
        self.file_duration = file_duration
        self.split_count: int = 0
        self.file_size: int = 0
        self.directory: str = ""

    def split_counter(self) -> tuple:
        """
        :return: Error message
        """
        self.file_size = int(f"{os.stat(self.file_name).st_size / float(1 << 20):.0f}")
        self.directory = self.file_name+"_list"

        if self.file_size < self.split_size:
            return False, f"File size is smaller than {self.split_size}MB, so can't cut it"
        else:
            self.split_count = int(math.ceil(self.file_size / self.split_size))

    def duration_file(self) -> None:
        """
        :return: None
        """
        self.file_duration = int(math.ceil(self.file_duration / self.split_count))

    def initialize_command(self, start: int, end: int, count: int, directory: str) -> str:
        """
        :param start: (start time to cut)
        :param end: (end time to cut)
        :param count: (integer number of which times for iterate)
        :param directory: (the directory for saving output file)
        :return: return command for running ffmpeg
        """
        return f"ffmpeg -ss {time_formatter(start)} -i {self.file_name} -t {time_formatter(end)} -c:v copy -c:a copy " \
               f"{directory}/{count}__{self.file}"

    async def cutter_file(self) -> None:
        """
        :return: None
        """
        os.system(f"mkdir {self.file_name}_list")
        for i in range(self.split_count+1):
            process = await asyncio.create_subprocess_shell(
                self.initialize_command(i*1*self.file_duration,
                                        self.file_duration,
                                        i,
                                        self.directory),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            await process.communicate()


class Information:

    def __init__(self, file_name):
        self.file_name = file_name
        self.load = ffmpeg.probe(self.file_name)

    def duration(self) -> int:
        return int(float(self.load['streams'][-1]['duration'] if self.load else 0))

