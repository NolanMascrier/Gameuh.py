import unittest
import numpy as np
from data.api.vec2d import Vec2


class TestVec2Initialization(unittest.TestCase):
    """Tests for Vec2 initialization."""
    
    def test_init_default_values(self):
        """Test initialization with default values (0, 0)."""
        v = Vec2()
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)
    
    def test_init_with_integers(self):
        """Test initialization with integer values."""
        v = Vec2(3, 4)
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)
    
    def test_init_with_floats(self):
        """Test initialization with float values."""
        v = Vec2(3.5, 4.7)
        self.assertAlmostEqual(v.x, 3.5, places=5)
        self.assertAlmostEqual(v.y, 4.7, places=5)
    
    def test_init_with_tuple(self):
        """Test initialization with tuple."""
        v = Vec2((5, 6))
        self.assertEqual(v.x, 5.0)
        self.assertEqual(v.y, 6.0)
    
    def test_init_with_tuple_floats(self):
        """Test initialization with tuple of floats."""
        v = Vec2((2.5, 3.5))
        self.assertAlmostEqual(v.x, 2.5, places=5)
        self.assertAlmostEqual(v.y, 3.5, places=5)
    
    def test_init_with_negative_values(self):
        """Test initialization with negative values."""
        v = Vec2(-3, -4)
        self.assertEqual(v.x, -3.0)
        self.assertEqual(v.y, -4.0)
    
    def test_init_with_zero_values(self):
        """Test initialization with explicit zeros."""
        v = Vec2(0, 0)
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)
    
    def test_init_creates_numpy_array(self):
        """Test that initialization creates numpy array."""
        v = Vec2(1, 2)
        self.assertIsInstance(v.arr, np.ndarray)
        self.assertEqual(v.arr.dtype, np.float32)
    
    def test_init_array_shape(self):
        """Test that array has correct shape."""
        v = Vec2(1, 2)
        self.assertEqual(v.arr.shape, (2,))


class TestVec2Properties(unittest.TestCase):
    """Tests for Vec2 properties."""
    
    def test_x_getter(self):
        """Test x property getter."""
        v = Vec2(5, 10)
        self.assertEqual(v.x, 5.0)
    
    def test_y_getter(self):
        """Test y property getter."""
        v = Vec2(5, 10)
        self.assertEqual(v.y, 10.0)
    
    def test_x_setter(self):
        """Test x property setter."""
        v = Vec2(1, 2)
        v.x = 7
        self.assertEqual(v.x, 7.0)
        self.assertEqual(v.y, 2.0)
    
    def test_y_setter(self):
        """Test y property setter."""
        v = Vec2(1, 2)
        v.y = 8
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 8.0)
    
    def test_x_setter_with_float(self):
        """Test x setter with float value."""
        v = Vec2(1, 2)
        v.x = 3.5
        self.assertAlmostEqual(v.x, 3.5, places=5)
    
    def test_y_setter_with_float(self):
        """Test y setter with float value."""
        v = Vec2(1, 2)
        v.y = 4.7
        self.assertAlmostEqual(v.y, 4.7, places=5)
    
    def test_x_setter_with_negative(self):
        """Test x setter with negative value."""
        v = Vec2(1, 2)
        v.x = -5
        self.assertEqual(v.x, -5.0)
    
    def test_y_setter_with_negative(self):
        """Test y setter with negative value."""
        v = Vec2(1, 2)
        v.y = -3
        self.assertEqual(v.y, -3.0)


class TestVec2Addition(unittest.TestCase):
    """Tests for Vec2 addition."""
    
    def test_add_positive_vectors(self):
        """Test addition of positive vectors."""
        v1 = Vec2(3, 4)
        v2 = Vec2(1, 2)
        result = v1 + v2
        
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)
    
    def test_add_returns_new_vector(self):
        """Test that addition returns new vector."""
        v1 = Vec2(3, 4)
        v2 = Vec2(1, 2)
        result = v1 + v2
        
        self.assertIsInstance(result, Vec2)
        self.assertIsNot(result, v1)
        self.assertIsNot(result, v2)
    
    def test_add_does_not_modify_original(self):
        """Test that addition doesn't modify original vectors."""
        v1 = Vec2(3, 4)
        v2 = Vec2(1, 2)
        v1 + v2
        
        self.assertEqual(v1.x, 3.0)
        self.assertEqual(v1.y, 4.0)
        self.assertEqual(v2.x, 1.0)
        self.assertEqual(v2.y, 2.0)
    
    def test_add_with_negative_vectors(self):
        """Test addition with negative vectors."""
        v1 = Vec2(5, 10)
        v2 = Vec2(-2, -3)
        result = v1 + v2
        
        self.assertEqual(result.x, 3.0)
        self.assertEqual(result.y, 7.0)
    
    def test_add_with_zero_vector(self):
        """Test addition with zero vector."""
        v1 = Vec2(5, 10)
        v2 = Vec2(0, 0)
        result = v1 + v2
        
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 10.0)
    
    def test_add_with_floats(self):
        """Test addition with float values."""
        v1 = Vec2(1.5, 2.5)
        v2 = Vec2(0.5, 0.5)
        result = v1 + v2
        
        self.assertAlmostEqual(result.x, 2.0, places=5)
        self.assertAlmostEqual(result.y, 3.0, places=5)


class TestVec2Subtraction(unittest.TestCase):
    """Tests for Vec2 subtraction."""
    
    def test_sub_positive_vectors(self):
        """Test subtraction of positive vectors."""
        v1 = Vec2(5, 7)
        v2 = Vec2(2, 3)
        result = v1 - v2
        
        self.assertEqual(result.x, 3.0)
        self.assertEqual(result.y, 4.0)
    
    def test_sub_returns_new_vector(self):
        """Test that subtraction returns new vector."""
        v1 = Vec2(5, 7)
        v2 = Vec2(2, 3)
        result = v1 - v2
        
        self.assertIsInstance(result, Vec2)
        self.assertIsNot(result, v1)
        self.assertIsNot(result, v2)
    
    def test_sub_does_not_modify_original(self):
        """Test that subtraction doesn't modify original vectors."""
        v1 = Vec2(5, 7)
        v2 = Vec2(2, 3)
        v1 - v2
        
        self.assertEqual(v1.x, 5.0)
        self.assertEqual(v1.y, 7.0)
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 3.0)
    
    def test_sub_resulting_in_negative(self):
        """Test subtraction resulting in negative values."""
        v1 = Vec2(2, 3)
        v2 = Vec2(5, 7)
        result = v1 - v2
        
        self.assertEqual(result.x, -3.0)
        self.assertEqual(result.y, -4.0)
    
    def test_sub_with_zero_vector(self):
        """Test subtraction with zero vector."""
        v1 = Vec2(5, 10)
        v2 = Vec2(0, 0)
        result = v1 - v2
        
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 10.0)
    
    def test_sub_from_zero(self):
        """Test subtracting from zero vector (negation)."""
        v1 = Vec2(0, 0)
        v2 = Vec2(3, 4)
        result = v1 - v2
        
        self.assertEqual(result.x, -3.0)
        self.assertEqual(result.y, -4.0)


class TestVec2Multiplication(unittest.TestCase):
    """Tests for Vec2 scalar multiplication."""
    
    def test_mul_by_positive_scalar(self):
        """Test multiplication by positive scalar."""
        v = Vec2(3, 4)
        result = v * 2
        
        self.assertEqual(result.x, 6.0)
        self.assertEqual(result.y, 8.0)
    
    def test_mul_by_zero(self):
        """Test multiplication by zero."""
        v = Vec2(3, 4)
        result = v * 0
        
        self.assertEqual(result.x, 0.0)
        self.assertEqual(result.y, 0.0)
    
    def test_mul_by_negative_scalar(self):
        """Test multiplication by negative scalar."""
        v = Vec2(3, 4)
        result = v * -1
        
        self.assertEqual(result.x, -3.0)
        self.assertEqual(result.y, -4.0)
    
    def test_mul_by_fraction(self):
        """Test multiplication by fraction."""
        v = Vec2(10, 20)
        result = v * 0.5
        
        self.assertAlmostEqual(result.x, 5.0, places=5)
        self.assertAlmostEqual(result.y, 10.0, places=5)
    
    def test_mul_returns_new_vector(self):
        """Test that multiplication returns new vector."""
        v = Vec2(3, 4)
        result = v * 2
        
        self.assertIsInstance(result, Vec2)
        self.assertIsNot(result, v)
    
    def test_mul_does_not_modify_original(self):
        """Test that multiplication doesn't modify original."""
        v = Vec2(3, 4)
        v * 2
        
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)


class TestVec2Division(unittest.TestCase):
    """Tests for Vec2 scalar division."""
    
    def test_div_by_positive_scalar(self):
        """Test division by positive scalar."""
        v = Vec2(10, 20)
        result = v / 2
        
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 10.0)
    
    def test_div_by_fraction(self):
        """Test division by fraction."""
        v = Vec2(3, 4)
        result = v / 0.5
        
        self.assertAlmostEqual(result.x, 6.0, places=5)
        self.assertAlmostEqual(result.y, 8.0, places=5)
    
    def test_div_by_negative_scalar(self):
        """Test division by negative scalar."""
        v = Vec2(10, 20)
        result = v / -2
        
        self.assertEqual(result.x, -5.0)
        self.assertEqual(result.y, -10.0)
    
    def test_div_returns_new_vector(self):
        """Test that division returns new vector."""
        v = Vec2(10, 20)
        result = v / 2
        
        self.assertIsInstance(result, Vec2)
        self.assertIsNot(result, v)
    
    def test_div_does_not_modify_original(self):
        """Test that division doesn't modify original."""
        v = Vec2(10, 20)
        v / 2
        
        self.assertEqual(v.x, 10.0)
        self.assertEqual(v.y, 20.0)


class TestVec2GetItem(unittest.TestCase):
    """Tests for Vec2 indexing."""
    
    def test_getitem_zero_index(self):
        """Test getting item at index 0 (x)."""
        v = Vec2(3, 4)
        self.assertEqual(v[0], 3.0)
    
    def test_getitem_one_index(self):
        """Test getting item at index 1 (y)."""
        v = Vec2(3, 4)
        self.assertEqual(v[1], 4.0)
    
    def test_getitem_returns_float(self):
        """Test that getitem returns float."""
        v = Vec2(3, 4)
        self.assertIsInstance(v[0], float)
        self.assertIsInstance(v[1], float)
    
    def test_getitem_negative_index(self):
        """Test negative indexing."""
        v = Vec2(3, 4)
        self.assertEqual(v[-1], 4.0)  # Last element
        self.assertEqual(v[-2], 3.0)  # Second to last
    
    def test_getitem_with_float_values(self):
        """Test getitem with float vector values."""
        v = Vec2(3.5, 4.7)
        self.assertAlmostEqual(v[0], 3.5, places=5)
        self.assertAlmostEqual(v[1], 4.7, places=5)


class TestVec2Length(unittest.TestCase):
    """Tests for Vec2 length method."""
    
    def test_length_3_4_triangle(self):
        """Test length of 3-4-5 triangle."""
        v = Vec2(3, 4)
        self.assertAlmostEqual(v.length(), 5.0, places=5)
    
    def test_length_zero_vector(self):
        """Test length of zero vector."""
        v = Vec2(0, 0)
        self.assertEqual(v.length(), 0.0)
    
    def test_length_unit_vector_x(self):
        """Test length of unit vector in x direction."""
        v = Vec2(1, 0)
        self.assertAlmostEqual(v.length(), 1.0, places=5)
    
    def test_length_unit_vector_y(self):
        """Test length of unit vector in y direction."""
        v = Vec2(0, 1)
        self.assertAlmostEqual(v.length(), 1.0, places=5)
    
    def test_length_negative_values(self):
        """Test length with negative values."""
        v = Vec2(-3, -4)
        self.assertAlmostEqual(v.length(), 5.0, places=5)
    
    def test_length_returns_float(self):
        """Test that length returns float."""
        v = Vec2(3, 4)
        length = v.length()
        self.assertIsInstance(length, float)
    
    def test_length_diagonal_unit_vector(self):
        """Test length of diagonal unit vector."""
        v = Vec2(1, 1)
        self.assertAlmostEqual(v.length(), np.sqrt(2), places=5)
    
    def test_length_large_values(self):
        """Test length with large values."""
        v = Vec2(300, 400)
        self.assertAlmostEqual(v.length(), 500.0, places=5)


class TestVec2Normalize(unittest.TestCase):
    """Tests for Vec2 normalize method."""
    
    def test_normalize_returns_unit_vector(self):
        """Test that normalize returns unit vector."""
        v = Vec2(3, 4)
        normalized = v.normalize()
        
        self.assertAlmostEqual(normalized.length(), 1.0, places=5)
    
    def test_normalize_direction_preserved(self):
        """Test that normalize preserves direction."""
        v = Vec2(3, 4)
        normalized = v.normalize()
        
        # Should be 0.6, 0.8 (3/5, 4/5)
        self.assertAlmostEqual(normalized.x, 0.6, places=5)
        self.assertAlmostEqual(normalized.y, 0.8, places=5)
    
    def test_normalize_zero_vector(self):
        """Test normalizing zero vector returns zero vector."""
        v = Vec2(0, 0)
        normalized = v.normalize()
        
        self.assertEqual(normalized.x, 0.0)
        self.assertEqual(normalized.y, 0.0)
        self.assertIs(normalized, v)  # Should return self
    
    def test_normalize_unit_vector(self):
        """Test normalizing already normalized vector."""
        v = Vec2(1, 0)
        normalized = v.normalize()
        
        self.assertAlmostEqual(normalized.x, 1.0, places=5)
        self.assertAlmostEqual(normalized.y, 0.0, places=5)
        self.assertAlmostEqual(normalized.length(), 1.0, places=5)
    
    def test_normalize_negative_vector(self):
        """Test normalizing negative vector."""
        v = Vec2(-3, -4)
        normalized = v.normalize()
        
        self.assertAlmostEqual(normalized.x, -0.6, places=5)
        self.assertAlmostEqual(normalized.y, -0.8, places=5)
        self.assertAlmostEqual(normalized.length(), 1.0, places=5)
    
    def test_normalize_returns_new_vector(self):
        """Test that normalize returns new vector (except for zero)."""
        v = Vec2(3, 4)
        normalized = v.normalize()
        
        self.assertIsNot(normalized, v)
        # Original unchanged
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)
    
    def test_normalize_diagonal_vector(self):
        """Test normalizing diagonal vector."""
        v = Vec2(1, 1)
        normalized = v.normalize()
        
        expected = float(1.0 / np.sqrt(2))
        self.assertAlmostEqual(float(normalized.x), expected, places=4)
        self.assertAlmostEqual(float(normalized.y), expected, places=4)


class TestVec2Copy(unittest.TestCase):
    """Tests for Vec2 copy method."""
    
    def test_copy_creates_new_instance(self):
        """Test that copy creates new instance."""
        v1 = Vec2(3, 4)
        v2 = v1.copy()
        
        self.assertIsNot(v1, v2)
    
    def test_copy_has_same_values(self):
        """Test that copy has same values."""
        v1 = Vec2(3, 4)
        v2 = v1.copy()
        
        self.assertEqual(v1.x, v2.x)
        self.assertEqual(v1.y, v2.y)
    
    def test_copy_independent_modification(self):
        """Test that modifying copy doesn't affect original."""
        v1 = Vec2(3, 4)
        v2 = v1.copy()
        
        v2.x = 10
        v2.y = 20
        
        self.assertEqual(v1.x, 3.0)
        self.assertEqual(v1.y, 4.0)
        self.assertEqual(v2.x, 10.0)
        self.assertEqual(v2.y, 20.0)
    
    def test_copy_zero_vector(self):
        """Test copying zero vector."""
        v1 = Vec2(0, 0)
        v2 = v1.copy()
        
        self.assertEqual(v2.x, 0.0)
        self.assertEqual(v2.y, 0.0)
        self.assertIsNot(v1, v2)
    
    def test_copy_with_float_values(self):
        """Test copying vector with float values."""
        v1 = Vec2(3.5, 4.7)
        v2 = v1.copy()
        
        self.assertAlmostEqual(v2.x, 3.5, places=5)
        self.assertAlmostEqual(v2.y, 4.7, places=5)


class TestVec2ToTuple(unittest.TestCase):
    """Tests for Vec2 to_tuple method."""
    
    def test_to_tuple_returns_tuple(self):
        """Test that to_tuple returns tuple."""
        v = Vec2(3, 4)
        result = v.to_tuple()
        
        self.assertIsInstance(result, tuple)
    
    def test_to_tuple_values(self):
        """Test that to_tuple returns correct values."""
        v = Vec2(3, 4)
        result = v.to_tuple()
        
        self.assertEqual(result, (3.0, 4.0))
    
    def test_to_tuple_length(self):
        """Test that tuple has length 2."""
        v = Vec2(3, 4)
        result = v.to_tuple()
        
        self.assertEqual(len(result), 2)
    
    def test_to_tuple_with_floats(self):
        """Test to_tuple with float values."""
        v = Vec2(3.5, 4.7)
        result = v.to_tuple()
        
        self.assertAlmostEqual(result[0], 3.5, places=5)
        self.assertAlmostEqual(result[1], 4.7, places=5)
    
    def test_to_tuple_with_negatives(self):
        """Test to_tuple with negative values."""
        v = Vec2(-3, -4)
        result = v.to_tuple()
        
        self.assertEqual(result, (-3.0, -4.0))


class TestVec2Repr(unittest.TestCase):
    """Tests for Vec2 __repr__ method."""
    
    def test_repr_format(self):
        """Test repr string format."""
        v = Vec2(3, 4)
        result = repr(v)
        
        self.assertEqual(result, "Vec2(3.00, 4.00)")
    
    def test_repr_with_floats(self):
        """Test repr with float values."""
        v = Vec2(3.456, 4.789)
        result = repr(v)
        
        self.assertEqual(result, "Vec2(3.46, 4.79)")
    
    def test_repr_with_negatives(self):
        """Test repr with negative values."""
        v = Vec2(-3.5, -4.7)
        result = repr(v)
        
        self.assertEqual(result, "Vec2(-3.50, -4.70)")
    
    def test_repr_zero_vector(self):
        """Test repr of zero vector."""
        v = Vec2(0, 0)
        result = repr(v)
        
        self.assertEqual(result, "Vec2(0.00, 0.00)")


class TestVec2EdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_very_large_values(self):
        """Test with very large values."""
        v = Vec2(1e10, 1e10)
        self.assertEqual(v.x, 1e10)
        self.assertEqual(v.y, 1e10)
    
    def test_very_small_values(self):
        """Test with very small values."""
        v = Vec2(1e-10, 1e-10)
        self.assertAlmostEqual(v.x, 1e-10, places=5)
        self.assertAlmostEqual(v.y, 1e-10, places=5)
    
    def test_mixed_sign_operations(self):
        """Test operations with mixed signs."""
        v1 = Vec2(3, -4)
        v2 = Vec2(-1, 2)
        result = v1 + v2
        
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, -2.0)
    
    def test_chain_operations(self):
        """Test chaining multiple operations."""
        v = Vec2(10, 20)
        result = ((v + Vec2(5, 5)) * 2) / 3
        
        self.assertAlmostEqual(result.x, 10.0, places=4)
        self.assertAlmostEqual(result.y, 16.6667, places=4)
    
    def test_normalize_very_small_vector(self):
        """Test normalizing very small but non-zero vector."""
        v = Vec2(1e-10, 1e-10)
        normalized = v.normalize()
        
        # Should still produce unit vector
        self.assertAlmostEqual(normalized.length(), 1.0, places=4)


class TestVec2ComplexOperations(unittest.TestCase):
    """Tests for complex vector operations."""
    
    def test_vector_arithmetic_combination(self):
        """Test combination of vector operations."""
        v1 = Vec2(3, 4)
        v2 = Vec2(1, 2)
        v3 = Vec2(2, 1)
        
        result = v1 + v2 - v3
        
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 5.0)
    
    def test_scalar_and_vector_operations(self):
        """Test mixing scalar and vector operations."""
        v1 = Vec2(10, 20)
        v2 = Vec2(5, 10)
        
        result = (v1 / 2) + v2
        
        self.assertEqual(result.x, 10.0)
        self.assertEqual(result.y, 20.0)
    
    def test_multiple_normalizations(self):
        """Test normalizing result of operations."""
        v1 = Vec2(3, 0)
        v2 = Vec2(0, 4)
        
        combined = v1 + v2
        normalized = combined.normalize()
        
        self.assertAlmostEqual(normalized.x, 0.6, places=5)
        self.assertAlmostEqual(normalized.y, 0.8, places=5)
        self.assertAlmostEqual(normalized.length(), 1.0, places=5)
    
    def test_perpendicular_vectors(self):
        """Test operations with perpendicular vectors."""
        v1 = Vec2(1, 0)
        v2 = Vec2(0, 1)
        
        result = v1 + v2
        
        self.assertEqual(result.x, 1.0)
        self.assertEqual(result.y, 1.0)
        self.assertAlmostEqual(result.length(), np.sqrt(2), places=5)
