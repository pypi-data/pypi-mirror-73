import urllib.request
import urllib.parse
import base64
import json
from urllib.request import Request

class SpotifyHandler:

    def AccessToken(self):
        encoded = base64.b64encode(bytes(self.clientId + ":" + self.clientSecret, encoding="utf_8")).decode("utf_8")
        parameters = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        headers = {"Authorization": f"Basic {encoded}"}

        request = Request(
            url = "https://accounts.spotify.com/api/token",
            data = parameters,
            headers = headers 
        )
        response = urllib.request.urlopen(request)
        return json.loads(response.read())["access_token"]

    def TrackInfo(self, trackId):
        token = self.AccessToken()
        request = Request(
            url = f"https://api.spotify.com/v1/tracks/{trackId}",
            data = None,
            headers = {"Authorization": f"Bearer {token}"}
        )
        response = urllib.request.urlopen(request)
        track = json.loads(response.read())
        a_artists = track["album"]["artists"]
        album_artists = []
        for artist in a_artists:
            album_artists+=[artist["name"]]
        t_artists = track["artists"]
        track_artists = []
        for artist in t_artists:
            track_artists+=[artist["name"]]
        return json.dumps({   
            "track_id": track["id"],
            "track_name": track["name"],
            "track_artists": track_artists,
            "track_number": track["track_number"],
            "track_duration": track["duration_ms"],
            "album_art_640": track["album"]["images"][1]["url"],
            "album_art_300": track["album"]["images"][0]["url"],
            "album_art_64": track["album"]["images"][2]["url"],
            "album_id": track["album"]["id"],
            "album_name": track["album"]["name"],
            "year": track["album"]["release_date"].split("-")[0],
            "album_artists": album_artists,
            "album_length": track["album"]["total_tracks"],
            "album_type": track["album"]["album_type"]
        }, indent = 4)

    def AlbumInfo(self, albumId):
        token = self.AccessToken()
        query = urllib.parse.urlencode({"limit": 50, "offset": 0})
        request = Request(
            url = f"https://api.spotify.com/v1/albums/{albumId}/tracks" + "?" + query,
            data = None,
            headers = {"Authorization": f"Bearer {token}"}
        )
        response = urllib.request.urlopen(request)
        tracks = json.loads(response.read())["items"]
        result = []
        for track in tracks:
            t_artists = track["artists"]
            track_artists = []
            for artist in t_artists:
                track_artists+=[artist["name"]]
            result+=[
                {
                    "track_id": track["id"],
                    "track_name": track["name"],
                    "track_artists": track_artists,
                    "track_number": track["track_number"],
                    "track_duration": track["duration_ms"],
                }
            ]
        return json.dumps({"tracks": result}, indent=4)
        

    def SearchSpotify(self, keyword, mode, offset, limit):
        token = self.AccessToken()
        query = urllib.parse.urlencode({"q": keyword, "type": mode, "limit": limit, "offset": offset})
        request = Request(
            url = "https://api.spotify.com/v1/search" + "?" + query,
            data = None,
            headers = {"Authorization": f"Bearer {token}"}
        )
        response = json.loads(urllib.request.urlopen(request).read())
        if mode == "track":
            tracks = []
            for track in response["tracks"]["items"]:
                a_artists = track["album"]["artists"]
                album_artists = []
                for artist in a_artists:
                    album_artists+=[artist["name"]]
                t_artists = track["artists"]
                track_artists = []
                for artist in t_artists:
                    track_artists+=[artist["name"]]
                tracks+=[
                    {   
                        "track_id": track["id"],
                        "track_name": track["name"],
                        "track_artists": album_artists,
                        "track_number": track["track_number"],
                        "track_duration": track["duration_ms"],
                        "album_id": track["album"]["id"],
                        "album_name": track["album"]["name"],
                        "year": track["album"]["release_date"].split("-")[0],
                        "album_artists": album_artists,
                        "album_art_640": track["album"]["images"][1]["url"],
                        "album_art_300": track["album"]["images"][0]["url"],
                        "album_art_64": track["album"]["images"][2]["url"],
                        "album_length": track["album"]["total_tracks"],
                        "album_type": track["album"]["album_type"]
                    }
                ]
            return json.dumps({"tracks": tracks}, indent = 4)
        elif mode == "album":
            albums = []
            for album in response["albums"]["items"]:
                a_artists = album["artists"]
                album_artists = []
                for artist in a_artists:
                    album_artists+=[artist["name"]]
                albums+=[
                    {   
                        "album_id": album["id"],
                        "album_name": album["name"],
                        "year": album["release_date"].split("-")[0],
                        "album_artists": album_artists,
                        "album_art_640": album["images"][1]["url"],
                        "album_art_300": album["images"][0]["url"],
                        "album_art_64": album["images"][2]["url"],
                        "album_length": album["total_tracks"],
                        "album_type": album["album_type"]
                    }
                ]
            return json.dumps({"albums": albums}, indent = 4)
        else:
            return("Enter mode=album or mode=track only in your GET request.")
