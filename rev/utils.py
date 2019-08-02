# -*- coding: utf-8 -*-

import os
import string
import traceback
from configparser import SafeConfigParser
from configparser import Error as ConfigParserError
from datetime import datetime, timedelta

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
    Read the settings file
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


def _to_delta(string):
    """ Convert Rev delta string, to seconds """
    t = datetime.strptime(string, "%H:%M:%S,%f")
    return timedelta(
        hours=t.hour,
        minutes=t.minute,
        seconds=t.second,
        microseconds=t.microsecond).total_seconds()


def json_to_df(content):
    """ Parse JSON response, and convert to pandas df """
    import pandas as pd

    all_elements = []
    for m in content['monologues']:
        for e in m['elements']:
            if 'timestamp' in e and 'end_timestamp' in e:
                onset = _to_delta(e.pop('timestamp'))
                duration = _to_delta(e.pop('end_timestamp')) - onset
                e.pop('type')
                e['onset'] = onset
                e['duration'] = duration
                e['speaker'] = m['speaker']
                e['text'] = e.pop('value').translate(str.maketrans('', '', string.punctuation)).lower()
                all_elements.append(e)
    return pd.DataFrame(all_elements)
