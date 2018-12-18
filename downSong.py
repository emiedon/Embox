import requests,os,time,sys,re
from scrapy.selector import Selector

class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers=self.headers


    def get_songurls_playlistID(self,playlistID):
        url=self.main_url+'playlist?id=%d'% playlistID
        re= self.session.get(url)
        sel=Selector(text=re.text)
        songurls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls

    def get_songurls_albumID(self,albumID):
        url=self.main_url+'album?id=%d'% albumID
        re= self.session.get(url)
        sel=Selector(text=re.text)
        songurls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls




    def get_songIDList(self,playlist):
        middleList = self.get_songurls(playlist)
        songIDList = []
        for songUrl in middleList:
            songIDList.append(songUrl.split('=')[1])
        return songIDList



    def get_songinfo(self,songurl):
        url=self.main_url+songurl
        re=self.session.get(url)
        sel=Selector(text=re.text)
        song_id = url.split('=')[1]
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer= '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        songname=singer+'-'+song_name
        return str(song_id),songname


    def download_song(self, songurl):
        song_id, songname = self.get_songinfo(songurl)
        song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_id
        r = requests.get(song_url)
        with open(songname+".mp3", "wb") as code:
            code.write(r.content)

    def DownloadMusicByListID(self, playlist):
        songurls = self.get_songurls_playlistID(playlist)
        for songurl in songurls:
            print(songurl,'下载完毕！')
            self.download_song(songurl)

    def DownloadMusicByAlbumID(self, playlist):
        songurls = self.get_songurls_albumID(playlist)
        for songurl in songurls:
            self.download_song(songurl)

    def DownLoadLyricsByListID(self,ID):
        tracks = self.get_songIDList(ID)
        with open('Lyrics.txt', 'a', encoding='utf-8') as f:
            for i in tracks:
                lrcurl = "http://music.163.com/api/song/lyric?os=pc&id=" + str(i) + "&lv=-1&kv=-1&tv=-1"
                lrcreq = requests.get(lrcurl)
                dt = lrcreq.json()
                if 'lrc' in dt:
                    lrc = re.sub(u"\\[.*?]", "", dt['lrc']['lyric'])
                    f.write(lrc)
            f.close()

if __name__ == '__main__':
    d = wangyiyun()
    d.DownloadMusicByAlbumID(72645619)