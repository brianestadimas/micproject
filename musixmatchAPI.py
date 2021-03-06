import requests
import urllib3
from bs4 import BeautifulSoup


def getAPIkey():
    return 'c29c3abf374df843346ed1bccb20f2ec'

"""
HOW TO MAKE THIS FUNCTION?
by Hanifa Arrumaisha (25/01/2017)

*   URL didapet dari link https://playground.musixmatch.com/
*   pilih API yang pengen diambil
*   klik expand operations dari API yg mau dipake
*   value dari URL adalah value yang ada di request URL di kotak warna biru tapi cuma sampe sebelum tanda tanya, 
    misal, aslinya request URL nya isinya 
    https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?format=jsonp&callback=callback&q_track=jatuh%20hati&q_artist=raisa&apikey=c29c3abf374df843346ed1bccb20f2ec
    tapi yang kita pake cuma sampe sebelum tanda tanya, berarti yang diambil
    https://api.musixmatch.com/ws/1.1/matcher.lyrics.get
*   PARAMS ikutin yang diminta di expand operations, ada list parameter apa aja yg harus dikirim
*   SELALU SERTAKAN APIKEY DI PARAMETER MESKIPUN TIDAK TERDAPAT DI EXPAND OPERATIONS
*   terakhir, tinggal gunain function ini di index.py yaaa tapi aku belum nyoba
"""

def getTracksWithSubLyrics(lyrics):
    URL = 'https://api.musixmatch.com/ws/1.1/track.search' 
    PARAMS = {
        'apikey' : getAPIkey(),
        'format' : 'json',
        'callback' : 'callback',
        'f_has_lyrics' : 1, #filter pencarian, nanti yg muncul cuma yg ada lyric nya
        'q_lyrics' : lyrics,
        's_track_rating' : 'desc', #rating track nya terurut dari yg paling tinggi ke rendah
        'page_size' : 100 # muncul 100 lyric yg ada sub lyric itu
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()
    return data.get('message').get("body").get("track_list")


def getTracksWithTrack(track):
    URL = 'https://api.musixmatch.com/ws/1.1/track.search' 
    PARAMS = {
        'apikey' : getAPIkey(),
        'format' : 'json',
        'callback' : 'callback',
        'f_has_lyrics' : 1,
        'q_track' : track,
        's_track_rating' : 'desc',
        'page_size' : 100 
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()

    return data.get('message').get("body").get("track_list")


def getTracksWithArtist(artist):
    URL = 'https://api.musixmatch.com/ws/1.1/track.search' 
    PARAMS = {
        'apikey': getAPIkey(),
        'format':'json',
        'callback':'callback',
        'q_artist':artist
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()
    return data.get('message').get("body").get("track_list")


def getTracksWithTrackArtist(track,artist):
    URL = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get' 
    PARAMS = {
        'apikey': getAPIkey(),
        'format':'json',
        'callback':'callback',
        'q_track':track,
        'q_artist':artist
    }

    r = requests.get(url = URL, params=PARAMS)

    data = r.json()
    print(data)
    return data.get('message').get("body").get("lyrics").get("lyrics_body")


### Menggunakan API BARU ####

def getFromKapanlagi(artist,track):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    track_split = track.replace(" ", "-")
    str_builder = ""

    URL = 'http://lirik.kapanlagi.com/artis/' + artist + '/' + track_split 
    # http = urllib3.PoolManager()
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, "html.parser")

    for elem in soup.find_all("span",class_="lirik_line") :
        str_builder = str_builder + elem.get_text()+'\n'
    
    return str_builder

def getFromMetro(artist,track):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    track_split = track.replace(" ", "-")
    artist_split = artist.replace(" ", "-")
    str_builder = ""

    URL = 'http://www.metrolyrics.com/' + track_split + '-lyrics-' + artist_split 
    # http = urllib3.PoolManager()
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, "html.parser")

    for elem in soup.find_all("p",class_="verse") :
        str_builder = str_builder + elem.get_text()+'\n'
    
    return str_builder

print(getFromMetro("ed sheeran","perfect"))


def getLyricsByTrackArtist(artist,track):
    track_split = track.replace(" ", "-")
    artist_split = artist.replace(" ","-")

    URL = 'https://genius.com/' + artist_split + '-' + track_split+'-lyrics'
    http = urllib3.PoolManager()
    response = http.request('GET', URL)
    soup = BeautifulSoup(response.data,'html.parser')
    lyrics_tmp = soup.find_all(attrs={"class": "lyrics"}) #lyrics isinya masih banyak tag ga penting

    if len(lyrics_tmp)==0:
        lyrics = getFromKapanlagi(artist, track);
        if len(lyrics)==0:
            lyrics = getFromMetro(artist, track);
        else :
            lyrics = "tidak ada"

    else:
        lyrics = lyrics_tmp[0].get_text()

    return lyrics

# print(getLyricsByTrackArtist('krisdayanti', 'menghitung hari'))



# def searchLyrics(track):
#     URL = 'https://genius.com/search?q=' + track
#     http = urllib3.PoolManager()
#     response = http.request('GET', URL)
#     soup = BeautifulSoup(response.data,'html.parser')
#     return soup
    
# # print(searchLyrics('imagination'))


#yang baru

# def getLyricsByTrackArtist(track,artist):
#     URL = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect' 
#     PARAMS = {
#         'artist':artist,
#         'song':track
#     }

#     r = requests.get(url = URL, params=PARAMS)

#     tree = ElementTree.fromstring(r.content)

#     # if the server sent a Gzip or Deflate compressed response, decompress
#     # as we read the raw stream:
#     response.raw.decode_content = True

#     events = ElementTree.iterparse(response.raw)

#     for event, elem in events:
#         tag = elem.tag
#         value = elem.text
#         if tag == 'Lyric':
#             return value

    # return lyric
    # data = r.json()
    # print(data)
    # return data.get('message').get("body").get("lyrics").get("lyrics_body")



# kalau mau coba
