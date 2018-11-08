import numpy as np
import fingerprint
import warnings
import json
warnings.filterwarnings("ignore")
from hashlib import sha1
from pydub import AudioSegment


def work_audio(audiofile, filename):
    data = np.fromstring(audiofile._data, np.int16)

    channels = []
    for chn in xrange(audiofile.channels):
        channels.append(data[chn::audiofile.channels])

    fs = audiofile.frame_rate
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=fs)
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)

    return [result, fs]

