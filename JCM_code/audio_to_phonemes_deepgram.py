
import deepgram
import map_cmu_to_ipa


def phonemes(audio):
    #
    # Deepgram returns a list of words, each word is a phoneme.
    # Each phoneme is from the CMU Prounouncing Dictionary
    # https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary
    #
    phonemes= deepgram.call_deepgram_api_audio_to_text(audio['url'])
    #
    for phoneme in phonemes:
        phoneme['type']= 'phone'
        phoneme["cmu"]= phoneme.pop("word")
        phoneme['ipa']= map_cmu_to_ipa.cmu_to_ipa(phoneme["cmu"])
    #
    return phonemes