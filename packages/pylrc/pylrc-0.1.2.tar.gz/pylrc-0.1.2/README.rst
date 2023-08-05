=====
PyLRC
=====
.. image:: https://img.shields.io/pypi/v/pylrc.svg
.. image:: https://img.shields.io/pypi/dm/pylrc.svg
.. image:: https://img.shields.io/github/license/doakey3/pylrc.svg

A python library for parsing and converting .lrc files

Usage
=====

.. code:: python

    import pylrc
    
    lrc_file = open('example.lrc')
    lrc_string = ''.join(lrc_file.readlines())
    lrc_file.close()
    
    subs = pylrc.parse(lrc_string)
    for sub in subs:
        sub.shift(minutes=1, seconds=13, milliseconds=325) # offset by 01:13.325
    
    srt = subs.toSRT() # convert lrc to srt string
    
    lrc_string = subs.toLRC() # convert to lrc string
    
Installation
============

.. code::

    sudo pip install pylrc
    
    
    
