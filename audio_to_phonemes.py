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
    breakpoint()
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

