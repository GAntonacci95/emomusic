import base64
import json
import os
import numpy as np
import requests
import time
from flask import Flask, redirect, render_template, request, url_for, session

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

# azure env vars
api_key_azure = os.environ['AZURE_APIKEY']
uri_azure = os.environ['AZURE_URI']

# default playlist
playlist_id_default = "rkvm1mxp9hjxu6qcenz93k9n7"

# spotify env vars
client_id_spotify = os.environ['SPOTIFY_ID']
redirect_uri_spotify = 'http://localhost:5000/callback'
state_spotify = 'lakdo'
scopes_spotify = 'user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative'

# spotify auth url
auth_url = 'https://accounts.spotify.com/authorize'
auth_url += '?response_type=token'
auth_url += '&client_id=' + quote(client_id_spotify)
auth_url += '&scope=' + quote(scopes_spotify)
auth_url += '&redirect_uri=' + quote(redirect_uri_spotify, safe='')
auth_url += '&state=' + quote(state_spotify)

# flask server run
app = Flask(__name__)
app.secret_key = os.environ['SESSION_SECRET']
app.debug = True

@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "GET"):
        # render template
        return render_template("main.html", url=auth_url)

    return redirect(url_for('index'))

# callback for spotify login
@app.route("/callback", methods=["GET"])
def callback():
    if (request.method == "GET"):
        # render template
        return render_template("callback.html")

# return chords progression in midi format
@app.route("/emotion", methods=["POST"])
def emotion():
    if (request.method == "POST"):
        # check request value
        assert request.values.get('token'), request.values.get('photo')
        # store token
        session['token'] = request.values.get('token')
        # get picture
        photo_base64 = request.values.get("photo")
        # remove base64 header
        photo_base64 = photo_base64[23:]
        # convert to bytes
        photo_byte = base64.b64decode(photo_base64)

        # check active device
        if (get_device()):
            # assert required values
            assert uri_azure, api_key_azure
            assert photo_byte
            # headers parameters
            headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': api_key_azure
            }
            # post parameters
            params = {
                'returnFaceId': 'true',
                'returnFaceLandmarks': 'false',
                'returnFaceAttributes': 'emotion',
            }
            # get response from azure
            response = requests.post(uri_azure, params=params, headers=headers, data=photo_byte)
            response_json = response.json()
            # check azure response and understand emotion
            assert response_json[0]
            # save smile and emotions results
            emotions = response_json[0]['faceAttributes']['emotion']
            # get tracks descriptors of user
            tracks_descriptors = get_tracks()

            choose_track(emotions, tracks_descriptors)
            return json.dumps({'success': True}), 200, {
                'ContentType': 'application/json'}

        else:
            return json.dumps({'success': False, 'message': 'No active device available playing music'}), 200, {
                'ContentType': 'application/json'}

# https://developer.spotify.com/console/get-users-available-devices/#
# GET METHOD : https://api.spotify.com/v1/me/player/devices
# SCOPE : user-read-playback-state
# RESPONSE :
#     {   "devices": [
#         {
#           "id": "********",
#           "is_active": true,
#           "is_private_session": false,
#           "is_restricted": false,
#             ...
#         }, {
#           "id": "********",
#           "is_active": false,
#             ...
#         } ]
#     }
def get_device():
    headers = {"Authorization": "Bearer %s" %session['token']}
    # search active devices
    # create request
    req = requests.get(headers=headers, url="https://api.spotify.com/v1/me/player/devices")
    # check required values
    assert req.status_code == 200, req.content
    response = req.json()
    # for each playlist extract track id
    # WHICH OPTION? return len(response['devices']) > 0
    for device in response['devices']:
        if device['is_active']:
            return True

# FOR SOLE PREMIUM ACCOUNTS!
# https://developer.spotify.com/documentation/web-api/reference/player/start-a-users-playback/
# PUT METHOD : https://api.spotify.com/v1/me/player/play
# SCOPE : user-modify-playback-state
# REQUEST :
#     body-parameters: {"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh"]}
def play_track(uri_track):
    headers = {"Authorization": "Bearer %s" %session['token']}
    params = {'uris': [str(uri_track)]}
    # create request
    response = requests.put(headers=headers, data=json.dumps(params), url="https://api.spotify.com/v1/me/player/play")
    # check required values
    assert response.status_code == 204
    return True

def get_tracks():
    headers = {"Authorization": "Bearer %s" %session['token']}
    # search music feature inside user's playlists
    # create request
    response = requests.get(headers=headers, url="https://api.spotify.com/v1/me/playlists")
    # check required values
    assert response.status_code == 200, response.content
    answer = response.json()
    # collect playlists
    playlist_links = []
    # for each playlist extract playlist reference
    for playlist in answer['items']:
        tracks = playlist['tracks']
        if (tracks['total'] > 0):  # exclusion of empty playlists
            playlist_links.append(tracks['href'])  # links are already unique
    # collect tracks
    track_ids = []
    # for each playlist, retrieve the ids of all the songs contained in it
    params = {'fields': 'items(track(id))'}
    for playlist_link in playlist_links:
        response = requests.get(headers=headers, url=playlist_link, params=params)
        # check required values
        assert response.status_code == 200, response.content
        for track in response.json()['items']:
            track_ids.append(track['track']['id'])
        time.sleep(0.005) # delay among each playlist request
    # truncate track_ids quantity to maximum value (100)
    track_ids = np.unique(track_ids)
    np.random.shuffle(track_ids)
    if (len(track_ids) > 100):
        track_ids = track_ids[0:99]
    # convert track_ids to string
    track_ids_str = np.array2string(track_ids, separator=',').translate({ord(i): None for i in "[] '\n"})
    # create request
    params = {'ids': track_ids_str}
    response = requests.get(headers=headers, url='https://api.spotify.com/v1/audio-features', params=params)
    # check required values
    assert response.status_code == 200, response.content
    # tracks information
    tracks_descriptors = response.json()['audio_features']

    return tracks_descriptors

# input-structures
#       tracks : [{                       emotions : {
#           "energy": float,                    "anger": float,
#           "tempo": float,                     "contempt": float,
#           "loudness": float,                  "disgust": float,
#           "mode": 0|1,                        "fear": float,
#           "speechiness": float,               "happiness": float,
#           "acousticness": float,              "neutral": float,
#           "instrumentalness": float,          "sadness": float,
#           "liveness": float,                  "surprise": float
#           "valence": float,              }
#           "uri": String,
#           ...
#           } , {
#           ...
#           }
#       ]
def choose_track(emotions, tracks_descriptors):
    # anger | fear | sadness || happiness | surprise --map-->
    # mode [0|1], valence [0,1], tempo [bpm], energy [0,1], loudness [dB], danceability [0,1] - filtering
    print(emotions)
    tb_filtered = tracks_descriptors.copy()

    # negative feelings 
    if (emotions['anger'] > 0.6 or emotions['fear'] > 0.6 or emotions['sadness'] > 0.6):
        print('negative vibes')
        tb_filtered = [t for t in tb_filtered if (t['valence'] < 0.4 and t['mode'] == 0)] # basic negativity filter
        print(tb_filtered)
        if (emotions['anger'] > 0.8):
            tb_filtered = [t for t in tb_filtered if (t['tempo'] > 90 and t['tempo'] < 150 and
                t['energy'] > 0.8 and t['loudness'] > 0.7)]
        else: # how could I distinguish fear from sadness?
            tb_filtered = [t for t in tb_filtered if (t['tempo'] > 70 and t['tempo'] < 100 and
                t['energy'] > 0.2 and t['energy'] < 0.6 and t['loudness'] > -30 and t['loudness'] < -10)]
    # positive ones
    elif (emotions['happiness'] > 0.6 or emotions['surprise'] > 0.6):
        print('positive vibes')
        tb_filtered = [t for t in tb_filtered if (t['valence'] > 0.6)] # here I wouldn't consider the mode, basic positivity filter
        print(tb_filtered)
        if (emotions['happiness'] > 0.8):
            tb_filtered = [t for t in tb_filtered if (t['valence'] > 0.8 and t['tempo'] > 90 and t ['tempo'] < 150 and
                t['energy'] > 0.7 and t['loudness'] > -15 and t['danceability'] > 0.7)]
        elif (emotions['surprise'] > 0.8): # how could I distinguish surprise from happiness?
            tb_filtered = []
        else:
            tb_filtered = []

    # select random track with high: tempo, loudness
    #                           low: speechiness
    # if (emotions["anger"] > 0.6):
    #     print("anger")

    # select random track with  low: tempo
    #                          high: speechiness
    # if (emotions["disgust"] > 0.6):
    #     print("disgust")

    # select random track with  low: instrumentalness
    #                          high: loudness
    # if (emotions["fear"] > 0.6):
    #     print("fear")

    if (len(tb_filtered) > 0):
        print('________________________________________________________________')
        chosen = np.random.choice(tb_filtered)
        print(chosen)
        play_track(chosen['uri'])
    else:
        print('No track found, please adjust the implementation/thresholds =)')
