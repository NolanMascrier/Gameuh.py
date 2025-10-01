import unittest
from data.api.widget import Widget  # Adjust import based on your module name


class TestWidgetInitialization(unittest.TestCase):
    """Tests for Widget initialization."""
    
    def test_init_default_values(self):
        """Test initialization with default values."""
        widget = Widget()
        self.assertEqual(widget.x, 0)
        self.assertEqual(widget.y, 0)
        self.assertEqual(widget.width, 0)
        self.assertEqual(widget.height, 0)
    
    def test_init_with_all_parameters(self):
        """Test initialization with all parameters."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.x, 10)
        self.assertEqual(widget.y, 20)
        self.assertEqual(widget.width, 100)
        self.assertEqual(widget.height, 50)
    
    def test_init_with_partial_parameters(self):
        """Test initialization with partial parameters."""
        widget = Widget(x=10, y=20)
        self.assertEqual(widget.x, 10)
        self.assertEqual(widget.y, 20)
        self.assertEqual(widget.width, 0)
        self.assertEqual(widget.height, 0)
    
    def test_init_with_floats(self):
        """Test initialization with float values."""
        widget = Widget(x=10.5, y=20.7, width=100.3, height=50.9)
        self.assertEqual(widget.x, 10.5)
        self.assertEqual(widget.y, 20.7)
        self.assertEqual(widget.width, 100.3)
        self.assertEqual(widget.height, 50.9)
    
    def test_init_with_negative_values(self):
        """Test initialization with negative values."""
        widget = Widget(x=-10, y=-20, width=100, height=50)
        self.assertEqual(widget.x, -10)
        self.assertEqual(widget.y, -20)
        self.assertEqual(widget.width, 100)
        self.assertEqual(widget.height, 50)
    
    def test_init_with_negative_dimensions(self):
        """Test initialization with negative dimensions."""
        widget = Widget(x=0, y=0, width=-100, height=-50)
        self.assertEqual(widget.width, -100)
        self.assertEqual(widget.height, -50)


class TestWidgetPositionProperties(unittest.TestCase):
    """Tests for Widget position properties."""
    
    def test_left_property(self):
        """Test left property returns x coordinate."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.left, 10)
    
    def test_right_property(self):
        """Test right property returns x + width."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.right, 110)
    
    def test_top_property(self):
        """Test top property returns y coordinate."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.top, 20)
    
    def test_bottom_property(self):
        """Test bottom property returns y + height."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.bottom, 70)
    
    def test_left_with_zero(self):
        """Test left property at origin."""
        widget = Widget(x=0, y=0, width=100, height=50)
        self.assertEqual(widget.left, 0)
    
    def test_right_with_zero_width(self):
        """Test right property with zero width."""
        widget = Widget(x=10, y=20, width=0, height=50)
        self.assertEqual(widget.right, 10)
    
    def test_bottom_with_zero_height(self):
        """Test bottom property with zero height."""
        widget = Widget(x=10, y=20, width=100, height=0)
        self.assertEqual(widget.bottom, 20)
    
    def test_boundaries_with_negative_position(self):
        """Test boundaries with negative position."""
        widget = Widget(x=-10, y=-20, width=30, height=40)
        self.assertEqual(widget.left, -10)
        self.assertEqual(widget.right, 20)
        self.assertEqual(widget.top, -20)
        self.assertEqual(widget.bottom, 20)


class TestWidgetXYProperties(unittest.TestCase):
    """Tests for Widget x and y properties."""
    
    def test_x_getter(self):
        """Test x property getter."""
        widget = Widget(x=50, y=100)
        self.assertEqual(widget.x, 50)
    
    def test_y_getter(self):
        """Test y property getter."""
        widget = Widget(x=50, y=100)
        self.assertEqual(widget.y, 100)
    
    def test_x_setter(self):
        """Test x property setter."""
        widget = Widget(x=10, y=20)
        widget.x = 50
        self.assertEqual(widget.x, 50)
        self.assertEqual(widget._x, 50)
    
    def test_y_setter(self):
        """Test y property setter."""
        widget = Widget(x=10, y=20)
        widget.y = 60
        self.assertEqual(widget.y, 60)
        self.assertEqual(widget._y, 60)
    
    def test_x_setter_updates_boundaries(self):
        """Test that changing x updates left and right."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.x = 50
        self.assertEqual(widget.left, 50)
        self.assertEqual(widget.right, 150)
    
    def test_y_setter_updates_boundaries(self):
        """Test that changing y updates top and bottom."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.y = 60
        self.assertEqual(widget.top, 60)
        self.assertEqual(widget.bottom, 110)
    
    def test_x_setter_with_float(self):
        """Test x setter with float value."""
        widget = Widget()
        widget.x = 10.5
        self.assertEqual(widget.x, 10.5)
    
    def test_y_setter_with_float(self):
        """Test y setter with float value."""
        widget = Widget()
        widget.y = 20.7
        self.assertEqual(widget.y, 20.7)
    
    def test_x_setter_with_negative(self):
        """Test x setter with negative value."""
        widget = Widget()
        widget.x = -10
        self.assertEqual(widget.x, -10)
    
    def test_y_setter_with_negative(self):
        """Test y setter with negative value."""
        widget = Widget()
        widget.y = -20
        self.assertEqual(widget.y, -20)


class TestWidgetDimensionProperties(unittest.TestCase):
    """Tests for Widget width and height properties."""
    
    def test_width_getter(self):
        """Test width property getter."""
        widget = Widget(width=100, height=50)
        self.assertEqual(widget.width, 100)
    
    def test_height_getter(self):
        """Test height property getter."""
        widget = Widget(width=100, height=50)
        self.assertEqual(widget.height, 50)
    
    def test_width_setter(self):
        """Test width property setter."""
        widget = Widget(width=100, height=50)
        widget.width = 200
        self.assertEqual(widget.width, 200)
        self.assertEqual(widget._width, 200)
    
    def test_height_setter(self):
        """Test height property setter."""
        widget = Widget(width=100, height=50)
        widget.height = 75
        self.assertEqual(widget.height, 75)
        self.assertEqual(widget._height, 75)
    
    def test_width_setter_updates_right(self):
        """Test that changing width updates right boundary."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.width = 200
        self.assertEqual(widget.right, 210)
    
    def test_height_setter_updates_bottom(self):
        """Test that changing height updates bottom boundary."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.height = 100
        self.assertEqual(widget.bottom, 120)
    
    def test_width_setter_with_float(self):
        """Test width setter with float value."""
        widget = Widget()
        widget.width = 100.5
        self.assertEqual(widget.width, 100.5)
    
    def test_height_setter_with_float(self):
        """Test height setter with float value."""
        widget = Widget()
        widget.height = 50.7
        self.assertEqual(widget.height, 50.7)
    
    def test_width_setter_with_zero(self):
        """Test width setter with zero."""
        widget = Widget(width=100)
        widget.width = 0
        self.assertEqual(widget.width, 0)
    
    def test_height_setter_with_zero(self):
        """Test height setter with zero."""
        widget = Widget(height=50)
        widget.height = 0
        self.assertEqual(widget.height, 0)


class TestWidgetCenterProperties(unittest.TestCase):
    """Tests for Widget center properties."""
    
    def test_center_x_property(self):
        """Test center_x property calculation."""
        widget = Widget(x=10, y=20, width=100, height=50)
        # Center x = 10 + 100/2 = 60
        self.assertEqual(widget.center_x, 60)
    
    def test_center_y_property(self):
        """Test center_y property calculation."""
        widget = Widget(x=10, y=20, width=100, height=50)
        # Center y = 20 + 50/2 = 45
        self.assertEqual(widget.center_y, 45)
    
    def test_center_property(self):
        """Test center property returns tuple."""
        widget = Widget(x=10, y=20, width=100, height=50)
        self.assertEqual(widget.center, (60, 45))
    
    def test_center_at_origin(self):
        """Test center calculation at origin."""
        widget = Widget(x=0, y=0, width=100, height=50)
        self.assertEqual(widget.center, (50, 25))
    
    def test_center_with_odd_dimensions(self):
        """Test center calculation with odd dimensions."""
        widget = Widget(x=0, y=0, width=11, height=21)
        self.assertEqual(widget.center, (5.5, 10.5))
    
    def test_center_with_negative_position(self):
        """Test center calculation with negative position."""
        widget = Widget(x=-50, y=-30, width=100, height=60)
        self.assertEqual(widget.center, (0, 0))
    
    def test_center_with_zero_dimensions(self):
        """Test center with zero dimensions."""
        widget = Widget(x=10, y=20, width=0, height=0)
        self.assertEqual(widget.center, (10, 20))
    
    def test_center_updates_with_position_change(self):
        """Test that center updates when position changes."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.x = 50
        self.assertEqual(widget.center_x, 100)
        widget.y = 60
        self.assertEqual(widget.center_y, 85)
    
    def test_center_updates_with_dimension_change(self):
        """Test that center updates when dimensions change."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.width = 200
        self.assertEqual(widget.center_x, 110)
        widget.height = 100
        self.assertEqual(widget.center_y, 70)


class TestWidgetCenterSetter(unittest.TestCase):
    """Tests for Widget center setter."""
    
    def test_center_setter_with_tuple(self):
        """Test center setter with tuple centers widget correctly."""
        widget = Widget(x=0, y=0, width=100, height=50)
        widget.center = (60, 45)
        # Center at (60, 45) means x = 60 - 100/2 = 10, y = 45 - 50/2 = 20
        self.assertEqual(widget.x, 10)
        self.assertEqual(widget.y, 20)
        self.assertEqual(widget.center, (60, 45))
    
    def test_center_setter_with_two_floats(self):
        """Test center setter with two float parameters."""
        widget = Widget(x=0, y=0, width=100, height=50)
        widget.center = 60.0, 45.0
        self.assertEqual(widget.x, 10.0)
        self.assertEqual(widget.y, 20.0)
        self.assertEqual(widget.center, (60.0, 45.0))
    
    def test_center_setter_centers_widget(self):
        """Test that center setter properly centers widget at coordinates."""
        widget = Widget(x=0, y=0, width=100, height=50)
        # Setting center to (100, 100) should position widget so its center is there
        widget.center = (100, 100)
        self.assertEqual(widget.center_x, 100)
        self.assertEqual(widget.center_y, 100)
        self.assertEqual(widget.x, 50)  # 100 - 100/2
        self.assertEqual(widget.y, 75)  # 100 - 50/2
    
    def test_center_setter_with_negative_values(self):
        """Test center setter with negative center coordinates."""
        widget = Widget(width=100, height=50)
        widget.center = (-10, -20)
        # x = -10 - 100/2 = -60, y = -20 - 50/2 = -45
        self.assertEqual(widget.x, -60)
        self.assertEqual(widget.y, -45)
        self.assertEqual(widget.center, (-10, -20))
    
    def test_center_setter_at_origin(self):
        """Test center setter centering widget at origin."""
        widget = Widget(x=100, y=100, width=50, height=50)
        widget.center = (0, 0)
        # x = 0 - 50/2 = -25, y = 0 - 50/2 = -25
        self.assertEqual(widget.x, -25)
        self.assertEqual(widget.y, -25)
        self.assertEqual(widget.center, (0, 0))
    
    def test_center_setter_updates_boundaries(self):
        """Test that center setter updates boundaries correctly."""
        widget = Widget(x=0, y=0, width=100, height=50)
        widget.center = (50, 30)
        # x = 50 - 50 = 0, y = 30 - 25 = 5
        self.assertEqual(widget.left, 0)
        self.assertEqual(widget.top, 5)
        self.assertEqual(widget.right, 100)
        self.assertEqual(widget.bottom, 55)
        self.assertEqual(widget.center, (50, 30))
    
    def test_center_setter_with_zero_dimensions(self):
        """Test center setter with zero width/height."""
        widget = Widget(width=0, height=0)
        widget.center = (100, 100)
        # With zero dimensions, x = 100 - 0/2 = 100
        self.assertEqual(widget.x, 100)
        self.assertEqual(widget.y, 100)
        self.assertEqual(widget.center, (100, 100))
    
    def test_center_setter_with_odd_dimensions(self):
        """Test center setter with odd dimensions."""
        widget = Widget(width=11, height=21)
        widget.center = (100, 100)
        # x = 100 - 11/2 = 94.5, y = 100 - 21/2 = 89.5
        self.assertEqual(widget.x, 94.5)
        self.assertEqual(widget.y, 89.5)
        self.assertAlmostEqual(widget.center_x, 100, places=5)
        self.assertAlmostEqual(widget.center_y, 100, places=5)


class TestWidgetEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_widget_at_origin(self):
        """Test widget at origin with zero dimensions."""
        widget = Widget(x=0, y=0, width=0, height=0)
        self.assertEqual(widget.left, 0)
        self.assertEqual(widget.right, 0)
        self.assertEqual(widget.top, 0)
        self.assertEqual(widget.bottom, 0)
        self.assertEqual(widget.center, (0, 0))
    
    def test_widget_with_very_large_values(self):
        """Test widget with very large values."""
        widget = Widget(x=1e10, y=1e10, width=1e10, height=1e10)
        self.assertEqual(widget.x, 1e10)
        self.assertEqual(widget.y, 1e10)
        self.assertEqual(widget.right, 2e10)
        self.assertEqual(widget.bottom, 2e10)
    
    def test_widget_with_very_small_values(self):
        """Test widget with very small values."""
        widget = Widget(x=0.001, y=0.001, width=0.001, height=0.001)
        self.assertAlmostEqual(widget.x, 0.001, places=5)
        self.assertAlmostEqual(widget.y, 0.001, places=5)
    
    def test_negative_width_affects_right(self):
        """Test that negative width affects right boundary."""
        widget = Widget(x=100, y=100, width=-50, height=50)
        self.assertEqual(widget.right, 50)  # 100 + (-50)
    
    def test_negative_height_affects_bottom(self):
        """Test that negative height affects bottom boundary."""
        widget = Widget(x=100, y=100, width=50, height=-50)
        self.assertEqual(widget.bottom, 50)  # 100 + (-50)
    
    def test_float_precision(self):
        """Test widget with float precision values."""
        widget = Widget(x=10.123456, y=20.654321, width=30.111111, height=40.999999)
        self.assertAlmostEqual(widget.x, 10.123456, places=6)
        self.assertAlmostEqual(widget.center_x, 10.123456 + 30.111111/2, places=6)


class TestWidgetPropertyInteractions(unittest.TestCase):
    """Tests for interactions between properties."""
    
    def test_changing_x_preserves_width(self):
        """Test that changing x doesn't change width."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.x = 50
        self.assertEqual(widget.width, 100)
    
    def test_changing_y_preserves_height(self):
        """Test that changing y doesn't change height."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.y = 60
        self.assertEqual(widget.height, 50)
    
    def test_changing_width_preserves_x(self):
        """Test that changing width doesn't change x."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.width = 200
        self.assertEqual(widget.x, 10)
    
    def test_changing_height_preserves_y(self):
        """Test that changing height doesn't change y."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.height = 100
        self.assertEqual(widget.y, 20)
    
    def test_multiple_property_changes(self):
        """Test multiple property changes in sequence."""
        widget = Widget(x=10, y=20, width=100, height=50)
        widget.x = 30
        widget.width = 150
        widget.y = 40
        widget.height = 75
        
        self.assertEqual(widget.x, 30)
        self.assertEqual(widget.y, 40)
        self.assertEqual(widget.width, 150)
        self.assertEqual(widget.height, 75)
        self.assertEqual(widget.right, 180)
        self.assertEqual(widget.bottom, 115)


class TestWidgetConsistency(unittest.TestCase):
    """Tests for widget property consistency."""
    
    def test_left_equals_x(self):
        """Test that left always equals x."""
        widget = Widget(x=25, y=50, width=100, height=75)
        self.assertEqual(widget.left, widget.x)
        
        widget.x = 100
        self.assertEqual(widget.left, widget.x)
    
    def test_top_equals_y(self):
        """Test that top always equals y."""
        widget = Widget(x=25, y=50, width=100, height=75)
        self.assertEqual(widget.top, widget.y)
        
        widget.y = 100
        self.assertEqual(widget.top, widget.y)
    
    def test_right_equals_x_plus_width(self):
        """Test that right always equals x + width."""
        widget = Widget(x=25, y=50, width=100, height=75)
        self.assertEqual(widget.right, widget.x + widget.width)
        
        widget.x = 50
        self.assertEqual(widget.right, widget.x + widget.width)
        
        widget.width = 200
        self.assertEqual(widget.right, widget.x + widget.width)
    
    def test_bottom_equals_y_plus_height(self):
        """Test that bottom always equals y + height."""
        widget = Widget(x=25, y=50, width=100, height=75)
        self.assertEqual(widget.bottom, widget.y + widget.height)
        
        widget.y = 100
        self.assertEqual(widget.bottom, widget.y + widget.height)
        
        widget.height = 150
        self.assertEqual(widget.bottom, widget.y + widget.height)
    
    def test_center_consistency(self):
        """Test that center calculations are consistent."""
        widget = Widget(x=10, y=20, width=100, height=50)
        
        # center should equal (center_x, center_y)
        self.assertEqual(widget.center, (widget.center_x, widget.center_y))
        
        # center_x should be left + width/2
        self.assertEqual(widget.center_x, widget.left + widget.width / 2)
        
        # center_y should be top + height/2
        self.assertEqual(widget.center_y, widget.top + widget.height / 2)


class TestWidgetRealWorldScenarios(unittest.TestCase):
    """Tests for real-world usage scenarios."""
    
    def test_move_widget(self):
        """Test moving a widget to new position."""
        widget = Widget(x=10, y=20, width=100, height=50)
        
        # Move widget
        widget.x = 200
        widget.y = 300
        
        self.assertEqual(widget.x, 200)
        self.assertEqual(widget.y, 300)
        self.assertEqual(widget.right, 300)
        self.assertEqual(widget.bottom, 350)
    
    def test_resize_widget(self):
        """Test resizing a widget."""
        widget = Widget(x=10, y=20, width=100, height=50)
        
        # Resize widget
        widget.width = 200
        widget.height = 100
        
        self.assertEqual(widget.width, 200)
        self.assertEqual(widget.height, 100)
        self.assertEqual(widget.right, 210)
        self.assertEqual(widget.bottom, 120)
    
    def test_position_widget_by_center(self):
        """Test positioning widget using center setter."""
        widget = Widget(width=100, height=50)
        
        # Position at specific location
        widget.center = (400, 300)
        self.assertEqual(widget.x, 350)
        self.assertEqual(widget.y, 275)
    
    def test_check_if_point_inside_widget(self):
        """Test checking if a point is inside widget bounds."""
        widget = Widget(x=100, y=100, width=200, height=100)
        
        # Point inside
        point_x, point_y = 150, 150
        inside = (widget.left <= point_x <= widget.right and 
                 widget.top <= point_y <= widget.bottom)
        self.assertTrue(inside)
        
        # Point outside
        point_x, point_y = 50, 50
        inside = (widget.left <= point_x <= widget.right and 
                 widget.top <= point_y <= widget.bottom)
        self.assertFalse(inside)
    
    def test_check_widget_overlap(self):
        """Test checking if two widgets overlap."""
        widget1 = Widget(x=100, y=100, width=100, height=100)
        widget2 = Widget(x=150, y=150, width=100, height=100)
        
        # Check overlap
        overlap = not (widget1.right < widget2.left or 
                      widget1.left > widget2.right or
                      widget1.bottom < widget2.top or
                      widget1.top > widget2.bottom)
        self.assertTrue(overlap)
        
        # Non-overlapping widgets
        widget3 = Widget(x=300, y=300, width=100, height=100)
        overlap = not (widget1.right < widget3.left or 
                      widget1.left > widget3.right or
                      widget1.bottom < widget3.top or
                      widget1.top > widget3.bottom)
        self.assertFalse(overlap)
