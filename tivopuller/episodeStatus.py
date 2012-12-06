EpisodeStatus = ['Ignored', 'Wanted', 'Downloading', 'Downloaded']

def getStatuses():
    return [(x, y) for x,y in enumerate(EpisodeStatus)]

def getStatusCode(val):
    return EpisodeStatus.index(val)