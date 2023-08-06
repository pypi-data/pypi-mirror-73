# spotify-flask-downloader


**A Flask Based Backend To Search And Download Music From Spotify.**

This is a little flask based backend to download music from YouTube by searching in Spotify, based on your network requests.


## Install


```
pip3 install spotify-flask-downloader
```


## Dependencies


- [flask](https://github.com/pallets/flask) By [pallets](https://palletsprojects.com)

- [flask-cors](https://github.com/corydolphin/flask-cors) By [corydolphin](https://github.com/corydolphin)

- [youtube-dl](https://github.com/ytdl-org/youtube-dl) By [ytdl-org](https://github.com/ytdl-org)

- [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) By [alexmercerind](https://github.com/alexmercerind)


## Like the module?


Consider starring the repository. Feel free to use.

Feel free to open issue, in case you find one.


## Usage


### Start the server

Execute this script and let it run in the background as you play with this module.

```python
from spotifyflaskdownloader import SpotifyFlaskDownloader

downloader = SpotifyFlaskDownloader("SPOTIFY-CLIENT-ID", "SPOTIFY-CLIENT-SECRET", 5000)
```

You can use something like [requests](https://pypi.org/project/requests/) or [urllib](https://docs.python.org/3/library/urllib.html) to access this flask server.


### Download Track

```python
import requests
response = requests.get(
    "http://localhost:5000/trackdownload",
    params= {
        "track_id": "7gHs73wELdeycvS48JfIos"    #Alternatively you can provide "track_name" in place of "track_id"
    }
)
print(response.json())
```

- Response

```json
{
    "download_url": "https://r8---sn-gwpa-5bgs.googlevideo.com/videoplayback?expire=1594409257&ei=yWwIX_3rNJOWvQSFwI5A&ip=2409%3A4053%3A2196%3Ad6fa%3Ac8bf%3Ab2d8%3A81bb%3Aad05&id=o-AE3zCFHWH5aAUBwVqKVBijX3Vjd9xf4LSZ5uyIa8l2qY&itag=249&source=youtube&requiressl=yes&mh=Hp&mm=31%2C29&mn=sn-gwpa-5bgs%2Csn-gwpa-qxa6&ms=au%2Crdu&mv=m&mvi=8&pl=36&initcwndbps=175000&vprv=1&mime=audio%2Fwebm&gir=yes&clen=1360728&dur=212.501&lmt=1576159977750934&mt=1594387597&fvip=8&keepalive=yes&c=WEB&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgP_4WHdnJO0h1wde12DLTcrfAQ8ShLLIezFkfO0AjRdoCIBqTZqhOP8kp7amBJObCMzKNJ_vzXZdvJcnY8j4PTAm0&sig=AOq0QJ8wRgIhAJe-DBmBKmfBx8dJcoKyp_WCeXg3Q3WKfxAvw4ztUwbVAiEApLFfh9DK9rRkkSRDSqPhXgUXdtStDUZOok2gxzEHhTY=&ratebypass=yes"
}
```


### Search for Music

```python
import requests
response = requests.get(
    "http://localhost:5000/search",
    params= {
        "keyword": "Faded Alan Walker",    #Search Query
        "mode": "track",                   #Default is "album", Supports "album" & "track"
        "offset": 0,                       #Default is 0
        "limit": 1                         #Default is 50
    }
)
print(response.json())
```

- Response

```json
{
    "tracks": [
        {
            "track_id": "7gHs73wELdeycvS48JfIos",
            "track_name": "Faded",
            "track_artists": [
                "Alan Walker"
            ],
            "track_number": 1,
            "track_duration": 212626,
            "album_id": "5HMjpBO0v78ayq5lreAyDd",
            "album_name": "Faded",
            "year": "2015",
            "album_artists": [
                "Alan Walker"
            ],
            "album_art_640": "https://i.scdn.co/image/ab67616d00001e02c4d00cac55ae1b4598c9bc90",
            "album_art_300": "https://i.scdn.co/image/ab67616d0000b273c4d00cac55ae1b4598c9bc90",
            "album_art_64": "https://i.scdn.co/image/ab67616d00004851c4d00cac55ae1b4598c9bc90",
            "album_length": 4,
            "album_type": "single"
        }
    ]
}
```


### Get Track Info

```python
import requests
response = requests.get(
    "http://localhost:5000/trackinfo",
    params= {
        "track_id": "7gHs73wELdeycvS48JfIos",
    }
)
print(response.json())
```

- Response

```json
{
    "track_id": "7gHs73wELdeycvS48JfIos",
    "track_name": "Faded",
    "track_artists": [
        "Alan Walker"
    ],
    "track_number": 1,
    "track_duration": 212626,
    "album_art_640": "https://i.scdn.co/image/ab67616d00001e02c4d00cac55ae1b4598c9bc90",
    "album_art_300": "https://i.scdn.co/image/ab67616d0000b273c4d00cac55ae1b4598c9bc90",
    "album_art_64": "https://i.scdn.co/image/ab67616d00004851c4d00cac55ae1b4598c9bc90",
    "album_id": "5HMjpBO0v78ayq5lreAyDd",
    "album_name": "Faded",
    "year": "2015",
    "album_artists": [
        "Alan Walker"
    ],
    "album_length": 4,
    "album_type": "single"
}
```

### Get Tracks Of An Album

```python
import requests
response = requests.get(
    "http://localhost:5000/albuminfo",
    params= {
        "album_id": "5HMjpBO0v78ayq5lreAyDd",
    }
)
print(response.json())
```

- Response

```json
{
    "tracks": [
        {
            "track_id": "7gHs73wELdeycvS48JfIos",
            "track_name": "Faded",
            "track_artists": [
                "Alan Walker"
            ],
            "track_number": 1,
            "track_duration": 212626
        },
        {
            "track_id": "0HmONWWIU1FXkwWLDpqrjl",
            "track_name": "Faded - Instrumental",
            "track_artists": [
                "Alan Walker"
            ],
            "track_number": 2,
            "track_duration": 214013
        },
        {
            "track_id": "34F4GJFUzPvPJmGrTpyqlZ",
            "track_name": "Faded (Restrung)",
            "track_artists": [
                "Alan Walker"
            ],
            "track_number": 3,
            "track_duration": 217053
        },
        {
            "track_id": "0RLjnX1vYWvtdThB8LABwo",
            "track_name": "Faded - Piano Version",
            "track_artists": [
                "Alan Walker"
            ],
            "track_number": 4,
            "track_duration": 215080
        }
    ]
}
```