import unittest
from unittest.mock import patch, Mock
import time
from data.api.clock import Clock


class TestClockInitialization(unittest.TestCase):
    """Tests for Clock initialization."""
    
    def test_init_default_buffer_size(self):
        """Test initialization with default buffer size."""
        clock = Clock()
        self.assertEqual(clock._frame_times.maxlen, 10)
        self.assertEqual(len(clock._frame_times), 0)
    
    def test_init_custom_buffer_size(self):
        """Test initialization with custom buffer size."""
        clock = Clock(buffer_size=20)
        self.assertEqual(clock._frame_times.maxlen, 20)
    
    def test_init_small_buffer_size(self):
        """Test initialization with small buffer size."""
        clock = Clock(buffer_size=1)
        self.assertEqual(clock._frame_times.maxlen, 1)
    
    def test_init_large_buffer_size(self):
        """Test initialization with large buffer size."""
        clock = Clock(buffer_size=1000)
        self.assertEqual(clock._frame_times.maxlen, 1000)
    
    def test_init_sets_last_time(self):
        """Test that initialization sets last_time."""
        before = time.perf_counter()
        clock = Clock()
        after = time.perf_counter()
        
        self.assertGreaterEqual(clock._last_time, before)
        self.assertLessEqual(clock._last_time, after)
    
    def test_init_frame_times_empty(self):
        """Test that frame_times starts empty."""
        clock = Clock()
        self.assertEqual(len(clock._frame_times), 0)


class TestClockTickNoFPSLimit(unittest.TestCase):
    """Tests for Clock tick method without FPS limiting."""
    
    def test_tick_no_fps_returns_milliseconds(self):
        """Test that tick returns elapsed time in milliseconds."""
        clock = Clock()
        time.sleep(0.01)  # Sleep 10ms
        
        elapsed = clock.tick()
        
        # Should be approximately 10ms (with some tolerance)
        self.assertGreaterEqual(elapsed, 9)
        self.assertLessEqual(elapsed, 15)
    
    def test_tick_no_fps_updates_last_time(self):
        """Test that tick updates last_time."""
        clock = Clock()
        initial_time = clock._last_time
        
        time.sleep(0.01)
        clock.tick()
        
        self.assertGreater(clock._last_time, initial_time)
    
    def test_tick_no_fps_appends_frame_time(self):
        """Test that tick appends to frame_times."""
        clock = Clock()
        
        self.assertEqual(len(clock._frame_times), 0)
        
        clock.tick()
        
        self.assertEqual(len(clock._frame_times), 1)
        self.assertGreater(clock._frame_times[0], 0)
    
    def test_tick_multiple_calls(self):
        """Test multiple tick calls."""
        clock = Clock()
        
        for i in range(5):
            time.sleep(0.001)
            elapsed = clock.tick()
            self.assertGreater(elapsed, 0)
        
        self.assertEqual(len(clock._frame_times), 5)
    
    def test_tick_with_none_fps(self):
        """Test tick with explicit None fps."""
        clock = Clock()
        time.sleep(0.01)
        
        elapsed = clock.tick(fps=None)
        
        self.assertGreater(elapsed, 0)
    
    def test_tick_with_zero_fps(self):
        """Test tick with zero fps (no limiting)."""
        clock = Clock()
        time.sleep(0.01)
        
        elapsed = clock.tick(fps=0)
        
        self.assertGreater(elapsed, 0)
    
    def test_tick_with_negative_fps(self):
        """Test tick with negative fps (no limiting)."""
        clock = Clock()
        time.sleep(0.01)
        
        elapsed = clock.tick(fps=-10)
        
        self.assertGreater(elapsed, 0)


class TestClockTickWithFPSLimit(unittest.TestCase):
    """Tests for Clock tick method with FPS limiting."""
    
    def test_tick_with_fps_limit_sleeps(self):
        """Test that tick sleeps to maintain FPS."""
        clock = Clock()
        
        # First tick to initialize
        clock.tick(fps=60)
        
        # Immediate second tick should sleep
        start = time.perf_counter()
        elapsed_ms = clock.tick(fps=60)
        end = time.perf_counter()
        
        actual_duration = end - start
        expected_duration = 1.0 / 60.0
        
        # Should have slept to reach frame duration
        self.assertGreaterEqual(actual_duration, expected_duration * 0.9)
    
    def test_tick_fps_60_returns_approximately_16ms(self):
        """Test that 60 FPS returns approximately 16ms per frame."""
        clock = Clock()
        
        # Run several frames
        for _ in range(3):
            elapsed = clock.tick(fps=60)
            # 1000ms / 60fps ≈ 16.67ms per frame
            self.assertGreaterEqual(elapsed, 15)
            self.assertLessEqual(elapsed, 18)
    
    def test_tick_fps_30_returns_approximately_33ms(self):
        """Test that 30 FPS returns approximately 33ms per frame."""
        clock = Clock()
        
        for _ in range(3):
            elapsed = clock.tick(fps=30)
            # 1000ms / 30fps ≈ 33.33ms per frame
            self.assertGreaterEqual(elapsed, 31)
            self.assertLessEqual(elapsed, 36)
    
    def test_tick_fps_120(self):
        """Test tick with 120 FPS."""
        clock = Clock()
        
        elapsed = clock.tick(fps=120)
        
        # 1000ms / 120fps ≈ 8.33ms per frame
        self.assertGreaterEqual(elapsed, 7)
        self.assertLessEqual(elapsed, 10)
    
    def test_tick_fps_updates_frame_times(self):
        """Test that tick with FPS limit still updates frame_times."""
        clock = Clock()
        
        clock.tick(fps=60)
        clock.tick(fps=60)
        
        self.assertEqual(len(clock._frame_times), 2)
        
        # Frame times should be approximately 1/60 second
        for dt in clock._frame_times:
            self.assertGreaterEqual(dt, 0.015)
            self.assertLessEqual(dt, 0.018)
    
    def test_tick_slow_frame_no_negative_sleep(self):
        """Test that slow frames don't cause negative sleep."""
        clock = Clock()
        
        # First tick
        clock.tick(fps=60)
        
        # Simulate slow frame
        time.sleep(0.05)  # 50ms (slower than 60 FPS)
        
        elapsed = clock.tick(fps=60)
        
        # Should return actual elapsed time, not target
        self.assertGreater(elapsed, 16)


class TestClockGetFPS(unittest.TestCase):
    """Tests for Clock get_fps method."""
    
    def test_get_fps_empty_buffer(self):
        """Test get_fps with empty buffer returns 0."""
        clock = Clock()
        
        fps = clock.get_fps()
        
        self.assertEqual(fps, 0.0)
    
    def test_get_fps_after_one_tick(self):
        """Test get_fps after one tick."""
        clock = Clock()
        
        clock.tick(fps=60)
        
        fps = clock.get_fps()
        
        # Should be approximately 60 FPS
        self.assertGreaterEqual(fps, 55)
        self.assertLessEqual(fps, 65)
    
    def test_get_fps_after_multiple_ticks(self):
        """Test get_fps after multiple ticks."""
        clock = Clock()
        
        for _ in range(10):
            clock.tick(fps=60)
        
        fps = clock.get_fps()
        
        # Average should be close to 60 FPS
        self.assertGreaterEqual(fps, 58)
        self.assertLessEqual(fps, 62)
    
    def test_get_fps_with_30_fps_target(self):
        """Test get_fps with 30 FPS target."""
        clock = Clock()
        
        for _ in range(10):
            clock.tick(fps=30)
        
        fps = clock.get_fps()
        
        # Should be approximately 30 FPS
        self.assertGreaterEqual(fps, 28)
        self.assertLessEqual(fps, 32)
    
    def test_get_fps_no_limit(self):
        """Test get_fps without FPS limiting."""
        clock = Clock()
        
        for _ in range(5):
            clock.tick()  # No FPS limit
        
        fps = clock.get_fps()
        
        # Should be high (system dependent)
        self.assertGreater(fps, 0)
    
    def test_get_fps_buffer_overflow(self):
        """Test that get_fps uses buffer correctly after overflow."""
        clock = Clock(buffer_size=5)
        
        # Fill buffer beyond capacity
        for _ in range(10):
            clock.tick(fps=60)
        
        # Buffer should only have 5 entries
        self.assertEqual(len(clock._frame_times), 5)
        
        fps = clock.get_fps()
        self.assertGreater(fps, 0)
    
    def test_get_fps_zero_frame_time(self):
        """Test get_fps handles zero average frame time."""
        clock = Clock()
        
        # Manually set frame times to zero (edge case)
        clock._frame_times.append(0.0)
        
        fps = clock.get_fps()
        
        self.assertEqual(fps, 0.0)


class TestClockBufferBehavior(unittest.TestCase):
    """Tests for Clock buffer management."""
    
    def test_buffer_maxlen_enforced(self):
        """Test that buffer enforces maxlen."""
        clock = Clock(buffer_size=3)
        
        # Add 5 frames
        for _ in range(5):
            clock.tick()
        
        # Should only have 3 entries (most recent)
        self.assertEqual(len(clock._frame_times), 3)
    
    def test_buffer_contains_recent_times(self):
        """Test that buffer contains most recent times."""
        clock = Clock(buffer_size=2)
        
        clock.tick()
        time.sleep(0.01)
        clock.tick()
        time.sleep(0.02)
        clock.tick()  # This and previous should remain
        
        # Should have 2 entries
        self.assertEqual(len(clock._frame_times), 2)
        
        # Most recent should be approximately 0.02
        self.assertGreaterEqual(clock._frame_times[-1], 0.019)
    
    def test_buffer_size_one(self):
        """Test buffer with size 1."""
        clock = Clock(buffer_size=1)
        
        clock.tick()
        first_time = clock._frame_times[0]
        
        time.sleep(0.01)
        clock.tick()
        second_time = clock._frame_times[0]
        
        # Should only have one entry
        self.assertEqual(len(clock._frame_times), 1)
        # Should be the most recent
        self.assertNotEqual(first_time, second_time)


class TestClockEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_very_high_fps_limit(self):
        """Test with very high FPS limit."""
        clock = Clock()
        
        elapsed = clock.tick(fps=1000)
        
        # Should be approximately 1ms per frame
        self.assertGreaterEqual(elapsed, 0)
        self.assertLessEqual(elapsed, 3)
    
    def test_very_low_fps_limit(self):
        """Test with very low FPS limit."""
        clock = Clock()
        
        # Don't actually run at 1 FPS as it would take 1 second
        # Just verify it doesn't crash
        clock._last_time = time.perf_counter() - 0.5  # Fake previous time
        elapsed = clock.tick(fps=2)
        
        # Should return actual elapsed time
        self.assertGreater(elapsed, 0)
    
    def test_fractional_fps(self):
        """Test with fractional FPS values."""
        clock = Clock()
        
        elapsed = clock.tick(fps=59.94)  # NTSC frame rate
        
        # Should handle fractional FPS
        self.assertGreater(elapsed, 0)
        self.assertLessEqual(elapsed, 20)
    
    def test_consecutive_ticks_without_sleep(self):
        """Test multiple consecutive ticks."""
        clock = Clock()
        
        times = []
        for _ in range(10):
            elapsed = clock.tick(fps=60)
            times.append(elapsed)
        
        # All should be reasonable values
        for t in times:
            self.assertGreaterEqual(t, 15)
            self.assertLessEqual(t, 20)
    
    def test_tick_after_long_pause(self):
        """Test tick after a long pause."""
        clock = Clock()
        
        clock.tick(fps=60)
        
        # Simulate long pause
        time.sleep(0.5)
        
        elapsed = clock.tick(fps=60)
        
        # Should return actual elapsed time (500ms)
        self.assertGreaterEqual(elapsed, 490)
    
    def test_get_fps_with_single_very_long_frame(self):
        """Test get_fps with one very long frame."""
        clock = Clock()
        
        clock.tick(fps=60)
        time.sleep(1.0)  # 1 second pause
        clock.tick()
        
        fps = clock.get_fps()
        
        # FPS should be very low due to long frame
        self.assertLess(fps, 10)


class TestClockAccuracy(unittest.TestCase):
    """Tests for clock timing accuracy."""
    
    def test_tick_elapsed_time_accuracy(self):
        """Test that tick accurately measures elapsed time."""
        clock = Clock()
        
        sleep_time = 0.05  # 50ms
        time.sleep(sleep_time)
        elapsed = clock.tick()
        
        # Should be approximately 50ms
        self.assertGreaterEqual(elapsed, 48)
        self.assertLessEqual(elapsed, 55)
    
    def test_fps_calculation_accuracy(self):
        """Test that FPS calculation is accurate."""
        clock = Clock()
        
        # Run at 60 FPS for several frames
        for _ in range(20):
            clock.tick(fps=60)
        
        fps = clock.get_fps()
        
        # Should be very close to 60 FPS
        self.assertGreaterEqual(fps, 59)
        self.assertLessEqual(fps, 61)
    
    def test_frame_time_consistency(self):
        """Test that frame times are consistent with FPS limit."""
        clock = Clock(buffer_size=10)
        
        for _ in range(10):
            clock.tick(fps=60)
        
        # All frame times should be similar
        times = list(clock._frame_times)
        avg_time = sum(times) / len(times)
        
        for dt in times:
            # Each frame should be within 10% of average
            self.assertAlmostEqual(dt, avg_time, delta=avg_time * 0.1)


class TestClockIntegration(unittest.TestCase):
    """Integration tests simulating real-world usage."""
    
    def test_typical_game_loop_60fps(self):
        """Test typical game loop at 60 FPS."""
        clock = Clock()
        
        frames = 0
        start_time = time.perf_counter()
        target_frames = 30
        
        while frames < target_frames:
            clock.tick(fps=60)
            frames += 1
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # 30 frames at 60 FPS should take ~0.5 seconds
        self.assertGreaterEqual(duration, 0.48)
        self.assertLessEqual(duration, 0.55)
        
        fps = clock.get_fps()
        self.assertGreaterEqual(fps, 58)
        self.assertLessEqual(fps, 62)
    
    def test_variable_frame_times(self):
        """Test with variable processing times per frame."""
        clock = Clock()
        
        for i in range(10):
            # Simulate variable work
            if i % 3 == 0:
                time.sleep(0.005)
            
            clock.tick(fps=60)
        
        fps = clock.get_fps()
        
        # Should still maintain approximately 60 FPS
        self.assertGreaterEqual(fps, 55)
        self.assertLessEqual(fps, 65)
    
    def test_unlocked_fps_benchmark(self):
        """Test unlocked FPS (no limit)."""
        clock = Clock()
        
        frames = 0
        start_time = time.perf_counter()
        target_duration = 0.1  # Run for 100ms
        
        while time.perf_counter() - start_time < target_duration:
            clock.tick()  # No FPS limit
            frames += 1
        
        fps = clock.get_fps()
        
        # Should be much higher than 60
        self.assertGreater(fps, 100)
        self.assertGreater(frames, 10)
