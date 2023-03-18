#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(prog='auto trimmomatic', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--dir", required=True, type=str, dest="dir",
                        help="Path to dir containg *.fastq.gz reads")
    parser.add_argument("-s", "--save", required=True, type=str, dest="save", help="Path to empty dir used for save")
    parser.add_argument("-a", "--adapters", required=True, type=str, dest="adapters", help="Path to adapter file")
    parser.add_argument("-t", "--threads", required=False, default=1, type=int, dest="threads",
                        help="Number of threads to use")

    #parser.add_argument("-c", "--clip", required=False, default="2:30:10", type=str, dest="clip",
    #                    help="Uzupełnij")#TODO: uzupełnij opis
    parser.add_argument("-l", "--leading", required=False, default="30", type=str, dest="leading",
                        help="Uzupełnij")#TODO: uzupełnij opis
    parser.add_argument("--tr", "--trailing", required=False, default="30", type=str, dest="trailing",
                        help="Uzupełnij")#TODO: uzupełnij opis
    parser.add_argument("-m", "--minlen", required=False, default="50", type=str, dest="minlen",
                        help="Uzupełnij")#TODO: uzupełnij opis
    return parser.parse_args()


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def main(args):
    dir, save, adapters = Path(args.dir), Path(args.save), Path(args.adapters)
    if not dir.is_dir():
        raise FileNotFoundError("Given dir is not dir")
    if not save.exists():
        save.mkdir()
    if not adapters.is_file():
        raise FileNotFoundError("File not found")

    if not all(x.name.endswith(".fastq.gz") for x in dir.iterdir()):
        raise FileExistsError(
            f"Give files are not *.fastq.gz: {list(filter(lambda x: not x.name.endswith('.fastq.gz'), list(dir.iterdir())))}")
    if len(list(save.iterdir())) > 0:
        raise FileExistsError("Save directory is not empty")

    for file1, file2 in grouper(2, sorted(list(dir.iterdir()))):
        if not file1 or not file2:
            continue
        outname = save / Path(file1.stem[:len(file1.stem) - 8]+ ".fastq.gz")# TODO: .fastq.gz
        print(f"Trimming PE files: {str(file1)}, {str(file2)}")
        output = subprocess.run(["trimmomatic", "PE", "-threads", str(args.threads),
                                 str(file1), str(file2), "-baseout", str(outname),
                                 f"ILLUMINACLIP:{str(adapters)}:2:30:10", f"LEADING:{str(args.leading)}",
                                 f"TRAILING:{str(args.trailing)}", f"SLIDINGWINDOW:4:15", f"MINLEN:{str(args.minlen)}"],
                                capture_output=True)

        print(output.stderr.decode())



if __name__ == "__main__":
    args = get_args()
    main(args)
