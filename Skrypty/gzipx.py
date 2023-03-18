#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(prog='licek', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--dir", required=True, type=str, dest="dir",
                        help="Path to dir containg *.fastq.gz reads")
    return parser.parse_args()

def main(args):
    dir = Path(args.dir)
    if not dir.is_dir():
        raise FileNotFoundError("Given dir is not dir")


    if not all(x.name.endswith(".fastq") for x in dir.iterdir()):
        raise FileExistsError(
            f"Give files are not *.fastq: {list(filter(lambda x: not x.name.endswith('.fastq'), list(dir.iterdir())))}")

    for file1 in dir.iterdir():
        if not file1:
            continue

        output = subprocess.run(["gzip", str(file1)],
                                capture_output=True)

        print(output.stdout.decode())

if __name__ == "__main__":
    args = get_args()
    main(args)
