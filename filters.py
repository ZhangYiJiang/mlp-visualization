# Character sets
# Mane 6 + Sunset (for the Equestria Girls)
ts = {'Twilight Sparkle'}
aj = {'Applejack'}
fs = {'Fluttershy'}
rd = {'Rainbow Dash'}
ra = {'Rarity'}
pp = {'Pinkie Pie'}
ss = {'Sunset Shimmer'}

mane_6 = ts | aj | fs | rd | ra | pp
mane_7 = mane_6 | {'Spike'}
princesses = {'Princess Celestia', 'Princess Luna', 'Princess Cadance', }
cmc = {'Apple Bloom', 'Sweetie Belle', 'Scootaloo', }

apples = {'Apple Bloom', 'Granny Smith', 'Big McIntosh', 'Applejack', }
pies = {'Pinkie Pie', 'Maud Pie', 'Igneous Rock', 'Cloudy Quartz', 'Limestone Pie', 'Marble Pie', }
cakes = {'Mr Cake', 'Mrs Cake', 'Pumpkin Cake', 'Pound Cake', }

antagonists = {'Nightmare Moon', 'Queen Chrysalis', 'King Sombra', 'Lord Tirek', 'Adagio Dazzle', 'Sonata Dusk',
               'Aria Blaze', 'Midnight Sparkle', }

small_bad = {'Flim', 'Flam', 'Mane-iac', 'Suri Polomare', 'Diamond Tiara', 'Dr Caballeron', 'Ahuizotl', 'Garble',
             'Hoops', 'Dumb-Bell', 'Score', 'Rover', 'Fido', 'Spot', }

# These are the main characters, whose classes are used in every episode
classes = {
    'Twilight Sparkle': 'ts',
    'Sci-Twi': 'ts',

    'Pinkie Pie': 'pp',
    'Rarity': 'r',
    'Rainbow Dash': 'rd',
    'Applejack': 'aj',
    'Fluttershy': 'fs',

    'Spike': 's',
    'Sunset Shimmer': 'su',

    'Apple Bloom': 'ab',
    'Sweetie Belle': 'sb',
    'Scootaloo': 'sc',

    'Princess Celestia': 'pc',
    'Princess Luna': 'pl',
    'Princess Cadance': 'ca'
}

legends = [
    ('Mane 8', mane_7 | ss),
    ('CMC', cmc),
    ('Princesses', princesses),
]


# Remapping characters for minor characters
char_map = {
    # Diamond dogs
    ('Rover', 'Fido', 'Spot'): 'dg',
    # Snips and snails
    ('Snips', 'Snails'): 'sn',
    # Spa ponies
    ('Aloe', 'Lotus Blossom'): 'spa',
    # Ponytones
    ('Toe-Tapper', 'Torch Song'): 'pt',
    # Wonderbolts
    ('Soarin', 'Spitfire', 'Fleetfoot', 'Misty Fly',): 'wb',
    # Our Town townsfolks
    ('Sugar Belle', 'Double Diamond', 'Party Favor', 'Night Glider', 'Citizens', ): 'ot',
    # Method Mares
    ('On Stage', 'Raspberry Beret', 'Late Show', 'Stardom',): 'mms',
    # Pie Family
    tuple(pies - pp): 'pf',
    # Shy family
    ('Mr Shy', 'Mrs Shy'): 'fsf',
}

# CSS classes to be used
special_char = {
    'Friendship is Magic, part 1': {'Narrator': 'na'},
    'Griffon the Brush Off': {'Gilda': 'gi'},
    'Boast Busters': {
        'Trixie': 'tx',
        'Snips and Snails': 'sn'
    },
    'Bridle Gossip': {'Zecora': 'z'},
    'Winter Wrap Up': {'Mayor Mare': 'mm'},
    'Call of the Cutie': {
        'Cheerilee': 'ch',
        'Diamond Tiara': 'dt',
        'Silver Spoon': 'ss'
    },
    'A Dog and Pony Show': {'Diamond Dogs': 'dg'},

    # Season Two
    'The Cutie Pox': {'Zecora': 'z'},
    'Sweet and Elite': {'Fancy Pants': 'fp'},
    'Family Appreciation Day': {
        'Cheerilee': 'ch',
        'Granny Smith': 'gs',
        'Diamond Tiara': 'dt',
    },
    'The Super Speedy Cider Squeezy 6000': {
        'Flim': 'fi',
        'Flam': 'fa',
        'Granny Smith': 'gs',
    },
    'Read It and Weep': {
        'Daring Do': 'dd',
        'Doctor Horse': 'dh',
    },
    'Hearts and Hooves Day': {
        'Cheerilee': 'ch',
        'Big McIntosh': 'bm'
    },
    'A Friend in Deed': {'Cranky Doodle Donkey': 'cr'},
    'Putting Your Hoof Down': {'Iron Will': 'iw'},
    'Dragon Quest': {'Garble': 'ga'},
    'Ponyville Confidential': {
        'Diamond Tiara': 'dt',
        'Cheerilee': 'ch'
    },

    'A Canterlot Wedding - Part 1': {
        'Shining Armor': 'sa'
    },

    'A Canterlot Wedding - Part 2': {
        'Shining Armor': 'sa'
    },

    # Season Three
    'The Crystal Empire - Part 1': {
        'Shining Armor': 'sa'
    },

    'One Bad Apple': {
        'Diamond Tiara': 'dt',
        'Silver Spoon': 'ss',
        'Babs Seed': 'bs'
    },

    'Magic Duel': {
        'Trixie': 'tx',
        'Zecora': 'z'
    },

    'Wonderbolts Academy': {
        'Lightning Dust': 'ld',
        'Spitfire': 'sf'
    },

    'Apple Family Reunion': {
        'Babs Seed': 'bs',
        'Granny Smith': 'gs'
    },

    'Games Ponies Play': {
        'Ms Harshwhinny': 'hw',
        'Ms Peachbottom': 'pb',
        'Shining Armor': 'sa'
    },

    'Flight to the Finish': {
        'Ms Harshwhinny': 'hw',
        'Diamond Tiara': 'dt',
        'Silver Spoon': 'ss',
    },

    # Season Four
    'Princess Twilight Sparkle - Part 1': {
        'Discord': 'd'
    },

    'Princess Twilight Sparkle - Part 2': {
        'Discord': 'd'
    },

    'Power Ponies': {'Mane-iac': 'mi'},
    "Daring Don't": {
        'Daring Do': 'dd',
        'AK Yearling': 'dd',
        'Ahuizotl': 'az',
    },

    'Rarity Takes Manehattan': {
        'Suri Polomare': 'sp',
        'Prim Hemline': 'ph'
    },

    'Pinkie Apple Pie': {
        'Big McIntosh': 'bm',
        'Granny Smith': 'gs',
        'Goldie Delicious': 'gd',
    },

    'Rainbow Falls': {
        'Wonderbolts': 'wb',
    },

    'Twilight Time': {
        'Diamond Tiara': 'dt',
        'Silver Spoon': 'ss',
    },

    'Filli Vanilli': {
        'Ponytones': 'pt',
        'Big McIntosh': 'bm',
    },

    "It Ain't Easy Being Breezies": {'Seabreeze': 'sz'},
    "Three's A Crowd": {'Discord': 'd'},
    'Pinkie Pride': {'Cheese Sandwich': 'cs'},
    'Simple Ways': {'Trenderhoof': 'th'},
    'Maud Pie': {'Maud Pie': 'mp'},

    'Leap of Faith': {
        'Flim': 'fi',
        'Flam': 'fa',
        'Granny Smith': 'gs'
    },

    "Twilight's Kingdom - Part 1": {
        'Discord': 'd',
    },

    "Twilight's Kingdom - Part 2": {
        'Discord': 'd',
    },

    # Season Five
    'The Cutie Map - Part 1': {
        'Townsfolk': 'ot',
    },

    'The Cutie Map - Part 2': {
        'Townsfolk': 'ot',
    },

    'Make New Friends but Keep Discord': {
        'Discord': 'd',
        'Tree Hugger': 'tre'
    },

    "Appleoosa's Most Wanted": {
        'Trouble Shoes': 'trs',
        'Sheriff Silverstar': 'sss',
    },

    'The Lost Treasure of Griffonstone': {'Gilda': 'gi'},
    'Amending Fences': {
        'Moon Dancer': 'md',
        'Minuette': 'mn',
        'Lemon Hearts': 'lh',
        'Twinkleshine': 'tw',
    },

    'Canterlot Boutique': {'Sassy Saddles': 'ss'},
    'Rarity Investigates!': {
        'The Wonderbolts': 'wb',
        'Wind Rider': 'wr',
    },

    'What About Discord?': {'Discord': 'd'},

    'Made in Manehattan': {
        'Coco Pommel': 'cp',
        'Method Mares': 'mms',
    },

    'Party Pooped': {
        'Prince Rutherford': 'prf',
    },

    'Brotherhooves Social': {
        'Big McIntosh': 'bm',
        'Granny Smith': 'gs'
    },

    'Princess Spike': {
        'Fancy Pants': 'fp',
    },

    'Hearthbreakers': {
        'Pie Family': 'pf',
        'Granny Smith': 'gs',
    },

    'The Hooffields and McColts': {
        'Hooffields': 'hf',
        'McColts': 'mc',
    },

    'Crusaders of the Lost Mark': {
        'Diamond Tiara': 'dt',
        'Silver Spoon': 'ss',
    },

    'The Mane Attraction': {
        'Coloratura': 'ct',
        'Svengallop': 'sv',
    },

    # Season Six
    'The Crystalling - Part 1': {
        'Shining Armor': 'sa',
        'Starlight Glimmer': 'sg',
        'Sunburst': 'st',
    },

    'The Crystalling - Part 2': {
        'Shining Armor': 'sa',
        'Starlight Glimmer': 'sg',
        'Sunburst': 'st',
    },

    'The Gift of the Maud Pie': {
        'Maud Pie': 'mp',
    },

    'Gauntlet of Fire': {
        'Princess Ember': 'pe',
        'Garble': 'ga',
        'Dragon Lord Torch': 'tor',
    },

    'Newbie Dash': {
        'The Wonderbolts': 'wb',
    },

    'No Second Prances': {
        'Trixie': 'tx',
        'Starlight Glimmer': 'sg',
    },

    "A Hearth's Warming Tail": {
        'Starlight Glimmer': 'sg',
    },

    'Applejack\'s "Day" Off': {
        'Aloe and Lotus': 'spa',
    },

    'Flutter Brutter': {
        'Zephyr Breeze': 'zb',
        'Mr and Mrs Shy': 'fsf',
    },

    'Spice Up Your Life': {
        'Coriander Cumin': 'cc',
        'Saffron Masala': 'sm',
        'Zesty Gourmand': 'zg',
    },

    # Equestria Girls
    "Equestria Girls: Friendship Games": {

    }
}

# Adjectives to strip out of speaker names
adjectives = ('Filly', 'Younger', 'Young', 'Future', 'Old', 'Pond', 'Past', 'Baby', 'Countess')

# Mapping of names to their replacement used by the speaker parser to ensure consistency
name_replace = {
    'Twilight': 'Twilight Sparkle',
    'Pinkie': 'Pinkie Pie',
    '3': 'Pinkie Pie',  # 'Pinkies 3 and 4'
    '4': 'Pinkie Pie',  # - from Too Many Pinkies
    'Rarity to Opal': 'Rarity',
    'Lady Rarity': 'Rarity',
    'Trixie Lulamoon': 'Trixie',
    'Maud': 'Maud Pie',
    'Sweetie Drops': 'Bon Bon',
    'Princesses Celestia': 'Princess Celestia',  # 'Princesses Celestia, Luna and Cadance'
    'Luna': 'Princess Luna',
    'Cadance': 'Princess Cadance',
    'Big Mac': 'Big McIntosh',
    'Mr': 'Mr Cake',  # 'Mr and Mrs Cake'
    'Ahuizotl with Fluttershys voice': 'Fluttershy',
    'At the same time Applejack': 'Applejack',
    'Stephen Magnet': 'Steven Magnet',  # His credited name in Slice of Life
    'Principal Celestia': 'Princess Celestia',
    'Vice Principal Luna': 'Princess Luna',
    'Train conductor': 'Train Conductor',
    'Cranky': 'Cranky Doodle Donkey'
}

set_replace = {
    ('Mane Six', 'Main Six', 'Main cast', 'Main Cast', 'Main cast sans Spike',
     'All ponies', 'the Rainbooms', 'Rainbooms', 'The Rainbooms'): mane_6,
    ('The Ponytones', 'The Pony Tones'): ('Rarity', 'Big McIntosh', 'Torch Song', 'Toe-Tapper'),
    ('Main 6 sans Twilight', 'Main cast bar Twilight', 'Main cast sans Twilight',
     'Everyone but Twilight', 'All except Twilight'): mane_6 - ts,
    ('Main cast sans Pinkie',): mane_6 - pp,
    ('Main cast sans Rainbow Dash',): mane_6 - rd,
    ('Main cast sans Fluttershy', 'All except Fluttershy'): mane_6 - fs,
    ('Main cast sans Rarity', 'All but Rarity', 'All sans Rarity'): mane_6 - ra,
    ('The cast',): mane_6 | ss,
    ('Cutie Mark Crusaders', 'Crusaders'): cmc,
    ('Apple family',): apples,
    ('The Dazzlings',): ('Adagio Dazzle', 'Sonata Dusk', 'Aria Blaze'),
    ('The Illusions',): ('Trixie', 'The Illusions')  # The other band members are unnamed
}

# There's a lot of dialog attributed to 'all' in the show
# turns out this value is different for each episode, hence this
# dict to hold the mapping
what_is_all = {
    'Castle Sweet Castle': mane_6 - ts,
    'Pinkie Apple Pie': apples | pp,
    'The Show Stoppers': cmc,
    'My Little Pony Equestria Girls': mane_6,
    'Suited For Success': mane_6 - ra,
    'The Best Night Ever': mane_6,
    'The Crystal Empire - Part 1': mane_6,
    "Twilight's Kingdom - Part 2": mane_6
}

what_is_rest = {
    'A Canterlot Wedding - Part 1': mane_6 - (ts | aj),
    'Bats!': mane_6 - ts,
    'Do Princesses Dream of Magic Sheep': mane_6 - fs,
    'Filli Vanilli': mane_6 - fs,
    "It Ain't Easy Being Breezies": mane_6 - fs,
    'Keep Calm and Flutter On': mane_6 - ts,
    'Maud Pie': mane_6 - aj,
    'MMMystery on the Friendship Express': mane_6 - pp,
    'My Little Pony Equestria Girls Rainbow Rocks': mane_6,
    'Sweet and Elite': mane_6 - ra,
    'The Super Speedy Cider Squeezy 6000': mane_6,
    'Wonderbolts Academy': mane_6 - rd
}