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
from meleeAIs import *
from spriteLoader import*
from entityRenderer import *

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

'''
player = Riku((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1]))
player.renderbox = AABB((SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2), LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1], CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1])
player.walkSpeed = 2
player.runSpeed = 4
'''


'''
player = Riku((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1]))
player.renderbox = AABB((SCRW/2)-(SAMURAI_ANIM_DIMS[1][0]/2)*2, LOWERYBOUND-SAMURAI_ANIM_DIMS[1][1], SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
player.walkSpeed = 2
player.runSpeed = 4
player.lastDirection=Direction.EAST
'''

player = RangedEnemy((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2), LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], INITIALHP, INITIALSP, MAXHP, MAXSP)
player.setHitbox(AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*2, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
player.renderbox = AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*2, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1], ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])
player.walkSpeed = 2
player.runSpeed = 4
player.lastDirection=Direction.EAST


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

arrowSystem = ArrowSystem()
for e in enemies:
    arrowSystem.addVulnerableEntity(e)

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCRW, SCRH))
pygame.display.set_caption("Fighter testing")

# Creation of animation objects: These are just 
# logical representations of each animation, without
# any image data inside them. Their current index is then
# used to access the 'animationsData' array below

rikuAnimations = [Animation(a[0], a[1]) for a in MELEE_ANIMATIONS_SETUP]
archerAnimations = [Animation(a[0], a[1]) for a in RANGED_ANIMATIONS_SETUP]

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

rightArrowSprite = rangedTier1AnimationsData[(2*12)-2][0]
leftArrowSprite = rangedTier1AnimationsData[(2*12)-1][0]

animationAtlas = [
    rikuAnimationsData,
    
    meleeTier1AnimationsData,
    meleeTier2AnimationsData,
    meleeTier3AnimationsData,
    meleeTier4AnimationsData,

    rangedTier1AnimationsData,
    [],
    [],
    [],

    [rightArrowSprite, leftArrowSprite]
]

# Attach animations in order !!

#for a in rikuAnimations:
#    player.addAnimation(a)

# Only for testing !!
for a in archerAnimations:
    player.addAnimation(a)

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

def handleInput():

    global running
    global keyboardMap
    global prevKeyboardMap

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

def update():

    global collisionsShown
    global arrowSystem
    global player
    global keyboardMap
    global enemies

    if(keyboardMap[pygame.K_c] 
    and (prevKeyboardMap[pygame.K_c] != keyboardMap[pygame.K_c])):
        collisionsShown = not collisionsShown;

    # (Later include all the update logic in its own function)

    # Update entity controllers
    updatePlayerControl(player, keyboardMap, enemies, 0, SCRW)

    # Update AIs
    #updateLobotomite(player, tstEnemy1)
    #updateLobotomite(player, tstEnemy2)
    #updateLobotomite(player, tstEnemy3)
    #updateLobotomite(player, tstEnemy4)

    # Update entity behaviour 
    player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW, arrowSystem)

    # Update enemy behaviour
    for e in enemies:
        e.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)

    arrowSystem.update(0, SCRW)

def render():

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

    objArr = []
    objTypeArr = []
    
    objArr.append(player)
    objTypeArr.append(RENDEROBJ_RANGEDTIER1)  #(RENDEROBJ_RIKU)
    
    objArr.append(tstEnemy1)
    objTypeArr.append(RENDEROBJ_MELEETIER1)
    objArr.append(tstEnemy2)
    objTypeArr.append(RENDEROBJ_MELEETIER2)
    objArr.append(tstEnemy3)
    objTypeArr.append(RENDEROBJ_MELEETIER3)
    objArr.append(tstEnemy4)
    objTypeArr.append(RENDEROBJ_MELEETIER4)

    for a in arrowSystem.arrows:
        objArr.append(a)
        objTypeArr.append(RENDEROBJ_ARROW)

    renderObjectsByPseudoZ(screen, objArr, objTypeArr, animationAtlas, collisionsShown)

    # Render the player
    #renderRiku(screen, player, rikuAnimationsData, collisionsShown, CAPTAIN_RENDER_CORRECTIONS)
    #renderMeleeEnemy(screen, player, meleeTier1AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    #renderRangedEnemy(screen, player, rangedTier1AnimationsData, collisionsShown) #, ARCHER_RENDER_CORRECTIONS)

    # Render test enemies
    
    #renderMeleeEnemy(screen, tstEnemy1, meleeTier1AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    #renderMeleeEnemy(screen, tstEnemy2, meleeTier2AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    #renderMeleeEnemy(screen, tstEnemy3, meleeTier3AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)
    #renderMeleeEnemy(screen, tstEnemy4, meleeTier4AnimationsData, collisionsShown, SAMURAI_RENDER_CORRECTIONS)

    #renderArrows(screen, arrowSystem, collisionsShown, leftArrowSprite, rightArrowSprite)

    #for e in enemies:
    #    renderMeleeEnemy(screen, e, 
    #               meleeTier2AnimationsData, 
    #               collisionsShown,
    #               SAMURAI_RENDER_CORRECTIONS)

    # Update display
    pygame.display.flip()

# Main entry point
if __name__ == '__main__':

    while running:

        ######## INPUT ########

        handleInput()

        ######## UPDATE ########
        
        update()

        ######## RENDER ########

        render()
 
        # Control frame rate
        clock.tick(60)

    # Exit...
    pygame.quit()
    sys.exit()
