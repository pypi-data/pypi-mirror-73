"""
Basic Text-To-Speech tools are stored here
"""

import os
import tempfile
from playsound import playsound
from logging import getLogger
from gtts import gTTS
from requests.exceptions import HTTPError
from kolibri import settings
log = getLogger(__name__)

def init():
    """ Initialize the pygame mixer """



def play_mp3(file_name, blocking=False):
    """Plays a local MP3 file

    :param file_name: top-level file name (e.g. hello.mp3)
    :param file_path: directory containing file ('media' folder by default)
    :param blocking: if false, play mp3 in background
    """
    if ".mp3" in file_name:
        playsound(file_name, block=blocking)


def speak(phrase, cache=False, filename='default.wav', show_text=True, language='en'):
    """Speaks a given text phrase

    :param phrase: text string to speak
    :param cache: if True, store .mp3 in 'media/responses'
    :param filename: filename if cached
    :param show_text: if True, store .mp3 in 'media/responses'
    :param cache: if True, store .mp3 in 'media/responses'
    """
    if show_text:
        log.info(phrase)
    if not settings.USE_TTS:
        log.info('SPOKEN: ' + phrase)
        return

    try:
        tts = gTTS(text=phrase, lang=language)

        if not cache:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3',
                                             delete=False) as f:
                tts.write_to_fp(f)

            play_mp3(f.name)
            os.remove(f.name)
        else:

            tts.save(filename)
            log.info('Saved to: ' + filename)

    except HTTPError as e:
        log.error('Google TTS might not be updated: ' + str(e))
    except Exception as e:
        log.error('Unknown Google TTS issue: ' + str(e))
