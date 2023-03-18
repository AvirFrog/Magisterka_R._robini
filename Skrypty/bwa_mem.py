#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(prog='bwa mem', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--index", required=True, default="rhizoglyphus_robini_genome_index", type=str, dest="index")
    parser.add_argument("-d", "--dir", required=True, type=str, dest="dir",
                        help="Path to dir containg *.fastq.gz reads")
    parser.add_argument("-s", "--save", required=True, type=str, dest="save", help="Path to empty dir used for save")
    parser.add_argument("-t", "--threads", required=False, default=1, type=int, dest="threads",
                        help="Number of threads to use")



    return parser.parse_args()


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def main(args):
    dir, save = Path(args.dir), Path(args.save)
    if not dir.is_dir():
        raise FileNotFoundError("Given dir is not dir")
    if not save.exists():
        save.mkdir()

    if not all(x.name.endswith(".fastq.gz") for x in dir.iterdir()):
        raise FileExistsError(
            f"Give files are not *.fastq.gz: {list(filter(lambda x: not x.name.endswith('.fastq.gz'), list(dir.iterdir())))}")
    if len(list(save.iterdir())) > 0:
        raise FileExistsError("Save directory is not empty")

    for file1, file2 in grouper(2, sorted(list(dir.iterdir()))):
        if not file1 or not file2:
            continue
        print(f"Mapping BWA MEM : {str(file1)}, {str(file2)}")
        outname = save / Path(file1.stem[:len(file1.stem) - 13] + ".sam")
        output = subprocess.run(["bwa", "mem", str(args.index), str(file1), str(file2), "-t", str(args.threads),
                                 "-o", str(outname)],
                                capture_output=True)

        print(output.stderr.decode())


if __name__ == "__main__":
    args = get_args()
    main(args)
