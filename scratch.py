## deepgram to audio with phonemes

import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)

load_dotenv()

AUDIO_URL = {
    "url": "https://us-nc-recordings.s3.amazonaws.com/recording_c75d9080f55e0fc4088d97a9ffc25571.mp3?digest=3f71809a7ff31d1489f1258d41e8f739"
}

API_KEY = os.getenv("DG_API_KEY")


# STEP 1 Create a Deepgram client using the API key
deepgram = DeepgramClient(API_KEY)

#STEP 2: Configure Deepgram options for audio analysis
options = PrerecordedOptions(
    model="phoneme",
    smart_format=True,
)

# STEP 3: Call the transcribe_url method with the audio payload and options
response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

# STEP 4: Print the response
print(response.to_json(indent=4))


## tinkering with JCM audio to phonemes code to use SDK

import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)

load_dotenv()

import map_cmu_to_ipa

API_KEY = os.getenv("DG_API_KEY")


def phonemes_from_url(audio_url):
    """
    # Deepgram returns a list of words, each word is a phoneme.
    # Each phoneme is from the CMU Prounouncing Dictionary
    # https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary

    Parameters:
    audio_url: url link for the audio to transcribe
    
    Return:
    string containing IPA phontic of the recording
    NOTE: due to limitations in Deepgram, this will not include stress
    marking or word boundaries
    """
    deepgram = DeepgramClient(API_KEY)

    options = PrerecordedOptions(
        model="phoneme",
        smart_format=True,
    )

    audio = {'url': audio_url}

    response = deepgram.listen.prerecorded.v("1").transcribe_url(audio, options)

    phonemes = response.to_dict()["results"]["channels"][0]['alternatives'][0]['words']
    
    
    for phoneme in phonemes:
        phoneme['type']= 'phone'
        phoneme["cmu"]= phoneme.pop("word")
        phoneme['ipa']= map_cmu_to_ipa.cmu_to_ipa(phoneme["cmu"])
    

    audio_ipa = ''.join(p['ipa'] for p in phonemes)
    
    return audio_ipa

## apply the deepgram transcription to testing set

import audio_to_phonemes

import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe


URL_DICT = {
    'testing': 'https://docs.google.com/spreadsheets/d/1BKHSTnqvgL29Y7Tn7cuuksIrOJTtIncayAZ9gy9pTw0/edit#gid=1255253900'
}

#load from gsheets
gc = gspread.oauth()

judging = gc.open_by_url(judgingSheetURL)
judgingTab = judging.worksheet(judgingTabName)
postProcessing = gc.open_by_url(ppSheetURL)
ppTab = postProcessing.worksheet(ppTabName)

# pull into dataframe
df = get_as_dataframe(judgingTab)
