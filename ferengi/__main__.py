import argparse
import itertools
from typing import BinaryIO
from pathlib import Path

JPEG_HEADR = bytes.fromhex("ffd8ffe1")


def jpeg_finder(image: BinaryIO, destination, cluster_size=32768, filename_fmt="pic_{i}.JPG"):
    jpeg_file = None
    counter = itertools.count()
    while cluster := image.read(cluster_size):
        if JPEG_HEADR in cluster:
            if jpeg_file:
                yield jpeg_file.name
            jpeg_file = open(destination / filename_fmt.format(i=next(counter)), 'wb')
        if jpeg_file:
            jpeg_file.write(cluster)
    if jpeg_file:
        jpeg_file.close()


def main():
    parser = argparse.ArgumentParser(
        prog='ferengi',
        description='parse image of SD card, and extracts jpeg images out of it')
    parser.add_argument('image_filename', type=argparse.FileType('rb'))
    parser.add_argument('-d', '--destination', type=Path, default=Path('.'))
    parser.add_argument('-o', '--output-format', default='pic_{i}.JPG')
    args = parser.parse_args()

    if not args.destination.exists():
        args.destination.mkdir(parents=True)

    for jpeg_filename in jpeg_finder(image=args.image_filename,
                                     destination=args.destination,
                                     filename_fmt=args.output_format):
        print(jpeg_filename)


if __name__ == "__main__":
    main()
