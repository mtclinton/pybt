"""Classes and functions for working with torrent files"""
from pbencode import decode as bencode_decode


def open_file(path: str):
    """Attempt to open and read torrent file"""
    with open(path, "rb") as torrent_file:
        decoded = bencode_decode(torrent_file.read())
        return decoded
