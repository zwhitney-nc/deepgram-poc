
import requests

#JCM probably should use the deepgram python sdk for this...
# https://developers.deepgram.com/sdks-tools/sdks/python-sdk/

# JCM authorization token should be in an environment variable

def call_deepgram_api_audio_to_text(audio_url):
    results= []
    apiUrl = 'https://api.deepgram.com/v1/listen?model=phoneme'
    headers = {
        'content-type': 'application/json', 
        'Authorization': 'Token 88be107363e973d14dbb58fcbc6ceb4d49a3df6c'
    }   
    payload = "{\"url\": \""+audio_url+"\"}"
    response = requests.post(apiUrl, data=payload, headers=headers)
    if hasattr(response, 'from_cache') and not response.from_cache:
        print("CACHE MISS",audio_url)
    if response.status_code  == 200:
        results= response.json()["results"]["channels"][0]['alternatives'][0]['words']
    else:
        print("WARNING - Deepgram API returned an error:", response.status_code);
    return results
