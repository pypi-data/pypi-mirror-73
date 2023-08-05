# -*- coding: utf-8 -*-
#
#   LulzCODE – simple way for good encoding some text.
#   Created by @LulzLoL231 at 4/27/20
#
from .coder import _EncodeBase32, _EncodeAlpha, _DecodeAlpha, _DecodeBase32, StringError


def encode(string) -> str:
    '''Return encoded in LulzCODE string from clear text.
    
    Args:
        string - clear text
    
    Returns:
        str'''
    _b32 = _EncodeBase32(string)
    _alpha = _EncodeAlpha(_b32)
    return _alpha


def decode(string) -> str:
    '''Return decoded clear text from string encoded in LulzCODE.
    
    Args:
        string - string encoded in LulzCODE
    
    Returns:
        str'''
    _b32 = _DecodeAlpha(string)
    _ct = _DecodeBase32(_b32)
    return _ct


def parseForTTS(string, separator='. ') -> str:
    '''Return parsed string for TextToSpeech Engine.
    
    Args:
        string    - string encoded in LulzCODE;
        separator - Separator between digits. (Default: ". ")
    
    Returns:
        str'''
    digs = []
    fs = True  # It's a first digit?
    frs = None  # first digit
    if len(string) % 2 != 0:
        raise StringError('String is not a LulzCODE encoded string.')
    for i in string:
        if fs:
            fs = False
            frs = i
        else:
            digs.append(frs+i)
            fs = True
    tts_string = ''
    for i in digs:
        tts_string += i + separator
    return tts_string


__version__ = '1.0'
__author__ = '@LulzLoL231'
__doc__ = 'LulzCODE - simple way for good encoding some text.'
