"""Fixed, connected maps with walls, landmarks, and a portal."""
from ui import say
from encounters import visible_monster
MAPS = {
    'valley': (
        '###############',
        '#@.E..#....M...#',
        '#.....#.......#',
        '#..A......S...#',
        '###.#####.###.#',
        '#...R.....>...#',
        '###############',
    ),
    'summit': (
        '#############',
        '#<....#....B#',
        '#.##..#.##..#',
        '#..T.....#..#',
        '####.##..#..#',
        '#....H......#',
        '#############',
    ),
}

def tile(player, x=None, y=None):
    x = player.x if x is None else x
    y = player.y if y is None else y
    rows = MAPS[player.map_name]
    if y < 0 or y >= len(rows) or x < 0 or x >= len(rows[y]):
        return '#'
    return rows[y][x]

def draw(player):
    say(f'── {player.map_name.upper()} ──')
    for y, row in enumerate(MAPS[player.map_name]):
        line = ''
        for x, ch in enumerate(row):
            spawn = visible_monster(player, x, y)
            if (x, y) == (player.x, player.y):
                line += '@'
            elif spawn:
                line += spawn[0]
            else:
                line += '.' if ch == '@' else ch
        say(line)
    say('@ you | # wall | E/M/A/R/T people | S shop | H beacon | B boss | </> travel')
    say('Monsters: 1 Drizzle Slime | 2 Gust Wolf | 3 Hail Golem | 4 Thunder Wraith')
    say('Step onto a person, monster, or landmark to interact automatically.')


def move(player, direction):
    dx, dy = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}[direction]
    x, y = player.x + dx, player.y + dy
    if tile(player, x, y) == '#':
        say('A cliff or wall blocks the way.', 'bad')
        return False
    player.x, player.y = x, y
    return True
