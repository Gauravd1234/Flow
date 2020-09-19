import spotify
import base64
import requests 

client_id = "f8248e959c474d44a10e54a4adbc8bf3"
client_secret = "8ce2af7922f04003b0e298767d8acfb9"


# Authorization 
def get_token():
    client_creds = f"{client_id}:{client_secret}"
    client_creds_bytes = client_creds.encode('ascii')

    client_creds_b64 = base64.b64encode(client_creds_bytes)

    token_url = "https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "client_credentials"


    }

    token_headers = {

        "Authorization": f"Basic {client_creds_b64.decode()}"

    }



    r = requests.post(token_url, data=token_data, headers=token_headers)
    access_token = r.json()['access_token']

    return access_token

# Get User Profile
def get_profile(token, user_id):
    user_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    user_token = {
        "Authorization": f"Bearer {token}"
    }

    u = requests.get(user_url, headers=user_token)


    return u.json()


# Get playlists
def get_playlist(profile):
    playlist = {}
    for x in profile['items']:
        url = x['external_urls']['spotify']

        index = url.index("https://open.spotify.com/playlist/") + 34
        playlist[x['name']] = url[index: len(url)]

    return playlist

def get_songs(playlist_id, token):
    tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    user_token = {
        "Authorization": f"Bearer {token}"

    }

    t = requests.get(tracks_url, headers=user_token)
    
    return t.json()

def return_song(user_id):
    token = get_token()
    profile = get_profile(token, user_id)

    playlist = get_playlist(profile)
 

    final = {}
    for x in playlist:
        songlist = []
        song = get_songs(playlist[x], token)
        song = song['items']

        for z in range(len(song)):     
           songlist.append(song[z]['track']['name'])

        
        final[x] = songlist

    return final


    

