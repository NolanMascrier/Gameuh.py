"""Store particles data."""

PARTICLE_CONFIGS = {
    'firebolt_trail': {
        'count': 8,
        'vel_range': (-2, 2),
        'color': [(255, 100, 0), (255, 150, 0), (255, 200, 50)],
        'size_range': (1, 5),
        'life_range': (0.2, 0.8),
        'spread_angle': 360,
        'fade': True,
        'gravity': 0
    },
    'voidbolt_trail': {
        'count': 12,
        'vel_range': (-1.5, 1.5),
        'color': [(32, 5, 115), (84, 17, 171), (134, 56, 186)],
        'size_range': (1, 3),
        'life_range': (0.1, 0.4),
        'spread_angle': 360,
        'fade': True,
        'gravity': 0
    },
    'firebolt_impact': {
        'count': 40,
        'vel_range': (3, 10),
        'color': [(255, 100, 0), (255, 150, 0), (255, 200, 50)],
        'size_range': (2, 8),
        'life_range': (0.3, 0.8),
        'spread_angle': 360,
        'fade': True,
        'gravity': 0.3
    },
    'arc_line': {
        'count': 30,
        'color': [(100, 200, 255), (150, 220, 255), (200, 230, 255)],
        'size_range': (2, 5),
        'life_range': (0.1, 0.2),
        'fade': True
    }
}
