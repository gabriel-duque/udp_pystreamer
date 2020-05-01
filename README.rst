UDP PyStreamer
==============

Introduction
------------

``udp_pystreamer`` is a simple script to stream a file over UDP, possibly
in an infinite loop. This script was mainly created to test other
software that need to receive a stream over a UDP connection.

Installation
------------

You can install the script by running:
::

    $ python3 setup.py install

This installs the script as ``udp_pystreamer``.

Usage
-----

The usage for the tool is as follows:
::

    usage: udp_pystreamer [-h] -t TARGET -p PORT [-l] file
    
    stream a file over a UDP connection
    
    positional arguments:
      file                  file we want to send
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TARGET, --target TARGET
                            IP address or hostname of the target
      -p PORT, --port PORT  port to send to file to
      -l, --loop            send the file indefinitely in a loop (Default: False)

Documentation
-------------

Instead of using this project as a script, you can include
``udp_pystreamer`` as a module in which case you can directly access the
``UDPFileStreamer`` class.

To build the **small** documentation about this class, you can run:
::

    $ python3 setup.py build_sphinx

The resulting documentation can be found in the ``docs/build`` directory.

The documentation for this project is also available `online`_.

.. _online: https://udp-pystreamer.zuh0.com
