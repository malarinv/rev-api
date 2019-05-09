# -*- coding: utf-8 -*-

import os
import traceback

from configparser import SafeConfigParser
from configparser import Error as ConfigParserError

from rev.exceptions import SettingsFileNotFoundError


def cleanup_txt(source, dest):
    """
    Remove annotations (speaker, inaudible, ...)
    """
    #TODO
    """
    with open(dest, "wb") as txt_file:
        txt = '\n'.join(newparatextlist)\
            .replace('’', '\'')\
            .replace('‘', '\'')\
            .replace('“', '\"')\
            .replace('”', '\"')\
            .replace('…', '...')\
            .replace('Speaker 1:', '')\
            .replace('\t', '')
        txt_file.write(txt)
    """
    raise NotImplementedError("TODO: implement me!")


def read_settings_file(settings_file_path=None):
    """
    Read the settings.ini file located at the root of this project
    """
    # read settings
    if settings_file_path is None:
        settings_file_path = os.path.expanduser("~/.rev_settings")
    settings = None
    try:
        if os.path.exists(settings_file_path):
            settings = SafeConfigParser()
            settings.read(settings_file_path)
        else:
            raise SettingsFileNotFoundError(
                "Settings file not found, please copy settings.example to "
                f"{settings_file_path} and fill in your details")
    except ConfigParserError as e:
        print("Error parsing settings file: ")
        print(e)
        print(traceback.format_exc())
        raise e
    return settings
