"""Particle system for visual effects."""

import numpy as np
from data.api.vec2d import Vec2
from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT

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
        return (0 <= self.pos.x <= SCREEN_WIDTH and
                0 <= self.pos.y <= SCREEN_HEIGHT)


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
        for particle in self._particles:
            if not particle.is_on_screen():
                continue
            color = list(particle.color) + [particle.get_alpha()]
            x = int(particle.pos.x)
            y = int(particle.pos.y)
            if particle.size <= 1:
                if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                    surface.set_at((x, y), color)
            else:
                surface.draw_circle(color, (x, y), int(particle.size))

    def clear(self):
        """Remove all particles."""
        self._particles.clear()

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
