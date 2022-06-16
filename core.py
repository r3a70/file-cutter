import sys
import asyncio
from main.cutter import Main


async def main(file_name: str, split_size: int) -> None:
    video = Main(file=file_name, split_size=split_size)
    video.split_counter()
    video.duration_file()

    task = asyncio.create_task(video.cutter_file())
    await task

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Example: python3 core.py file_name.ext split_size")
        exit(1)

    asyncio.run(main(sys.argv[1], int(sys.argv[2])))

