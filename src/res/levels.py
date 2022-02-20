tile_size = 32 #Tile size used as a base to construct the level
room_num = 3

"""
    The following variable consist of a list of strings that sets the layout for the level
    that we want to draw, 'X' represent the walls and the 'P' represents the player spawn.
"""

level_test = [
    '                       ',
    '                       ',
    '          XXXXX        ',
    '          X   X        ',
    '          X   X        ',
    '          X   XXXXXX   ',
    '  XXXXXXXXX   X    X   ',
    '  X       X   X    X   ',
    '  X                X   ',
    '  X       X   XXXXXX   ',
    '  XXXXXXXXX   X        ',
    '          X   XXXXXXX  ',
    '          X   X P   X  ',
    '          X   X     X  ',
    '      XXXXX         X  ',
    '      X   X   X     X  ',
    '      X       X     X  ',
    '      X   X   XXXXXXX  ',
    '      X   X   X        ',
    '      XXXXXXXXX        ',
    '                       ',
    '                       ',
]

basic_layout = [
    '                        ',
    '                        ',
    '          XXXXXX        ',
    '          X    X        ',
    '          X    X        ',
    '          X    X        ',
    '          X    X        ',
    '          X    X        ',
    '          D    D        ',
    '          X    X        ',
    '          X    X        ',
    '          X    XXXXXXX  ',
    '          X    XXP   X  ',
    '          X    XX    X  ',
    '          X          X  ',
    '          X    XX    X  ',
    '          D    XX    X  ',
    '          X    XXXXXXX  ',
    '          X    X        ',
    '          XXXXXX        ',
    '                        ',
    '                        ',
]

rooms = [
    [
        'XXXXX',
        'X   X',
        'X   D',
        'X   X',
        'X   X',
        'XXXXX',
    ],
    [
        'XXXXXXX',
        'X     X',
        'X     D',
        'X     X',
        'XXXXXXX',
    ],
    [
        'XXXXXXXXXX',
        'X        X',
        'X        D',
        'X        X',
        'XXXXXXXXXX',
    ]
]
