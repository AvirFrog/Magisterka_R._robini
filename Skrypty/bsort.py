#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(prog='licek', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--dir", required=True, type=str, dest="dir",
                        help="Path to dir containg *.fastq.gz reads")
    parser.add_argument("-s", "--save", required=True, type=str, dest="save", help="Path to empty dir used for save")
    parser.add_argument("-t", "--threads", required=False, default=1, type=int, dest="threads",
                        help="Number of threads to use")
    return parser.parse_args()


def main(args):
    dir, save = Path(args.dir), Path(args.save)
    if not dir.is_dir():
        raise FileNotFoundError("Given dir is not dir")
    if not save.exists():
        save.mkdir()

    if not all(x.name.endswith(".bam") for x in dir.iterdir()):
        raise FileExistsError(
            f"Give files are not *.bam: {list(filter(lambda x: not x.name.endswith('.bam'), list(dir.iterdir())))}")
    if len(list(save.iterdir())) > 0:
        raise FileExistsError("Save directory is not empty")


    for file1 in dir.iterdir():
        if not file1:
            continue
        outname = save / Path(file1.stem[:len(file1.stem)] + ".bam")
        output = subprocess.run(["samtools", "sort", str(file1), "-o", str(outname),
                                 "-@", str(args.threads)], capture_output=True)

        print(output.stderr.decode())



if __name__ == "__main__":
    args = get_args()
    main(args)
