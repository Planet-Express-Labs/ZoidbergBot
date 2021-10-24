# This software is provided free of charge without a warranty. 
# This Source Code Form is subject to the terms of the Mozilla Public License, 
# v. 2.0. If a copy of the MPL was not provided with this file, You can obtain one at https://mozilla.org/MPL/2.0/.import json
import codecs
import json
import requests_async as requests
from urllib import request
from config import GOOGLE_API_KEY

def generate_video_link(self, videoID):
    return 'https://www.youtube.com/watch?v={}'.format(videoID)


class YoutubeSubscription:

    def __init__(self, User):
        self.reader = codecs.getreader('utf-8')
        self.GOOGLE_API = GOOGLE_API_KEY
        self.user = User
        self.user_id = self.getUserID()
        self.video_data = self.getVideo(self.data)

    def getUserID(self):
        data = json.load(self.reader(request.urlopen(f'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={self.user}&key={self.GOOGLE_API}')))
        return data['items'][0]['id']

    def getStreamingState(self):
        data = json.load(self.reader(request.urlopen(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={self.getUserID()}&type=video&eventType=live&key={self.GOOGLE_API}')))
        if len(data['items']) == 0:
            return False
        else:
            self.streaming_id = self.getStreamingData()
        return True

    def getStreamingData(self):
        data = json.load(self.reader(urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={self.getUserID()}&type=video&eventType=live&key={self.GOOGLE_API}')))
        self.streaming_id = data['items'][0]['id']['videoId']
        return data['items'][0]['id']['videoId']

    def getVideo(self, data):
        videosNr = 0
        for item in data['items']:
            videosNr += 1
        videosTitles = []
        videosLinks  = []
        i = 0
        while i < videosNr:
            videosTitles.append(data['items'][i]['snippet']['title'])
            videosLinks.append(data['items'][i]['snippet']['resourceId']['videoId'])
            i += 1
        video_data = []
        for item in videosTitles:
            tempList = []
            tempList.append(item)
            tempList.append(videosLinks[videosTitles.index(item)])
            video_data.append(tempList)
        return video_data

    def update(self):
        self.old_videos = self.video_data
        self.data = self.getPlaylistData()
        self.video_data = self.getVideo(self.data)
        return self.video_data

    def isNewVideo(self):
        if not self.old_videos:
            return False
        if (self.old_videos[0][0] == self.video_data[0][0]) and (self.old_videos[0][1] == self.video_data[0][1]):
            return False
        return True
