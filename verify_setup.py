"""
Setup Verification Script
Checks if the environment is properly configured to run the application
"""

import sys
import platform


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"  ✓ Python {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ✗ ERROR: Python 3.8 or higher is required")
        return False
    
    print(f"  ✓ Version check passed (>= 3.8)")
    return True


def check_pygame():
    """Check if Pygame is installed and importable"""
    print("\nChecking Pygame installation...")
    try:
        import pygame
        version = pygame.version.ver
        print(f"  ✓ Pygame {version} installed")
        
        # Test Pygame initialization
        pygame.init()
        print(f"  ✓ Pygame initialized successfully")
        pygame.quit()
        return True
    except ImportError:
        print("  ✗ ERROR: Pygame not installed")
        print("  → Run: pip install pygame")
        return False
    except Exception as e:
        print(f"  ✗ ERROR: Pygame initialization failed: {e}")
        return False


def check_multiprocessing():
    """Check if multiprocessing is available"""
    print("\nChecking multiprocessing support...")
    try:
        import multiprocessing as mp
        cpu_count = mp.cpu_count()
        print(f"  ✓ Multiprocessing available")
        print(f"  ✓ CPU cores detected: {cpu_count}")
        return True
    except Exception as e:
        print(f"  ✗ ERROR: Multiprocessing not available: {e}")
        return False


def check_project_files():
    """Check if all project files exist"""
    print("\nChecking project files...")
    import os
    
    required_files = [
        "main.py",
        "water_sample.py",
        "test_engine.py",
        "config.py",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            all_exist = False
    
    return all_exist


def check_imports():
    """Check if project modules can be imported"""
    print("\nChecking project module imports...")
    
    modules = [
        ("water_sample", "WaterSample"),
        ("test_engine", "TestEngine"),
        ("config", None)
    ]
    
    all_imported = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            if class_name:
                getattr(module, class_name)
                print(f"  ✓ {module_name}.{class_name}")
            else:
                print(f"  ✓ {module_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")
            all_imported = False
        except AttributeError as e:
            print(f"  ✗ {module_name}.{class_name}: {e}")
            all_imported = False
    
    return all_imported


def test_water_sample_generation():
    """Test if water samples can be generated"""
    print("\nTesting water sample generation...")
    try:
        from water_sample import WaterSample
        
        sample = WaterSample.generate_random_sample(1)
        print(f"  ✓ Generated sample #{sample.sample_id}")
        print(f"    - Source: {sample.source_location}")
        print(f"    - pH: {sample.ph_level}")
        print(f"    - Quality: {sample.get_quality_rating().value}")
        return True
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False


def print_system_info():
    """Print system information"""
    print("\n" + "="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Python Implementation: {platform.python_implementation()}")


def main():
    """Run all verification checks"""
    print("="*60)
    print("WATER QUALITY LAB - SETUP VERIFICATION")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Pygame Installation", check_pygame),
        ("Multiprocessing Support", check_multiprocessing),
        ("Project Files", check_project_files),
        ("Module Imports", check_imports),
        ("Sample Generation", test_water_sample_generation)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ✗ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:12} : {name}")
    
    print(f"\nResults: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to run the application.")
        print("\nTo start the application, run:")
        print("  python main.py")
        print("\nFor a CLI demo, run:")
        print("  python demo.py")
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        print("\nCommon fixes:")
        print("  - Install Pygame: pip install pygame")
        print("  - Update Python to 3.8+")
        print("  - Ensure all project files are present")
    
    print_system_info()
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
