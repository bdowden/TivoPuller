
class PlayListEntry:
    def __init__(self):
        self.title = ''
        self.episode = ''
        self.desc = ''
        self.date = 0
        self.size = ''
        self.channel = ''
        self.station = ''
        self.copyprotected = False
        self.url = ''
        self.details_url = ''
        self.inprogress = False
        self.episodeId = ''
        self.seriesId = ''

    def getFileName(self):
        filename = self.title + "." + self.episode
        filename = filename.replace(" ", ".").replace(":", ".") + ".tivo"
        return filename

    def __str__(self):
        return ':'.join([self.title, self.desc, str(self.date), str(self.size), self.channel, self.url])