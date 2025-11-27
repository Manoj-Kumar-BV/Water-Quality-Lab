"""
Test Engine Module
Handles parallel and sequential water quality testing
Demonstrates performance benefits of parallel programming
"""

import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Tuple, Dict
import random
from water_sample import WaterSample


class TestEngine:
    """
    Water quality test engine supporting both sequential and parallel execution.
    
    This engine demonstrates the performance benefits of parallel programming
    by comparing execution times between sequential and parallel test runs.
    """
    
    def __init__(self, num_workers: int = None):
        """
        Initialize the test engine.
        
        Args:
            num_workers: Number of parallel workers (defaults to CPU count)
        """
        self.num_workers = num_workers or mp.cpu_count()
        self.results_history: List[Dict] = []
    
    @staticmethod
    def simulate_water_test(sample: WaterSample) -> WaterSample:
        """
        Simulate water quality testing for a single sample.
        
        This function simulates the time-consuming process of testing water quality.
        In real scenarios, this would involve chemical analysis, spectroscopy, etc.
        
        Args:
            sample: WaterSample to test
            
        Returns:
            Tested WaterSample with updated status
        """
        # Simulate realistic testing time (1-3 seconds per test)
        test_duration = random.uniform(1.0, 3.0)
        time.sleep(test_duration)
        
        # Mark sample as tested
        sample.tested = True
        sample.test_duration = round(test_duration, 3)
        
        return sample
    
    def test_sequential(self, samples: List[WaterSample]) -> Tuple[List[WaterSample], float]:
        """
        Test water samples sequentially (one after another).
        
        Args:
            samples: List of WaterSample objects to test
            
        Returns:
            Tuple of (tested_samples, total_time)
        """
        start_time = time.time()
        tested_samples = []
        
        for sample in samples:
            tested_sample = self.simulate_water_test(sample)
            tested_samples.append(tested_sample)
        
        total_time = time.time() - start_time
        
        # Record results
        self.results_history.append({
            'mode': 'sequential',
            'num_samples': len(samples),
            'total_time': total_time,
            'avg_time_per_sample': total_time / len(samples) if samples else 0
        })
        
        return tested_samples, total_time
    
    def test_parallel_multiprocessing(self, samples: List[WaterSample]) -> Tuple[List[WaterSample], float]:
        """
        Test water samples in parallel using multiprocessing.
        
        Multiprocessing creates separate processes, each with its own Python interpreter.
        This is ideal for CPU-bound tasks and bypasses Python's GIL (Global Interpreter Lock).
        
        Args:
            samples: List of WaterSample objects to test
            
        Returns:
            Tuple of (tested_samples, total_time)
        """
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            tested_samples = list(executor.map(self.simulate_water_test, samples))
        
        total_time = time.time() - start_time
        
        # Record results
        self.results_history.append({
            'mode': 'parallel_multiprocessing',
            'num_samples': len(samples),
            'num_workers': self.num_workers,
            'total_time': total_time,
            'avg_time_per_sample': total_time / len(samples) if samples else 0
        })
        
        return tested_samples, total_time
    
    def test_parallel_threading(self, samples: List[WaterSample]) -> Tuple[List[WaterSample], float]:
        """
        Test water samples in parallel using threading.
        
        Threading creates lightweight threads within a single process.
        This is ideal for I/O-bound tasks. Note: Due to Python's GIL,
        threading may not provide full parallelism for CPU-bound tasks.
        
        Args:
            samples: List of WaterSample objects to test
            
        Returns:
            Tuple of (tested_samples, total_time)
        """
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            tested_samples = list(executor.map(self.simulate_water_test, samples))
        
        total_time = time.time() - start_time
        
        # Record results
        self.results_history.append({
            'mode': 'parallel_threading',
            'num_samples': len(samples),
            'num_workers': self.num_workers,
            'total_time': total_time,
            'avg_time_per_sample': total_time / len(samples) if samples else 0
        })
        
        return tested_samples, total_time
    
    def calculate_speedup(self, sequential_time: float, parallel_time: float) -> float:
        """
        Calculate speedup ratio (sequential time / parallel time).
        
        Args:
            sequential_time: Time taken for sequential execution
            parallel_time: Time taken for parallel execution
            
        Returns:
            Speedup ratio
        """
        if parallel_time == 0:
            return 0
        return sequential_time / parallel_time
    
    def calculate_efficiency(self, speedup: float) -> float:
        """
        Calculate parallel efficiency (speedup / num_workers).
        
        Args:
            speedup: Speedup ratio
            
        Returns:
            Efficiency percentage (0-100)
        """
        return (speedup / self.num_workers) * 100
    
    def get_performance_summary(self) -> Dict:
        """
        Get a summary of the most recent test runs.
        
        Returns:
            Dictionary containing performance metrics
        """
        if len(self.results_history) < 2:
            return {}
        
        # Get last sequential and parallel runs
        sequential = None
        parallel = None
        
        for result in reversed(self.results_history):
            if result['mode'] == 'sequential' and sequential is None:
                sequential = result
            elif 'parallel' in result['mode'] and parallel is None:
                parallel = result
            
            if sequential and parallel:
                break
        
        if not sequential or not parallel:
            return {}
        
        speedup = self.calculate_speedup(
            sequential['total_time'],
            parallel['total_time']
        )
        
        efficiency = self.calculate_efficiency(speedup)
        
        return {
            'sequential_time': sequential['total_time'],
            'parallel_time': parallel['total_time'],
            'speedup': speedup,
            'efficiency': efficiency,
            'num_workers': self.num_workers,
            'num_samples': parallel['num_samples'],
            'time_saved': sequential['total_time'] - parallel['total_time']
        }
