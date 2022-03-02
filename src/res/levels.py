tile_size = 32 #Tile size used as a base to construct the map
room_num = 5

"""
    The following variable consist of a list of strings that sets the layout for the map
    that we want to draw:

    'X' -> bottom and top walls
    'P' -> player spawn.
    'F' -> floor
    'L' -> left wall
    'R' -> right wall
    'K' -> top right intersection
    'J' -> top left intersection
    'H' -> bottom left intersection
    'G' -> bottom right intersection

    For now we're using the same sprite for each type of wall
"""

# player -> p
# enemy basic0 -> w (worm)
# enemy basic1 -> r (rabbit)
# enemy basic2 -> m (magic range)
# enemy normal2 -> t (tracked)

basic_layout = [
    '                                                                       ',
    '            JXXXXXXXXK                                                 ',
    '            LFFFFFFFFR                                                 ',
    '            LFFFFFFFFR                                                 ',
    '            LFPFFFFFFR                                                 ',
    '            LFFFFFFFFRJXXXXXXXXK                                       ',
    '            LFFFFFFFFHGFFFFFFFFH                                       ',
    '            LFFFFFFFFFFFFFFFFFFD                                       ',
    '            LFFFFFFFFJKFFFFFFFFJ                                       ',
    '            LFFFFFFFFRLFFFFFFFFR                                       ',
    '            LFFFFFFFFRLFFFFFFFFR                                       ',
    '            LFFFFFFFFRLFFFFFFFFR                                       ',
    '            LFFFFFFFFRLFFFFFFFFR                                       ',
    '            HXXXXXXXXGLFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      GFFFFFFFFH                                       ',
    '                      DFFFFFFFFD                                       ',
    '                      KFFFFFFFFJ                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      LFFFFFFFFH                                       ',
    '                      LFFFFFFFFD                                       ',
    '                      LFFFFFFFFJ                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      GFFFFFFFFR                                       ',
    '                      DFFFFFFFFR                                       ',
    '                      KFFFFFFFFR                                       ',
    '                      LFFFFFFFFR                                       ',
    '                      HXXXXXXXXG                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
    '                                                                       ',
]

rooms = [
    [
        'XXXXX',
        'XFFFX',
        'XFFFD',
        'XFFFX',
        'XFFFX',
        'XXXXX',
    ],
    [
        'XXXXXXX',
        'XFFFFFX',
        'XFFFFFD',
        'XFFFFFX',
        'XXXXXXX',
    ],
    [
        'XXXXXXXXXXXX',
        'XFFFFFFFFFFX',
        'XFFWFFFFFFFX',
        'XFFFRFFFFFFX',
        'XFFFFMFFFFFX',
        'XFFFFFTFFFFD',
        'XFFFFFFFFFFX',
        'XFFFFFFFFFFX',
        'XFFFFFFFFFFX',
        'XFFFFFFFFFFX',
        'XXXXXXXXXXXX',
    ],
    [
        'XXXXXXXXXXXXXXXXXXXXX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFD',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XXXXXXXXXXXXXXXXXXXXX',
    ],
    [
        'XXXXXXXXXXXXXXXXXXXXX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFD',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XFFFFFFFFFFFFFFFFFFFX',
        'XXXXXXXXXXXXXXXXXXXXX',
    ]
]
