#!/usr/bin/python3
from gmusicapi import Mobileclient
import os
import eyed3
import logging
import unidecode
import requests
import sys
import argparse
import getpass
import re


class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Gmusicdownloader:
    _api = None
    outputDir = ""

    def __init__(self, email, password, deviceid, outputDir=os.getcwd()):
        self._api = Mobileclient(False)
        self.outputDir = outputDir
        print("Logging in...", end='', flush=True)
        self._api.login(email, password, deviceid)
        if self._api.is_authenticated():
            print(bColors.OKGREEN + " Logged in!" + bColors.ENDC)
        else:
            print(bColors.FAIL + " Unable to log in!" + bColors.ENDC)
            sys.exit(1)


    def escapeName(self, string):
        return re.sub('[<>:"/\\\|?*]', '', string)

    def tagTrack(self, path, track):
        audiofile = eyed3.load(path)
        audiofile.initTag()
        audiofile.tag.artist = track['artist']
        audiofile.tag.album = track['album']
        audiofile.tag.album_artist = track['albumArtist']
        audiofile.tag.title = track['title']
        audiofile.tag.track_num = track['trackNumber']
        if 'discNumber' in track:
            audiofile.tag.disc_num = track['discNumber']
        if 'year' in track:
            audiofile.tag.release_date = track['year']
        if 'genre' in track:
            audiofile.tag.genre = track['genre']
        audiofile.tag.save()


    def downloadCover(self, dirpath, album):
        if os.path.exists(dirpath + '/' + 'cover.jpg'):
            return
        resp = requests.get(album['albumArtRef'])
        with open(dirpath + '/' + 'cover.jpg', 'wb') as f:
            f.write(resp.content)


    def parseSelection(self, selection):
        try:
            items = []
            if selection.find(',') > 0:
                items += selection.split(',')
            else:
                items += [selection]
            for i in range(len(items)):
                item = items[i] 
                if item.find('-') < 0:
                    continue
                rng = item.split('-')
                del items[i]
                items += [str(i) for i in range(int(rng[0]), int(rng[1]) + 1)]
            
            items = [int(i) for i in items]
            items.sort()
            return items
        except:
            raise ValueError('Invalid selection!')

    def downloadAlbum(self, album):
        dirpath = "{}/{}/{}".format(self.outputDir, 
                                            self.escapeName(album['albumArtist']),
                                            self.escapeName(album['name']))
        dirpath = unidecode.unidecode(dirpath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.downloadCover(dirpath, album)
        
        #Iterate over album tracks
        for track in album['tracks']:
            trackId = track['nid']
            path = dirpath + "/{} {}.mp3".format(str(track['trackNumber']).zfill(2),
                                                    self.escapeName(track['title']))
            path = unidecode.unidecode(path)
            if not os.path.exists(path):
                stream = self._api.get_stream_url(trackId)
                resp = requests.get(stream)
                with open(path, 'wb') as f:
                    f.write(resp.content)
                self.tagTrack(path, track)
                print("{}✔️  {} -- {} {}".format(bColors.OKGREEN,
                                                track['artist'],
                                                track['title'],
                                                bColors.ENDC))
    
    #Iterate over selected albums
    def downloadSelection(self, selection, search):
        for albumNum in self.parseSelection(selection):

            if albumNum > len(search['album_hits']):
                raise ValueError('Invalid index: ' + str(albumNum))
            album = self._api.get_album_info(search['album_hits'][albumNum - 1]['album']['albumId'])
            print()
            print(bColors.WARNING + 'Downloading ' + bColors.ENDC + 
                  bColors.FAIL + album['albumArtist'] + ' -- ' + \
                  album['name'] + '...' + bColors.ENDC)
            self.downloadAlbum(album)

    def searchAndDownload(self):
        while True:
            print()
            #Album search
            searchStr = input(bColors.OKBLUE + bColors.BOLD + 
                        "? Search for an album: " + bColors.ENDC)
            print()
            search = self._api.search(searchStr, 20)
            if len(search['album_hits']) == 0:
                print(bColors.FAIL + "Nothing found!" + bColors.ENDC)
                print()
                continue
            if 'album_hits' in search:
                albumCounter = 1
                for album in search['album_hits']:
                    album = album['album']
                    albumStr = "{}) {} -- {}".format(str(albumCounter),
                                                     album['albumArtist'],
                                                     album['name'])
                    if 'year' in album:
                        albumStr += " ({})".format(str(album['year']))
                    print(bColors.HEADER + albumStr + bColors.ENDC)
                    albumCounter += 1
                print()
                selection = input(bColors.OKBLUE + bColors.BOLD + 
                            '? Album to download (eg. 1, 2, 3.. or 1-3) or (b)ack or (e)xit: ' 
                            + bColors.ENDC)
                if selection == 'e':
                    sys.exit(0)
                elif selection == 'b':
                    continue
            self.downloadSelection(selection, search)
    def sync(self):
        library = self._api.get_all_songs()
        library = sorted(library, key=lambda k: (k['artist'], k['album'], k['trackNumber'])) 
        print()
        for track in library:
    
            dirpath = "{}/{}/{}".format(self.outputDir, 
                                                self.escapeName(album['albumArtist']),
                                                self.escapeName(album['name']))
            dirpath = unidecode.unidecode(dirpath)
            if not os.path.isdir(dirpath):
                os.makedirs(dirpath)
            track['albumArtRef'] = track['albumArtRef'][0]['url']
            self.downloadCover(dirpath, track)
            trackId = track['nid']
            path = dirpath + "/{} {}.mp3".format(str(track['trackNumber']).zfill(2),
                                                    self.escapeName(track['title']))
            path = unidecode.unidecode(path)
            if not os.path.exists(path):
                stream = self._api.get_stream_url(trackId)
                resp = requests.get(stream)
                with open(path, 'wb') as f:
                    f.write(resp.content)
                self.tagTrack(path, track)
                print("{}✔️  {} -- {} {}".format(bColors.OKGREEN,
                                                track['artist'],
                                                track['title'],
                                                bColors.ENDC))

if __name__ == "__main__":
    #Argument parsing
    parser = argparse.ArgumentParser(description=
                                    'Google Play Music album downloader')
    parser.add_argument('-e', '--email',
                        help='Google Play Music email')

    parser.add_argument('-p', '--password',
                        help='Google Play Music password')

    parser.add_argument('-d', '--deviceid',
                        help='Google Play Music device ID')

    parser.add_argument('-o', '--output',
                        help='output directory')

    parser.add_argument('-s', '--sync', action='store_true',
                        help='sync Google Play Music library to output folder')

    args = parser.parse_args()

    #Disable eyeD3 logging
    eyed3log = logging.getLogger('eyed3.mp3.headers')
    eyed3log.disabled = True
    eyed3log = logging.getLogger('eyed3.id3')
    eyed3log.disabled = True

    #Logging in
    if not args.email:
        args.email = input(bColors.BOLD + \
                           "? Enter Google Play Music email: " + \
                           bColors.ENDC)

    if not args.password:
        args.password = getpass.getpass(bColors.BOLD + \
                           "? Enter Google Play Music password: " + \
                           bColors.ENDC)

    if not args.deviceid:
        args.deviceid = input(bColors.BOLD + \
                           "? Enter Google Play Music device ID: " + \
                           bColors.ENDC)

    if not args.output:
        args.output = os.getcwd()
    downloader = Gmusicdownloader(args.email,
                                  args.password,
                                  args.deviceid,
                                  args.output)

    if args.sync:
        downloader.sync()
    else:
        downloader.searchAndDownload()

