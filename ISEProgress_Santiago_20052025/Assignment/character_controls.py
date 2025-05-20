import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Character Controls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Get the absolute path to the sprite folder
SPRITE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Samurai')
print(f"Sprite folder path: {SPRITE_FOLDER}")

# Stamina properties
MAX_STAMINA = 100
stamina = MAX_STAMINA
stamina_recovery_rate = 0.5  # Stamina points per frame
stamina_drain_rates = {
    'running': 0.8,
    'blocking': 0.5,
    'double_jump': 20,
    'attack1': 0,  # No stamina cost for attack1
    'attack2': int(MAX_STAMINA * 0.15),  # 15% of max stamina
    'attack3': int(MAX_STAMINA * 0.35)   # 35% of max stamina
}
exhausted_speed_multiplier = 0.5  # Speed multiplier when stamina is depleted

# Sprite loading function
def load_sprite_sheet(filename, frame_count):
    try:
        full_path = os.path.join(SPRITE_FOLDER, filename)
        print(f"Attempting to load sprite: {full_path}")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Sprite file not found: {full_path}")
            
        sprite_sheet = pygame.image.load(full_path).convert_alpha()
        print(f"Successfully loaded {filename}")
        print(f"Sprite sheet dimensions: {sprite_sheet.get_width()}x{sprite_sheet.get_height()}")
        
        frame_width = (sprite_sheet.get_width() / frame_count)
        frame_height = sprite_sheet.get_height()
        frames = []
        
        for i in range(frame_count):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            print(f"New frame surface = {frame.get_width()}x{frame.get_height()}")
            frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
            
        print(f"Created {len(frames)} frames for {filename}")
        return frames
    except Exception as e:
        print(f"Error loading sprite {filename}: {e}")
        print(f"Current working directory: {os.getcwd()}")
        # Return a default frame if loading fails
        default_frame = pygame.Surface((50, 50), pygame.SRCALPHA)
        default_frame.fill((255, 0, 255))  # Magenta color to indicate error
        return [default_frame]

# Load all sprite animations
print("\nLoading sprite animations...")
SPRITES = {
    'idle': load_sprite_sheet('Idle.png', 6),
    'walk': load_sprite_sheet('Walk.png', 1),
    'run': load_sprite_sheet('Run.png', 1), #14),
    'jump': load_sprite_sheet('Jump.png', 1), # 11),
    'attack1': load_sprite_sheet('Attack_1.png', 1),
    'attack2': load_sprite_sheet('Attack_2.png', 1),
    'attack3': load_sprite_sheet('Attack_3.png', 1),
    'block': load_sprite_sheet('Protection.png', 1),
    #'hurt': load_sprite_sheet('Hurt.png', 3), #9),
    #'dead': load_sprite_sheet('Dead.png', 6), #14),
}
print("Finished loading sprite animations\n")

# Character properties
character_x = WINDOW_WIDTH // 2
character_y = WINDOW_HEIGHT // 2
character_speed = 3  # Reduced from 5 to 3 for slower walking
initial_jump_speed = 3
run_speed = 8
gravity = 0.1
vertical_velocity = 0
ground_y = WINDOW_HEIGHT - 50  # Ground level
is_jumping = False
available_jumps = 2
is_exhausted = False

# Animation properties
current_state = 'idle'
current_frame = 0
animation_speed = 0.2
animation_timer = 0
facing_right = True  # Track direction
is_attacking = False
is_blocking = False
attack_frame = 0
block_frame = 0

# Mapping from state keys to user-friendly action names
ACTION_NAMES = {
    'idle': 'Idle',
    'walk': 'Walk',
    'run': 'Run',
    'jump': 'Jump',
    'attack1': 'Attack 1',
    'attack2': 'Attack 2',
    'attack3': 'Attack 3',
    'block': 'Block',
    'hurt': 'Hurt',
    'dead': 'Dead',
}

# Add these variables after the other character properties
attack3_hold_time = 0
attack3_hold_threshold = 0.75  # Three quarters of a second to hold for attack3

# Add after the other character properties
attack_damages = {
    'attack1': 15,
    'attack2': 25,
    'attack3': 50
}

# Add damage display system
class DamageNumber:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.lifetime = 1.0  # seconds
        self.velocity = -2  # pixels per frame
        self.alpha = 255  # for fade out

damage_numbers = []

# Add after the other character properties
show_hitbox = False

# Add after other character properties
last_attack_time = 0
attack_cooldown = 0.35  # 0.35 seconds cooldown between attacks

# Add after other character properties
last_stamina_use_time = 0
stamina_regen_delay = 1.5  # 1.5 seconds delay before stamina regen starts

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
            
            # Check if enough time has passed since last attack
            can_attack = current_time - last_attack_time >= attack_cooldown
            
            # Toggle hitbox with Esc key
            if event.key == pygame.K_ESCAPE:
                show_hitbox = not show_hitbox
                print(f"Hitbox visibility toggled: {show_hitbox}")
            
            # BLOCKING LOGIC
            if event.key == pygame.K_b and not is_attacking and stamina > 0:
                is_blocking = True
                current_state = 'block'
                block_frame = 0
            
            # ATTACK 1 LOGIC
            elif event.key == pygame.K_j and not is_attacking and not is_blocking and can_attack:
                is_attacking = True
                current_state = 'attack1'
                attack_frame = 0
                last_attack_time = current_time
                # Add damage number for attack1
                damage_numbers.append(DamageNumber(character_x + 50, character_y, attack_damages['attack1']))
            
            # ATTACK 2 LOGIC
            elif event.key == pygame.K_k and not is_attacking and not is_blocking and stamina >= stamina_drain_rates['attack2'] and can_attack:
                is_attacking = True
                current_state = 'attack2'
                attack_frame = 0
                stamina -= stamina_drain_rates['attack2']
                last_attack_time = current_time
                last_stamina_use_time = current_time
                # Add damage number for attack2
                damage_numbers.append(DamageNumber(character_x + 50, character_y, attack_damages['attack2']))
            
            # ATTACK 3 LOGIC
            elif event.key == pygame.K_l and not is_attacking and not is_blocking:
                attack3_hold_time = 0  # Start counting hold time

            # JUMP LOGIC
            elif event.key == pygame.K_SPACE and not is_attacking and not is_blocking:
                if available_jumps > 0:
                    vertical_velocity = -initial_jump_speed
                    is_jumping = True
                    available_jumps -= 1
                    current_state = 'jump'
                    # Drain stamina only on double jump
                    if available_jumps == 0 and stamina >= stamina_drain_rates['double_jump']:
                        stamina -= stamina_drain_rates['double_jump']
                        last_stamina_use_time = current_time
        
        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_b:
                is_blocking = False
                current_state = 'idle'
            
            # ATTACK 3 LOGIC
            elif event.key == pygame.K_l:
                if attack3_hold_time >= attack3_hold_threshold and stamina >= stamina_drain_rates['attack3'] and can_attack:
                    is_attacking = True
                    current_state = 'attack3'
                    attack_frame = 0
                    stamina -= stamina_drain_rates['attack3']
                    last_attack_time = current_time
                    last_stamina_use_time = current_time
                    # Add damage number for attack3
                    damage_numbers.append(DamageNumber(character_x + 50, character_y, attack_damages['attack3']))
                attack3_hold_time = 0

    # Get keyboard state
    keys = pygame.key.get_pressed()
    
    # Update stamina
    if stamina < MAX_STAMINA:
        # Only regenerate if enough time has passed since last stamina use
        if current_time - last_stamina_use_time >= stamina_regen_delay:
            stamina = min(MAX_STAMINA, stamina + stamina_recovery_rate)
    
    # Check if exhausted
    is_exhausted = stamina <= 0
    
    if not is_attacking and not is_blocking:  # Only allow movement when not attacking or blocking
        # Movement controls
        if keys[pygame.K_a]:
            facing_right = False
            if keys[pygame.K_LSHIFT] and not is_exhausted and stamina > 0:
                character_x -= run_speed
                current_state = 'run'
                stamina -= stamina_drain_rates['running']
            else:
                speed_multiplier = exhausted_speed_multiplier if is_exhausted else 1
                character_x -= character_speed * speed_multiplier
                current_state = 'walk'
        elif keys[pygame.K_d]:
            facing_right = True
            if keys[pygame.K_LSHIFT] and not is_exhausted and stamina > 0:
                character_x += run_speed
                current_state = 'run'
                stamina -= stamina_drain_rates['running']
            else:
                speed_multiplier = exhausted_speed_multiplier if is_exhausted else 1
                character_x += character_speed * speed_multiplier
                current_state = 'walk'
        elif not is_jumping:
            current_state = 'idle'
    
    # Update attack3 hold time
    if keys[pygame.K_l] and not is_attacking and not is_blocking:
        attack3_hold_time += clock.get_time() / 1000.0  # Convert to seconds
    
    try:
        if is_blocking:
            current_sprite = SPRITES[current_state][block_frame]
        elif is_attacking:
            current_sprite = SPRITES[current_state][attack_frame]
        elif is_jumping:
            current_sprite = SPRITES[current_state][0]
        else:
            current_sprite = SPRITES[current_state][current_frame]
        # Flip sprite if facing left
        if not facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        sprite_height = current_sprite.get_height()
    
    except (IndexError, KeyError) as e:
        print(f"Animation error: {e}")
        # Draw a default rectangle if sprite loading fails
        pygame.draw.rect(screen, (255, 0, 255), (character_x, character_y, 50, 50))

    vertical_velocity += gravity # Apply gravity
    character_y += vertical_velocity # Update velocity
    
    sprite_height = current_sprite.get_height() # Update height
    # Ground collision
    if (character_y+sprite_height) > ground_y:
        character_y = ground_y-sprite_height #- sprite_height #ground_y
        vertical_velocity = 0
        is_jumping = False
        available_jumps = 2
        if not is_attacking and not is_blocking:
            current_state = 'idle'
    elif is_jumping:  # Keep jump animation while in air
        current_state = 'jump'

    # Keep character within screen bounds
    character_x = max(0, min(character_x, WINDOW_WIDTH - 50))
    
    # Animation update
    animation_timer += clock.get_time() / 1000.0
    if animation_timer >= animation_speed:
        animation_timer = 0
        if is_attacking:
            if len(SPRITES[current_state]) > 1:
                attack_frame += 1
                if attack_frame >= len(SPRITES[current_state]):
                    is_attacking = False
                    attack_frame = 0
                    current_state = 'idle'
            else:
                attack_frame = 0
                is_attacking = False
                current_state = 'idle'
        elif is_blocking:
            if len(SPRITES[current_state]) > 1:
                block_frame = (block_frame + 1) % len(SPRITES[current_state])
            else:
                block_frame = 0
            if stamina > 0:
                stamina -= stamina_drain_rates['blocking']
        else:
            if len(SPRITES[current_state]) > 1:
                current_frame = (current_frame + 1) % len(SPRITES[current_state])
            else:
                current_frame = 0
    
    # Update damage numbers
    for damage_number in damage_numbers[:]:
        damage_number.lifetime -= clock.get_time() / 1000.0
        damage_number.y += damage_number.velocity
        damage_number.alpha = int((damage_number.lifetime / 1.0) * 255)
        if damage_number.lifetime <= 0:
            damage_numbers.remove(damage_number)

    # Draw damage numbers
    for damage_number in damage_numbers:
        font = pygame.font.Font(None, 36)
        text = font.render(str(damage_number.damage), True, (255, 0, 0))
        text.set_alpha(damage_number.alpha)
        screen.blit(text, (damage_number.x, damage_number.y))

    # Clear screen
    screen.fill(WHITE)
    
    # Draw ground
    pygame.draw.line(screen, BLACK, (0, ground_y), (WINDOW_WIDTH, ground_y), 2)
    
    # Draw character with error handling
    try:
        
        screen.blit(current_sprite, (character_x, character_y))#ground_y + 50 - sprite_height))

        # Draw hitbox if enabled
        if show_hitbox:
            # Calculate reduced hitbox size
            hitbox_width = int(current_sprite.get_width())# * 0.5)
            #print(hitbox_width)
            hitbox_height = int(sprite_height)# * 0.5)
            hitbox_x = character_x + (current_sprite.get_width() - hitbox_width) // 2
            hitbox_y = character_y#ground_y + 50 - hitbox_height  # Align to feet
            hitbox_rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
            pygame.draw.rect(screen, (0, 255, 0), hitbox_rect, 2)  # Green outline

        # Draw Attack 3 charge meter when holding L key
        if keys[pygame.K_l] and not is_attacking and not is_blocking:
            charge_meter_width = 50
            charge_meter_height = 5
            charge_meter_x = character_x + (current_sprite.get_width() // 2) - (charge_meter_width // 2)
            charge_meter_y = ground_y + 50 - sprite_height - 15  # Position above character
            
            # Draw meter background
            pygame.draw.rect(screen, BLACK, (charge_meter_x, charge_meter_y, charge_meter_width, charge_meter_height), 1)
            
            # Calculate fill width based on hold time
            fill_width = (attack3_hold_time / attack3_hold_threshold) * charge_meter_width
            fill_width = min(fill_width, charge_meter_width)  # Cap at max width
            
            # Draw fill
            pygame.draw.rect(screen, RED, (charge_meter_x + 1, charge_meter_y + 1, fill_width - 2, charge_meter_height - 2))

    except (IndexError, KeyError) as e:
        print(f"Animation error: {e}")
        # Draw a default rectangle if sprite loading fails
        pygame.draw.rect(screen, (255, 0, 255), (character_x, character_y, 50, 50))
    
    # Draw stamina bar
    stamina_bar_width = 200
    stamina_bar_height = 20
    stamina_bar_x = 10
    stamina_bar_y = 40
    
    # Draw stamina bar background
    pygame.draw.rect(screen, BLACK, (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height), 2)
    
    # Draw stamina bar fill
    stamina_fill_width = (stamina / MAX_STAMINA) * stamina_bar_width
    stamina_color = GREEN if stamina > 50 else YELLOW if stamina > 20 else RED
    pygame.draw.rect(screen, stamina_color, (stamina_bar_x + 2, stamina_bar_y + 2, stamina_fill_width - 4, stamina_bar_height - 4))
    
    # Draw stamina text
    font = pygame.font.Font(None, 36)
    stamina_text = font.render(f"Stamina: {int(stamina)}%", True, BLACK)
    screen.blit(stamina_text, (stamina_bar_x, stamina_bar_y - 30))

    # Draw current action text
    action_name = ACTION_NAMES.get(current_state, current_state.capitalize())
    action_text = font.render(f"Action: {action_name}", True, BLACK)
    screen.blit(action_text, (stamina_bar_x, stamina_bar_y + 30))

    # Draw jump counter with more spacing below action
    jump_text = font.render(f"Jumps: {available_jumps}", True, BLACK)
    screen.blit(jump_text, (stamina_bar_x, stamina_bar_y + 70))

    # Draw damage values in the UI
    damage_text = font.render(f"Attack 1: {attack_damages['attack1']} DMG | Attack 2: {attack_damages['attack2']} DMG | Attack 3: {attack_damages['attack3']} DMG", True, BLACK)
    screen.blit(damage_text, (stamina_bar_x, stamina_bar_y + 100))
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit() 