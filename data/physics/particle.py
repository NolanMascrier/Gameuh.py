"""Particle system for visual effects."""

import math

import numpy as np
from data.api.vec2d import Vec2
from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PARTICULE_TRACKER, SYSTEM

class Particle:
    """Single particle instance."""
    __slots__ = ('pos', 'vel', 'color', 'size', 'life', 'max_life', 'fade', 'gravity')

    def __init__(self, x, y, vx, vy, color, size, life, fade=True, gravity=0):
        self.pos = Vec2(x, y)
        self.vel = Vec2(vx, vy)
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.fade = fade
        self.gravity = gravity

    def tick(self):
        """Update particle state."""
        self.pos += self.vel
        if self.gravity:
            self.vel.y += self.gravity
        self.life -= 0.016
        return self.life > 0

    def get_alpha(self):
        """Calculate alpha based on lifetime."""
        if not self.fade:
            return 255
        return int(255 * (self.life / self.max_life))

    def is_on_screen(self):
        """Check if particle is visible."""
        if "level" not in SYSTEM or SYSTEM["level"] is None:
            return True
        camera_x, camera_y = SYSTEM["level"].map.camera_offset
        screen_x = self.pos.x - camera_x
        screen_y = self.pos.y - camera_y
        return -50 <= screen_x <= SCREEN_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50

class Segment:
    """Line segment for arc effects."""
    __slots__ = ('start', 'end')

    def __init__(self, x1, y1, x2, y2):
        self.start = Vec2(x1, y1)
        self.end = Vec2(x2, y2)


class ParticleEmitter:
    """Manages a collection of particles."""
    __slots__ = ('_particles', '_max_particles', '_enabled')

    def __init__(self, max_particles=1000):
        self._particles = []
        self._max_particles = max_particles
        self._enabled = True

    def emit(self, x, y, count, vel_range, color, size_range, life_range,
             spread_angle=360, fade=True, gravity=0):
        """Emit particles from a point.

        Args:
            x, y: Origin position
            count: Number of particles to spawn
            vel_range: (min_speed, max_speed)
            color: (r, g, b) or list of colors
            size_range: (min_size, max_size)
            life_range: (min_life, max_life)
            spread_angle: Cone angle in degrees (360 = full circle)
            fade: Whether particles fade out
            gravity: Gravity effect on y-velocity
        """
        if not self._enabled:
            return
        if len(self._particles) >= self._max_particles:
            return
        count = min(count, self._max_particles - len(self._particles))
        for _ in range(count):
            angle = np.random.uniform(0, spread_angle) * np.pi / 180
            speed = np.random.uniform(*vel_range)
            vx = np.cos(angle) * speed
            vy = np.sin(angle) * speed
            if isinstance(color, list):
                particle_color = color[np.random.randint(0, len(color))]
            else:
                particle_color = color
            size = np.random.uniform(*size_range)
            life = np.random.uniform(*life_range)
            particle = Particle(x, y, vx, vy, particle_color, size, life, fade, gravity)
            self._particles.append(particle)

    def emit_line(self, x1, y1, x2, y2, particle_count, color, size_range,
                  life_range, fade=True):
        """Emit particles along a line (for arc effect).

        Args:
            x1, y1, x2, y2: Line endpoints
            particle_count: Number of particles along the line
            color: Base color or list of colors
            size_range: (min_size, max_size)
            life_range: (min_life, max_life)
            fade: Whether particles fade out
        """
        if not self._enabled:
            return
        if len(self._particles) >= self._max_particles:
            return
        count = min(particle_count, self._max_particles - len(self._particles))
        for i in range(count):
            t = i / max(1, count - 1)
            jitter = np.random.uniform(-0.05, 0.05)
            t = max(0, min(1, t + jitter))
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx*dx + dy*dy)
            if length > 0:
                perp_x = -dy / length
                perp_y = dx / length
                offset = np.random.uniform(-3, 3)
                x += perp_x * offset
                y += perp_y * offset
            vx = np.random.uniform(-0.5, 0.5)
            vy = np.random.uniform(-0.5, 0.5)
            if isinstance(color, list):
                particle_color = color[np.random.randint(0, len(color))]
            else:
                particle_color = color
            size = np.random.uniform(*size_range)
            life = np.random.uniform(*life_range)
            particle = Particle(x, y, vx, vy, particle_color, size, life, fade, 0)
            self._particles.append(particle)

    def tick(self):
        """Update all particles."""
        if not self._enabled:
            self._particles.clear()
            return
        self._particles = [p for p in self._particles if p.tick()]


    def draw(self, surface):
        """Render all particles.

        Args:
            surface: Surface to draw on
        """
        if not self._enabled:
            return
        if "level" in SYSTEM and SYSTEM["level"] is not None:
            camera_x, camera_y = SYSTEM["level"].map.camera_offset
        else:
            camera_x, camera_y = 0, 0
        for particle in self._particles:
            if not particle.is_on_screen():
                continue
            color = list(particle.color) + [particle.get_alpha()]
            screen_x = int(particle.pos.x - camera_x)
            screen_y = int(particle.pos.y - camera_y)
            if particle.size <= 1:
                if 0 <= screen_x < surface.get_width() and 0 <= screen_y < surface.get_height():
                    surface.set_at((screen_x, screen_y), color)
            else:
                surface.draw_circle(color, (screen_x, screen_y), int(particle.size))
        for i in PARTICULE_TRACKER:
            x1, y1, x2, y2 = i[0] - camera_x, i[1] - camera_y, i[2] - camera_x, i[3] - camera_y
            self.draw_lightning(x1, y1, x2, y2, surface)
            i[4] -= 0.016
        PARTICULE_TRACKER[:] = [i for i in PARTICULE_TRACKER if i[4] > 0]

    def rotate(self, x1, y1, x2, y2, angle):
        """Rotate a point counterclockwise by a given angle around a given origin.  
        The angle should be given in radians."""
        ox, oy = x1, y1
        px, py = x2, y2
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (qx, qy)

    def draw_lightning(self, x1, y1, x2, y2, surface):
        """Draw a lightning arc between two points."""
        # Start with the single segment and iteratively subdivide it.
        segments = [Segment(x1, y1, x2, y2)]
        offset_amount = max(6.0, np.hypot(x2 - x1, y2 - y1) * 0.25)
        iterations = 4
        for _ in range(iterations):
            new_segs = []
            for seg in segments:
                mid_x = (seg.start.x + seg.end.x) / 2.0
                mid_y = (seg.start.y + seg.end.y) / 2.0
                dx = seg.end.x - seg.start.x
                dy = seg.end.y - seg.start.y

                length = np.hypot(dx, dy)
                if length != 0:
                    perp_x = -dy / length
                    perp_y = dx / length
                else:
                    perp_x = perp_y = 0
                displacement = np.random.uniform(-offset_amount, offset_amount)
                mid_x += perp_x * displacement
                mid_y += perp_y * displacement
                new_segs.append(Segment(seg.start.x, seg.start.y, mid_x, mid_y))
                new_segs.append(Segment(mid_x, mid_y, seg.end.x, seg.end.y))

                # Add lightning branches
                # Calculate direction vector from segment start to midpoint
                dir_x = mid_x - seg.start.x
                dir_y = mid_y - seg.start.y

                # Rotate direction by random small angle
                random_angle = np.random.uniform(-0.3, 0.3)  # radians
                cos_a = np.cos(random_angle)
                sin_a = np.sin(random_angle)
                rotated_x = dir_x * cos_a - dir_y * sin_a
                rotated_y = dir_x * sin_a + dir_y * cos_a

                # Scale the rotated direction (0.7 gives good branch lengths)
                length_scale = 0.7
                rotated_x *= length_scale
                rotated_y *= length_scale

                # Calculate branch endpoint and add segment
                split_end_x = mid_x + rotated_x
                split_end_y = mid_y + rotated_y
                new_segs.append(Segment(mid_x, mid_y, split_end_x, split_end_y))
            segments = new_segs
            offset_amount /= 2.0
        for seg in segments:
            surface.draw_line((255, 255, 0), (seg.start.x, seg.start.y), (seg.end.x, seg.end.y), 2)

    def clear(self):
        """Remove all particles."""
        self._particles.clear()
        PARTICULE_TRACKER.clear()

    @property
    def enabled(self):
        """Returns whether particles are enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """Enable or disable particle rendering."""
        self._enabled = value
        if not value:
            self._particles.clear()

    @property
    def count(self):
        """Current particle count."""
        return len(self._particles)
