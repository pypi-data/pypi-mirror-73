from youtubesearchpython import SearchVideos
import youtube_dl
import json

class YoutubeHandler:

    def AudioUrl(self, videoId):
        import youtube_dl
        ydl_opts = {
            'format': 'bestaudio',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f'https://www.youtube.com/watch?v={videoId}', download=False)
            return info['formats'][0]['url']

    def SearchYoutube(self, keyword, offset, mode, max_results):
        search = SearchVideos(keyword, offset, mode, max_results)
        return search.result()

    def TrackDownload(self, trackId, trackName):
        if trackName == None:
            trackInfo = json.loads(self.TrackInfo(trackId))
        
            artists = ""
            for artist in trackInfo["album_artists"]:
                artists+=artist+" "

            videoId = self.SearchYoutube(trackInfo["track_name"] + " " + artists + " " + trackInfo["album_name"], 1, "dict", 1)["search_result"][0]["id"]
            audioUrl = self.AudioUrl(videoId)
            
            return json.dumps({"download_url": audioUrl}, indent=4)
        if trackId == None:
            trackId = json.loads(self.SearchSpotify(trackName, "track", 0, 1))["tracks"][0]["track_id"]
            trackInfo = json.loads(self.TrackInfo(trackId))
            artists = ""
            for artist in trackInfo["album_artists"]:
                artists+=artist+" "

            videoId = self.SearchYoutube(trackInfo["track_name"] + " " + artists + " " + trackInfo["album_name"], 1, "dict", 1)["search_result"][0]["id"]
            audioUrl = self.AudioUrl(videoId)
            
            return json.dumps({"download_url": audioUrl}, indent=4)