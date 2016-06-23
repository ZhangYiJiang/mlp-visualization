# Visualizing My Little Pony: Friendship is Magic

This is a set of Python scripts that contains several classes (contained in `models.py`)
to help scrape, cache, process and store television show transcripts. The classes
are fairly flexible and exposes a simple but powerful API that allows them to be
extended for use in any TV show.

To demonstrate a use of them, `mlp_models.py` contains the classes extended for use
with My Little Pony's transcript from http://mlp.wikia.com/wiki/My_Little_Pony_Friendship_is_Magic_Wiki.
Full documentation is forthcoming, but here's a demonstration of the classes in
action:

    from mlp_modules import MLP

    # Scrapes episode listing from wiki. The episodes are then scraped and parsed
    # into lines
    mlp = MLP(url='http://mlp.wikia.com/wiki/Episodes')

    len(mlp.lines) # Count the number of lines in total from the show...
    len(mlp.seasons[0].lines)  # ... a single season...
    len(mlp.seasons[1].episode('Lesson Zero').lines)  # or an episode

    # Characters are represented by sets of strings. Here we grab Twilight and Applejack
    # to use as a filter
    from filters import ts, aj

    # The first ten lines spoken by Twilight Sparkle
    mlp.lines.by(ts)[:10]

    # The first ten lines spoken by either AJ or Twilight from the episode
    # 'The Mane Attraction'
    mlp.seasons[4].episode('The Mane Attraction').by(ts | aj)[:10]