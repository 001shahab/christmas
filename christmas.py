"""
Merry Christmas & Happy New Year - Magical Animation
=====================================================
A stunning festive visualization featuring a decorated Christmas tree,
falling snowflakes, twinkling stars, and spectacular New Year fireworks.

Created by: Prof. Shahab Anbarjafari
Organization: 3S Holding OU, Tartu, Estonia
"""

import pygame
import math
import random
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen configuration
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Merry Christmas & Happy New Year! ✨")
clock = pygame.time.Clock()

# Color palette - Rich, warm festive colors
COLORS = {
    'night_sky_top': (10, 15, 44),
    'night_sky_bottom': (25, 35, 75),
    'snow_ground': (240, 248, 255),
    'tree_dark': (20, 60, 30),
    'tree_mid': (34, 85, 45),
    'tree_light': (45, 110, 55),
    'trunk': (101, 67, 33),
    'trunk_dark': (70, 45, 20),
    'gold': (255, 215, 0),
    'star_glow': (255, 255, 200),
    'ornament_red': (220, 20, 60),
    'ornament_gold': (255, 200, 50),
    'ornament_blue': (65, 105, 225),
    'ornament_silver': (192, 192, 210),
    'ornament_purple': (148, 0, 211),
    'white': (255, 255, 255),
    'snow': (250, 250, 255),
}


@dataclass
class Particle:
    """Base particle class for various effects"""
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float


class Snowflake:
    """Beautiful falling snowflake with drift and rotation"""
    def __init__(self):
        self.reset()
        self.y = random.uniform(-50, HEIGHT)
        
    def reset(self):
        self.x = random.uniform(-50, WIDTH + 50)
        self.y = random.uniform(-100, -10)
        self.size = random.uniform(2, 6)
        self.speed = random.uniform(0.5, 2) * (self.size / 3)
        self.drift_speed = random.uniform(0.5, 1.5)
        self.drift_offset = random.uniform(0, math.pi * 2)
        self.alpha = random.randint(150, 255)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        
    def update(self, dt, time_elapsed):
        self.y += self.speed * dt * 60
        self.x += math.sin(time_elapsed * self.drift_speed + self.drift_offset) * 0.5
        self.rotation += self.rot_speed
        
        if self.y > HEIGHT + 20:
            self.reset()
            
    def draw(self, surface):
        # Draw a beautiful 6-pointed snowflake
        center = (int(self.x), int(self.y))
        for i in range(6):
            angle = math.radians(self.rotation + i * 60)
            end_x = center[0] + math.cos(angle) * self.size
            end_y = center[1] + math.sin(angle) * self.size
            
            # Main branch
            color = (*COLORS['snow'][:3], self.alpha)
            surf = pygame.Surface((int(self.size * 3), int(self.size * 3)), pygame.SRCALPHA)
            pygame.draw.line(surf, color, (self.size * 1.5, self.size * 1.5), 
                           (self.size * 1.5 + math.cos(angle) * self.size, 
                            self.size * 1.5 + math.sin(angle) * self.size), 
                           max(1, int(self.size / 3)))
        
        # Simple circle for performance
        glow_surf = pygame.Surface((int(self.size * 4), int(self.size * 4)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*COLORS['white'], self.alpha // 2), 
                          (int(self.size * 2), int(self.size * 2)), int(self.size * 1.5))
        pygame.draw.circle(glow_surf, (*COLORS['white'], self.alpha), 
                          (int(self.size * 2), int(self.size * 2)), int(self.size))
        surface.blit(glow_surf, (int(self.x - self.size * 2), int(self.y - self.size * 2)))


class Star:
    """Twinkling background star"""
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT * 0.6)
        self.base_size = random.uniform(1, 3)
        self.twinkle_speed = random.uniform(1, 4)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        self.color = random.choice([
            (255, 255, 255),
            (255, 255, 220),
            (220, 220, 255),
            (255, 240, 200),
        ])
        
    def update(self, time_elapsed):
        self.current_size = self.base_size * (0.5 + 0.5 * math.sin(time_elapsed * self.twinkle_speed + self.twinkle_offset))
        self.current_alpha = int(100 + 155 * (0.5 + 0.5 * math.sin(time_elapsed * self.twinkle_speed + self.twinkle_offset)))
        
    def draw(self, surface):
        if self.current_size > 0.5:
            # Draw star with glow
            glow_size = int(self.current_size * 4)
            if glow_size > 0:
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*self.color, self.current_alpha // 3), 
                                 (glow_size, glow_size), glow_size)
                pygame.draw.circle(glow_surf, (*self.color, self.current_alpha), 
                                 (glow_size, glow_size), max(1, int(self.current_size)))
                surface.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))


class Ornament:
    """Glowing tree ornament with reflection"""
    def __init__(self, x, y, color, size=12):
        self.x = x
        self.y = y
        self.base_color = color
        self.size = size
        self.glow_offset = random.uniform(0, math.pi * 2)
        self.glow_speed = random.uniform(0.5, 2)
        
    def update(self, time_elapsed):
        self.glow_intensity = 0.7 + 0.3 * math.sin(time_elapsed * self.glow_speed + self.glow_offset)
        
    def draw(self, surface):
        # Outer glow
        glow_radius = int(self.size * 2 * self.glow_intensity)
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Multiple glow layers
        for i in range(3):
            alpha = int(50 * (1 - i/3) * self.glow_intensity)
            radius = int(glow_radius * (1 - i * 0.2))
            pygame.draw.circle(glow_surf, (*self.base_color, alpha), (glow_radius, glow_radius), radius)
        
        # Main ornament
        pygame.draw.circle(glow_surf, self.base_color, (glow_radius, glow_radius), self.size)
        
        # Highlight reflection
        highlight_pos = (glow_radius - self.size // 3, glow_radius - self.size // 3)
        pygame.draw.circle(glow_surf, (255, 255, 255, 150), highlight_pos, self.size // 4)
        
        surface.blit(glow_surf, (int(self.x - glow_radius), int(self.y - glow_radius)))


class FireworkParticle:
    """Individual firework particle"""
    def __init__(self, x, y, angle, speed, color, is_trail=False):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.025) if not is_trail else 0.05
        self.size = random.uniform(2, 4) if not is_trail else random.uniform(1, 2)
        self.is_trail = is_trail
        self.gravity = 0.08
        self.trail_points = []
        
    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += self.gravity * dt * 60
        self.vx *= 0.99
        self.life -= self.decay * dt * 60
        
        if not self.is_trail and len(self.trail_points) < 8:
            self.trail_points.append((self.x, self.y, self.life))
        
        return self.life > 0
        
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * self.life)
            size = max(1, int(self.size * self.life))
            
            # Draw trail
            for i, (tx, ty, tlife) in enumerate(self.trail_points):
                trail_alpha = int(alpha * (i / len(self.trail_points)) * 0.5)
                trail_size = max(1, int(size * (i / len(self.trail_points))))
                trail_surf = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (*self.color, trail_alpha), (trail_size, trail_size), trail_size)
                surface.blit(trail_surf, (int(tx - trail_size), int(ty - trail_size)))
            
            # Draw main particle with glow
            glow_size = size * 3
            glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, alpha // 4), (int(glow_size), int(glow_size)), int(glow_size))
            pygame.draw.circle(glow_surf, (*self.color, alpha), (int(glow_size), int(glow_size)), size)
            surface.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))


class Firework:
    """Complete firework with launch and explosion"""
    def __init__(self, x=None):
        self.x = x if x else random.uniform(WIDTH * 0.1, WIDTH * 0.9)
        self.y = HEIGHT + 10
        self.target_y = random.uniform(HEIGHT * 0.15, HEIGHT * 0.45)
        self.speed = random.uniform(8, 12)
        self.exploded = False
        self.particles: List[FireworkParticle] = []
        self.color = random.choice([
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 150, 255),  # Blue
            (255, 255, 100),  # Yellow
            (255, 150, 255),  # Pink
            (255, 200, 100),  # Orange
            (200, 100, 255),  # Purple
            (100, 255, 255),  # Cyan
            (255, 215, 0),    # Gold
        ])
        self.secondary_color = random.choice([
            (255, 255, 255),
            self.color,
            (255, 200, 100),
        ])
        self.pattern = random.choice(['burst', 'ring', 'double', 'willow', 'star'])
        
    def update(self, dt):
        if not self.exploded:
            self.y -= self.speed * dt * 60
            if self.y <= self.target_y:
                self.explode()
        else:
            self.particles = [p for p in self.particles if p.update(dt)]
            
        return not self.exploded or len(self.particles) > 0
        
    def explode(self):
        self.exploded = True
        
        if self.pattern == 'burst':
            # Classic burst pattern
            num_particles = random.randint(80, 120)
            for i in range(num_particles):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(3, 8)
                self.particles.append(FireworkParticle(self.x, self.y, angle, speed, self.color))
                
        elif self.pattern == 'ring':
            # Ring pattern
            num_particles = 36
            for i in range(num_particles):
                angle = (i / num_particles) * math.pi * 2
                speed = random.uniform(5, 6)
                self.particles.append(FireworkParticle(self.x, self.y, angle, speed, self.color))
            # Inner burst
            for i in range(30):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 4)
                self.particles.append(FireworkParticle(self.x, self.y, angle, speed, self.secondary_color))
                
        elif self.pattern == 'double':
            # Double explosion
            for ring in range(2):
                num_particles = 40
                for i in range(num_particles):
                    angle = (i / num_particles) * math.pi * 2
                    speed = 4 + ring * 3
                    color = self.color if ring == 0 else self.secondary_color
                    self.particles.append(FireworkParticle(self.x, self.y, angle, speed, color))
                    
        elif self.pattern == 'willow':
            # Willow/waterfall effect
            num_particles = 100
            for i in range(num_particles):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 6)
                p = FireworkParticle(self.x, self.y, angle, speed, self.color)
                p.gravity = 0.15  # Heavier gravity for willow effect
                p.decay = 0.008
                self.particles.append(p)
                
        elif self.pattern == 'star':
            # Star pattern
            points = 5
            for i in range(points):
                main_angle = (i / points) * math.pi * 2 - math.pi / 2
                for j in range(15):
                    angle = main_angle + random.uniform(-0.2, 0.2)
                    speed = random.uniform(4, 8)
                    self.particles.append(FireworkParticle(self.x, self.y, angle, speed, self.color))
            # Center burst
            for i in range(20):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(1, 3)
                self.particles.append(FireworkParticle(self.x, self.y, angle, speed, self.secondary_color))
                
    def draw(self, surface):
        if not self.exploded:
            # Draw rising rocket with trail
            trail_length = 30
            for i in range(trail_length):
                y = self.y + i * 2
                alpha = int(255 * (1 - i / trail_length))
                size = max(1, int(3 * (1 - i / trail_length)))
                trail_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (*self.color, alpha), (size * 2, size * 2), size)
                surface.blit(trail_surf, (int(self.x - size * 2), int(y - size * 2)))
            
            # Rocket head
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)
        else:
            for particle in self.particles:
                particle.draw(surface)


class ChristmasTree:
    """Beautiful layered Christmas tree"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ornaments: List[Ornament] = []
        self.generate_ornaments()
        
    def generate_ornaments(self):
        # Define tree shape for ornament placement
        tree_layers = [
            (self.y + 50, 180),   # Bottom layer
            (self.y - 20, 140),   # Second layer  
            (self.y - 80, 100),   # Third layer
            (self.y - 130, 60),   # Top layer
        ]
        
        ornament_colors = [
            COLORS['ornament_red'],
            COLORS['ornament_gold'],
            COLORS['ornament_blue'],
            COLORS['ornament_silver'],
            COLORS['ornament_purple'],
        ]
        
        for layer_y, width in tree_layers:
            num_ornaments = width // 25
            for i in range(num_ornaments):
                ox = self.x + random.uniform(-width/2 + 15, width/2 - 15)
                oy = layer_y + random.uniform(-25, 25)
                color = random.choice(ornament_colors)
                size = random.randint(8, 14)
                self.ornaments.append(Ornament(ox, oy, color, size))
                
    def update(self, time_elapsed):
        for ornament in self.ornaments:
            ornament.update(time_elapsed)
            
    def draw(self, surface):
        # Draw trunk with wood texture effect
        trunk_rect = pygame.Rect(self.x - 30, self.y + 80, 60, 100)
        pygame.draw.rect(surface, COLORS['trunk'], trunk_rect)
        pygame.draw.rect(surface, COLORS['trunk_dark'], trunk_rect, 3)
        
        # Wood grain lines
        for i in range(5):
            line_y = self.y + 90 + i * 18
            pygame.draw.line(surface, COLORS['trunk_dark'], 
                           (self.x - 25, line_y), (self.x + 25, line_y), 1)
        
        # Tree layers (triangles with gradient effect)
        layers = [
            (self.y + 80, 200, COLORS['tree_dark']),
            (self.y + 10, 160, COLORS['tree_mid']),
            (self.y - 50, 120, COLORS['tree_mid']),
            (self.y - 100, 80, COLORS['tree_light']),
        ]
        
        for base_y, width, color in layers:
            # Main triangle
            points = [
                (self.x, base_y - 100),
                (self.x - width, base_y),
                (self.x + width, base_y),
            ]
            pygame.draw.polygon(surface, color, points)
            
            # Subtle edge highlight
            lighter = tuple(min(255, c + 20) for c in color)
            pygame.draw.line(surface, lighter, points[0], points[1], 2)
            
        # Draw ornaments
        for ornament in self.ornaments:
            ornament.draw(surface)
            
        # Draw star on top
        self.draw_star(surface, self.x, self.y - 195, 35)
        
    def draw_star(self, surface, x, y, size):
        """Draw a glowing star on top of tree"""
        # Outer glow
        for i in range(5):
            glow_size = size * (2 - i * 0.3)
            alpha = int(50 - i * 10)
            glow_surf = pygame.Surface((int(glow_size * 4), int(glow_size * 4)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*COLORS['star_glow'], alpha), 
                             (int(glow_size * 2), int(glow_size * 2)), int(glow_size))
            surface.blit(glow_surf, (int(x - glow_size * 2), int(y - glow_size * 2)))
        
        # Star shape
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = size if i % 2 == 0 else size * 0.4
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
        
        pygame.draw.polygon(surface, COLORS['gold'], points)
        pygame.draw.polygon(surface, COLORS['star_glow'], points, 2)


def draw_gradient_background(surface, time_elapsed):
    """Draw beautiful gradient night sky with aurora effect"""
    for y in range(HEIGHT):
        # Base gradient
        ratio = y / HEIGHT
        r = int(COLORS['night_sky_top'][0] * (1 - ratio) + COLORS['night_sky_bottom'][0] * ratio)
        g = int(COLORS['night_sky_top'][1] * (1 - ratio) + COLORS['night_sky_bottom'][1] * ratio)
        b = int(COLORS['night_sky_top'][2] * (1 - ratio) + COLORS['night_sky_bottom'][2] * ratio)
        
        # Subtle aurora effect in upper portion
        if y < HEIGHT * 0.4:
            aurora_intensity = (1 - y / (HEIGHT * 0.4)) * 0.2
            aurora_wave = math.sin(time_elapsed * 0.3 + y * 0.01) * aurora_intensity
            g = min(255, int(g + aurora_wave * 30))
            b = min(255, int(b + aurora_wave * 20))
        
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_ground(surface):
    """Draw snowy ground with subtle hills"""
    # Snow hills
    points = [(0, HEIGHT)]
    for x in range(0, WIDTH + 50, 50):
        y = HEIGHT - 50 - math.sin(x * 0.02) * 20 - random.uniform(0, 5)
        points.append((x, y))
    points.append((WIDTH, HEIGHT))
    
    # Main snow
    pygame.draw.polygon(surface, COLORS['snow_ground'], points)
    
    # Snow sparkles
    for _ in range(20):
        sx = random.randint(0, WIDTH)
        sy = random.randint(HEIGHT - 60, HEIGHT - 10)
        pygame.draw.circle(surface, (255, 255, 255), (sx, sy), random.randint(1, 2))


def draw_text_with_glow(surface, text, font, x, y, main_color, glow_color, glow_radius=3):
    """Draw text with beautiful glow effect"""
    # Glow layers
    for offset in range(glow_radius, 0, -1):
        alpha = int(100 * (1 - offset / glow_radius))
        glow_surf = font.render(text, True, (*glow_color, alpha) if len(glow_color) == 3 else glow_color)
        for dx in range(-offset, offset + 1):
            for dy in range(-offset, offset + 1):
                if dx * dx + dy * dy <= offset * offset:
                    temp_surf = glow_surf.copy()
                    temp_surf.set_alpha(alpha)
                    surface.blit(temp_surf, (x + dx, y + dy))
    
    # Main text
    text_surf = font.render(text, True, main_color)
    surface.blit(text_surf, (x, y))


def main():
    """Main animation loop"""
    # Initialize elements
    snowflakes = [Snowflake() for _ in range(150)]
    stars = [Star() for _ in range(100)]
    tree = ChristmasTree(WIDTH // 2, HEIGHT // 2 + 50)
    fireworks: List[Firework] = []
    
    # Load fonts
    try:
        title_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 48)
        credit_font = pygame.font.Font(None, 28)
    except:
        title_font = pygame.font.SysFont('arial', 72, bold=True)
        subtitle_font = pygame.font.SysFont('arial', 48)
        credit_font = pygame.font.SysFont('arial', 28)
    
    # Animation timing
    start_time = pygame.time.get_ticks()
    christmas_duration = 15000  # 15 seconds of Christmas scene
    transition_duration = 3000  # 3 second transition
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        time_elapsed = elapsed / 1000.0  # Time in seconds
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Manual firework on space
                    fireworks.append(Firework())
        
        # Calculate phase (Christmas -> Transition -> New Year)
        if elapsed < christmas_duration:
            phase = 'christmas'
            firework_chance = 0.005
        elif elapsed < christmas_duration + transition_duration:
            phase = 'transition'
            progress = (elapsed - christmas_duration) / transition_duration
            firework_chance = 0.01 + progress * 0.04
        else:
            phase = 'newyear'
            firework_chance = 0.05
        
        # Draw background
        draw_gradient_background(screen, time_elapsed)
        
        # Update and draw stars
        for star in stars:
            star.update(time_elapsed)
            star.draw(screen)
        
        # Draw ground
        draw_ground(screen)
        
        # Update and draw tree
        tree.update(time_elapsed)
        tree.draw(screen)
        
        # Update and draw snowflakes
        for flake in snowflakes:
            flake.update(dt, time_elapsed)
            flake.draw(screen)
        
        # Fireworks logic
        if random.random() < firework_chance:
            fireworks.append(Firework())
        
        # Update and draw fireworks
        fireworks = [fw for fw in fireworks if fw.update(dt)]
        for fw in fireworks:
            fw.draw(screen)
        
        # Draw greeting text
        if phase == 'christmas':
            text1 = "✨ Merry Christmas! ✨"
            text1_surf = title_font.render(text1, True, COLORS['white'])
            text1_rect = text1_surf.get_rect(center=(WIDTH // 2, 60))
            draw_text_with_glow(screen, text1, title_font, text1_rect.x, text1_rect.y,
                              COLORS['white'], COLORS['gold'], 4)
        elif phase == 'transition':
            # Fade between messages
            progress = (elapsed - christmas_duration) / transition_duration
            if progress < 0.5:
                text = "✨ Merry Christmas! ✨"
                alpha = int(255 * (1 - progress * 2))
            else:
                text = "🎆 Happy New Year! 🎆"
                alpha = int(255 * ((progress - 0.5) * 2))
            
            text_surf = title_font.render(text, True, COLORS['white'])
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, 60))
            screen.blit(text_surf, text_rect)
        else:
            text1 = "🎆 Happy New Year! 🎆"
            text1_surf = title_font.render(text1, True, COLORS['white'])
            text1_rect = text1_surf.get_rect(center=(WIDTH // 2, 60))
            draw_text_with_glow(screen, text1, title_font, text1_rect.x, text1_rect.y,
                              COLORS['white'], COLORS['gold'], 4)
            
            # Year display with pulsing effect
            pulse = 1 + 0.1 * math.sin(time_elapsed * 3)
            year_text = "2 0 2 6"
            year_surf = title_font.render(year_text, True, COLORS['gold'])
            year_rect = year_surf.get_rect(center=(WIDTH // 2, 120))
            screen.blit(year_surf, year_rect)
        
        # Credits
        credit_text = "Created by Prof. Shahab Anbarjafari | 3S Holding OU, Tartu, Estonia"
        credit_surf = credit_font.render(credit_text, True, (200, 200, 220))
        screen.blit(credit_surf, (WIDTH // 2 - credit_surf.get_width() // 2, HEIGHT - 35))
        
        # Instructions
        if elapsed < 5000:
            inst_text = "Press SPACE for fireworks | ESC to exit"
            inst_surf = credit_font.render(inst_text, True, (150, 150, 170))
            inst_surf.set_alpha(int(255 * (1 - elapsed / 5000)))
            screen.blit(inst_surf, (WIDTH // 2 - inst_surf.get_width() // 2, HEIGHT - 60))
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
