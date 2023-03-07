import sys
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", action="store", help="Torrent file", required=True)
    parser.add_argument("-o", "--output", action="store", help="Filename to save to", required=True)

    args = parser.parse_args()

    torrent_filename = args.input
    output_filename = args.output