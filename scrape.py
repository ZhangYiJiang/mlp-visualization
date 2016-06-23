from mlp_models import MLP, MLPSeason


class MLPScraperSeason(MLPSeason):
    def add_episode(self, episode):
        super().add_episode(episode)
        print(episode.title)

mlp = MLP(url='http://mlp.wikia.com/wiki/Episodes', season=MLPScraperSeason)
mlp.serialize()
