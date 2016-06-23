from mlp_models import MLP, MLPLine
from models import ModelEncoder
from mako.template import Template
import os
import filters

try:
    import simplejson as json
except ImportError:
    import json


class MLPVisualizationLine(MLPLine):
    def _parse_text(self, text, episode, number):
        return self.without_action(super()._parse_text(text, episode, number))

    def classname(self):
        class_map = {**filters.classes, **filters.special_char.get(self.episode.title, {})}
        classes = set()

        for char in self.speaker:
            if char in class_map:
                classes.add(class_map[char])
                continue

            for char_sets, classname in filters.char_map.items():
                if char in char_sets and classname in class_map.values():
                    classes.add(classname)
                    break

            if 'Hooffield' in char:
                classes.add('hf')
            if 'McColt' in char:
                classes.add('mc')

        if self.song:
            classes.add('so')

        if self.is_antagonist():
            classes.add('a')

        return ' '.join(classes)

output_prefix = 'web'
visualization = MLP(hydrate=True, line=MLPVisualizationLine)
template = Template(filename='template.mako')

with open(os.path.join(output_prefix, "index.html"), encoding="utf-8", mode="w") as f:
    f.write(template.render(seasons=visualization.seasons))

transcript = MLP(hydrate=True)
for season in transcript.seasons:
    path = os.path.join(output_prefix, str(season.code) + '.json')
    with open(path, encoding="utf-8", mode="w") as f:
        data = map(lambda ep: ep.lines.filter(lambda l: not l.is_action()), season.episodes)
        json.dump(list(data), f, cls=ModelEncoder)
