
import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import datetime
import html_unescape
import Cookie
import playlistEntry
import os


class TivoFetcher:
  def __init__(self, tivo_host, media_key):
    self.tivo_host = tivo_host
    self.media_key = media_key

    # The Tivo uses Digest Auth, with username 'TiVo DVR' and password as the
    # media access key.  Setup a urllib opener to have that auth information
    # for both http and https.
    authinfo = urllib2.HTTPDigestAuthHandler()
    authinfo.add_password('TiVo DVR', 'http://%s/' % (tivo_host), 'tivo', 
        media_key)
    authinfo.add_password('TiVo DVR', 'https://%s/' % (tivo_host), 'tivo',
        media_key)
    self.opener = urllib2.build_opener(authinfo)

    # The TiVo requires some other cookies for downloading videos.  Those
    # cookies are set when accessing the index, and stored here by
    # ExtractCookies to be used when downloading.
    self.cookies = Cookie.SimpleCookie()

  def Download(self, entry, destfn, moveTo):
    # Use curl, since wget and urllib both generate bad data (one webpage
    # points to a bug in wget's chunked encoding handling)
    if not entry.url:
      print "Unable to download %s, no url" % (entry.title)
      return

    cookie_str = []
    for morsel in self.cookies.values():
      cookie_str.append("%s=%s" % (morsel.key, morsel.value))

    args = []
    args.append('curl')
    args.append('--silent')
    args.append('--cookie')
    args.append(';'.join(cookie_str))
    args.append('--digest')
    args.append('-u')
    args.append('tivo:%s' % self.media_key)
    args.append('--output')
    args.append('%s.dl' % destfn)
    args.append(entry.url)

    r = None;

    try:
      r = os.spawnvp(os.P_WAIT, 'curl', args)
    except Exception, e:

        if (not e.args or not e.args[0]):
          print "Exception thrown!"
          return
        else:
          print "Exception generated in curl: " + e.args[0]
          return

    if r == 0:
      file_size = os.path.getsize('%s.dl' % destfn)
      # Check the size, it should be at least 60% of the size, and pretty big
      # 60% seems small, but I've seen Robot Chicken episodes as small as 66%
      # Actually, I've now seen episodes in the 35% range... but I don't know
      # if I want to make this that lenient.
      if (file_size < 100*1024*1024) or (file_size < 0.6 * int(entry.size)):
        print '%s file size too small: %d < %d' % (destfn, file_size,
            int(entry.size))
        return
      os.rename('%s.dl' % destfn, moveTo)
    elif not r:
      print "could not generate curl"
    else:
      print '%s returned %d' % (' '.join(args), r)

    print "hi"
    return

    # The urllib downloader, which generates a broken file.  I haven't
    # debugged this yet.
    headers = {}
    headers['Cookie'] = '; '.join(cookie_str)
    req = urllib2.Request(entry.url, headers=headers)
    f = self.opener.open(req)
    fpo = open(destfn, 'w')
    while 1:
      buf = f.read(65536)
      if not buf: break
      fpo.write(buf)

  def ExtractCookies(self, headers):
    if headers.has_key("set-cookie"):
      for value in headers.getheaders("set-cookie"):
        self.cookies.load(value)

  def FetchPlayList(self):

    if (self.tivo_host is None or self.tivo_host == ""):
      return []

    # /TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes&AnchorOffset=0
    offset = 0
    totalcount = 0
    results = []
    while 1:
      url = "https://%s/TiVoConnect?Command=QueryContainer&Container=%%2FNowPlaying&Recurse=Yes&AnchorOffset=%d" % (self.tivo_host, offset)

      f = self.opener.open(url)
      self.ExtractCookies(f.headers)

      data = str(f.read())

      soup = BeautifulSoup(data)

      if totalcount == 0:
        totalcount = int(soup.tivocontainer.details.totalitems.string)
      for item in soup.tivocontainer.findAll('item'):
        entry = playlistEntry.PlayListEntry()
        entry.title = html_unescape.unescape(item.details.title.string)
        if item.details.episodetitle:
          entry.episode = html_unescape.unescape(item.details.episodetitle.string)
        if item.details.description:
          entry.desc = html_unescape.unescape(item.details.description.string).replace('Copyright Tribune Media Services, Inc.', '').strip()
        entry.date = int(item.details.capturedate.string, 0)
        entry.size = item.details.sourcesize.string
        if item.details.sourcechannel:
          entry.channel = item.details.sourcechannel.string
          entry.station = item.details.sourcestation.string
        if item.details.inprogress:
          entry.inprogress = True
        entry.url = html_unescape.unescape(item.links.content.url.string)
        # urllib2's http auth support doesn't like :80
        entry.url = entry.url.replace(':80/', '/')
        if item.details.copyprotected:
          entry.copyprotected = True
        entry.details_url = html_unescape.unescape(item.links.tivovideodetails.url.string)
        if (item.details.seriesid):
          entry.seriesId = item.details.seriesid.string
        else:
          entry.seriesId = item.details.programid.string
        entry.episodeId = item.details.programid.string

        results.append(entry)
      if len(results) < totalcount and offset < len(results):
        offset = len(results) + 1
      else:
        break
        
    return results

