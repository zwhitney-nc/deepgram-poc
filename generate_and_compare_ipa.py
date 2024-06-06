from audio_to_phonemes import phonemes_from_url

import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from phon_utils.phon_utils.NCtoIPA import convert_NC_to_IPA

import textdistance
import re

URL_DICT = {
    'testing': 'https://docs.google.com/spreadsheets/d/1BKHSTnqvgL29Y7Tn7cuuksIrOJTtIncayAZ9gy9pTw0/edit#gid=1255253900',
}

#TODO: break this out into separate functions for NC and DG
def generate_nc_ipa(sheet_url = URL_DICT['testing'],
                    tabName = 'Deepgram Testing',
                    NCPhonCol = 'Namecoach Phonetic',
                    NCIPACol = 'Namecoach IPA',
                    ):

    #load from gsheets
    gc = gspread.oauth()

    testing = gc.open_by_url(sheet_url)
    testTab = testing.worksheet(tabName)

    # pull into dataframe
    df = get_as_dataframe(testTab)
    df.dropna(axis=0, how='all', inplace=True)
    #df.drop(columns=df.loc[:, 'Unnamed: 10':], inplace=True)

    # convert existing Namecoach phonetic to IPA
    df[NCIPACol] = df[NCPhonCol].apply(
        lambda x: convert_NC_to_IPA(x)
    )

    set_with_dataframe(testTab, df, row=2, include_column_header=False)

    
    return df

def generate_dg_ipa(sheet_url = URL_DICT['testing'],
                    tabName = 'Deepgram Testing',
                    sourceCol = 'Namecoach Source',
                    dgIPACol = 'Deepgram IPA - raw',
                    ):

    #load from gsheets
    gc = gspread.oauth()

    testing = gc.open_by_url(sheet_url)
    testTab = testing.worksheet(tabName)

    # pull into dataframe
    df = get_as_dataframe(testTab)
    df.dropna(axis=0, how='all', inplace=True)

    # convert each URL to IPA with deepgram
    df[dgIPACol] = df[sourceCol].apply(
        lambda x: phonemes_from_url(x)
    )

    set_with_dataframe(testTab, df, row=2, include_column_header=False)

    
    return df

    
def compare_ipas(sheet_url = URL_DICT['testing'],
                 tabName = 'Deepgram Testing',
                 col1 = 'Namecoach IPA',
                 col2 = 'Deepgram IPA - cleaned',
                 resultCol = 'Text Distance between IPAs',
                 ignoreStressAndSyls = False,
                 ):

    #load from gsheets
    gc = gspread.oauth()

    testing = gc.open_by_url(sheet_url)
    testTab = testing.worksheet(tabName)

    # pull into dataframe
    df = get_as_dataframe(testTab)
    df.dropna(axis=0, how='all', inplace=True)
    df = df.fillna('').infer_objects(copy=False)
    
    if ignoreStressAndSyls:
        breakpoint()
        col1_temp = col1 + '_noStressNoSyl'
        df[col1_temp] = df[col1]
        df[col1_temp] = df[col1_temp].str.replace('[.ˈˌ]', '', regex=True)
        df[col1_temp] = df[col1_temp].str.replace('ʌ', 'ə')

        df[resultCol] = df.apply(
            lambda x: textdistance.levenshtein(x[col1_temp], x[col2]),
            axis = 1,
        )
        
        df.drop(columns=col1_temp, inplace=True)
        
    else:
        df[resultCol] = df.apply(
            lambda x: textdistance.levenshtein(x[col1], x[col2]),
            axis = 1,
        )

    
    set_with_dataframe(testTab, df, row = 2, include_column_header=False)
                       
    return df

"""if __name__ == '__main__':
    main()"""


