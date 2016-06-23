import re
from models import Show, Season, Episode, Line
from urllib.parse import urldefrag, urljoin
from filters import what_is_all, what_is_rest, antagonists, princesses, adjectives, name_replace, small_bad, set_replace
from bs4 import BeautifulSoup
from ordered_set import OrderedSet
from collections import OrderedDict


class MLPEpisode(Episode):
    def _parse(self, ep):
        title = ep.select('#WikiaPageHeader h1')[0].string
        title = title.split('/')[-1]
        title = title.replace('My Little Pony', '')
        title = re.sub(r'\([^\)]+\)', '', title)
        title = title.strip()

        main = ep.find(id='WikiaArticle')
        lines = []

        for dialog in main.select('#mw-content-text > dl'):
            for dd in dialog.children:
                try:
                    # For some reason some lines are empty. We ignore those
                    if not self.get_text(dd).strip():
                        continue

                    # Replace italics with * (Markdown syntax)
                    for i in dd('i'):
                        i.replace_with('*' + self.get_text(i) + '*')

                    # Sometimes there are songs here
                    if dd.dl:
                        if dd.b:
                            speaker = self.get_text(dd.b).strip()
                        else:
                            # Some songs continue from spoken lines, so the speaker is
                            # omitted in the markup
                            speaker = lines[-1]['speaker']

                        lines.append({
                            'speaker': speaker,
                            'text': '\n'.join(self.get_text(d).strip() for d in dd.dl.children),
                            'song': True
                        })
                    else:
                        line_text = self.get_text(dd).strip()

                        # Some lines are purely stage action or sounds. Catch those since
                        # they have no speaker
                        if line_text.startswith('[') and line_text.endswith(']'):
                            speaker = 'action'
                        elif not dd.b:
                            # If there is no speaker, we assume it's continuing from
                            # the previous line (this usually happens with friendship
                            # letters)
                            speaker = lines[-1]['speaker']
                        else:
                            speaker, line_text = line_text.split(':', 1)

                        lines.append({
                            'speaker': speaker.strip(),
                            'text': line_text.strip()
                        })
                except Exception as e:
                    print(e)
                    print('Died on: ' + self.get_text(dd))

        return title, lines


class MLPSeason(Season):
    def __init__(self, order=None, name=None, show=None, urls=None, hydrate=False):
        # Make seasons always titlecase
        if name:
            name = name.title()

        super().__init__(order, name, show, urls, hydrate)

        if 'season' in self.name.lower():
            self.code = self.order
        else:
            self.code = 'eqg'


class MLPLine(Line):
    def __init__(self, speaker, text, episode, number=None, song=False):
        super().__init__(speaker, text, episode, number)
        self.song = song

    def is_princess(self) -> bool:
        """Returns true if the character is a princess"""
        for name in self.speaker:
            if name in princesses:
                return True

            # Check for Twilight's ascension
            season = self.episode.season.code
            ep = self.episode.number

            if name == 'Twilight Sparkle':
                if season == 'eqg':
                    return True
                if season > 3:
                    return True
                if season == 3 and ep == 13 and self.number > 118:
                    return True
        return False

    def is_bad(self) -> bool:
        """Returns true if the character is a bad guy"""
        for name in self.speaker:
            if name in antagonists or name in small_bad:
                return True

            season = self.episode.season.code
            ep = self.episode.number

            if name == 'Trixie':
                if season == 'eqg':
                    return False
                if season <= 3:
                    return True
                if season == 3 and ep == 5 and self.number < 270:
                    return True
            if name == 'Gilda':
                if season < 5:
                    return True
        return False

    def is_antagonist(self) -> bool:
        """Returns true if the character is a big bad"""
        for name in self.speaker:
            if name in antagonists:
                return True

            season = self.episode.season.code
            ep = self.episode.number

            if name == 'Discord':
                if season > 3:
                    return False  # Discord Redemption in Keep Calm and Flutter On
                if season == 3 and ep == 10 and self.number > 246:
                    return False
                return True

            if name == 'Sunset Shimmer':
                if ep == 1:
                    return True

            if name == 'Starlight Glimmer':
                if season > 5:
                    return False
                return True

            if name == 'Princess Cadance':
                if season == 2 and ep == 25:
                    if self.number < 80:  # Flashback
                        return False
                    else:
                        return True
                if season == 2 and ep == 26:
                    if self.number < 25:
                        return True

        return False

    def is_action(self):
        return not bool(self.without_action(self.text))

    @staticmethod
    def without_action(text):
        return re.sub(r'\[[^\]]*\]\s*', '', text).strip()

    def _parse_speaker(self, text, episode, number) -> set:
        # Remove symbols
        text = re.sub(r'[\[\]:"\'.]+', '', text)
        # Remove things in brackets
        text = re.sub(r'\s?\([^)]+\)', '', text)

        # Bail if 'all' or 'rest' is found
        episode = self.episode.title
        if 'All' in text and episode in what_is_all:
            return what_is_all[episode]
        elif 'Rest of main cast' in text and episode in what_is_rest:
            return what_is_rest[episode]

        # Split along the word 'and'
        names = filter(None, re.split(r'\s*(?:,|\band\b)\s*', text))

        ret = []
        for name in names:
            for a in adjectives:
                name = re.sub(r'\b' + a + r'\b', '', name)

            if 'Pinkie Pie' in name:
                name = 'Pinkie Pie'  # To handle all the duplicate Pinkies

            if 'Changeling' in name:
                name = 'Changeling'

            name = name.strip()

            for s, r in name_replace.items():
                if name == s:
                    name = r

            for s, r in set_replace.items():
                if name in s:
                    ret.extend(r)
                    break
            else:
                ret.append(name)

        return set(ret)

    def _parse_text(self, text, episode, number) -> str:
        return text


class MLP(Show):
    def __init__(self, url=None, hydrate=False, season=MLPSeason, episode=MLPEpisode, line=MLPLine):
        super().__init__(url, hydrate, season, episode, line)

    def storage_dir(self):
        return 'result'

    def _parse(self, page: BeautifulSoup, url):
        seasons = OrderedDict()
        eqg = OrderedSet()

        child = page.select_one('#WikiaArticle h2')
        season = child.text

        while child.next_sibling:
            child = child.next_sibling

            if child.name == 'table':
                for a in child.find_all('a', string='Transcript'):
                    if not a.has_attr('class') or 'new' not in a['class']:
                        episode_url, fragment = urldefrag(a['href'])
                        episode_url = urljoin(url, episode_url)
                        if 'Equestria Girls' not in season:
                            if season not in seasons:
                                seasons[season] = OrderedSet()
                            seasons[season].append(episode_url)
                        else:
                            eqg.append(episode_url)
                continue

            if child.name == 'h2':
                season = child.text
                continue

        seasons['Equestria Girls'] = eqg
        return seasons
