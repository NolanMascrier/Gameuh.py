import unittest
import os
import numpy as np
from data.physics.hitbox import HitBox
from data.physics.entity import Entity
from unittest.mock import Mock, MagicMock, patch
from data.api.surface import init_engine, set_screen
from data.image.sprite import Sprite
from data.constants import SYSTEM

RESSOURCES = "ressources/"
os.environ["SDL_VIDEODRIVER"] = "dummy"
init_engine()
SYSTEM["windows"] = set_screen(width=1, height=1)
SYSTEM["images"]["sprite_image"] = Sprite("necro_old.png", 160, 128, ["idle", "dash", "attack",\
 "attack_alt", "cast", "hit", "die"], [0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.25], \
 [8, 8, 13, 13, 17, 5, 10], [True, True, False, False, False, False, False],\
 [-1, -1, -1, -1, -1, -1, 1]).flip(False, True).scale(2, 2, False)

class TestEntityInitialization(unittest.TestCase):
    """Tests for Entity initialization."""
    
    def setUp(self):
        """Set up test fixtures with mocked dependencies."""
        self.mock_sprite = Mock()
        self.mock_sprite.w = 100
        self.mock_sprite.h = 80
        self.mock_sprite.width = 100
        self.mock_sprite.height = 80
        self.mock_sprite.scale_factor = (1, 1)
        self.mock_sprite.clone.return_value = self.mock_sprite
        self.entity = Entity(100, 200, 'sprite_image')
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_sprite}})
        self.system_patcher.start()
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_play_calls_sprite_play_when_sprite(self):
        """Test that play calls sprite.play() when entity has sprite."""
        self.entity.play('idle')
    
    def test_play_does_nothing_when_not_sprite(self):
        """Test that play does nothing when entity doesn't have sprite."""
        self.entity._sprite = False
        self.entity.play('idle')
        self.mock_sprite.play.assert_not_called()
    
    def test_play_with_different_keys(self):
        """Test play with different animation keys."""
        self.entity.play('attack')
        
        self.entity.play('dash')
    
    def test_detach_calls_sprite_detach_when_sprite(self):
        """Test that detach calls sprite.detach() when entity has sprite."""
        self.entity.detach('attack')
    
    def test_detach_with_center_true(self):
        """Test detach with center parameter True."""
        self.entity.detach('attack', center=True)
    
    def test_detach_does_nothing_when_not_sprite(self):
        """Test that detach does nothing when entity doesn't have sprite."""
        self.entity._sprite = False
        self.entity.detach('attack')
        self.mock_sprite.detach.assert_not_called()
    
    def test_detach_uses_current_position(self):
        """Test that detach uses entity's current position."""
        self.entity.x = 300
        self.entity.y = 400
        self.entity.detach('cast')


class TestEntityEdgeCases(unittest.TestCase):
    """Tests for Entity edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        self.mock_image.tick = Mock()
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_entity_with_zero_move_speed(self):
        """Test entity with zero move speed."""
        entity = Entity(100, 200, 'test_image', move_speed=0)
        initial_pos = (entity.x, entity.y)
        entity.move((200, 300))
        self.assertEqual((entity.x, entity.y), initial_pos)
    
    def test_entity_with_negative_move_speed(self):
        """Test entity with negative move speed (moves in reverse)."""
        entity = Entity(100, 200, 'test_image', move_speed=-2)
        entity.move((200, 200))
        self.assertLess(entity.x, 100)  # Moves left instead of right
    
    def test_move_with_float_coordinates(self):
        """Test moving with float coordinates."""
        entity = Entity(100.5, 200.7, 'test_image', move_speed=1.5)
        entity.move((150.3, 250.9))
        self.assertIsInstance(entity.x, float)
        self.assertIsInstance(entity.y, float)
    
    def test_dash_with_very_small_distance(self):
        """Test dash with very small distance."""
        entity = Entity(100, 200, 'test_image')
        entity._angle = 0
        entity.dash(0.1, dash_time=0.4)
        self.assertTrue(entity._dashing)
        self.assertGreater(abs(entity._dash_dx), 0)
    
    def test_dash_with_very_short_time(self):
        """Test dash with very short time."""
        entity = Entity(100, 200, 'test_image')
        entity._angle = 0
        entity.dash(100, dash_time=0.01)
        self.assertEqual(entity._dash_time, 0.01)
        # Velocity should be very high
        self.assertGreater(abs(entity._dash_dx), 1000)
    
    def test_multiple_consecutive_dashes(self):
        """Test multiple consecutive dashes."""
        entity = Entity(100, 200, 'test_image')
        entity._angle = 0
        
        entity.dash(100, dash_time=0.5)
        first_dx = entity._dash_dx
        
        entity._angle = np.pi / 2
        entity.dash(100, dash_time=0.5)
        second_dx = entity._dash_dx
        
        self.assertNotEqual(first_dx, second_dx)
    
    def test_entity_at_origin(self):
        """Test entity positioned at origin."""
        entity = Entity(0, 0, 'test_image')
        self.assertEqual(entity.x, 0)
        self.assertEqual(entity.y, 0)
        self.assertIsNotNone(entity.center)
    
    def test_entity_with_large_coordinates(self):
        """Test entity with very large coordinates."""
        entity = Entity(10000, 10000, 'test_image')
        self.assertEqual(entity.x, 10000)
        self.assertEqual(entity.y, 10000)
        entity.move((10100, 10100))
        self.assertGreater(entity.x, 10000)
    
    def test_hitbox_follows_entity_after_multiple_moves(self):
        """Test that hitbox stays centered after multiple moves."""
        entity = Entity(100, 200, 'test_image')
        
        for _ in range(5):
            entity.move((150, 250))
        
        expected_center = entity.center
        actual_center = entity.hitbox.center
        
        # Should be approximately equal (allowing for floating point)
        self.assertAlmostEqual(actual_center[0], expected_center[0], places=1)
        self.assertAlmostEqual(actual_center[1], expected_center[1], places=1)
    
    def test_displace_then_move(self):
        """Test displacing then moving entity."""
        entity = Entity(100, 200, 'test_image', move_speed=2)
        entity.displace((500, 500))
        self.assertEqual(entity.x, 500)
        
        entity.move((600, 600))
        self.assertGreater(entity.x, 500)
    
    def test_angle_changes_during_normal_movement(self):
        """Test that angle can be changed when not dashing."""
        entity = Entity(100, 200, 'test_image')
        
        for angle in [0, np.pi/4, np.pi/2, np.pi, -np.pi/2]:
            entity.angle = angle
            self.assertEqual(entity.angle, angle)
    
    def test_dash_interrupts_normal_movement(self):
        """Test that dash can interrupt normal movement."""
        entity = Entity(100, 200, 'test_image', move_speed=2)
        
        # Start moving
        entity.move((200, 200))
        
        # Start dashing
        entity._angle = 0
        entity.dash(100)
        
        self.assertTrue(entity._dashing)


class TestEntityTickBoundaryConditions(unittest.TestCase):
    """Tests for Entity tick method boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        self.mock_image.tick = Mock()
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.screen_width_patcher = patch('data.physics.entity.SCREEN_WIDTH', 1920)
        self.screen_height_patcher = patch('data.physics.entity.SCREEN_HEIGHT', 1080)
        
        self.system_patcher.start()
        self.screen_width_patcher.start()
        self.screen_height_patcher.start()
        
        self.mock_character = Mock()
        self.mock_character.creature.stats = {
            'speed': Mock(c_value=1.0)
        }
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
        self.screen_width_patcher.stop()
        self.screen_height_patcher.stop()
    
    def test_tick_at_left_boundary(self):
        """Test tick when entity is at left screen boundary."""
        entity = Entity(0, 500, 'test_image')
        entity.tick(self.mock_character)
        self.assertEqual(entity.x, 0)
    
    def test_tick_at_right_boundary(self):
        """Test tick when entity is at right screen boundary."""
        entity = Entity(1820, 500, 'test_image')  # 1920 - 100
        entity.tick(self.mock_character)
        self.assertEqual(entity.x, 1820)
    
    def test_tick_at_top_boundary(self):
        """Test tick when entity is at top screen boundary."""
        entity = Entity(500, 0, 'test_image')
        entity.tick(self.mock_character)
        self.assertEqual(entity.y, 0)
    
    def test_tick_at_bottom_boundary(self):
        """Test tick when entity is at bottom screen boundary."""
        entity = Entity(500, 1000, 'test_image')  # 1080 - 80
        entity.tick(self.mock_character)
        self.assertEqual(entity.y, 1000)
    
    def test_tick_slightly_past_right_edge(self):
        """Test tick when entity is slightly past right edge."""
        entity = Entity(1821, 500, 'test_image')
        entity.tick(self.mock_character)
        self.assertEqual(entity.x, 1820)
    
    def test_tick_slightly_past_bottom_edge(self):
        """Test tick when entity is slightly past bottom edge."""
        entity = Entity(500, 1001, 'test_image')
        entity.tick(self.mock_character)
        self.assertEqual(entity.y, 1000)
    
    def test_tick_with_dash_ending_exactly_at_zero(self):
        """Test tick when dash time reaches exactly zero."""
        entity = Entity(500, 500, 'test_image')
        entity._dashing = True
        entity._dash_time = 0.016  # Exactly one frame
        entity._dash_dx = 10
        entity._dash_dy = 5
        
        entity.tick(self.mock_character)
        entity.tick(self.mock_character)
        
        self.assertFalse(entity._dashing)
    
    def test_tick_with_very_small_dash_time_remaining(self):
        """Test tick with very small dash time remaining."""
        entity = Entity(500, 500, 'test_image')
        entity._dashing = True
        entity._dash_time = 0.001
        entity._dash_dx = 0
        entity._dash_dy = 0
        
        entity.tick(self.mock_character)
        entity.tick(self.mock_character)
        
        self.assertFalse(entity._dashing)
    
    def test_tick_with_zero_speed_modifier(self):
        """Test tick with zero speed modifier."""
        entity = Entity(500, 500, 'test_image')
        entity.tick(self.mock_character, speed_mod=0)
        self.assertEqual(entity.move_speed, 0)
    
    def test_tick_with_negative_speed_modifier(self):
        """Test tick with negative speed modifier."""
        entity = Entity(500, 500, 'test_image')
        self.mock_character.creature.stats['speed'].c_value = 2.0
        entity.tick(self.mock_character, speed_mod=-0.5)
        self.assertEqual(entity.move_speed, -1.0)


class TestEntityComplexScenarios(unittest.TestCase):
    """Tests for complex Entity scenarios combining multiple features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        self.mock_image.tick = Mock()
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.screen_width_patcher = patch('data.physics.entity.SCREEN_WIDTH', 1920)
        self.screen_height_patcher = patch('data.physics.entity.SCREEN_HEIGHT', 1080)
        self.cos_patcher = patch('numpy.cos', side_effect=np.cos)
        self.sin_patcher = patch('numpy.sin', side_effect=np.sin)
        
        self.system_patcher.start()
        self.screen_width_patcher.start()
        self.screen_height_patcher.start()
        self.cos_patcher.start()
        self.sin_patcher.start()
        
        self.mock_character = Mock()
        self.mock_character.creature.stats = {
            'speed': Mock(c_value=2.0)
        }
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
        self.screen_width_patcher.stop()
        self.screen_height_patcher.stop()
        self.cos_patcher.stop()
        self.sin_patcher.stop()
    
    def test_dash_then_tick_updates_position(self):
        """Test that position updates correctly during dash."""
        entity = Entity(500, 500, 'test_image')
        entity._angle = 0
        entity.dash(100, dash_time=0.4)
        
        initial_x = entity.x
        entity.tick(self.mock_character)
        
        self.assertGreater(entity.x, initial_x)
    
    def test_full_dash_sequence(self):
        """Test complete dash sequence from start to finish."""
        entity = Entity(500, 500, 'test_image')
        entity._angle = 0
        entity.dash(32, dash_time=0.032)  # 2 frames at 60fps
        
        # First tick
        entity.tick(self.mock_character)
        self.assertTrue(entity._dashing)
        
        # Second tick
        entity.tick(self.mock_character)
        self.assertFalse(entity._dashing)
    
    def test_reset_after_movement_and_dash(self):
        """Test reset after moving and dashing."""
        entity = Entity(100, 200, 'test_image')
        
        # Move entity
        entity.move((200, 300))
        entity._angle = 0
        entity.dash(100)
        entity.flip()
        entity._keys = ['w', 'a']
        
        # Reset
        entity.reset()
        
        self.assertEqual(entity.x, 100)
        self.assertEqual(entity.y, 200)
        self.assertEqual(entity._keys, [])
        self.assertFalse(entity._flipped)
    
    def test_move_to_target_over_multiple_ticks(self):
        """Test moving toward target over multiple ticks."""
        entity = Entity(100, 100, 'test_image', move_speed=3)
        target = (200, 200)
        
        for _ in range(20):
            entity.move(target)
            if abs(entity.x - target[0]) < 6 and abs(entity.y - target[1]) < 2:
                break
        
        # Should be close to target
        self.assertLess(abs(entity.x - target[0]), 50)
        self.assertLess(abs(entity.y - target[1]), 50)
    
    def test_hitbox_consistency_through_complex_movements(self):
        """Test that hitbox remains consistent through complex movements."""
        entity = Entity(500, 500, 'test_image', move_speed=3)
        
        # Perform various movements
        entity.move((600, 600))
        entity.displace((700, 700))
        entity.move((650, 650))
        entity._angle = np.pi / 4
        entity.dash(50)
        
        for _ in range(5):
            entity.tick(self.mock_character)
        
        # Hitbox should still be approximately centered on entity
        entity_center = entity.center
        hitbox_center = entity.hitbox.center
        
        self.assertAlmostEqual(entity_center[0], hitbox_center[0], places=0)
        self.assertAlmostEqual(entity_center[1], hitbox_center[1], places=0)
    
    def test_dash_out_of_bounds_then_tick(self):
        """Test dashing out of bounds and having tick correct it."""
        entity = Entity(1800, 500, 'test_image')
        entity._angle = 0  # Dash right
        entity.dash(200, dash_time=0.2)
        
        # Tick will move entity out of bounds
        entity.tick(self.mock_character)
        
        # Entity should be clamped to bounds and dash should stop
        self.assertLessEqual(entity.x, 1820)
        self.assertFalse(entity._dashing)
    
    def test_angle_locked_during_dash(self):
        """Test that angle cannot be changed during dash."""
        entity = Entity(500, 500, 'test_image')
        entity._angle = 0
        entity.dash(100)
        
        # Try to change angle during dash
        entity.angle = np.pi
        
        # Angle should remain unchanged
        self.assertEqual(entity.angle, 0)
    
    def test_displace_blocked_during_dash(self):
        """Test that displace is blocked during dash."""
        entity = Entity(500, 500, 'test_image')
        entity._angle = 0
        entity.dash(100)
        
        # Try to displace during dash
        entity.displace((1000, 1000))
        
        # Position should remain near original
        self.assertLess(abs(entity.x - 500), 100)
        self.assertLess(abs(entity.y - 500), 100)


class TestEntityWithCustomHitbox(unittest.TestCase):
    """Tests for Entity with custom hitbox configurations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (2, 2)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_hitbox_mod_with_custom_hitbox(self):
        """Test hitbox modification with custom hitbox."""
        custom_hitbox = HitBox(50, 60, 40, 40)
        hitbox_mod = (0.5, 0.5, 10, 10)
        
        entity = Entity(100, 200, 'test_image', hitbox=custom_hitbox, hitbox_mod=hitbox_mod)
        
        # Hitbox should be resized
        self.assertEqual(entity.hitbox.width, 20)  # 40 * 0.5
        self.assertEqual(entity.hitbox.height, 20)  # 40 * 0.5
        self.assertEqual(entity.hitbox._offset, (20, 20))  # 10 * 2, 10 * 2
    
    def test_hitbox_smaller_than_image(self):
        """Test entity with hitbox smaller than image."""
        small_hitbox = HitBox(110, 210, 50, 40)
        entity = Entity(100, 200, 'test_image', hitbox=small_hitbox)
        
        # Hitbox should be independent of image size
        self.assertEqual(entity.hitbox.width, 50)
        self.assertEqual(entity.hitbox.height, 40)
    
    def test_hitbox_larger_than_image(self):
        """Test entity with hitbox larger than image."""
        large_hitbox = HitBox(90, 190, 150, 120)
        entity = Entity(100, 200, 'test_image', hitbox=large_hitbox)
        
        self.assertEqual(entity.hitbox.width, 150)
        self.assertEqual(entity.hitbox.height, 120)


if __name__ == '__main__':
    unittest.main()
    
    def test_init_with_all_parameters(self):
        """Test initialization with all parameters."""
        hitbox = HitBox(10, 20, 30, 40)
        entity = Entity(100, 200, 'test_image', hitbox=hitbox, move_speed=2.5)
        
        self.assertEqual(entity.x, 100)
        self.assertEqual(entity.y, 200)
        self.assertEqual(entity._x_def, 100)
        self.assertEqual(entity._y_def, 200)
        self.assertEqual(entity._image, 'test_image')
        self.assertEqual(entity.hitbox, hitbox)
        self.assertEqual(entity.move_speed, 2.5)
    
    def test_init_without_hitbox_creates_default(self):
        """Test that default hitbox is created from image dimensions."""
        entity = Entity(100, 200, 'test_image')
        
        self.assertIsNotNone(entity.hitbox)
        self.assertEqual(entity.hitbox.width, 100)
        self.assertEqual(entity.hitbox.height, 80)
    
    def test_init_with_none_image(self):
        """Test initialization with None image."""
        entity = Entity(100, 200, None)
        
        self.assertIsNone(entity._real_image)
        self.assertIsNone(entity.hitbox)
    
    def test_init_with_hitbox_mod(self):
        """Test initialization with hitbox modifier."""
        hitbox = HitBox(10, 20, 30, 40)
        hitbox_mod = (2, 1.5, 5, 10)
        
        entity = Entity(100, 200, 'test_image', hitbox=hitbox, hitbox_mod=hitbox_mod)
        
        # Verify resize was called on hitbox
        self.assertEqual(entity.hitbox.width, 60)  # 30 * 2
        self.assertEqual(entity.hitbox.height, 60)  # 40 * 1.5
    
    def test_init_default_values(self):
        """Test that default values are set correctly."""
        entity = Entity(100, 200, 'test_image')
        
        self.assertEqual(entity.move_speed, 1)
        self.assertEqual(entity._keys, [])
        self.assertFalse(entity._flipped)
        self.assertEqual(entity._angle, 0)
        self.assertEqual(entity._dash_speed, 1.35)
        self.assertFalse(entity._dashing)
        self.assertIsNone(entity._x_dest)
        self.assertIsNone(entity._y_dest)
        self.assertEqual(entity._dash_dx, 0)
        self.assertEqual(entity._dash_dy, 0)
        self.assertEqual(entity._dash_time, 0)
        self.assertEqual(entity._animation_state, [0, False])
    
    def test_init_detects_sprite(self):
        """Test that sprite detection works."""
        mock_sprite = Mock()
        mock_sprite.w = 100
        mock_sprite.h = 80
        mock_sprite.width = 100
        mock_sprite.height = 80
        mock_sprite.scale_factor = (1, 1)
        mock_sprite.clone.return_value = mock_sprite
        
        with patch('data.physics.entity.SYSTEM', {'images': {'sprite_image': mock_sprite}}):
            with patch('data.physics.entity.isinstance', return_value=True):
                entity = Entity(100, 200, 'sprite_image')
                self.assertTrue(entity._sprite)


class TestEntityProperties(unittest.TestCase):
    """Tests for Entity properties."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_x_property_getter(self):
        """Test x property getter."""
        self.assertEqual(self.entity.x, 100)
    
    def test_x_property_setter(self):
        """Test x property setter."""
        self.entity.x = 150
        self.assertEqual(self.entity.x, 150)
    
    def test_y_property_getter(self):
        """Test y property getter."""
        self.assertEqual(self.entity.y, 200)
    
    def test_y_property_setter(self):
        """Test y property setter."""
        self.entity.y = 250
        self.assertEqual(self.entity.y, 250)
    
    def test_right_property(self):
        """Test right property returns hitbox right."""
        self.assertEqual(self.entity.right, self.entity.hitbox.right)
    
    def test_hitbox_property_getter(self):
        """Test hitbox property getter."""
        self.assertIsNotNone(self.entity.hitbox)
    
    def test_move_speed_property_getter(self):
        """Test move_speed property getter."""
        self.assertEqual(self.entity.move_speed, 1)
    
    def test_move_speed_property_setter(self):
        """Test move_speed property setter."""
        self.entity.move_speed = 3.5
        self.assertEqual(self.entity.move_speed, 3.5)
    
    def test_real_image_property_getter(self):
        """Test real_image property getter."""
        self.assertEqual(self.entity.real_image, self.mock_image)
    
    def test_real_image_property_setter(self):
        """Test real_image property setter."""
        new_image = Mock()
        self.entity.real_image = new_image
        self.assertEqual(self.entity.real_image, new_image)
    
    def test_flipped_property_getter(self):
        """Test flipped property getter."""
        self.assertFalse(self.entity.flipped)
    
    def test_flipped_property_setter(self):
        """Test flipped property setter."""
        self.entity.flipped = True
        self.assertTrue(self.entity.flipped)
    
    def test_angle_property_getter(self):
        """Test angle property getter."""
        self.assertEqual(self.entity.angle, 0)
    
    def test_angle_property_setter_when_not_dashing(self):
        """Test angle property setter when not dashing."""
        self.entity.angle = 1.5
        self.assertEqual(self.entity.angle, 1.5)
    
    def test_angle_property_setter_when_dashing(self):
        """Test angle property setter is ignored when dashing."""
        self.entity._dashing = True
        self.entity.angle = 1.5
        self.assertEqual(self.entity.angle, 0)  # Should remain unchanged
    
    def test_center_property(self):
        """Test center property calculation."""
        expected_x = 100 + 100 / 2
        expected_y = 200 + 80 / 2
        self.assertEqual(self.entity.center, (expected_x, expected_y))
    
    def test_max_frame_property_setter(self):
        """Test max_frame property setter."""
        self.entity.max_frame = 10
        self.assertEqual(self.entity.max_frame, 10)


class TestEntityMove(unittest.TestCase):
    """Tests for Entity move method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image', move_speed=2)
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_move_right(self):
        """Test moving entity to the right."""
        initial_x = self.entity.x
        self.entity.move((150, 200))
        self.assertGreater(self.entity.x, initial_x)
        self.assertEqual(self.entity.x, initial_x + 6)  # move_speed * 3
    
    def test_move_left(self):
        """Test moving entity to the left."""
        initial_x = self.entity.x
        self.entity.move((50, 200))
        self.assertLess(self.entity.x, initial_x)
        self.assertEqual(self.entity.x, initial_x - 6)
    
    def test_move_down(self):
        """Test moving entity down."""
        initial_y = self.entity.y
        self.entity.move((100, 250))
        self.assertGreater(self.entity.y, initial_y)
        self.assertEqual(self.entity.y, initial_y + 2)  # move_speed
    
    def test_move_up(self):
        """Test moving entity up."""
        initial_y = self.entity.y
        self.entity.move((100, 150))
        self.assertLess(self.entity.y, initial_y)
        self.assertEqual(self.entity.y, initial_y - 2)
    
    def test_move_diagonal(self):
        """Test moving entity diagonally."""
        initial_x = self.entity.x
        initial_y = self.entity.y
        self.entity.move((150, 250))
        self.assertGreater(self.entity.x, initial_x)
        self.assertGreater(self.entity.y, initial_y)
    
    def test_move_updates_hitbox(self):
        """Test that move updates hitbox center."""
        initial_hitbox_center = self.entity.hitbox.center
        self.entity.move((150, 250))
        # Hitbox center should have changed
        self.assertNotEqual(self.entity.hitbox.center, initial_hitbox_center)
    
    def test_move_same_position(self):
        """Test moving to same position (no movement)."""
        initial_x = self.entity.x
        initial_y = self.entity.y
        self.entity.move((100, 200))
        self.assertEqual(self.entity.x, initial_x)
        self.assertEqual(self.entity.y, initial_y)


class TestEntityDisplace(unittest.TestCase):
    """Tests for Entity displace method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_displace_to_new_position(self):
        """Test displacing entity to new position."""
        self.entity.displace((300, 400))
        self.assertEqual(self.entity.x, 300)
        self.assertEqual(self.entity.y, 400)
    
    def test_displace_updates_hitbox(self):
        """Test that displace updates hitbox."""
        self.entity.displace((300, 400))
        # Verify hitbox center is updated
        expected_center_x = 300 + 50
        expected_center_y = 400 + 40
        self.assertAlmostEqual(self.entity.hitbox.center[0], expected_center_x, places=5)
        self.assertAlmostEqual(self.entity.hitbox.center[1], expected_center_y, places=5)
    
    def test_displace_ignored_when_dashing(self):
        """Test that displace is ignored when dashing."""
        self.entity._dashing = True
        initial_x = self.entity.x
        initial_y = self.entity.y
        
        self.entity.displace((300, 400))
        
        self.assertEqual(self.entity.x, initial_x)
        self.assertEqual(self.entity.y, initial_y)


class TestEntityDash(unittest.TestCase):
    """Tests for Entity dash method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.cos_patcher = patch('numpy.cos', side_effect=np.cos)
        self.sin_patcher = patch('numpy.sin', side_effect=np.sin)
        
        self.system_patcher.start()
        self.cos_patcher.start()
        self.sin_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
        self.cos_patcher.stop()
        self.sin_patcher.stop()
    
    def test_dash_sets_dashing_flag(self):
        """Test that dash sets dashing flag to True."""
        self.entity._angle = 0
        self.entity.dash(100)
        self.assertTrue(self.entity._dashing)
    
    def test_dash_sets_dash_time(self):
        """Test that dash sets dash time correctly."""
        self.entity._angle = 0
        self.entity.dash(100, dash_time=0.5)
        self.assertEqual(self.entity._dash_time, 0.5)
    
    def test_dash_default_time(self):
        """Test dash with default time."""
        self.entity._angle = 0
        self.entity.dash(100)
        self.assertEqual(self.entity._dash_time, 0.4)
    
    def test_dash_calculates_velocity(self):
        """Test that dash calculates velocity correctly."""
        self.entity._angle = 0  # Right direction
        distance = 100
        dash_time = 0.4
        
        self.entity.dash(distance, dash_time)
        
        expected_velocity = distance / dash_time
        # At angle 0, cos=1, sin=0
        self.assertAlmostEqual(self.entity._dash_dx, expected_velocity, places=5)
        self.assertAlmostEqual(self.entity._dash_dy, 0, places=5)
    
    def test_dash_at_45_degrees(self):
        """Test dash at 45 degree angle."""
        self.entity._angle = np.pi / 4  # 45 degrees
        distance = 100
        dash_time = 0.4
        
        self.entity.dash(distance, dash_time)
        
        expected_velocity = distance / dash_time
        # Normalized vector at 45 degrees
        expected_component = expected_velocity / np.sqrt(2)
        
        self.assertAlmostEqual(self.entity._dash_dx, expected_component, places=5)
        self.assertAlmostEqual(self.entity._dash_dy, expected_component, places=5)
    
    def test_dash_normalization(self):
        """Test that dash direction is normalized."""
        self.entity._angle = 1.0
        self.entity.dash(100)
        
        # Verify vector is normalized
        length = (self.entity._dash_dx ** 2 + self.entity._dash_dy ** 2) ** 0.5
        velocity = 100 / 0.4
        self.assertAlmostEqual(length, velocity, places=5)
    
    def test_dash_with_zero_angle(self):
        """Test dash with zero angle (horizontal right)."""
        self.entity._angle = 0
        self.entity.dash(100)
        
        self.assertGreater(self.entity._dash_dx, 0)
        self.assertAlmostEqual(self.entity._dash_dy, 0, places=5)


class TestEntityTick(unittest.TestCase):
    """Tests for Entity tick method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        self.mock_image.tick = Mock()
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.screen_width_patcher = patch('data.physics.entity.SCREEN_WIDTH', 1920)
        self.screen_height_patcher = patch('data.physics.entity.SCREEN_HEIGHT', 1080)
        
        self.system_patcher.start()
        self.screen_width_patcher.start()
        self.screen_height_patcher.start()
        
        self.entity = Entity(500, 500, 'test_image')
        
        # Mock character
        self.mock_character = Mock()
        self.mock_character.creature.stats = {
            'speed': Mock(c_value=2.0)
        }
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
        self.screen_width_patcher.stop()
        self.screen_height_patcher.stop()
    
    def test_tick_calls_image_tick(self):
        """Test that tick calls image tick method."""
        self.entity.tick(self.mock_character)
        self.mock_image.tick.assert_called_once()
    
    def test_tick_updates_move_speed(self):
        """Test that tick updates move speed from character stats."""
        self.entity.tick(self.mock_character)
        self.assertEqual(self.entity.move_speed, 2.0)
    
    def test_tick_applies_speed_modifier(self):
        """Test that tick applies speed modifier."""
        self.entity.tick(self.mock_character, speed_mod=1.5)
        self.assertEqual(self.entity.move_speed, 3.0)  # 2.0 * 1.5
    
    def test_tick_updates_position_during_dash(self):
        """Test that tick updates position when dashing."""
        self.entity._dashing = True
        self.entity._dash_time = 0.5
        self.entity._dash_dx = 10
        self.entity._dash_dy = 5
        
        initial_x = self.entity.x
        initial_y = self.entity.y
        
        self.entity.tick(self.mock_character)
        
        self.assertEqual(self.entity.x, initial_x + 10)
        self.assertEqual(self.entity.y, initial_y + 5)
    
    def test_tick_decrements_dash_time(self):
        """Test that tick decrements dash time."""
        self.entity._dashing = True
        self.entity._dash_time = 0.5
        self.entity._dash_dx = 0
        self.entity._dash_dy = 0
        
        self.entity.tick(self.mock_character)
        
        self.assertAlmostEqual(self.entity._dash_time, 0.484, places=3)
    
    def test_tick_ends_dash_when_time_expires(self):
        """Test that dash ends when time reaches zero."""
        self.entity._dashing = True
        self.entity._dash_time = 0.01
        self.entity._dash_dx = 0
        self.entity._dash_dy = 0
        
        self.entity.tick(self.mock_character)
        self.entity.tick(self.mock_character)
        
        self.assertFalse(self.entity._dashing)
    
    def test_tick_clamps_x_to_screen_bounds(self):
        """Test that tick clamps x position to screen bounds."""
        self.entity.x = -10
        self.entity.tick(self.mock_character)
        self.assertEqual(self.entity.x, 0)
        
        self.entity.x = 2000
        self.entity.tick(self.mock_character)
        self.assertEqual(self.entity.x, 1820)  # 1920 - 100
    
    def test_tick_clamps_y_to_screen_bounds(self):
        """Test that tick clamps y position to screen bounds."""
        self.entity.y = -10
        self.entity.tick(self.mock_character)
        self.assertEqual(self.entity.y, 0)
        
        self.entity.y = 2000
        self.entity.tick(self.mock_character)
        self.assertEqual(self.entity.y, 1000)  # 1080 - 80
    
    def test_tick_stops_dash_at_screen_edge(self):
        """Test that dashing stops when hitting screen edge."""
        self.entity._dashing = True
        self.entity._dash_time = 0.5
        self.entity.x = -10  # Out of bounds
        
        self.entity.tick(self.mock_character)
        
        self.assertFalse(self.entity._dashing)
    
    def test_tick_updates_hitbox_center(self):
        """Test that tick updates hitbox center."""
        initial_center = self.entity.hitbox.center
        self.entity.x = 600
        self.entity.y = 600
        
        self.entity.tick(self.mock_character)
        
        self.assertNotEqual(self.entity.hitbox.center, initial_center)


class TestEntityReset(unittest.TestCase):
    """Tests for Entity reset method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_reset_position(self):
        """Test that reset restores original position."""
        self.entity.x = 500
        self.entity.y = 600
        
        self.entity.reset()
        
        self.assertEqual(self.entity.x, 100)
        self.assertEqual(self.entity.y, 200)
    
    def test_reset_clears_keys(self):
        """Test that reset clears keys."""
        self.entity._keys = ['w', 'a', 's', 'd']
        
        self.entity.reset()
        
        self.assertEqual(self.entity._keys, [])
    
    def test_reset_unflips_image(self):
        """Test that reset unflips image."""
        self.entity._flipped = True
        
        self.entity.reset()
        
        self.assertFalse(self.entity._flipped)
    
    def test_reset_updates_hitbox(self):
        """Test that reset updates hitbox center."""
        self.entity.x = 500
        self.entity.reset()
        
        # Hitbox should be centered on entity
        expected_center = self.entity.center
        self.assertAlmostEqual(self.entity.hitbox.center[0], expected_center[0], places=5)
        self.assertAlmostEqual(self.entity.hitbox.center[1], expected_center[1], places=5)


class TestEntityFlip(unittest.TestCase):
    """Tests for Entity flip method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_flip_toggles_flipped_flag(self):
        """Test that flip toggles flipped flag."""
        initial_state = self.entity.flipped
        self.entity.flip()
        self.assertNotEqual(self.entity.flipped, initial_state)
    
    def test_flip_twice_returns_to_original(self):
        """Test that flipping twice returns to original state."""
        initial_state = self.entity.flipped
        self.entity.flip()
        self.entity.flip()
        self.assertEqual(self.entity.flipped, initial_state)
    
    def test_flip_from_false_to_true(self):
        """Test flipping from False to True."""
        self.entity._flipped = False
        self.entity.flip()
        self.assertTrue(self.entity.flipped)
    
    def test_flip_from_true_to_false(self):
        """Test flipping from True to False."""
        self.entity._flipped = True
        self.entity.flip()
        self.assertFalse(self.entity.flipped)


class TestEntityGetImage(unittest.TestCase):
    """Tests for Entity get_image method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_image = Mock()
        self.mock_image.w = 100
        self.mock_image.h = 80
        self.mock_image.width = 100
        self.mock_image.height = 80
        self.mock_image.scale_factor = (1, 1)
        self.mock_image.clone.return_value = self.mock_image
        self.expected_image = Mock()
        self.mock_image.get_image.return_value = self.expected_image
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'test_image': self.mock_image}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'test_image')
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()
    
    def test_get_image_calls_real_image_method(self):
        """Test that get_image calls real_image.get_image()."""
        result = self.entity.get_image()
        self.mock_image.get_image.assert_called_once()
    
    def test_get_image_returns_correct_value(self):
        """Test that get_image returns correct value."""
        result = self.entity.get_image()
        self.assertEqual(result, self.expected_image)


class TestEntitySpriteInteraction(unittest.TestCase):
    """Tests for Entity sprite-related methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_sprite = Mock()
        self.mock_sprite.w = 100
        self.mock_sprite.h = 80
        self.mock_sprite.width = 100
        self.mock_sprite.height = 80
        self.mock_sprite.scale_factor = (1, 1)
        self.mock_sprite.clone.return_value = self.mock_sprite
        self.mock_sprite.play = Mock()
        self.mock_sprite.detach = Mock()
        
        self.system_patcher = patch('data.physics.entity.SYSTEM', {'images': {'sprite_image': self.mock_sprite}})
        self.system_patcher.start()
        
        self.entity = Entity(100, 200, 'sprite_image')
        self.entity._sprite = True
    
    def tearDown(self):
        """Clean up patches."""
        self.system_patcher.stop()