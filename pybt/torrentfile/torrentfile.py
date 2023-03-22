"""Classes and functions for working with torrent files"""
import hashlib

from pbencode import decode as bencode_decode
from pbencode import encode as bencode_encode


class TorrentFile:
    """Representation of a torrent file"""

    def __init__(self, announce, infohash, piecehashes, piecelength, length, name):
        self.announce = announce
        self.infohash = infohash
        self.piecehashes = piecehashes
        self.piecelength = piecelength
        self.length = length
        self.name = name

    announce: str
    infohash: bytes
    piecehashes: list
    piecelength: int
    length: int
    name: str


class BencodeInfo:
    """Tracking the download of a torrent"""

    def __init__(self, pieces, piecelength, length, name):
        self.pieces = pieces
        self.piecelength = piecelength
        self.length = length
        self.name = name

    pieces: bytes
    piecelength: int
    length: int
    name: str

    def hash(self):
        return hashlib.sha1(
            bencode_encode(
                {
                    b"length": self.length,
                    b"name": self.name.encode(),
                    b"piece length": self.piecelength,
                    b"pieces": self.pieces,
                }
            )
        ).digest()

    def split_piece_hashes(self):
        if len(self.pieces) % 20 != 0:
            raise Exception("Received malformed pieces of length %d", len(self.pieces))

        num_hashes = len(self.pieces) // 20

        hashes = []

        for i in range(num_hashes):
            hashes.append(self.pieces[i * 20 : (i + 1) * 20])
        return hashes


class BencodeTorrent:
    """Tracking the download of a torrent and how to tell peers"""

    def __init__(self, announce, info):
        self.announce = announce
        self.info = info

    announce: str
    info: BencodeInfo

    def torrent_file(self) -> TorrentFile:
        infohash = self.info.hash()

        piecehashes = self.info.split_piece_hashes()

        return TorrentFile(
            announce=self.announce,
            infohash=infohash,
            piecehashes=piecehashes,
            piecelength=self.info.piecelength,
            length=self.info.length,
            name=self.info.name,
        )


def open_file(path: str):
    """Attempt to open and read torrent file"""
    with open(path, "rb") as torrent_file:
        decoded = bencode_decode(torrent_file.read())

        return BencodeTorrent(
            announce=decoded[b"announce"].decode(),
            info=BencodeInfo(
                pieces=decoded[b"info"][b"pieces"],
                piecelength=decoded[b"info"][b"piece length"],
                length=decoded[b"info"][b"length"],
                name=decoded[b"info"][b"name"].decode(),
            ),
        ).torrent_file()
