#!/usr/bin/env python3
"""This is a simple command-line tool to send a file over the
network using UDP sockets.
"""

import argparse
import os
import socket
import sys

from typing import NoReturn


def __info(msg: str) -> None:
    """Log a message to stdout.

    :param msg: message to print
    :type msg: str
    """
    green: str = "[\033[0;32m"
    reset: str = "\033[0m]"
    print(f"{green}*{reset} {msg}")


def __die(msg: str) -> None:
    """Log an error to stderr.

    :param msg: message to print
    :type msg: str
    """
    red: str = "[\033[0;31m"
    reset: str = "\033[0m]"
    print(f"{red}*{reset} {msg}", file=sys.stderr)
    sys.exit(1)


class UDPFileStreamer:
    """Representation of our UDP capable file streamer."""
    ip: str
    port: int

    def __init__(self, target: str, port: int) -> None:
        """Create a new UDPFileStreamer object.

        :param target: IP or hostname of the target
        :type target: str
        :param port: port to send packets to
        :type port: int
        """
        self.ip = socket.gethostbyname(target)
        self.port = port

    def __call__(self, file_name: str, loop: bool) -> None:
        """Stream our file over a UDP socket.

        :param file_name: file to stream
        :type file_name: str
        :param loop: send the file in an infinite loop
        :type loop: bool
        """

        CHUNK_SIZE: int = 1024
        if not os.access(file_name, os.R_OK):
            __die(
                f"udp_streamer: {file_name} does not exist or is not readable."
            )
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect((self.ip, self.port))
                with open(file_name, "rb") as fp:
                    while True:
                        chunk: bytes = fp.read(CHUNK_SIZE)
                        if len(chunk) == 0:
                            if loop:
                                fp.seek(0)
                                continue
                            else:
                                break
                        sock.sendall(chunk)
        except socket.error as e:
            __die("error during socket handling: {e.strerror}")
        except OSError as e:
            __die(f"{os.path.basename(sys.argv[0])}: {e.strerror}")


def __main() -> None:
    """Parse arguments and stream our file."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="stream a file over a UDP connection."
    )
    parser.add_argument("file", help="file we want to send.")
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        required=True,
        help="IP address or hostname of the target.",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        help="port to send to file to.",
    )
    parser.add_argument(
        "-l",
        "--loop",
        action="store_true",
        default=False,
        help="send the file indefinitely in a loop (Default: False).",
    )
    args: argparse.Namespace = parser.parse_args()
    streamer: UDPFileStreamer = UDPFileStreamer(args.target, args.port)
    streamer(args.file, args.loop)


if __name__ == "__main__":
    __main()
