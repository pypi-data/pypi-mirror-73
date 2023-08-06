import sys

from pathlib import Path

from d64 import DiskImage, ProgramFile

with DiskImage(Path(sys.argv[1])) as image:
    with image.path(sys.argv[2]).open() as f:
        p = ProgramFile(f)

for line in p.dump():
    print(line)
