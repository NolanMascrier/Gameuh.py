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
    'firecone_trail': {
        'count': 4,
        'vel_range': (-2, 2),
        'color': [(255, 100, 0), (255, 150, 0), (255, 200, 50)],
        'size_range': (1, 4),
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
    'firecone_impact': {
        'count': 20,
        'vel_range': (3, 10),
        'color': [(255, 100, 0), (255, 150, 0), (255, 200, 50)],
        'size_range': (2, 7),
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
    },
    'arc_trail': {
        'count': 15,
        'vel_range': (-2, 2),
        'color': [(100, 200, 255), (150, 220, 255), (200, 230, 255)],
        'size_range': (3, 5),
        'life_range': (0.2, 0.8),
        'spread_angle': 45,
        'fade': True,
        'gravity': 0
    },
    'lightning_bolt_trail': {
        'count': 5,
        'vel_range': (-1, 1),
        'color': [(255, 255, 40), (255, 255, 100), (255, 255, 200)],
        'size_range': (0.5, 2),
        'life_range': (0.1, 0.3),
        'spread_angle': 360,
        'fade': False,
        'gravity': 0
    }
}