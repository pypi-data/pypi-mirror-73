from flask import Flask, url_for, request
from flask_cors import CORS, cross_origin

import urllib.request
import urllib.parse
from urllib.request import Request

from spotifyflaskdownloader.spotify import SpotifyHandler
from spotifyflaskdownloader.youtube import YoutubeHandler

class SpotifyFlaskDownloader(SpotifyHandler, YoutubeHandler):

    def __init__(self, clientId, clientSecret, port = 5000):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.port = port
        self.SearchApplication()

    def SearchApplication(self):
        self.searchApplication = Flask("SpotifyDownloaderFlask")
        CORS(self.searchApplication)
        
        @self.searchApplication.route('/accesstoken')
        def AccessToken():
            return self.AccessToken()
        
        @self.searchApplication.route('/search')
        def SearchSpotify():
            return self.SearchSpotify(request.args.get('keyword'), request.args.get('mode', 'album'), request.args.get('offset', 0), request.args.get('limit', 50))
        
        @self.searchApplication.route('/searchyoutube')
        def SearchYoutube():
            return self.SearchYoutube(request.args.get('keyword'), request.args.get('offset', 1), request.args.get('mode', 'json'), request.args.get('max_results', 1))
        
        @self.searchApplication.route('/audiourl')
        def AudioUrl():
            return self.AudioUrl(request.args.get('video_id'))
        
        @self.searchApplication.route('/trackinfo')
        def TrackInfo():
            return self.TrackInfo(request.args.get('track_id'))

        @self.searchApplication.route('/albuminfo')
        def AlbumInfo():
            return self.AlbumInfo(request.args.get('album_id'))

        @self.searchApplication.route('/trackdownload')
        def TrackDownload():
            return self.TrackDownload(request.args.get('track_id', None), request.args.get('track_name', None))
        
        self.searchApplication.run(host = "localhost", port = self.port)