from datetime import datetime
from spotframework.model.track import Track
from spotframework.model.uri import Uri
from enum import Enum
from typing import Union


class Context:
    def __init__(self,
                 uri: Union[str, Uri],
                 object_type: str = None,
                 href: str = None,
                 external_spot: str = None):
        if isinstance(uri, str):
            self.uri = Uri(uri)
        else:
            self.uri = uri
        if self.uri.object_type not in [Uri.ObjectType.album, Uri.ObjectType.artist, Uri.ObjectType.playlist]:
            raise TypeError('context uri must be one of album, artist, playlist')
        self.object_type = object_type
        self.href = href
        self.external_spot = external_spot

    def __eq__(self, other):
        return isinstance(other, Context) and other.uri == self.uri

    def __repr__(self):
        return f'Context: {self.object_type} uri({self.uri})'

    def __str__(self):
        return str(self.uri)


class Device:

    class DeviceType(Enum):
        COMPUTER = 1
        TABLET = 2
        SMARTPHONE = 3
        SPEAKER = 4
        TV = 5
        AVR = 6
        STB = 7
        AUDIODONGLE = 8
        GAMECONSOLE = 9
        CASTVIDEO = 10
        CASTAUDIO = 11
        AUTOMOBILE = 12
        UNKNOWN = 13

    def __init__(self,
                 device_id: str,
                 is_active: bool,
                 is_private_session: bool,
                 is_restricted: bool,
                 name: str,
                 object_type: DeviceType,
                 volume: int):
        self.device_id = device_id
        self.is_active = is_active
        self.is_private_session = is_private_session
        self.is_restricted = is_restricted
        self.name = name
        self.object_type = object_type
        self.volume = volume

    def __repr__(self):
        return f'Device: {self.name} active({self.is_active}) type({self.object_type}) vol({self.volume})'

    def __str__(self):
        return self.name


class CurrentlyPlaying:
    def __init__(self,
                 context: Context,
                 timestamp: datetime,
                 progress_ms: int,
                 is_playing: bool,
                 track: Track,
                 device: Device,
                 shuffle: bool,
                 repeat: bool,
                 currently_playing_type: str):
        self.context = context
        self.timestamp = timestamp
        self.progress_ms = progress_ms
        self.is_playing = is_playing
        self.track = track
        self.device = device
        self.shuffle = shuffle
        self.repeat = repeat
        self.currently_playing_type = currently_playing_type

    def __repr__(self):
        return f'CurrentlyPlaying: is_playing({self.is_playing}) progress({self.progress_ms}) ' \
            f'context({self.context}) track({self.track}) device({self.device}) shuffle({self.shuffle}) ' \
            f'repeat({self.repeat}) time({self.timestamp})'

    def __eq__(self, other):
        return isinstance(other, CurrentlyPlaying) and other.track == self.track and other.context == self.context

    @staticmethod
    def _format_duration(duration):
        total_seconds = duration / 1000
        minutes = int((total_seconds/60) % 60)
        seconds = int(total_seconds % 60)
        return f'{minutes}:{seconds}'

    def __str__(self):
        if self.is_playing:
            playing = 'playing'
        else:
            playing = '(paused)'

        return f'{playing} {self.track} on {self.device} from {self.context} ({self._format_duration(self.progress_ms)})'
