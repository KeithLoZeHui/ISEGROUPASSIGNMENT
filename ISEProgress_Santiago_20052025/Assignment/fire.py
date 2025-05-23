import pygame
import os
from fighter import AABB

class Fire:
    def __init__(self, x, y, width, height, damage=1, damage_interval=1000):
        self.hitbox = AABB(x, y, width, height)
        self.damage = damage
        self.damage_interval = damage_interval  # Time between damage ticks in milliseconds
        self.last_damage_time = 0
        
        # Animation properties
        self.animation_frames = []
        self.current_frame = 0
        self.frame_delay = 100  # Milliseconds between frames
        self.last_frame_time = 0
        self.num_frames = 4  # Number of frames in the sprite sheet
        
        # Load fire animation from sprite sheet
        fire_path = os.path.join("resources", "Fire", "Fire+Sparks.png")
        try:
            # Load the sprite sheet
            sprite_sheet = pygame.image.load(fire_path).convert_alpha()
            
            # Calculate frame dimensions
            frame_width = sprite_sheet.get_width() // self.num_frames
            frame_height = sprite_sheet.get_height()
            
            # Extract individual frames
            for i in range(self.num_frames):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), 
                          (i * frame_width, 0, frame_width, frame_height))
                # Scale frame to match hitbox size
                frame = pygame.transform.scale(frame, (width, height))
                self.animation_frames.append(frame)
                
        except Exception as e:
            print(f"Failed to load fire animation: {e}")
            self.animation_frames = []

    def update(self, current_time, entities):
        # Update animation frame
        if self.animation_frames and current_time - self.last_frame_time >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.last_frame_time = current_time

        # Deal damage to entities in fire
        for entity in entities:
            if self.hitbox.overlaps(entity.hitbox):
                if current_time - self.last_damage_time >= self.damage_interval:
                    entity.hurt(self.damage)
                    self.last_damage_time = current_time

    def render(self, screen):
        if self.animation_frames:
            # Render the current animation frame
            screen.blit(self.animation_frames[self.current_frame], 
                       (self.hitbox.x, self.hitbox.y))
        else:
            # Fallback to a red rectangle if animation fails to load
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.hitbox.x, self.hitbox.y, 
                            self.hitbox.w, self.hitbox.h)) 