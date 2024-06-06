#ZAW will need to fix this to handle consonant clusters, sometimes we get those in the CMU
#ZAW can probably use the same behavior as in NCtoIPA

import warnings

# https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary
# https://github.com/margonaut/CMU-to-IPA-Converter/blob/master/cmu_ipa_mapping.rb
# https://en.wikipedia.org/wiki/ARPABET

#TODO: update these to match NCtoIPA characters
CMU_IPA_MAPPING = {
  "b": "b",
  "ch": "t͡ʃ",
  "d": "d",
  "dh": "ð",
  "f": "f",
  "g": "g",
  "hh": "h",
  "jh": "d͡ʒ",
  "k": "k",
  "l": "l",
  "m": "m",
  "n": "n",
  "ng": "ŋ",
  "p": "p",
  "r": "ɹ",
  "s": "s",
  "sh": "ʃ",
  "t": "t",
  "th": "θ",
  "v": "v",
  "w": "w",
  "y": "j",
  "z": "z",
  "zh": "ʒ",
  #
  # vowel sounds with stress marks 0, 1, 2...
  #
  "aa0": "ɑ",
  "aa1": "ɑ",
  "aa2": "ɑ",
  "ae0": "æ",
  "ae1": "æ",
  "ae2": "æ",
  "ah0": "ə",
  "ah1": "ʌ",
  "ah2": "ʌ",
  "ao0": "ɔ",
  "ao1": "ɔ",
  "ao2": "ɔ",
  "eh0": "ɛ",
  "eh1": "ɛ",
  "eh2": "ɛ",
  "er0": "ɚ",
  "er1": "ɝ",
  "er2": "ɝ",
  "ih0": "ɪ",
  "ih1": "ɪ",
  "ih2": "ɪ",
  "iy0": "i",
  "iy1": "i",
  "iy2": "i",
  "uh0": "ʊ",
  "uh1": "ʊ",
  "uh2": "ʊ",
  "uw0": "u",
  "uw1": "u",
  "uw2": "u",
  "aw0": "aʊ",
  "aw1": "aʊ",
  "aw2": "aʊ",
  "ay0": "aɪ",
  "ay1": "aɪ",
  "ay2": "aɪ",
  "ey0": "eɪ",
  "ey1": "eɪ",
  "ey2": "eɪ",
  "ow0": "oʊ",
  "ow1": "oʊ",
  "ow2": "oʊ",
  "oy0": "ɔɪ",
  "oy1": "ɔɪ",
  "oy2": "ɔɪ",

#
# JCM But Deepgram doesn't generate the stress marks,
# JCM so while I figure out how to add those back. 
#   

  "aa": "ɑ",
  "ae": "æ",
  "ah": "ə",
  "ao": "ɔ",
  "eh": "ɛ",
  "er": "ɚ",
  "ih": "ɪ",
  "iy": "i",
  "uh": "ʊ",
  "uw": "u",
  "aw": "aʊ",
  "ay": "aɪ",
  "ey": "eɪ",
  "ow": "oʊ",
  "oy": "ɔɪ",
}

def cmu_to_ipa(cmu):

    ipa = ''
    
    i = 0
    while i < len(cmu):
        longest_match = ""
        for key in CMU_IPA_MAPPING.keys():
            if cmu[i:i+len(key)] == key:
                if len(key) > len(longest_match):
                    longest_match = key

        if longest_match:
            ipa += CMU_IPA_MAPPING[longest_match]

            i += len(longest_match)
        else:
            warnings.warn(
                f"WARNING - possible invalid CMU, see substring {cmu[i:]}"
            )
            
            i += 1

    return ipa


#ZAW we probably don't need this anymore?
def cmu_to_ipa_substring(cmu):
    if cmu in CMU_IPA_MAPPING:
        ipa= CMU_IPA_MAPPING[cmu]
    else:
        ipa= "-unknown-"
        print(f"WARNING - '{cmu}' is not a CMU phoneme") # JCM need better warnings...
    return ipa
