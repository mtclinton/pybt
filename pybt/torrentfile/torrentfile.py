"""Classes and functions for working with torrent files"""
from pbencode import decode as bencode_decode


class TorrentFile:
    """Representation of a torrent file"""

    announce: str
    infohash: bytes
    piecehashes: list
    piecelength: int
    length: int
    name: str


class BencodeInfo:
    """Tracking the download of a torrent"""

    pieces: bytes
    piecelength: int
    length: int
    name: str


class BencodeTorrent:
    """Tracking the download of a torrent and how to tell peers"""

    announce: str
    info: BencodeInfo


def open_file(path: str):
    """Attempt to open and read torrent file"""
    with open(path, "rb") as torrent_file:
        decoded = bencode_decode(torrent_file.read())
        return decoded
