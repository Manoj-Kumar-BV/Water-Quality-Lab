"""
Water Sample Module
Represents individual water samples with quality parameters
Supports SDG 6: Clean Water and Sanitation
"""

import random
from dataclasses import dataclass
from typing import Tuple
from enum import Enum


class WaterQuality(Enum):
    """Water quality classification based on test results"""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    MODERATE = "Moderate"
    POOR = "Poor"
    UNSAFE = "Unsafe"


@dataclass
class WaterSample:
    """
    Represents a water sample with various quality parameters.
    
    Attributes:
        sample_id: Unique identifier for the sample
        ph_level: pH level (0-14, ideal: 6.5-8.5)
        turbidity: Turbidity in NTU (Nephelometric Turbidity Units, ideal: <5)
        dissolved_oxygen: DO in mg/L (ideal: >6)
        total_coliform: Coliform bacteria count per 100ml (ideal: 0)
        nitrate_level: Nitrate concentration in mg/L (ideal: <10)
        source_location: Origin of the water sample
    """
    sample_id: int
    ph_level: float
    turbidity: float
    dissolved_oxygen: float
    total_coliform: int
    nitrate_level: float
    source_location: str
    tested: bool = False
    test_duration: float = 0.0
    
    @staticmethod
    def generate_random_sample(sample_id: int) -> 'WaterSample':
        """
        Generate a random water sample with realistic parameters.
        
        Args:
            sample_id: Unique identifier for the sample
            
        Returns:
            WaterSample instance with random parameters
        """
        locations = [
            "River Delta", "Mountain Spring", "Urban Lake", 
            "Coastal Bay", "Underground Well", "Reservoir",
            "Treatment Plant", "Agricultural Runoff", "Industrial Area"
        ]
        
        # Generate realistic ranges with some variation
        quality_type = random.choice(['excellent', 'good', 'moderate', 'poor', 'unsafe'])
        
        if quality_type == 'excellent':
            ph = random.uniform(7.0, 8.0)
            turbidity = random.uniform(0.5, 2.0)
            do = random.uniform(7.0, 10.0)
            coliform = random.randint(0, 1)
            nitrate = random.uniform(0.5, 3.0)
        elif quality_type == 'good':
            ph = random.uniform(6.5, 8.5)
            turbidity = random.uniform(2.0, 5.0)
            do = random.uniform(6.0, 8.0)
            coliform = random.randint(0, 10)
            nitrate = random.uniform(3.0, 8.0)
        elif quality_type == 'moderate':
            ph = random.uniform(6.0, 9.0)
            turbidity = random.uniform(5.0, 15.0)
            do = random.uniform(4.0, 6.0)
            coliform = random.randint(10, 50)
            nitrate = random.uniform(8.0, 15.0)
        elif quality_type == 'poor':
            ph = random.uniform(5.5, 9.5)
            turbidity = random.uniform(15.0, 50.0)
            do = random.uniform(2.0, 4.0)
            coliform = random.randint(50, 200)
            nitrate = random.uniform(15.0, 30.0)
        else:  # unsafe
            ph = random.uniform(4.0, 11.0)
            turbidity = random.uniform(50.0, 200.0)
            do = random.uniform(0.5, 2.0)
            coliform = random.randint(200, 1000)
            nitrate = random.uniform(30.0, 100.0)
        
        return WaterSample(
            sample_id=sample_id,
            ph_level=round(ph, 2),
            turbidity=round(turbidity, 2),
            dissolved_oxygen=round(do, 2),
            total_coliform=coliform,
            nitrate_level=round(nitrate, 2),
            source_location=random.choice(locations)
        )
    
    def get_quality_rating(self) -> WaterQuality:
        """
        Determine overall water quality based on all parameters.
        
        Returns:
            WaterQuality enum value
        """
        if not self.tested:
            return WaterQuality.MODERATE
        
        score = 0
        max_score = 5
        
        # pH scoring (ideal: 6.5-8.5)
        if 6.5 <= self.ph_level <= 8.5:
            score += 1
        elif 6.0 <= self.ph_level <= 9.0:
            score += 0.5
        
        # Turbidity scoring (ideal: <5 NTU)
        if self.turbidity < 5:
            score += 1
        elif self.turbidity < 15:
            score += 0.5
        
        # Dissolved Oxygen scoring (ideal: >6 mg/L)
        if self.dissolved_oxygen >= 6:
            score += 1
        elif self.dissolved_oxygen >= 4:
            score += 0.5
        
        # Coliform scoring (ideal: 0)
        if self.total_coliform == 0:
            score += 1
        elif self.total_coliform < 10:
            score += 0.7
        elif self.total_coliform < 50:
            score += 0.3
        
        # Nitrate scoring (ideal: <10 mg/L)
        if self.nitrate_level < 10:
            score += 1
        elif self.nitrate_level < 20:
            score += 0.5
        
        # Convert score to quality rating
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return WaterQuality.EXCELLENT
        elif percentage >= 70:
            return WaterQuality.GOOD
        elif percentage >= 50:
            return WaterQuality.MODERATE
        elif percentage >= 30:
            return WaterQuality.POOR
        else:
            return WaterQuality.UNSAFE
    
    def get_quality_color(self) -> Tuple[int, int, int]:
        """
        Get RGB color representation of water quality.
        
        Returns:
            Tuple of (R, G, B) values
        """
        quality = self.get_quality_rating()
        
        color_map = {
            WaterQuality.EXCELLENT: (0, 200, 100),      # Bright green
            WaterQuality.GOOD: (100, 220, 100),         # Light green
            WaterQuality.MODERATE: (255, 200, 0),       # Yellow
            WaterQuality.POOR: (255, 130, 0),           # Orange
            WaterQuality.UNSAFE: (220, 50, 50)          # Red
        }
        
        return color_map.get(quality, (150, 150, 150))
    
    def __str__(self) -> str:
        """String representation of the water sample"""
        status = "✓ Tested" if self.tested else "○ Pending"
        return (f"Sample #{self.sample_id} [{status}]\n"
                f"Source: {self.source_location}\n"
                f"Quality: {self.get_quality_rating().value}")
