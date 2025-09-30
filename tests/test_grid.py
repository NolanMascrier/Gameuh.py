import unittest
from data.physics.spatialgrid import SpatialGrid
from data.physics.hitbox import HitBox


class TestSpatialGridInitialization(unittest.TestCase):
    """Tests for SpatialGrid initialization."""
    
    def test_init_with_default_cell_size(self):
        """Test initialization with default cell size."""
        grid = SpatialGrid()
        self.assertEqual(grid._cell_size, 64)
        self.assertIsNotNone(grid._grid)
    
    def test_init_with_custom_cell_size(self):
        """Test initialization with custom cell size."""
        grid = SpatialGrid(cell_size=128)
        self.assertEqual(grid._cell_size, 128)
    
    def test_init_with_small_cell_size(self):
        """Test initialization with small cell size."""
        grid = SpatialGrid(cell_size=16)
        self.assertEqual(grid._cell_size, 16)
    
    def test_init_with_large_cell_size(self):
        """Test initialization with large cell size."""
        grid = SpatialGrid(cell_size=512)
        self.assertEqual(grid._cell_size, 512)
    
    def test_grid_starts_empty(self):
        """Test that grid starts empty."""
        grid = SpatialGrid()
        self.assertEqual(len(grid._grid), 0)


class TestSpatialGridGetCells(unittest.TestCase):
    """Tests for SpatialGrid _get_cells method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_get_cells_single_cell(self):
        """Test hitbox that fits in a single cell."""
        hitbox = HitBox(10, 10, 20, 20)  # From (10,10) to (30,30)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertEqual(len(cells), 1)
        self.assertIn((0, 0), cells)
    
    def test_get_cells_spanning_two_horizontal_cells(self):
        """Test hitbox spanning two cells horizontally."""
        hitbox = HitBox(50, 10, 30, 20)  # From (50,10) to (80,30)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertEqual(len(cells), 2)
        self.assertIn((0, 0), cells)
        self.assertIn((1, 0), cells)
    
    def test_get_cells_spanning_two_vertical_cells(self):
        """Test hitbox spanning two cells vertically."""
        hitbox = HitBox(10, 50, 20, 30)  # From (10,50) to (30,80)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertEqual(len(cells), 2)
        self.assertIn((0, 0), cells)
        self.assertIn((0, 1), cells)
    
    def test_get_cells_spanning_four_cells(self):
        """Test hitbox spanning four cells (2x2 grid)."""
        hitbox = HitBox(50, 50, 30, 30)  # From (50,50) to (80,80)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertEqual(len(cells), 4)
        self.assertIn((0, 0), cells)
        self.assertIn((1, 0), cells)
        self.assertIn((0, 1), cells)
        self.assertIn((1, 1), cells)
    
    def test_get_cells_at_cell_boundary(self):
        """Test hitbox exactly at cell boundary."""
        hitbox = HitBox(64, 64, 10, 10)  # Starts exactly at cell (1,1)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertIn((1, 1), cells)
    
    def test_get_cells_crossing_cell_boundary(self):
        """Test hitbox crossing cell boundary."""
        hitbox = HitBox(60, 60, 10, 10)  # From (60,60) to (70,70), crosses boundary
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertEqual(len(cells), 4)
        self.assertIn((0, 0), cells)
        self.assertIn((1, 0), cells)
        self.assertIn((0, 1), cells)
        self.assertIn((1, 1), cells)
    
    def test_get_cells_large_hitbox(self):
        """Test large hitbox spanning many cells."""
        hitbox = HitBox(0, 0, 200, 200)  # Spans multiple cells
        cells = list(self.grid._get_cells(hitbox))
        
        # Should span 4x4 = 16 cells (0-192 covers cells 0,1,2,3)
        self.assertEqual(len(cells), 16)
    
    def test_get_cells_with_negative_coordinates(self):
        """Test hitbox with negative coordinates."""
        hitbox = HitBox(-70, -70, 20, 20)  # From (-70,-70) to (-50,-50)
        cells = list(self.grid._get_cells(hitbox))
        
        # Negative coordinates should map to negative cell indices
        self.assertIn((-2, -2), cells)
    
    def test_get_cells_spanning_negative_and_positive(self):
        """Test hitbox spanning negative and positive coordinates."""
        hitbox = HitBox(-10, -10, 30, 30)  # From (-10,-10) to (20,20)
        cells = list(self.grid._get_cells(hitbox))
        
        self.assertIn((-1, -1), cells)
        self.assertIn((0, -1), cells)
        self.assertIn((-1, 0), cells)
        self.assertIn((0, 0), cells)
    
    def test_get_cells_zero_size_hitbox(self):
        """Test hitbox with zero size."""
        hitbox = HitBox(100, 100, 0, 0)
        cells = list(self.grid._get_cells(hitbox))
        
        # Zero-size hitbox should still occupy one cell
        self.assertEqual(len(cells), 1)
        self.assertIn((1, 1), cells)
    
    def test_get_cells_with_different_cell_size(self):
        """Test get_cells with different cell size."""
        grid = SpatialGrid(cell_size=32)
        hitbox = HitBox(0, 0, 64, 64)  # Should span 3x3 cells with size 32
        cells = list(grid._get_cells(hitbox))
        
        # 64/32 = 2, so spans cells 0,1,2 in each dimension
        self.assertEqual(len(cells), 9)


class TestSpatialGridAdd(unittest.TestCase):
    """Tests for SpatialGrid add method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_add_single_object(self):
        """Test adding a single object."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        
        # Object should be in cell (0,0)
        self.assertIn(obj, self.grid._grid[(0, 0)])
    
    def test_add_multiple_objects_same_cell(self):
        """Test adding multiple objects to the same cell."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)
        hitbox2 = HitBox(20, 20, 15, 15)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        
        # Both objects should be in cell (0,0)
        self.assertIn(obj1, self.grid._grid[(0, 0)])
        self.assertIn(obj2, self.grid._grid[(0, 0)])
        self.assertEqual(len(self.grid._grid[(0, 0)]), 2)
    
    def test_add_object_spanning_multiple_cells(self):
        """Test adding object that spans multiple cells."""
        obj = "large_object"
        hitbox = HitBox(50, 50, 30, 30)  # Spans 4 cells
        
        self.grid.add(obj, hitbox)
        
        # Object should be in all 4 cells
        self.assertIn(obj, self.grid._grid[(0, 0)])
        self.assertIn(obj, self.grid._grid[(1, 0)])
        self.assertIn(obj, self.grid._grid[(0, 1)])
        self.assertIn(obj, self.grid._grid[(1, 1)])
    
    def test_add_objects_in_different_cells(self):
        """Test adding objects in different cells."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)  # Cell (0,0)
        hitbox2 = HitBox(100, 100, 20, 20)  # Cell (1,1)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        
        self.assertIn(obj1, self.grid._grid[(0, 0)])
        self.assertNotIn(obj1, self.grid._grid.get((1, 1), []))
        self.assertIn(obj2, self.grid._grid[(1, 1)])
        self.assertNotIn(obj2, self.grid._grid.get((0, 0), []))
    
    def test_add_same_object_twice(self):
        """Test adding the same object twice (e.g., after movement)."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        self.grid.add(obj, hitbox)
        
        # Object should appear twice in the cell
        self.assertEqual(self.grid._grid[(0, 0)].count(obj), 2)
    
    def test_add_with_negative_coordinates(self):
        """Test adding object with negative coordinates."""
        obj = "object1"
        hitbox = HitBox(-100, -100, 20, 20)
        
        self.grid.add(obj, hitbox)
        
        # Should be in negative cell
        self.assertIn(obj, self.grid._grid[(-2, -2)])
    
    def test_add_various_object_types(self):
        """Test adding different types of objects."""
        obj_str = "string"
        obj_int = 42
        obj_dict = {"key": "value"}
        obj_list = [1, 2, 3]
        
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj_str, hitbox)
        self.grid.add(obj_int, hitbox)
        self.grid.add(obj_dict, hitbox)
        self.grid.add(obj_list, hitbox)
        
        cell_contents = self.grid._grid[(0, 0)]
        self.assertIn(obj_str, cell_contents)
        self.assertIn(obj_int, cell_contents)
        self.assertIn(obj_dict, cell_contents)
        self.assertIn(obj_list, cell_contents)


class TestSpatialGridQuery(unittest.TestCase):
    """Tests for SpatialGrid query method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_query_empty_grid(self):
        """Test querying an empty grid."""
        hitbox = HitBox(10, 10, 20, 20)
        results = list(self.grid.query(hitbox))
        
        self.assertEqual(len(results), 0)
    
    def test_query_single_object_same_cell(self):
        """Test querying for object in the same cell."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        results = list(self.grid.query(hitbox))
        
        self.assertEqual(len(results), 1)
        self.assertIn(obj, results)
    
    def test_query_multiple_objects_same_cell(self):
        """Test querying for multiple objects in the same cell."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)
        hitbox2 = HitBox(20, 20, 15, 15)
        query_hitbox = HitBox(15, 15, 10, 10)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        results = list(self.grid.query(query_hitbox))
        
        self.assertEqual(len(results), 2)
        self.assertIn(obj1, results)
        self.assertIn(obj2, results)
    
    def test_query_object_in_different_cell(self):
        """Test querying doesn't return objects from other cells."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)  # Cell (0,0)
        hitbox2 = HitBox(200, 200, 20, 20)  # Cell (3,3)
        query_hitbox = HitBox(10, 10, 20, 20)  # Query cell (0,0)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        results = list(self.grid.query(query_hitbox))
        
        self.assertIn(obj1, results)
        self.assertNotIn(obj2, results)
    
    def test_query_spanning_multiple_cells(self):
        """Test query that spans multiple cells."""
        obj1 = "object1"
        obj2 = "object2"
        obj3 = "object3"
        hitbox1 = HitBox(10, 10, 20, 20)  # Cell (0,0)
        hitbox2 = HitBox(70, 70, 20, 20)  # Cell (1,1)
        hitbox3 = HitBox(200, 200, 20, 20)  # Cell (3,3)
        query_hitbox = HitBox(50, 50, 30, 30)  # Spans cells (0,0), (1,0), (0,1), (1,1)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        self.grid.add(obj3, hitbox3)
        results = list(self.grid.query(query_hitbox))
        
        self.assertIn(obj1, results)
        self.assertIn(obj2, results)
        self.assertNotIn(obj3, results)
    
    def test_query_deduplicates_objects(self):
        """Test that query doesn't return duplicates for objects in multiple cells."""
        obj = "object1"
        # Add object that spans multiple cells
        hitbox = HitBox(50, 50, 30, 30)  # Spans 4 cells
        self.grid.add(obj, hitbox)
        
        # Query that also spans multiple cells including the same ones
        query_hitbox = HitBox(50, 50, 30, 30)
        results = list(self.grid.query(query_hitbox))
        
        # Object should appear only once despite being in multiple queried cells
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], obj)
    
    def test_query_with_object_added_twice(self):
        """Test query when same object added twice to same cell."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        self.grid.add(obj, hitbox)
        
        results = list(self.grid.query(hitbox))
        
        # Object added twice should still only appear once in query results
        self.assertEqual(len(results), 1)
    
    def test_query_neighboring_cells(self):
        """Test that query returns objects from neighboring cells."""
        obj1 = "object1"
        obj2 = "object2"
        # Place objects in adjacent cells
        hitbox1 = HitBox(10, 10, 20, 20)  # Cell (0,0)
        hitbox2 = HitBox(70, 10, 20, 20)  # Cell (1,0)
        # Query at boundary between cells
        query_hitbox = HitBox(60, 10, 20, 20)  # Spans cells (0,0) and (1,0)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        results = list(self.grid.query(query_hitbox))
        
        # Should return both objects from neighboring cells
        self.assertEqual(len(results), 2)
        self.assertIn(obj1, results)
        self.assertIn(obj2, results)
    
    def test_query_with_negative_coordinates(self):
        """Test query with negative coordinates."""
        obj = "object1"
        hitbox = HitBox(-100, -100, 20, 20)
        
        self.grid.add(obj, hitbox)
        results = list(self.grid.query(hitbox))
        
        self.assertEqual(len(results), 1)
        self.assertIn(obj, results)
    
    def test_query_returns_generator(self):
        """Test that query returns a generator."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        result = self.grid.query(hitbox)
        
        # Should be a generator
        import types
        self.assertIsInstance(result, types.GeneratorType)


class TestSpatialGridClear(unittest.TestCase):
    """Tests for SpatialGrid clear method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_clear_empty_grid(self):
        """Test clearing an empty grid."""
        self.grid.clear()
        self.assertEqual(len(self.grid._grid), 0)
    
    def test_clear_grid_with_objects(self):
        """Test clearing grid with objects."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)
        hitbox2 = HitBox(100, 100, 20, 20)
        
        self.grid.add(obj1, hitbox1)
        self.grid.add(obj2, hitbox2)
        
        self.assertGreater(len(self.grid._grid), 0)
        
        self.grid.clear()
        
        self.assertEqual(len(self.grid._grid), 0)
    
    def test_clear_then_add(self):
        """Test adding objects after clearing."""
        obj1 = "object1"
        obj2 = "object2"
        hitbox1 = HitBox(10, 10, 20, 20)
        hitbox2 = HitBox(100, 100, 20, 20)
        
        self.grid.add(obj1, hitbox1)
        self.grid.clear()
        self.grid.add(obj2, hitbox2)
        
        results = list(self.grid.query(hitbox1))
        self.assertNotIn(obj1, results)
        
        results = list(self.grid.query(hitbox2))
        self.assertIn(obj2, results)
    
    def test_multiple_clears(self):
        """Test multiple consecutive clears."""
        obj = "object1"
        hitbox = HitBox(10, 10, 20, 20)
        
        self.grid.add(obj, hitbox)
        self.grid.clear()
        self.grid.clear()
        self.grid.clear()
        
        self.assertEqual(len(self.grid._grid), 0)


class TestSpatialGridEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_very_large_hitbox(self):
        """Test with very large hitbox."""
        obj = "large_object"
        hitbox = HitBox(0, 0, 1000, 1000)
        
        self.grid.add(obj, hitbox)
        results = list(self.grid.query(HitBox(500, 500, 10, 10)))
        
        self.assertIn(obj, results)
    
    def test_very_small_cell_size(self):
        """Test with very small cell size."""
        grid = SpatialGrid(cell_size=1)
        obj = "object1"
        hitbox = HitBox(5, 5, 10, 10)
        
        grid.add(obj, hitbox)
        results = list(grid.query(hitbox))
        
        self.assertIn(obj, results)
    
    def test_cell_size_one(self):
        """Test with cell size of 1."""
        grid = SpatialGrid(cell_size=1)
        obj = "object1"
        hitbox = HitBox(0, 0, 1, 1)
        
        grid.add(obj, hitbox)
        results = list(grid.query(hitbox))
        
        self.assertEqual(len(results), 1)
        self.assertIn(obj, results)
    
    def test_hitbox_exactly_at_origin(self):
        """Test hitbox exactly at origin."""
        obj = "object1"
        hitbox = HitBox(0, 0, 10, 10)
        
        self.grid.add(obj, hitbox)
        results = list(self.grid.query(hitbox))
        
        self.assertIn(obj, results)
    
    def test_float_coordinates(self):
        """Test with float coordinates."""
        obj = "object1"
        hitbox = HitBox(10.5, 20.7, 15.3, 25.8)
        
        self.grid.add(obj, hitbox)
        results = list(self.grid.query(hitbox))
        
        self.assertIn(obj, results)
    
    def test_many_objects_same_cell(self):
        """Test performance with many objects in same cell."""
        objects = [f"object{i}" for i in range(100)]
        hitbox = HitBox(10, 10, 20, 20)
        
        for obj in objects:
            self.grid.add(obj, hitbox)
        
        results = list(self.grid.query(hitbox))
        
        self.assertEqual(len(results), 100)
        for obj in objects:
            self.assertIn(obj, results)
    
    def test_many_objects_different_cells(self):
        """Test with many objects spread across different cells."""
        objects = []
        for i in range(10):
            for j in range(10):
                obj = f"object_{i}_{j}"
                hitbox = HitBox(i * 70, j * 70, 20, 20)
                self.grid.add(obj, hitbox)
                objects.append((obj, hitbox))
        
        # Query one specific cell
        query_hitbox = HitBox(70, 70, 20, 20)
        results = list(self.grid.query(query_hitbox))
        
        # Should only get objects from nearby cells
        self.assertGreater(len(results), 0)
        self.assertLess(len(results), 100)


class TestSpatialGridIntegration(unittest.TestCase):
    """Integration tests simulating real-world usage patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grid = SpatialGrid(cell_size=64)
    
    def test_typical_game_loop_pattern(self):
        """Test typical game loop: clear, add all objects, query."""
        # Frame 1: Add objects
        obj1 = "player"
        obj2 = "enemy1"
        obj3 = "enemy2"
        
        self.grid.add(obj1, HitBox(50, 50, 20, 20))
        self.grid.add(obj2, HitBox(100, 50, 20, 20))
        self.grid.add(obj3, HitBox(200, 200, 20, 20))
        
        # Query for collisions near player
        results = list(self.grid.query(HitBox(50, 50, 30, 30)))
        self.assertIn(obj1, results)
        self.assertIn(obj2, results)
        self.assertNotIn(obj3, results)
        
        # Frame 2: Clear and re-add with new positions
        self.grid.clear()
        self.grid.add(obj1, HitBox(60, 60, 20, 20))
        self.grid.add(obj2, HitBox(110, 60, 20, 20))
        self.grid.add(obj3, HitBox(65, 65, 20, 20))
        
        # Query again
        results = list(self.grid.query(HitBox(60, 60, 30, 30)))
        self.assertIn(obj1, results)
        self.assertIn(obj3, results)
    
    def test_moving_object_across_cells(self):
        """Test object moving across multiple cells over time."""
        obj = "moving_object"
        
        # Start in cell (0, 0)
        self.grid.add(obj, HitBox(10, 10, 20, 20))
        results = list(self.grid.query(HitBox(10, 10, 20, 20)))
        self.assertIn(obj, results)
        
        # Move to cell (1, 1)
        self.grid.clear()
        self.grid.add(obj, HitBox(100, 100, 20, 20))
        
        # Query old position - should not find it
        results = list(self.grid.query(HitBox(10, 10, 20, 20)))
        self.assertNotIn(obj, results)
        
        # Query new position - should find it
        results = list(self.grid.query(HitBox(100, 100, 20, 20)))
        self.assertIn(obj, results)
    
    def test_collision_detection_optimization(self):
        """Test that spatial grid reduces collision checks."""
        # Add objects in opposite corners
        obj1 = "object1"
        obj2 = "object2"
        
        self.grid.add(obj1, HitBox(0, 0, 20, 20))
        self.grid.add(obj2, HitBox(1000, 1000, 20, 20))
        
        # Query near obj1 should not return obj2
        results = list(self.grid.query(HitBox(0, 0, 30, 30)))
        self.assertIn(obj1, results)
        self.assertNotIn(obj2, results)