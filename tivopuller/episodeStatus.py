EpisodeStatus = ['Ignored', 'Wanted', 'Downloading', 'Downloaded', 'Queued', 'Removed from Tivo']

def getStatuses():
    return [(x, y) for x,y in enumerate(EpisodeStatus)]

def getStatusCode(val):
    return EpisodeStatus.index(val)