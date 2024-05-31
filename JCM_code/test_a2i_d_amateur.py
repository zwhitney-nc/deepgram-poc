
#
# A2I Test (Amateur Audio) 
# for a name, put the corresponding set of amatuer audio (from hedb) through deepgram
# to get the IPA, then find the most frequent longest common substring of IPA...
#

import sys
sys.path.append('pipe')

import audio_to_phonemes_deepgram


#
# https://docs.google.com/spreadsheets/d/1fHQPZZKc-oMKBuMg8lFakSt394eP1IBSk4z48gYQIwo/edit#gid=155631742
#

#urls= [
#"https://us-nc-recordings.s3.amazonaws.com/recording_79bc56c40cd5d1e497f65b61d9e1a57c.mp3",
#"https://us-nc-recordings.s3.amazonaws.com/recording_1060ac1ef683b4462554ee79f4165d69.mp3",
#"https://us-nc-recordings.s3.amazonaws.com/recording_033b6cc60be46c8fe0da09bbcbf9feb8.mp3"
#]

import requests_cache
requests_cache.install_cache(
    expire_after=requests_cache.NEVER_EXPIRE,
    backend='filesystem',
    allowable_methods=['GET', 'POST']
    )

# Aaron
urls= ["https://us-nc-recordings.s3.amazonaws.com/recording_b6b5ecc7afa7220e2dc3f0fad07e8263.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_845bb8ef1dbfa38a31eccf64288e295c.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_2c4c534b816750c4fe1a855dc9899fd0.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_033b6cc60be46c8fe0da09bbcbf9feb8.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_79bc56c40cd5d1e497f65b61d9e1a57c.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_c704d8b3586c9f910c65bf9127a05459.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_51c113a4c6c9f248a88e9ef6edbdb480.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_7429228aa5b6fe7369b610f75676a806.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_0255b621372f2a631a357433ce364513.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_01f53411ad42ce13b9a6842794e8e193.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_cbc02bb935b468aff136b7bc50f0f7f6.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_2994ea2f8ff92dbb0941d22789beb228.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_4afe458c39f3aea3365a95eb9a1853bd.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_bfbcfca3eb55439c7945f93cfc7b844f.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_f10e84f2a653eaa1727cc0d298e43de0.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_36790f95008f937322a17f4c4f47f73a.mp3", "https://us-nc-recordings.s3.amazonaws.com/7156_9049_1267C.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_e9c94b59520ea526e2b459d471ba820b.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_db85dcee1499e6f5560fa966f0932c01.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_29bccb0e3b28f6093c1dbce625db2023.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_020a98316651977773892a955493a4ca.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_14ef945344eb92e9be3b3ef0685f5200.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_d6a686c1dc0b36b68491e2f41267feba.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_088109f2e368405bd843ce51690ea8f8.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_f1731619f48621efb47e5415ee1a61fe.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_be92b2e953a30e9aab73b4799558c7bf.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_d0544c05daa01d494c7ca578aabc21e4.mp3", "https://us-nc-recordings.s3.amazonaws.com/14607_21662_233E1.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_bbaf7107dc58eb40e5045066d208cf8f.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_38590b31fc48fe36d253208b6be0f6dd.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_ddecf14bdbf9a7a912f6b5dcb667d051.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_21e81ab80edd1a0d8a41c0498a909743.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_ff3de914b52e7bb131da1deb708ef3e1.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_1a77134db61268d9c1113aaf1b2b2492.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_632883c29bd0b689a126cbaa97fef86d.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_27378972665eddd011950611a89e6677.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_e54f7268ac0722e4aebcc35f7803d00b.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_1060ac1ef683b4462554ee79f4165d69.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_3a4e326037675fd5c7fa016ed2486711.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_b579ad3a1c2cc96821f784232802a7c1.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_55a54c39b4f99b260fa43b1b7741beae.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_18d29e8ca84dc0c768fe986ed8094aa9.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_61c4e129df0e4d194db43304dabba74e.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_56f47cba7b4b133c0bf8332e3ebb9300.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_40dbb2b07fbe82b8a285897b3bce6059.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_ff6592e38826f0569a86032fee9902f3.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_ceeac588d378f4400510d412d614b4ed.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_e2baa844d25fa040ef8a96cf6c338c78.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_d5ee0fdeda32f4df6c128bd5a1a22762.mp3", "https://us-nc-recordings.s3.amazonaws.com/recording_50a8168bf6f3c499b5d9333319b21ac9.mp3"]

ipas= []
for url in urls:
    audio= {'url': url}
    phonemes= audio_to_phonemes_deepgram.phonemes(audio)
    # JCM skip empasis and break detection
    ipa= "".join(p["ipa"] for p in phonemes)
    print('full ipa:',ipa)
    ipas.append(ipa)

# JCM find an easier to understand implementation of Suffix Tree

# JCM could use a Trie instead
# https://github.com/google/pygtrie

# build a suffix tree
import suffix_tree 
t= suffix_tree.Tree()
for ipa in ipas:
    t.add(ipa,ipa) # (id,ipa) JCM what's the id for?

c_s= t.common_substrings()
# JCM the return from this function is strange...
# JCM [(k, length, path)]
# JCM is it all paths?
# JCM have to use frequency to find the most common substring 
f= {}
for k, length, path in c_s:
    #print('longest substring ipa (candidate):',k, length, path)
    s= str(path).replace(" ","")
    if s in f:
        f[s] += 1
    else:
        f[s] = 1
#print(f)
l= sorted(f.items(), key=lambda x: x[1], reverse=True)
if len(l)==0:
    print('lonsest substring ipa: Warning - None')
elif len(l)==1:
    print('longest substring ipa:',l[0])
else:
    print('longest substring ipa: Warning - Many')
    print('longest substrings ipa:',1)
    print('longest substring ipa:',l[0])

# JCM once we have the longest common substring (LCS)...
# JCM for each audio select the audio segment for the LCS...
# JCM find the stress from the pitch/volume
# JCM find the breaks from the intensity
# JCM generate ipa with empahsis and syllables
# JCM find the most common ipa
  