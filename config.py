"""
Sample Dataset Configuration
Pre-configured water samples for testing
"""

SAMPLE_LOCATIONS = [
    "River Delta",
    "Mountain Spring",
    "Urban Lake",
    "Coastal Bay",
    "Underground Well",
    "Reservoir",
    "Treatment Plant",
    "Agricultural Runoff",
    "Industrial Area",
    "Rainwater Collection",
    "Desalination Plant",
    "Natural Spring",
    "Municipal Supply",
    "Irrigation Canal",
    "Wetland Area"
]

# Pre-defined sample datasets for consistent testing
PRESET_SAMPLES = {
    "excellent_set": [
        {"ph": 7.2, "turbidity": 1.5, "do": 8.5, "coliform": 0, "nitrate": 2.0, "location": "Mountain Spring"},
        {"ph": 7.4, "turbidity": 0.8, "do": 9.0, "coliform": 0, "nitrate": 1.5, "location": "Natural Spring"},
        {"ph": 7.6, "turbidity": 1.2, "do": 8.0, "coliform": 0, "nitrate": 2.5, "location": "Treatment Plant"},
    ],
    "mixed_quality": [
        {"ph": 7.2, "turbidity": 1.5, "do": 8.5, "coliform": 0, "nitrate": 2.0, "location": "Mountain Spring"},
        {"ph": 6.8, "turbidity": 4.5, "do": 6.5, "coliform": 5, "nitrate": 7.0, "location": "Urban Lake"},
        {"ph": 8.0, "turbidity": 12.0, "do": 5.0, "coliform": 25, "nitrate": 12.0, "location": "Reservoir"},
        {"ph": 5.8, "turbidity": 35.0, "do": 3.0, "coliform": 150, "nitrate": 25.0, "location": "Agricultural Runoff"},
        {"ph": 9.2, "turbidity": 80.0, "do": 1.5, "coliform": 500, "nitrate": 45.0, "location": "Industrial Area"},
    ],
    "contaminated_set": [
        {"ph": 5.5, "turbidity": 45.0, "do": 2.5, "coliform": 180, "nitrate": 28.0, "location": "Agricultural Runoff"},
        {"ph": 9.5, "turbidity": 95.0, "do": 1.2, "coliform": 450, "nitrate": 55.0, "location": "Industrial Area"},
        {"ph": 6.0, "turbidity": 60.0, "do": 2.0, "coliform": 300, "nitrate": 35.0, "location": "Urban Runoff"},
    ]
}

# Water quality parameter ranges
PARAMETER_RANGES = {
    "ph": {
        "min": 0.0,
        "max": 14.0,
        "ideal_min": 6.5,
        "ideal_max": 8.5,
        "unit": ""
    },
    "turbidity": {
        "min": 0.0,
        "max": 200.0,
        "ideal_max": 5.0,
        "unit": "NTU"
    },
    "dissolved_oxygen": {
        "min": 0.0,
        "max": 15.0,
        "ideal_min": 6.0,
        "unit": "mg/L"
    },
    "coliform": {
        "min": 0,
        "max": 1000,
        "ideal": 0,
        "unit": "per 100ml"
    },
    "nitrate": {
        "min": 0.0,
        "max": 100.0,
        "ideal_max": 10.0,
        "unit": "mg/L"
    }
}

# Testing configuration
TEST_CONFIG = {
    "min_test_duration": 1.0,  # seconds
    "max_test_duration": 3.0,  # seconds
    "max_samples": 30,
    "default_samples": 6
}
