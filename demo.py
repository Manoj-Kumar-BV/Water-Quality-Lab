"""
Demo Script
Quick demonstration of the water quality testing simulation
"""

from water_sample import WaterSample, WaterQuality
from test_engine import TestEngine


def print_sample_details(sample: WaterSample):
    """Print detailed information about a water sample"""
    print(f"\n{'='*60}")
    print(f"Sample #{sample.sample_id}")
    print(f"{'='*60}")
    print(f"Source Location: {sample.source_location}")
    print(f"pH Level: {sample.ph_level} (Ideal: 6.5-8.5)")
    print(f"Turbidity: {sample.turbidity} NTU (Ideal: <5)")
    print(f"Dissolved Oxygen: {sample.dissolved_oxygen} mg/L (Ideal: >6)")
    print(f"Total Coliform: {sample.total_coliform} per 100ml (Ideal: 0)")
    print(f"Nitrate Level: {sample.nitrate_level} mg/L (Ideal: <10)")
    
    if sample.tested:
        quality = sample.get_quality_rating()
        print(f"\nQuality Rating: {quality.value}")
        print(f"Test Duration: {sample.test_duration:.2f} seconds")


def demo_sequential_vs_parallel():
    """Demonstrate sequential vs parallel testing"""
    print("\n" + "="*60)
    print("WATER QUALITY TESTING LAB - PARALLEL PROCESSING DEMO")
    print("SDG 6: Clean Water and Sanitation")
    print("="*60)
    
    # Create test engine
    engine = TestEngine()
    print(f"\nTest Engine Initialized")
    print(f"Available CPU Cores: {engine.num_workers}")
    
    # Generate sample set
    num_samples = 8
    print(f"\nGenerating {num_samples} water samples...")
    samples = [WaterSample.generate_random_sample(i+1) for i in range(num_samples)]
    
    print("\nSample Sources:")
    for sample in samples:
        print(f"  - Sample #{sample.sample_id}: {sample.source_location}")
    
    # Sequential testing
    print("\n" + "-"*60)
    print("SEQUENTIAL TESTING (One sample at a time)")
    print("-"*60)
    
    # Reset samples
    for sample in samples:
        sample.tested = False
    
    print("Starting sequential tests...")
    tested_samples_seq, seq_time = engine.test_sequential(samples.copy())
    
    print(f"✓ Sequential testing completed!")
    print(f"Total Time: {seq_time:.2f} seconds")
    print(f"Average per Sample: {seq_time/num_samples:.2f} seconds")
    
    # Parallel testing
    print("\n" + "-"*60)
    print("PARALLEL TESTING (Multiple samples simultaneously)")
    print("-"*60)
    
    # Reset samples
    for sample in samples:
        sample.tested = False
    
    print(f"Starting parallel tests with {engine.num_workers} workers...")
    tested_samples_par, par_time = engine.test_parallel_multiprocessing(samples.copy())
    
    print(f"✓ Parallel testing completed!")
    print(f"Total Time: {par_time:.2f} seconds")
    print(f"Average per Sample: {par_time/num_samples:.2f} seconds")
    
    # Performance comparison
    speedup = engine.calculate_speedup(seq_time, par_time)
    efficiency = engine.calculate_efficiency(speedup)
    time_saved = seq_time - par_time
    
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    print(f"Sequential Time:  {seq_time:.2f}s")
    print(f"Parallel Time:    {par_time:.2f}s")
    print(f"\n🚀 Speedup:       {speedup:.2f}x")
    print(f"⚡ Efficiency:    {efficiency:.1f}%")
    print(f"⏱️  Time Saved:    {time_saved:.2f}s ({time_saved/seq_time*100:.1f}%)")
    
    # Quality analysis
    print("\n" + "="*60)
    print("WATER QUALITY RESULTS")
    print("="*60)
    
    quality_counts = {
        WaterQuality.EXCELLENT: 0,
        WaterQuality.GOOD: 0,
        WaterQuality.MODERATE: 0,
        WaterQuality.POOR: 0,
        WaterQuality.UNSAFE: 0
    }
    
    for sample in tested_samples_par:
        quality = sample.get_quality_rating()
        quality_counts[quality] += 1
    
    print("\nQuality Distribution:")
    for quality, count in quality_counts.items():
        if count > 0:
            percentage = (count / num_samples) * 100
            bar = "█" * int(percentage / 5)
            print(f"  {quality.value:12} : {bar} ({count}/{num_samples} - {percentage:.0f}%)")
    
    # Show sample details
    print("\n" + "="*60)
    print("DETAILED SAMPLE ANALYSIS")
    print("="*60)
    
    # Show first 3 samples
    for sample in tested_samples_par[:3]:
        print_sample_details(sample)
    
    if num_samples > 3:
        print(f"\n... and {num_samples - 3} more samples")
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print(f"\nParallel processing achieved a {speedup:.2f}x speedup,")
    print(f"saving {time_saved:.2f} seconds ({time_saved/seq_time*100:.1f}%) in testing time.")
    print("\nThis demonstrates how parallel programming can significantly")
    print("improve water quality testing efficiency, supporting SDG 6 goals")
    print("by enabling faster and more scalable water quality monitoring.")
    print("\n" + "="*60)


if __name__ == "__main__":
    demo_sequential_vs_parallel()
