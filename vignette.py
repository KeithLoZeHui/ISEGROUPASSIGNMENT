import pygame
from colorConstants import *

def generatePixelartVignette(width, height, color, steps=5, radius=0.7):

    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    #vignette.set_alpha(255)
    
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    
    center_x, center_y = width // 2, height // 2
    max_dist = min(center_x, center_y) * radius
    
    # Calculate step sizes
    step_size = max_dist // steps
    
    for step in range(steps + 1):
        current_radius = step * step_size
        alpha = 255 * step // steps
        
        # Draw concentric squares
        rect = pygame.Rect(
            center_x - current_radius,
            center_y - current_radius,
            current_radius * 2,
            current_radius * 2
        )
        
        # Only draw if we have space
        if rect.width > 0 and rect.height > 0:
            pygame.draw.rect(
                overlay, 
                (*color, alpha), 
                rect, 
                width=1  # Outline only for pixel art look
            )
        
    # Fill the center (optional - remove if you want full vignette)
    if steps > 0:
        inner_rect = pygame.Rect(
            center_x - (max_dist - step_size),
            center_y - (max_dist - step_size),
            (max_dist - step_size) * 2,
            (max_dist - step_size) * 2
        )
        overlay.fill((*color, 0), inner_rect)
    
    # Blend with MULT to darken the image
    vignette.blit(overlay, (0, 0), special_flags=pygame.BLEND_ADD)
    
    return vignette