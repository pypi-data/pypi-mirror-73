# -*- coding: utf-8 -*-
#
#   LulzCODE Module: coder – utils for encoding & decoding.
#   Created by @LulzLoL231 at 4/27/20
#
from base64 import b32encode, b32decode


ALPHA_BET_DECODE = {'00': 'Z', '11': 'A', '12': 'F', '13': 'K', '14': 'P', '15': 'U',
                    '21': 'B', '22': 'G', '23': 'L', '24': 'Q', '25': 'V', '31': 'C',
                    '32': 'H', '33': 'M', '34': 'R', '35': 'W', '41': 'D', '42': 'I',
                    '43': 'N', '44': 'S', '45': 'X', '51': 'E', '52': 'J', '53': 'O',
                    '54': 'T', '55': 'Y', '16': '='}
ALPHA_BET_ENCODE = {'Z': '00', 'A': '11', 'F': '12', 'K': '13', 'P': '14', 'U': '15',
                    'B': '21', 'G': '22', 'L': '23', 'Q': '24', 'V': '25', 'C': '31',
                    'H': '32', 'M': '33', 'R': '34', 'W': '35', 'D': '41', 'I': '42',
                    'N': '43', 'S': '44', 'X': '45', 'E': '51', 'J': '52', 'O': '53',
                    'T': '54', 'Y': '55', '=': '16'}
ALPHA_DIG_DECODE = {'99': '0', '66': '1', '67': '4', '68': '7',
                    '76': '2', '77': '5', '78': '8', '86': '3', '87': '6', '88': '9'}
ALPHA_DIG_ENCODE = {'0': '99', '1': '66', '4': '67', '7': '68',
                    '2': '76', '5': '77', '8': '78', '3': '86', '6': '87', '9': '88'}


class AlphaEncodeError(Exception):
    pass


class AlphaDecodeError(Exception):
    pass


class StringError(Exception):
    pass


def _EncodeBase32(string) -> str:
    '''Return string encoded in base32.
    
    Args:
        string - any string.
    
    Returns:
        str'''
    if type(string) != bytes:
        string = string.encode()
    return b32encode(string).decode()


def _DecodeBase32(string) -> str:
    '''Return string decoded with base32.
    
    Args:
        string - any encoded in base32 string.
    
    Returns:
        str'''
    if type(string) != bytes:
        string = string.encode()
    return b32decode(string).decode()


def _EncodeAlpha(ordered_text) -> str:
    '''Return string encoded in Alpha language.
    
    Args:
        ordered_text - ordered string.
    
    Returns:
        str
    
    Raises:
        AlphaEncodeError - if symbol cannot be found in ALPHA_ENCODE_BET or ALPHA_ENCODE_DIG.'''
    string = ''
    for i in ordered_text:
        try:
            string += ALPHA_BET_ENCODE[i]
        except KeyError:
            try:
                string += ALPHA_DIG_ENCODE[i]
            except KeyError:
                raise AlphaEncodeError(f'Can\'t encode symbol "{str(i)}" in Alpha language.')
    return string


def _DecodeAlpha(alpha_string) -> str:
    '''Return decoded string from Alpha language.
    
    Args:
        alpha_string - string encoded in Alpha language.
    
    Returns:
        str
    
    Raises:
        AlphaDecodeError - if symbol cannot be found in ALPHA_DECODE_BET or ALPHA_DECODE_DIG.'''
    string = ''
    fs = True
    frs = None
    alpha_list = []
    while int(len(alpha_string) / 2) != len(alpha_list):
        for i in alpha_string:
            if fs:
                frs = i
                fs = False
            else:
                alpha_list.append(frs+i)
                fs = True
    for i in alpha_list:
        try:
            string += ALPHA_BET_DECODE[i]
        except KeyError:
            try:
                string += ALPHA_DIG_DECODE[i]
            except KeyError:
                raise AlphaDecodeError(
                    f'Can\'t decode symbol "{str(i)}" in Alpha language.')
    return string
