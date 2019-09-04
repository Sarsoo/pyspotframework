import csv
import datetime
import logging

logger = logging.getLogger(__name__)

headers = ['name', 'artist', 'album', 'album artist', 'added', 'track id', 'album id', 'added by']


def export_playlist(playlist, path, name=None):

    logger.info(f'{playlist.name} {path} {name}')
    
    date = str(datetime.datetime.now())

    if name is None:
        name = playlist.name

    with open('{}/{}_{}.csv'.format(path, name.replace('/', '_'), date.split('.')[0]), 'w', newline='') as fileobj:

        writer = csv.DictWriter(fileobj, fieldnames=headers)
        writer.writeheader()

        for track in playlist.tracks:

            trackdict = {
                'name':track.name,
                'album':track.album.name,
                'added':track.added_at,
                'track id':track.spotify_id,
                'album id':track.album.spotify_id,
                'added by':track.added_by.username}

            trackdict['album artist'] = ', '.join(x.name for x in track.album.artists)

            trackdict['artist'] = ', '.join(x.name for x in track.artists)

            writer.writerow(trackdict)
