import pygame
import sys
import os

from entityConstants import * 
from colorConstants import * 
from animation import *
#from fighter import *
from riku import *
from meleeEnemy import *
from rangedEnemy import *
from spritesheet import *
from playerController import *
from spriteLoader import*
from entityRenderer import *
from fire import Fire  # Import the Fire class

SCRW = 1760
SCRH = 990
MAXHP = 100
MAXSP = 100
INITIALHP = MAXHP 
INITIALSP = MAXSP

# Y boundaries of the fight 'arena'
UPPERYBOUND = (SCRH/4)*3+20 
LOWERYBOUND = SCRH - 10 #(SCRH/5)

#f = Fighter((SCRW/2)-(CAPTAIN_WALKANIM_DIMS[0]/2), SCRH-CAPTAIN_WALKANIM_DIMS[1], INITIALHP, INITIALSP, MAXHP, MAXSP)

player = Riku((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1]))
player.renderbox = AABB((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1])
player.walkSpeed = 2
player.runSpeed = 4


'''
player = Riku((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
player.renderbox = AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
player.walkSpeed = 2
player.runSpeed = 4
player.lastDirection=Direction.EAST
'''

'''
player = RangedEnemy((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2), LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*2, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
player.renderbox = AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*2, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])
player.walkSpeed = 2
player.runSpeed = 4
player.lastDirection=Direction.EAST
'''

# Tier 1
tstEnemy1 = MeleeEnemy((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2), LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
tstEnemy1.setHitbox(AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2), LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
tstEnemy1.renderbox = AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2), LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
tstEnemy1.walkSpeed = 2
tstEnemy1.runSpeed = 4
tstEnemy1.lastDirection=Direction.EAST

# Tier 2
tstEnemy2 = MeleeEnemy((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
tstEnemy2.setHitbox(AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
tstEnemy2.renderbox = AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
tstEnemy2.walkSpeed = 2
tstEnemy2.runSpeed = 4
tstEnemy2.lastDirection=Direction.EAST

# Tier 3
tstEnemy3 = MeleeEnemy((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*4, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
tstEnemy3.setHitbox(AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*4, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
tstEnemy3.renderbox = AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*4, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
tstEnemy3.walkSpeed = 2
tstEnemy3.runSpeed = 4
tstEnemy3.lastDirection=Direction.EAST

# Tier 4
tstEnemy4 = MeleeEnemy((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*6, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
tstEnemy4.setHitbox(AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*6, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
tstEnemy4.renderbox = AABB((SCRW/2)+(SAMURAI_ANIM_DIMS[1][0]/2)*6, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
tstEnemy4.walkSpeed = 2
tstEnemy4.runSpeed = 4
tstEnemy4.lastDirection=Direction.EAST

enemies = [tstEnemy1, tstEnemy2, tstEnemy3, tstEnemy4]

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCRW, SCRH))
pygame.display.set_caption("Fighter testing")

# Create fire effects on both sides of the map
fire_width = 100
fire_height = 50
left_fire = Fire(0, LOWERYBOUND - fire_height, fire_width, fire_height, damage=1, damage_interval=500)
right_fire = Fire(SCRW - fire_width, LOWERYBOUND - fire_height, fire_width, fire_height, damage=1, damage_interval=500)

# Creation of animation objects: These are just 
# logical representations of each animation, without
# any image data inside them. Their current index is then
# used to access the 'animationsData' array below

rikuAnimations = [
    Animation(1000/5, 5), # idleLeftAnimation
    Animation(1000/5, 5), # idleRightAnimation

    Animation(1000/9, 9), # walkLeftAnimation
    Animation(1000/9, 9), # walkRightAnimation

    Animation(1000/8, 8), # runLeftAnimation
    Animation(1000/8, 8), # runRightAnimation

    Animation(100/2, 2), # blockLeftAnimation
    Animation(100/2, 2), # blockRightAnimation 

    Animation(100/2, 2), # hurtLeftAnimation
    Animation(100/2, 2), # hurtRightAnimation

    Animation(800/6, 6), # deadLeftAnimation
    Animation(800/6, 6), # deadRightAnimation

    Animation(400/4, 4), # attack1LeftAnimation
    Animation(400/4, 4), # attack1RightAnimation 

    Animation(400/5, 5), # attack2LeftAnimation
    Animation(400/5, 5), # attack2RightAnimation

    Animation(400/4, 4), # attack3LeftAnimation
    Animation(400/4, 4)  # attack3RightAnimation
]

archerAnimations = [
    Animation(1000/5, 9), # idleLeftAnimation
    Animation(1000/5, 9), # idleRightAnimation

    Animation(1000/9, 8), # walkLeftAnimation
    Animation(1000/9, 8), # walkRightAnimation

    Animation(1000/8, 8), # runLeftAnimation
    Animation(1000/8, 8), # runRightAnimation

    Animation(0, 0), # blockLeftAnimation
    Animation(0, 0), # blockRightAnimation 

    Animation(100/2, 3), # hurtLeftAnimation
    Animation(100/2, 3), # hurtRightAnimation

    Animation(800/6, 5), # deadLeftAnimation
    Animation(800/6, 5), # deadRightAnimation

    Animation(400/4, 5), # attack1LeftAnimation
    Animation(400/4, 5), # attack1RightAnimation 

    Animation(400/5, 5), # attack2LeftAnimation
    Animation(400/5, 5), # attack2RightAnimation

    Animation(400/4, 5), # attack3LeftAnimation
    Animation(400/4, 5),  # attack3RightAnimation

    Animation(1000/11, 11), # Shot charge left animation
    Animation(2000/11, 11), # Shot charge right animation

    Animation(500/3, 3), # Shot left animation
    Animation(500/3, 3), # Shot right animation

    Animation(1000, 1), # Arrow (not an animation)
    Animation(1000, 1), # Arrow (not an animation)
]

# Load the background picture
background = loadBackground()

# This is the actual image data, which is later accessed
# in the rendering phase, within the main loop

rikuAnimationsData = loadRikuSprites();

meleeTier1AnimationsData = loadMeleeSprites(1)
meleeTier2AnimationsData = loadMeleeSprites(2)
meleeTier3AnimationsData = loadMeleeSprites(3)
meleeTier4AnimationsData = loadMeleeSprites(4)

rangedTier1AnimationsData = loadRangedTier1Sprites()

# Attach animations in order !!

for a in rikuAnimations:
    player.addAnimation(a)

# Only for testing !!
#for a in archerAnimations:
#    player.addAnimation(a)

for e in enemies:
    for a in rikuAnimations:
        e.addAnimation(a)

# Create the keyboard map

MAXKEYS = 200

prevKeyboardMap = []
for i in range (0, MAXKEYS):
    prevKeyboardMap.append(False)

keyboardMap = []
for i in range (0, MAXKEYS):
    keyboardMap.append(False)

#print(keyboardArr)

def setKeyDown(keyID):
    keyboardMap[keyID] = True

def setKeyUp(keyID):
    keyboardMap[keyID] = False

holdingSpace = False

running = True
clock = pygame.time.Clock()

# Set to True to show hitboxes/boundaries
collisionsShown = False

while running:
    current_time = pygame.time.get_ticks()  # Get current time for fire damage

    ######## INPUT ########

    keyboardChanged = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type==pygame.KEYDOWN:
            keyboardChanged = True
   
            if (event.key < MAXKEYS): setKeyDown(event.key) 
            #print(f'k\'{event.key}\' down')

        if event.type==pygame.KEYUP:
            keyboardChanged = True

            # Save to prevKeyboardMap
            #for i in keyboardMap: prevKeyboardMap[i]=keyboardMap[i]

            if (event.key < MAXKEYS): setKeyUp(event.key) 
            #print(f'k\'{event.key}\' up')
    
    # Save to prevKeyboardMap
    if keyboardChanged:
        for i in keyboardMap: prevKeyboardMap[i]=keyboardMap[i]

    # (Later include all the input logic in its own function ?)

    ######## UPDATE ########

    if(keyboardMap[pygame.K_c] 
    and (prevKeyboardMap[pygame.K_c] != keyboardMap[pygame.K_c])):
        collisionsShown = not collisionsShown;

    # Update fire effects
    all_entities = [player] + enemies
    left_fire.update(current_time, all_entities)
    right_fire.update(current_time, all_entities)

    # Update entity controllers
    updatePlayerControl(player, keyboardMap, enemies, 0, SCRW)

    # Update entity behaviour 
    player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)

    # Update enemy behaviour
    for e in enemies:
        e.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)

    ######## RENDER ########

    # (Later include all the render logic in its own function)

    # Clear screen
    screen.fill(BLACK)

    # Render background
    bgScale = (SCRW, SCRH)
    scaledBg = pygame.transform.scale(background, bgScale)
    screen.blit(scaledBg, (0,0))

    # Draw the y boundaries
    if collisionsShown:
        pygame.draw.line(screen, WHITE, (0, UPPERYBOUND), (SCRW, UPPERYBOUND))
        pygame.draw.line(screen, WHITE, (0, LOWERYBOUND), (SCRW, LOWERYBOUND))

    # Render fire effects
    left_fire.render(screen)
    right_fire.render(screen)

    # Render the player
    renderRiku(screen, player, rikuAnimationsData, collisionsShown, CAPTAIN_RENDER_CORRECTIONS)
    #renderMeleeEnemy(screen, player, meleeTier1AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    #renderRangedEnemy(screen, player, rangedTier1AnimationsData, collisionsShown, ARCHER_RENDER_CORRECTIONS)

    # Render test enemies
    
    renderMeleeEnemy(screen, tstEnemy1, meleeTier1AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    renderMeleeEnemy(screen, tstEnemy2, meleeTier2AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    renderMeleeEnemy(screen, tstEnemy3, meleeTier3AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    renderMeleeEnemy(screen, tstEnemy4, meleeTier4AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)

    #for e in enemies:
    #    renderMeleeEnemy(screen, e, 
    #               meleeTier2AnimationsData, 
    #               collisionsShown,
    #               SAMURAI_RENDER_CORRECTIONS)

    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
