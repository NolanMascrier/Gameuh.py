import unittest
from data.physics.hitbox import HitBox

class TestHitBoxInitialization(unittest.TestCase):
    """Tests for HitBox initialization."""
    
    def test_init_with_positive_values(self):
        """Test initialization with positive values."""
        hb = HitBox(10, 20, 30, 40)
        self.assertEqual(hb.x, 10)
        self.assertEqual(hb.y, 20)
        self.assertEqual(hb.width, 30)
        self.assertEqual(hb.height, 40)
        self.assertEqual(hb._offset, (0, 0))
    
    def test_init_with_zero_values(self):
        """Test initialization with zero values."""
        hb = HitBox(0, 0, 0, 0)
        self.assertEqual(hb.x, 0)
        self.assertEqual(hb.y, 0)
        self.assertEqual(hb.width, 0)
        self.assertEqual(hb.height, 0)
    
    def test_init_with_negative_values(self):
        """Test initialization with negative values."""
        hb = HitBox(-10, -20, 30, 40)
        self.assertEqual(hb.x, -10)
        self.assertEqual(hb.y, -20)
        self.assertEqual(hb.width, 30)
        self.assertEqual(hb.height, 40)
    
    def test_init_with_float_values(self):
        """Test initialization with float values."""
        hb = HitBox(10.5, 20.7, 30.2, 40.9)
        self.assertEqual(hb.x, 10.5)
        self.assertEqual(hb.y, 20.7)
        self.assertEqual(hb.width, 30.2)
        self.assertEqual(hb.height, 40.9)


class TestHitBoxProperties(unittest.TestCase):
    """Tests for HitBox properties."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hb = HitBox(10, 20, 30, 40)
    
    def test_left_property(self):
        """Test left property returns x coordinate."""
        self.assertEqual(self.hb.left, 10)
    
    def test_right_property(self):
        """Test right property returns x + width."""
        self.assertEqual(self.hb.right, 40)
    
    def test_top_property(self):
        """Test top property returns y coordinate."""
        self.assertEqual(self.hb.top, 20)
    
    def test_bottom_property(self):
        """Test bottom property returns y + height."""
        self.assertEqual(self.hb.bottom, 60)
    
    def test_center_x_property(self):
        """Test center_x returns horizontal center."""
        self.assertEqual(self.hb.center_x, 25)
    
    def test_center_y_property(self):
        """Test center_y returns vertical center."""
        self.assertEqual(self.hb.center_y, 40)
    
    def test_center_property(self):
        """Test center returns tuple of center coordinates."""
        self.assertEqual(self.hb.center, (25, 40))
    
    def test_center_offset_property_no_offset(self):
        """Test center_offset with default offset."""
        self.assertEqual(self.hb.center_offset, (10, 20))
    
    def test_center_offset_property_with_offset(self):
        """Test center_offset with custom offset."""
        self.hb._offset = (5, 10)
        self.assertEqual(self.hb.center_offset, (15, 30))
    
    def test_x_setter(self):
        """Test x property setter."""
        self.hb.x = 50
        self.assertEqual(self.hb.x, 50)
        self.assertEqual(self.hb.left, 50)
    
    def test_y_setter(self):
        """Test y property setter."""
        self.hb.y = 100
        self.assertEqual(self.hb.y, 100)
        self.assertEqual(self.hb.top, 100)
    
    def test_width_setter(self):
        """Test width property setter."""
        self.hb.width = 50
        self.assertEqual(self.hb.width, 50)
        self.assertEqual(self.hb.right, 60)
    
    def test_height_setter(self):
        """Test height property setter."""
        self.hb.height = 80
        self.assertEqual(self.hb.height, 80)
        self.assertEqual(self.hb.bottom, 100)


class TestHitBoxIsInside(unittest.TestCase):
    """Tests for is_inside method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hb = HitBox(10, 20, 30, 40)  # Box from (10,20) to (40,60)
    
    def test_point_inside_center(self):
        """Test point at center of box."""
        self.assertTrue(self.hb.is_inside((25, 40)))
    
    def test_point_on_left_edge(self):
        """Test point on left edge (inclusive)."""
        self.assertTrue(self.hb.is_inside((10, 40)))
    
    def test_point_on_right_edge(self):
        """Test point on right edge (inclusive)."""
        self.assertTrue(self.hb.is_inside((40, 40)))
    
    def test_point_on_top_edge(self):
        """Test point on top edge (inclusive)."""
        self.assertTrue(self.hb.is_inside((25, 20)))
    
    def test_point_on_bottom_edge(self):
        """Test point on bottom edge (inclusive)."""
        self.assertTrue(self.hb.is_inside((25, 60)))
    
    def test_point_on_top_left_corner(self):
        """Test point on top-left corner."""
        self.assertTrue(self.hb.is_inside((10, 20)))
    
    def test_point_on_bottom_right_corner(self):
        """Test point on bottom-right corner."""
        self.assertTrue(self.hb.is_inside((40, 60)))
    
    def test_point_left_of_box(self):
        """Test point to the left of box."""
        self.assertFalse(self.hb.is_inside((5, 40)))
    
    def test_point_right_of_box(self):
        """Test point to the right of box."""
        self.assertFalse(self.hb.is_inside((45, 40)))
    
    def test_point_above_box(self):
        """Test point above box."""
        self.assertFalse(self.hb.is_inside((25, 15)))
    
    def test_point_below_box(self):
        """Test point below box."""
        self.assertFalse(self.hb.is_inside((25, 65)))
    
    def test_point_outside_diagonal(self):
        """Test point outside box diagonally."""
        self.assertFalse(self.hb.is_inside((5, 15)))
        self.assertFalse(self.hb.is_inside((45, 65)))


class TestHitBoxIsColliding(unittest.TestCase):
    """Tests for is_colliding method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hb1 = HitBox(10, 10, 20, 20)  # Box from (10,10) to (30,30)
    
    def test_collision_with_overlapping_box(self):
        """Test collision with overlapping box."""
        hb2 = HitBox(20, 20, 20, 20)  # Box from (20,20) to (40,40)
        self.assertTrue(self.hb1.is_colliding(hb2))
        self.assertTrue(hb2.is_colliding(self.hb1))
    
    def test_collision_with_contained_box(self):
        """Test collision with fully contained box."""
        hb2 = HitBox(15, 15, 5, 5)  # Small box inside
        self.assertTrue(self.hb1.is_colliding(hb2))
        self.assertTrue(hb2.is_colliding(self.hb1))
    
    def test_collision_with_containing_box(self):
        """Test collision with larger containing box."""
        hb2 = HitBox(0, 0, 50, 50)  # Large box containing hb1
        self.assertTrue(self.hb1.is_colliding(hb2))
        self.assertTrue(hb2.is_colliding(self.hb1))
    
    def test_collision_with_identical_box(self):
        """Test collision with identical box."""
        hb2 = HitBox(10, 10, 20, 20)
        self.assertTrue(self.hb1.is_colliding(hb2))
    
    def test_collision_touching_right_edge(self):
        """Test boxes touching on right edge."""
        hb2 = HitBox(30, 10, 20, 20)  # Touching right edge
        self.assertTrue(self.hb1.is_colliding(hb2))
    
    def test_collision_touching_bottom_edge(self):
        """Test boxes touching on bottom edge."""
        hb2 = HitBox(10, 30, 20, 20)  # Touching bottom edge
        self.assertTrue(self.hb1.is_colliding(hb2))
    
    def test_no_collision_separated_horizontally(self):
        """Test boxes separated horizontally."""
        hb2 = HitBox(50, 10, 20, 20)
        self.assertFalse(self.hb1.is_colliding(hb2))
    
    def test_no_collision_separated_vertically(self):
        """Test boxes separated vertically."""
        hb2 = HitBox(10, 50, 20, 20)
        self.assertFalse(self.hb1.is_colliding(hb2))
    
    def test_no_collision_separated_diagonally(self):
        """Test boxes separated diagonally."""
        hb2 = HitBox(50, 50, 20, 20)
        self.assertFalse(self.hb1.is_colliding(hb2))

    def test_collision_left(self):
        """if not isinstance(other, HitBox):
            return False
        if self.left > other.right or self.right < other.left:
            return False
        if self.top > other.bottom or self.bottom < other.top:
            return False
        if self.left < other.right and self.top < other.bottom:
            return True
        if self.right < other.left and self.bottom < other.top:
            return True
        return False"""
        hb2 = HitBox(0, 0, 5, 5)
        self.assertFalse(self.hb1.is_colliding(hb2))
        hb2 = HitBox(15, 15, 10, 10)
        self.assertTrue(self.hb1.is_colliding(hb2))
    
    def test_collision_with_non_hitbox(self):
        """Test collision check with non-HitBox object."""
        self.assertFalse(self.hb1.is_colliding("not a hitbox"))
        self.assertFalse(self.hb1.is_colliding(None))
        self.assertFalse(self.hb1.is_colliding(123))
        self.assertFalse(self.hb1.is_colliding([10, 10, 20, 20]))
    
    def test_collision_with_zero_size_box(self):
        """Test collision with zero-size box."""
        hb2 = HitBox(15, 15, 0, 0)
        # Zero-size box inside should still collide
        result = self.hb1.is_colliding(hb2)
        self.assertIsInstance(result, bool)


class TestHitBoxGetRect(unittest.TestCase):
    """Tests for get_rect method."""
    
    def test_get_rect_returns_tuple(self):
        """Test get_rect returns correct tuple."""
        hb = HitBox(10, 20, 30, 40)
        rect = hb.get_rect()
        self.assertEqual(rect, (10, 20, 30, 40))
        self.assertIsInstance(rect, tuple)
    
    def test_get_rect_after_modification(self):
        """Test get_rect after modifying hitbox."""
        hb = HitBox(10, 20, 30, 40)
        hb.x = 50
        hb.width = 100
        rect = hb.get_rect()
        self.assertEqual(rect, (50, 20, 100, 40))


class TestHitBoxMove(unittest.TestCase):
    """Tests for move method."""
    
    def test_move_to_new_position(self):
        """Test moving box to new position."""
        hb = HitBox(10, 20, 30, 40)
        hb.move((50, 60))
        self.assertEqual(hb.x, 50)
        self.assertEqual(hb.y, 60)
        self.assertEqual(hb.width, 30)
        self.assertEqual(hb.height, 40)
    
    def test_move_to_origin(self):
        """Test moving box to origin."""
        hb = HitBox(10, 20, 30, 40)
        hb.move((0, 0))
        self.assertEqual(hb.x, 0)
        self.assertEqual(hb.y, 0)
    
    def test_move_to_negative_position(self):
        """Test moving box to negative coordinates."""
        hb = HitBox(10, 20, 30, 40)
        hb.move((-10, -20))
        self.assertEqual(hb.x, -10)
        self.assertEqual(hb.y, -20)
    
    def test_move_with_float_position(self):
        """Test moving box to float coordinates."""
        hb = HitBox(10, 20, 30, 40)
        hb.move((15.5, 25.7))
        self.assertEqual(hb.x, 15.5)
        self.assertEqual(hb.y, 25.7)


class TestHitBoxMoveCenter(unittest.TestCase):
    """Tests for move_center method."""
    
    def test_move_center_to_new_position(self):
        """Test moving center to new position."""
        hb = HitBox(10, 20, 30, 40)  # Center at (25, 40)
        hb.move_center((50, 60))
        self.assertEqual(hb.center, (50, 60))
        self.assertEqual(hb.x, 35)  # 50 - 30/2
        self.assertEqual(hb.y, 40)  # 60 - 40/2
    
    def test_move_center_to_origin(self):
        """Test moving center to origin."""
        hb = HitBox(10, 20, 30, 40)
        hb.move_center((0, 0))
        self.assertEqual(hb.x, -15)
        self.assertEqual(hb.y, -20)
        self.assertEqual(hb.center, (0, 0))
    
    def test_move_center_preserves_size(self):
        """Test that move_center preserves hitbox size."""
        hb = HitBox(10, 20, 30, 40)
        hb.move_center((100, 100))
        self.assertEqual(hb.width, 30)
        self.assertEqual(hb.height, 40)


class TestHitBoxExpand(unittest.TestCase):
    """Tests for expand method."""
    
    def test_expand_positive_values(self):
        """Test expanding with positive values."""
        hb = HitBox(10, 20, 30, 40)
        hb.expand(5, 10)
        self.assertEqual(hb.x, 0)  # 10 - 10
        self.assertEqual(hb.y, 15)  # 20 - 5
        self.assertEqual(hb.width, 50)  # 30 + 2*10
        self.assertEqual(hb.height, 50)  # 40 + 2*5
    
    def test_expand_zero_values(self):
        """Test expanding with zero values."""
        hb = HitBox(10, 20, 30, 40)
        hb.expand(0, 0)
        self.assertEqual(hb.x, 10)
        self.assertEqual(hb.y, 20)
        self.assertEqual(hb.width, 30)
        self.assertEqual(hb.height, 40)
    
    def test_expand_negative_values(self):
        """Test expanding with negative values (shrinking)."""
        hb = HitBox(10, 20, 30, 40)
        hb.expand(-5, -5)
        self.assertEqual(hb.x, 15)  # 10 - (-5)
        self.assertEqual(hb.y, 25)  # 20 - (-5)
        self.assertEqual(hb.width, 20)  # 30 + 2*(-5)
        self.assertEqual(hb.height, 30)  # 40 + 2*(-5)
    
    def test_expand_preserves_center(self):
        """Test that expand preserves center position."""
        hb = HitBox(10, 20, 30, 40)
        original_center = hb.center
        hb.expand(5, 10)
        self.assertEqual(hb.center, original_center)


class TestHitBoxResize(unittest.TestCase):
    """Tests for resize method."""
    
    def test_resize_without_scale_factor(self):
        """Test resize without scale factor."""
        hb = HitBox(10, 20, 30, 40)
        original_center = hb.center
        hb.resize((2, 1.5, 5, 10))
        self.assertEqual(hb.width, 60)  # 30 * 2
        self.assertEqual(hb.height, 60)  # 40 * 1.5
        self.assertEqual(hb._offset, (5, 10))
        self.assertEqual(hb.center, original_center)
    
    def test_resize_with_scale_factor(self):
        """Test resize with scale factor."""
        hb = HitBox(10, 20, 30, 40)
        original_center = hb.center
        hb.resize((2, 1.5, 10, 20), scale_factor=(0.5, 0.5))
        self.assertEqual(hb.width, 60)
        self.assertEqual(hb.height, 60)
        self.assertEqual(hb._offset, (5, 10))  # 10*0.5, 20*0.5
        self.assertEqual(hb.center, original_center)
    
    def test_resize_with_scale_factor_different_axes(self):
        """Test resize with different scale factors for x and y."""
        hb = HitBox(10, 20, 30, 40)
        hb.resize((1, 1, 10, 20), scale_factor=(2, 3))
        self.assertEqual(hb._offset, (20, 60))
    
    def test_resize_preserves_center(self):
        """Test that resize preserves center position."""
        hb = HitBox(10, 20, 30, 40)
        original_center = hb.center
        hb.resize((1.5, 2, 0, 0))
        self.assertEqual(hb.center, original_center)
    
    def test_resize_with_zero_scale(self):
        """Test resize with zero width/height multipliers."""
        hb = HitBox(10, 20, 30, 40)
        hb.resize((0, 0, 0, 0))
        self.assertEqual(hb.width, 0)
        self.assertEqual(hb.height, 0)
    
    def test_resize_updates_offset(self):
        """Test that resize properly updates offset."""
        hb = HitBox(10, 20, 30, 40)
        hb.resize((1, 1, 15, 25))
        self.assertEqual(hb._offset, (15, 25))


class TestHitBoxEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_zero_size_hitbox(self):
        """Test hitbox with zero width and height."""
        hb = HitBox(10, 10, 0, 0)
        self.assertEqual(hb.left, hb.right)
        self.assertEqual(hb.top, hb.bottom)
        self.assertEqual(hb.center, (10, 10))
    
    def test_negative_dimensions(self):
        """Test hitbox with negative dimensions."""
        hb = HitBox(10, 10, -20, -20)
        self.assertEqual(hb.width, -20)
        self.assertEqual(hb.height, -20)
        self.assertEqual(hb.right, -10)  # 10 + (-20)
        self.assertEqual(hb.bottom, -10)
    
    def test_very_large_values(self):
        """Test hitbox with very large values."""
        hb = HitBox(1e10, 1e10, 1e10, 1e10)
        self.assertEqual(hb.x, 1e10)
        self.assertTrue(hb.is_inside((1.5e10, 1.5e10)))
    
    def test_float_precision(self):
        """Test hitbox with float precision edge cases."""
        hb = HitBox(0.1, 0.2, 0.3, 0.4)
        self.assertAlmostEqual(hb.center_x, 0.25, places=10)
        self.assertAlmostEqual(hb.center_y, 0.4, places=10)
