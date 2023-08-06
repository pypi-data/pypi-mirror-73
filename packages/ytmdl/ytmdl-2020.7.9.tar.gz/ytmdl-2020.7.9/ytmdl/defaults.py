"""Contains the definition of class DEFAULT."""
from ytmdl import setupConfig
import os
from xdg.BaseDirectory import xdg_cache_home


class DEFAULT:
    """DEFAULT class contains value of different paths."""

    # The home dir
    HOME_DIR = os.path.expanduser('~')

    # the directory where songs will be saved
    SONG_DIR = setupConfig.GIVE_DEFAULT(1, 'SONG_DIR')

    # the temp directory where songs will be modded
    SONG_TEMP_DIR = os.path.join(xdg_cache_home, 'ytmdl')

    # The path to keep cover image
    COVER_IMG = os.path.join(SONG_TEMP_DIR, 'cover.jpg')

    # The song quality
    SONG_QUALITY = setupConfig.GIVE_DEFAULT(1, 'QUALITY')


class FORMAT:
    """
    Class to handle stuff related to the passed
    format.
    """
    valid_formats = [
        'mp3',
        'm4a'
    ]
