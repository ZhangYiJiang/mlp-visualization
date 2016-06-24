import requests
import time
import os
from hashlib import md5
from bs4 import BeautifulSoup
from collections import OrderedDict
from utils import remove_special, word_count, identity
from natsort import natsorted
from operator import attrgetter
import pickle

try:
    import simplejson as json
except ImportError:
    import json


class JSONSerializable:
    serializable = True
    hidden = []

    def to_json(self):
        if self.serializable:
            o = self.__dict__
            for k in self.hidden:
                o.pop(k, None)
            return o
        else:
            return None


class IterableWrapper:
    iterable = None

    def __iter__(self):
        return getattr(self, self.iterable).__iter__()

    def __getitem__(self, item):
        return getattr(self, self.iterable).__getitem__(item)

    def __len__(self):
        return getattr(self, self.iterable).__len__()

    def __contains__(self, item):
        return getattr(self, self.iterable).__contains__(item)

    def __bool__(self):
        return True


class LineSet(JSONSerializable, IterableWrapper):
    iterable = 'lines'

    def __init__(self, *lines):
        self.lines = []

        for l in lines:
            self.lines.extend(l)

    def to_json(self):
        return self.lines

    def speakers(self) -> set:
        speakers = set()
        for line in self.lines:
            speakers |= line.speaker
        return speakers

    def filter(self, function, transform=identity):
        return LineSet(filter(function, map(transform, self.lines)))

    def map(self, function):
        return LineSet(map(function, self.lines))

    def by(self, char):
        if isinstance(char, str):
            char = {char}
        else:
            char = set(char)
        return self.filter(lambda l: char & l.speaker)

    def contain(self, search, transform=identity):
        if not callable(search):
            search = lambda l: search in l
        return self.filter(search, transform)

    @property
    def wc(self):
        return sum(map(attrgetter('wc'), self.lines))

    def __repr__(self):
        return self.lines.__repr__()


class PageParser:
    cache = 'cache'
    ttl = 360

    @classmethod
    def get_file(cls, url):
        path = cls._cache_path(url)
        try:
            last_modified = os.path.getmtime(path)
            if (time.time() - last_modified) // 60 < cls.ttl:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            r = requests.get(url)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            return r.text

    @classmethod
    def _cache_path(cls, url):
        return os.path.join(cls.cache, md5(url.encode('utf-8')).hexdigest())

    @classmethod
    def get_page(cls, url):
        # TODO: use pickle for caching
        return BeautifulSoup(cls.get_file(url), "lxml")

    @classmethod
    def clear_cache(cls, url):
        path = cls._cache_path(url)
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass

    @classmethod
    def clear_all_cache(cls):
        for f in os.scandir(cls.cache):
            os.unlink(f.path)

    @staticmethod
    def get_text(tag):
        if tag.string:
            return tag.string.strip()
        return ''.join(tag.find_all(string=True))


class ModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JSONSerializable):
            return o.to_json()
        if isinstance(o, (map, filter)):
            return list(o)
        if isinstance(o, set):
            return list(sorted(o))
        return super().default(o)


class Episode(PageParser, JSONSerializable, IterableWrapper):
    hidden = ['show', 'season']
    iterable = 'lines'

    def __init__(self, season=None, number=None, url=None, hydrate=None, show=None):
        self.lines = LineSet()
        self.season = season
        self.show = show or season.show

        if hydrate:
            self.hydrate(hydrate)
            return

        if url:
            self.load(url)
        else:
            self.title = None

        if number is None:
            number = len(season.episodes) + 1
        self.number = number

    def load(self, url):
        ret = self._parse(self.get_page(url))

        # TODO: There might be a better way to do this
        try:  # Try three value return format first
            self.title, lines, kwargs = ret
            for k, v in kwargs.items():
                setattr(self, k, v)
        except ValueError:  # If not, then assume only two values returned
            self.title, lines = ret

        self._add_lines(lines)
        return self

    def hydrate(self, data):
        for k, v in data.items():
            if k != 'lines':
                setattr(self, k, v)
            else:
                self._add_lines(v)

        return self

    def serialize(self):
        with open(self._filepath(), encoding='utf-8', mode='w') as f:
            json.dump(self, f, indent=4, cls=ModelEncoder)

    def _filepath(self):
        return os.path.join(self.season.storage_dir(), self._filename())

    def _filename(self, ext='json'):
        return str(self.number) + ' - ' + remove_special(self.title) + '.' + ext

    def _add_lines(self, lines):
        for line in lines:
            self.add_line(**line)

    def add_line(self, *args, **kwargs):
        kwargs['episode'] = self
        line = self.show.create_line(*args, **kwargs)
        self.lines.lines.append(line)
        return line

    # TODO: Consider splitting this into individual functions
    def _parse(self, ep):
        raise NotImplementedError

    def __repr__(self):
        return self.title


class Season(IterableWrapper):
    iterable = 'episodes'

    def __init__(self, order=None, name=None, show=None, urls=None, hydrate=False):
        self.show = show

        if order is None:
            order = len(show.seasons) + 1
        if name is None:
            name = order

        self.order = order
        self.name = name
        self.episodes = []

        if urls:
            self.load(urls)
        elif hydrate:
            self.hydrate()

    def load(self, episodes):
        for url in episodes:
            episode = self.show.create_episode(season=self, url=url)
            self.add_episode(episode)

    def serialize(self):
        if not os.path.exists(self.storage_dir()):
            os.mkdir(self.storage_dir())

        for episode in self.episodes:
            episode.serialize()

    def hydrate(self):
        files = os.scandir(self.storage_dir())
        for file in natsorted(files, key=attrgetter('path')):
            with open(file.path, encoding='utf-8') as f:
                data = json.load(f)
            self.create_episode(hydrate=data, season=self)

        return self

    def storage_dir(self):
        return os.path.join(self.show.storage_dir(), self.name)

    def create_episode(self, *args, **kwargs):
        episode = self.show.create_episode(*args, **kwargs)
        self.add_episode(episode)

    def add_episode(self, episode):
        self.episodes.append(episode)
        return episode

    @property
    def lines(self):
        return LineSet(*map(attrgetter('lines'), self.episodes))

    def episode(self, title):
        for episode in self.episodes:
            if episode.title == title:
                return episode

    def __repr__(self):
        return self.name


class Line(JSONSerializable, IterableWrapper):
    hidden = ['episode']
    iterable = 'text'

    def __init__(self, speaker, text, episode: Episode, number=None):
        self.episode = episode

        if number is None:
            number = len(episode.lines) + 1

        self.number = number
        self.text = self._parse_text(text, episode, number)

        if isinstance(speaker, str):
            self.speaker = self._parse_speaker(speaker, episode, number)
        else:
            self.speaker = set(speaker)

    def _parse_speaker(self, speaker, episode, number):
        raise NotImplementedError

    def _parse_text(self, text, episode, number) -> str:
        raise NotImplementedError

    @property
    def wc(self):
        return word_count(self.text)

    def __repr__(self):
        return ', '.join(self.speaker) + ': ' + self.text


class Show(PageParser, IterableWrapper):
    ttl = 60 * 24
    iterable = 'seasons'

    def __init__(self, url=None, hydrate=False, season=Season, episode=Episode, line=Line):
        self.seasons = []
        self.episode_class = episode
        self.season_class = season
        self.line_class = line

        if url:
            self.load(url)
        elif hydrate:
            self.hydrate()

    def create_episode(self, *args, **kwargs) -> Episode:
        return self.episode_class(*args, **kwargs)

    def create_season(self, *args, **kwargs) -> Season:
        return self.season_class(*args, **kwargs)

    def create_line(self, *args, **kwargs) -> Line:
        return self.line_class(*args, **kwargs)

    def add_season(self, *args, **kwargs) -> Season:
        season = self.create_season(*args, **kwargs)
        self.seasons.append(season)
        return season

    def load(self, url: str):
        seasons_page = self.get_page(url)
        seasons = self._parse(seasons_page, url)
        for name, episodes in seasons.items():
            self.add_season(name=name, show=self, urls=episodes)

    def storage_dir(self):
        return type(self).__name__.lower()

    def seasons_file(self):
        return os.path.join(self.storage_dir(), 'seasons.json')

    def _parse(self, page: BeautifulSoup, url: str):
        raise NotImplementedError

    def hydrate(self):
        with open(self.seasons_file(), encoding='utf-8') as f:
            seasons = json.load(f)
        for season in seasons:
            self.add_season(name=season, show=self, hydrate=True)

    def serialize(self):
        if not os.path.exists(self.storage_dir()):
            os.mkdir(self.storage_dir())

        with open(self.seasons_file(), encoding='utf-8', mode='w') as f:
            json.dump([s.name for s in self.seasons], f, indent=4)

        for season in self.seasons:
            season.serialize()

    @property
    def lines(self):
        return LineSet(*map(attrgetter('lines'), self.seasons))
