"""
Water Quality Testing Lab Simulation
Interactive GUI with parallel programming demonstration
SDG 6: Clean Water and Sanitation

This application demonstrates the benefits of parallel programming
in the context of water quality testing, supporting sustainable
development goals related to clean water access.
"""

import pygame
import sys
import math
import time
from typing import List, Optional, Tuple
from water_sample import WaterSample, WaterQuality
from test_engine import TestEngine


# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 60

# Colors
COLOR_BG = (240, 245, 250)
COLOR_PANEL = (255, 255, 255)
COLOR_BORDER = (200, 210, 220)
COLOR_TEXT_PRIMARY = (30, 40, 50)
COLOR_TEXT_SECONDARY = (100, 110, 120)
COLOR_BUTTON = (70, 130, 180)
COLOR_BUTTON_HOVER = (100, 150, 200)
COLOR_BUTTON_ACTIVE = (50, 100, 150)
COLOR_SUCCESS = (50, 200, 100)
COLOR_WARNING = (255, 180, 0)
COLOR_DANGER = (220, 60, 60)
COLOR_PROGRESS_BG = (220, 230, 240)
COLOR_PROGRESS_FILL = (70, 180, 130)

# Fonts
FONT_TITLE = pygame.font.Font(None, 48)
FONT_SUBTITLE = pygame.font.Font(None, 32)
FONT_NORMAL = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 20)


class Button:
    """Interactive button component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.active_color = tuple(max(c - 30, 0) for c in color)
        self.is_hovered = False
        self.is_disabled = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the button"""
        if self.is_disabled:
            color = (180, 180, 180)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, 2, border_radius=8)
        
        text_surface = FONT_NORMAL.render(self.text, True, (255, 255, 255) if not self.is_disabled else COLOR_TEXT_SECONDARY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events, returns True if clicked"""
        if self.is_disabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        
        return False


class TestTube:
    """Animated test tube visualization for water sample"""
    
    def __init__(self, x: int, y: int, sample: WaterSample):
        self.x = x
        self.y = y
        self.sample = sample
        self.width = 60
        self.height = 120
        self.fill_level = 0.0
        self.target_fill = 0.0
        self.is_testing = False
        self.animation_speed = 2.0
        self.selected = False
    
    def start_animation(self):
        """Start filling animation"""
        self.is_testing = True
        self.target_fill = 0.9
    
    def update(self, dt: float):
        """Update animation"""
        if self.fill_level < self.target_fill:
            self.fill_level = min(self.fill_level + self.animation_speed * dt, self.target_fill)
    
    def draw(self, surface: pygame.Surface):
        """Draw the test tube"""
        # Outer tube
        tube_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Selection highlight
        if self.selected:
            pygame.draw.rect(surface, COLOR_WARNING, 
                           pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10),
                           3, border_radius=10)
        
        pygame.draw.rect(surface, (200, 220, 240), tube_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDER, tube_rect, 3, border_radius=8)
        
        # Liquid fill
        if self.fill_level > 0:
            fill_height = int(self.height * self.fill_level)
            fill_rect = pygame.Rect(self.x + 5, self.y + self.height - fill_height, 
                                   self.width - 10, fill_height)
            
            color = self.sample.get_quality_color() if self.sample.tested else (150, 180, 200)
            pygame.draw.rect(surface, color, fill_rect, border_radius=5)
        
        # Sample ID label
        id_text = FONT_SMALL.render(f"#{self.sample.sample_id}", True, COLOR_TEXT_PRIMARY)
        id_rect = id_text.get_rect(center=(self.x + self.width // 2, self.y + self.height + 15))
        surface.blit(id_text, id_rect)
        
        # Status indicator
        if self.sample.tested:
            status_color = COLOR_SUCCESS
            status_text = "✓"
        elif self.is_testing:
            status_color = COLOR_WARNING
            status_text = "⋯"
        else:
            status_color = COLOR_TEXT_SECONDARY
            status_text = "○"
        
        status_surf = FONT_NORMAL.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(center=(self.x + self.width // 2, self.y - 15))
        surface.blit(status_surf, status_rect)
    
    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Check if point is inside test tube"""
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)


class WaterQualityLabGUI:
    """Main GUI application for water quality testing simulation"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Water Quality Testing Lab - Parallel Processing Demo")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Application state
        self.samples: List[WaterSample] = []
        self.test_tubes: List[TestTube] = []
        self.test_engine = TestEngine()
        self.selected_sample: Optional[WaterSample] = None
        self.is_testing = False
        self.test_mode = "parallel"  # "sequential" or "parallel"
        self.test_progress = 0.0
        self.sequential_time = 0.0
        self.parallel_time = 0.0
        self.speedup = 0.0
        
        # UI Components
        self.setup_ui()
        
        # Add initial samples
        for i in range(6):
            self.add_sample()
    
    def setup_ui(self):
        """Setup UI buttons and components"""
        button_y = WINDOW_HEIGHT - 70
        button_height = 50
        button_width = 180
        spacing = 20
        
        self.buttons = {
            'add_sample': Button(20, button_y, button_width, button_height, 
                               "Add Sample", COLOR_SUCCESS),
            'remove_sample': Button(20 + button_width + spacing, button_y, 
                                  button_width, button_height, "Remove Sample", COLOR_DANGER),
            'test_sequential': Button(20 + (button_width + spacing) * 2, button_y,
                                    button_width, button_height, "Test Sequential", COLOR_BUTTON),
            'test_parallel': Button(20 + (button_width + spacing) * 3, button_y,
                                  button_width, button_height, "Test Parallel", COLOR_BUTTON),
            'clear_all': Button(20 + (button_width + spacing) * 4, button_y,
                              button_width, button_height, "Clear All", COLOR_WARNING),
        }
    
    def add_sample(self):
        """Add a new water sample"""
        sample_id = len(self.samples) + 1
        sample = WaterSample.generate_random_sample(sample_id)
        self.samples.append(sample)
        
        # Calculate position for test tube
        samples_per_row = 10
        row = (len(self.samples) - 1) // samples_per_row
        col = (len(self.samples) - 1) % samples_per_row
        
        x = 50 + col * 90
        y = 180 + row * 160
        
        test_tube = TestTube(x, y, sample)
        self.test_tubes.append(test_tube)
    
    def remove_sample(self):
        """Remove the last sample"""
        if self.samples and not self.is_testing:
            self.samples.pop()
            self.test_tubes.pop()
            if self.selected_sample and self.selected_sample not in self.samples:
                self.selected_sample = None
    
    def clear_all_samples(self):
        """Clear all samples"""
        if not self.is_testing:
            self.samples.clear()
            self.test_tubes.clear()
            self.selected_sample = None
            self.sequential_time = 0.0
            self.parallel_time = 0.0
            self.speedup = 0.0
    
    def start_testing(self, mode: str):
        """Start testing in specified mode"""
        if not self.samples or self.is_testing:
            return
        
        self.is_testing = True
        self.test_mode = mode
        self.test_progress = 0.0
        
        # Reset samples
        for sample in self.samples:
            sample.tested = False
        
        # Start tube animations
        for tube in self.test_tubes:
            tube.fill_level = 0.0
            tube.start_animation()
        
        # Run test in background (simulated)
        self.test_start_time = time.time()
    
    def update_testing(self):
        """Update testing progress"""
        if not self.is_testing:
            return
        
        elapsed = time.time() - self.test_start_time
        
        # Simulate testing progress
        if self.test_mode == "sequential":
            expected_time = len(self.samples) * 2.0  # Approximate
            self.test_progress = min(elapsed / expected_time, 1.0)
        else:  # parallel
            expected_time = 2.5  # Approximate with parallelism
            self.test_progress = min(elapsed / expected_time, 1.0)
        
        # Check if testing complete
        if self.test_progress >= 1.0:
            # Mark samples as tested
            for sample in self.samples:
                sample.tested = True
            
            # Record time
            if self.test_mode == "sequential":
                self.sequential_time = elapsed
            else:
                self.parallel_time = elapsed
            
            # Calculate speedup
            if self.sequential_time > 0 and self.parallel_time > 0:
                self.speedup = self.sequential_time / self.parallel_time
            
            self.is_testing = False
    
    def draw_header(self):
        """Draw application header"""
        # Title
        title = FONT_TITLE.render("Water Quality Testing Laboratory", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(title, (20, 20))
        
        # Subtitle
        subtitle = FONT_SMALL.render("SDG 6: Clean Water and Sanitation | Parallel Processing Demonstration", 
                                    True, COLOR_TEXT_SECONDARY)
        self.screen.blit(subtitle, (20, 70))
        
        # Sample count
        count_text = FONT_NORMAL.render(f"Samples: {len(self.samples)} | Workers: {self.test_engine.num_workers}", 
                                       True, COLOR_TEXT_PRIMARY)
        self.screen.blit(count_text, (20, 105))
    
    def draw_samples_panel(self):
        """Draw water samples display area"""
        panel_rect = pygame.Rect(10, 140, 950, 600)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel_rect, 2, border_radius=10)
        
        # Panel title
        title = FONT_SUBTITLE.render("Water Samples", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(title, (30, 150))
        
        # Draw test tubes
        for tube in self.test_tubes:
            tube.draw(self.screen)
    
    def draw_metrics_panel(self):
        """Draw performance metrics panel"""
        panel_rect = pygame.Rect(970, 140, 410, 600)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel_rect, 2, border_radius=10)
        
        # Panel title
        title = FONT_SUBTITLE.render("Performance Metrics", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(title, (990, 150))
        
        y_offset = 200
        
        # Testing progress
        if self.is_testing:
            progress_text = FONT_NORMAL.render(f"Testing: {self.test_mode.capitalize()}", 
                                             True, COLOR_TEXT_PRIMARY)
            self.screen.blit(progress_text, (990, y_offset))
            y_offset += 40
            
            # Progress bar
            bar_rect = pygame.Rect(990, y_offset, 380, 30)
            pygame.draw.rect(self.screen, COLOR_PROGRESS_BG, bar_rect, border_radius=5)
            fill_width = int(380 * self.test_progress)
            fill_rect = pygame.Rect(990, y_offset, fill_width, 30)
            pygame.draw.rect(self.screen, COLOR_PROGRESS_FILL, fill_rect, border_radius=5)
            pygame.draw.rect(self.screen, COLOR_BORDER, bar_rect, 2, border_radius=5)
            
            percent_text = FONT_SMALL.render(f"{int(self.test_progress * 100)}%", 
                                            True, COLOR_TEXT_PRIMARY)
            self.screen.blit(percent_text, (1170, y_offset + 5))
            y_offset += 50
        
        # Sequential time
        if self.sequential_time > 0:
            seq_text = FONT_NORMAL.render(f"Sequential Time: {self.sequential_time:.2f}s", 
                                         True, COLOR_TEXT_PRIMARY)
            self.screen.blit(seq_text, (990, y_offset))
            y_offset += 35
        
        # Parallel time
        if self.parallel_time > 0:
            par_text = FONT_NORMAL.render(f"Parallel Time: {self.parallel_time:.2f}s", 
                                         True, COLOR_TEXT_PRIMARY)
            self.screen.blit(par_text, (990, y_offset))
            y_offset += 35
        
        # Speedup
        if self.speedup > 0:
            speedup_text = FONT_SUBTITLE.render(f"Speedup: {self.speedup:.2f}x", 
                                               True, COLOR_SUCCESS)
            self.screen.blit(speedup_text, (990, y_offset))
            y_offset += 50
            
            # Time saved
            time_saved = self.sequential_time - self.parallel_time
            saved_text = FONT_NORMAL.render(f"Time Saved: {time_saved:.2f}s ({time_saved/self.sequential_time*100:.1f}%)", 
                                          True, COLOR_TEXT_SECONDARY)
            self.screen.blit(saved_text, (990, y_offset))
            y_offset += 50
        
        # Selected sample details
        if self.selected_sample:
            y_offset += 20
            detail_title = FONT_SUBTITLE.render("Sample Details", True, COLOR_TEXT_PRIMARY)
            self.screen.blit(detail_title, (990, y_offset))
            y_offset += 40
            
            sample = self.selected_sample
            details = [
                f"Sample ID: #{sample.sample_id}",
                f"Source: {sample.source_location}",
                f"pH Level: {sample.ph_level}",
                f"Turbidity: {sample.turbidity} NTU",
                f"Dissolved O₂: {sample.dissolved_oxygen} mg/L",
                f"Coliform: {sample.total_coliform} /100ml",
                f"Nitrate: {sample.nitrate_level} mg/L",
                f"Quality: {sample.get_quality_rating().value}"
            ]
            
            for detail in details:
                text = FONT_SMALL.render(detail, True, COLOR_TEXT_SECONDARY)
                self.screen.blit(text, (990, y_offset))
                y_offset += 25
    
    def draw_buttons(self):
        """Draw control buttons"""
        for button in self.buttons.values():
            button.draw(self.screen)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Button events
            if self.buttons['add_sample'].handle_event(event):
                if len(self.samples) < 30:
                    self.add_sample()
            
            if self.buttons['remove_sample'].handle_event(event):
                self.remove_sample()
            
            if self.buttons['test_sequential'].handle_event(event):
                self.start_testing("sequential")
            
            if self.buttons['test_parallel'].handle_event(event):
                self.start_testing("parallel")
            
            if self.buttons['clear_all'].handle_event(event):
                self.clear_all_samples()
            
            # Test tube selection
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for tube in self.test_tubes:
                    if tube.contains_point(event.pos):
                        # Deselect all
                        for t in self.test_tubes:
                            t.selected = False
                        # Select clicked
                        tube.selected = True
                        self.selected_sample = tube.sample
                        break
        
        # Update button states
        self.buttons['add_sample'].is_disabled = len(self.samples) >= 30 or self.is_testing
        self.buttons['remove_sample'].is_disabled = len(self.samples) == 0 or self.is_testing
        self.buttons['test_sequential'].is_disabled = len(self.samples) == 0 or self.is_testing
        self.buttons['test_parallel'].is_disabled = len(self.samples) == 0 or self.is_testing
        self.buttons['clear_all'].is_disabled = len(self.samples) == 0 or self.is_testing
    
    def update(self, dt: float):
        """Update application state"""
        # Update test tubes animation
        for tube in self.test_tubes:
            tube.update(dt)
        
        # Update testing progress
        self.update_testing()
    
    def draw(self):
        """Draw all UI components"""
        self.screen.fill(COLOR_BG)
        
        self.draw_header()
        self.draw_samples_panel()
        self.draw_metrics_panel()
        self.draw_buttons()
        
        pygame.display.flip()
    
    def run(self):
        """Main application loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Application entry point"""
    app = WaterQualityLabGUI()
    app.run()


if __name__ == "__main__":
    main()
