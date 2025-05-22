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
from rangedAIs import *
from spriteLoader import*
from entityRenderer import *
from slideShow import *

SCRW = 1760
SCRH = 990
MAXHP = 100
MAXSP = 100
INITIALHP = MAXHP 
INITIALSP = MAXSP

# Y boundaries of the fight 'arena'
UPPERYBOUND = (SCRH/4)*3+40 
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

'''
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
'''

shooter = RangedEnemy((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*6, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1]*(3/2), INITIALHP, INITIALSP, MAXHP, MAXSP)
shooter.setHitbox(AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*6, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1]*(3/2), ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
shooter.renderbox = AABB((SCRW/2)-(ARCHER_ANIM_DIMS[0][0]/2)*6, LOWERYBOUND-ARCHER_ANIM_DIMS[0][1]*(3/2), ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])
shooter.walkSpeed = 2
shooter.runSpeed = 4
shooter.lastDirection=Direction.EAST

enemies = [shooter, tstEnemy1] #[tstEnemy1, tstEnemy2, tstEnemy3, tstEnemy4]

blackBackground = pygame.Surface((SCRW, SCRH), flags=0, depth=32, masks=pygame.Color(BLACK))
blackBackground.set_alpha(255/2)

arrowSystem = ArrowSystem()
for e in enemies:
    arrowSystem.addVulnerableEntity(e)
arrowSystem.addVulnerableEntity(player)

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCRW, SCRH))
pygame.display.set_caption("百の剣 (Hundred Blades)")

# Creation of animation objects: These are just
# logical representations of each animation, without
# any image data inside them. Their current index is then 
# used to access the 'animationsData' array below 

rikuAnimations = [Animation(a[0], a[1]) for a in MELEE_ANIMATIONS_SETUP]
archerAnimations = [Animation(a[0], a[1]) for a in RANGED_ANIMATIONS_SETUP]

# Load the background picture
background = loadBackground()

font = pygame.font.Font(os.path.join("resources", "DoubleHomicide.ttf"), 36)
japFont = pygame.font.Font(os.path.join("resources", "ipaexg.ttf"), 24)

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

for a in rikuAnimations:
    player.addAnimation(a)

# Only for testing !!
#for a in archerAnimations:
#    player.addAnimation(a)

#for e in enemies:
#   for a in rikuAnimations:
#        e.addAnimation(a)

for a in rikuAnimations:
        tstEnemy1.addAnimation(a)

for a in archerAnimations:
    shooter.addAnimation(a)

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

# Menu substates
MENUFADEIN = 0
MENUIDLE = 1
MENUFADEOUT = 2

menuSubstate = MENUFADEIN

# "百の剣"
japText = u"百の剣"
newJapText = japText.encode("utf-8").decode("utf-8")
titleJap = japFont.render(newJapText, False, WHITE)
titleJap.set_alpha(0)

titleLatin = font.render("HUNDRED BLADES", False, WHITE)
titleLatin.set_alpha(0)

menuText1 = font.render("Press 's' to start", False, WHITE)
menuText1.set_alpha(0)

placeHolderImage = pygame.surface.Surface((400,400))
placeHolderImage.fill((BLUE))
placeHolderImage.set_alpha(255)

slides = [
    Slide(  
         placeHolderImage, 
          ["Japan, 1590 — The Final Fires of the Sengoku Era"],
          2500, 
          5000, 
          2500
    ),
    Slide(  
        placeHolderImage, 
        [
            "As the war-torn nation crawls toward unification under Toyotomi rule, two legendary clans ",
            "dominate the northern provinces: the dignified Momoyama Clan, based in their majestic ",
            "stronghold at Fushimi-Momoyama Castle, and the feared Kuronagi Clan, who rule the ",
            "mountain shadows with unmatched brutality."
        ],
        2500, 
        10000, 
        2500
    ),
    Slide(  
        placeHolderImage, 
        [
            "Amid this fragile peace stands Riku Yamada, a promising samurai of the Momoyama clan. ",
            "Raised in a time of bloodshed but trained in the arts of both war and diplomacy, ",
            "Riku believed in loyalty",
            "— until the day he was betrayed."],
        2500, 
        10000, 
        2500
    ),
    Slide(  
        placeHolderImage, 
        [
            "False letters, forged maps, and a whisper campaign frame Riku as a spy. In a ",
            "desperate bid to maintain political ties, the Momoyama clan turns him over ",
            "to the Kuronagi, offering him as a scapegoat to silence accusations and ",
            "preserve the illusion of unity."
        ],
        2500, 
        10000, 
        2500
    ),
    Slide(  
        placeHolderImage, 
        [
            "But the Kuronagi do not offer swift death. Instead, they sentence him to ",
            "the Trial of Hyaku-no-Ken — a forgotten rite once used to test those ",
            "accused of dishonor. Riku is cast into the Arena of a Hundred Blades, ",
            "a brutal amphitheater built into the sacred slopes of Mount Kurama."
        ],
        2500, 
        10000, 
        2500
    ),
    Slide(  
        placeHolderImage, 
        [
            "His punishment is simple: ",
            "defeat one hundred warriors — blades forged from both clans."
        ],
        2500, 
        10000, 
        2500
    ),
]

slideShowIntro = SlideShow(slides, font, screen)

# Application states
MAINMENU = 0
SLIDESHOW_INTRO = 1
GAME = 2
PAUSE = 3
SLIDESHOW_OUTRO = 4

interfaceState = MAINMENU 
#MAINMENU

def handleMainMenuInput():
    
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
    #if keyboardChanged:
    for i in keyboardMap: prevKeyboardMap[i]=keyboardMap[i]

alphaModulation = 0

def updateMainMenu():
    global interfaceState
    global menuSubstate
    global gameSubstate
    global titleJap
    global menuText1
    global titleLatin
    global alphaModulation

    #titleJapAlpha = 0
    #menuText1Alpha = 0

    if(menuSubstate==MENUFADEIN):
        if(alphaModulation>=250):
            menuSubstate=MENUIDLE
            alphaModulation = 255
        else:    
            alphaModulation+=4
            titleJap.set_alpha(alphaModulation)
            titleLatin.set_alpha(alphaModulation)
            menuText1.set_alpha(alphaModulation)

        print("titleJapAlpha = ",alphaModulation)
        print("menuText1Alpha = ", alphaModulation)

    elif(menuSubstate==MENUIDLE):
        if(keyboardMap[pygame.K_s]):
            menuSubstate = MENUFADEOUT
    elif(menuSubstate==MENUFADEOUT):
        if(alphaModulation < 10):
            #interfaceState=GAME
            #gameSubstate=GAMEFADEIN
            interfaceState=SLIDESHOW_INTRO
            slideShowIntro.slideState=SlideShow.FADE_IN
            alphaModulation=255
        else:
            alphaModulation -=4    
            titleJap.set_alpha(alphaModulation)
            titleLatin.set_alpha(alphaModulation)
            menuText1.set_alpha(alphaModulation)

        print("titleJapAlpha = ", alphaModulation)
        print("menuText1Alpha = ", alphaModulation)

def renderMainMenu():

    screen.fill(BLACK)

    # "百の剣"
    titleJapScaled = pygame.transform.scale_by(titleJap, (6, 6))
    screen.blit(titleJapScaled, 
                ((SCRW/2)-(titleJapScaled.get_width()/2),
                (titleJapScaled.get_height())))
    
    titleLatinScaled = pygame.transform.scale_by(titleLatin, (2, 2))
    screen.blit(titleLatinScaled,
                ((SCRW/2)-(titleLatinScaled.get_width()/2),
                titleJapScaled.get_height()+(titleLatinScaled.get_height()*(2.5)))) 
    
    menuText1Scaled = pygame.transform.scale_by(menuText1, (1, 1))
    screen.blit(menuText1Scaled, 
                ((SCRW/2)-(menuText1Scaled.get_width()/2),
                (SCRH/2)+(menuText1Scaled.get_height()/2)))

    # Update display
    pygame.display.flip()


running = True
paused = False
clock = pygame.time.Clock()

# Set to True to show hitboxes/boundaries
collisionsShown = False

# Game state substates
GAMEFADEIN = 0
GAMEPLAY_PRELUDE = 1
GAMEPLAY_STAGE1 = 2
GAMEPLAY_INTERLUDE1 = 3
GAMEPLAY_STAGE2 = 4
GAMEPLAY_INTERLUDE2 = 5
GAMEPLAY_STAGE3 = 6
GAMEPLAY_INTERLUDE3 = 7
GAMEPLAY_STAGE4 = 8
GAMEPLAY_BOSSCUTSCENE = 9
GAMEPLAY_BOSSFIGHT = 10
GAMEPLAY_OUTRO = 11

gameSubstate = GAMEFADEIN #GAMEFADEIN

def handleGameInput():

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
    #if keyboardChanged:
    for i in keyboardMap: prevKeyboardMap[i]=keyboardMap[i]

stage1Text = font.render("STAGE I", False, WHITE)
stage2Text = font.render("STAGE II", False, WHITE)

STAGETEXT_GOINGDOWN = 0
STAGETEXT_STALL = 1
STAGETEXT_GOINGUP = 2 
stageTextPhase = STAGETEXT_GOINGDOWN
stageTextSpeed = 9.9
stageTextAcceleration = -0.1
stageTextX = (SCRW/2)-(stage1Text.get_width()/2)
stageTextY = 0
stageTextMaxY = (SCRH/2)-(stage1Text.get_height()/2)

STAGETEXTSTALLTIME = 3000
stageTextStallT0 = 0
stageTextStallElapsed = 0

def updateStageXFallingText(textToRender):
        global gameSubstate
        global stageTextPhase
        global stageTextSpeed
        global stageTextAcceleration
        global stageTextX
        global stageTextY
        global stageTextMaxY
        global stageTextStallT0
        global stageTextStallElapsed

        if(stageTextPhase == STAGETEXT_GOINGDOWN):
            if(stageTextY>=stageTextMaxY):
                stageTextPhase = STAGETEXT_STALL
                stageTextStallT0 = pygame.time.get_ticks()
                stageTextStallElapsed
            else:
                if 0<stageTextSpeed+stageTextAcceleration:
                    stageTextSpeed+=stageTextAcceleration 
                stageTextY+=stageTextSpeed
        elif(stageTextPhase == STAGETEXT_STALL):
            if(stageTextStallElapsed >= STAGETEXTSTALLTIME):    
                stageTextPhase = STAGETEXT_GOINGUP
                textToRender.set_alpha(255)
            else:
                if(0==stageTextStallElapsed%200):
                    #stage1Text.set_alpha(255/2)
                    pass
                else:
                    #stage1Text.set_alpha(0)
                    pass
                stageTextStallElapsed = pygame.time.get_ticks() - stageTextStallT0
        elif(stageTextPhase == STAGETEXT_GOINGUP):
            if(stageTextY <= 0-(stage1Text.get_width()*6)):
                stageTextPhase=STAGETEXT_STALL
                gameSubstate=GAMEPLAY_STAGE1
                blackBackground.set_alpha(255/2) # set for pause menu
            else:
                stageTextSpeed-=stageTextAcceleration
                stageTextY-=stageTextSpeed    

def updateGame():

    global collisionsShown
    global arrowSystem
    global player
    global keyboardMap
    global enemies
    global paused
    global interfaceState
    global gameSubstate
    global menuSubstate
    global alphaModulation

    global stageTextPhase 
    global stageTextSpeed
    global stageTextAcceleration
    global stageTextX
    global stageTextY
    global stageTextMaxY
    global stageTextStallT0
    global stageTextStallElapsed

    #if keyboardMap[pygame.K_p]:
    #    paused = not paused

    if(gameSubstate==GAMEFADEIN):

        if(0>=alphaModulation):
            gameSubstate=GAMEPLAY_PRELUDE
        else:
            alphaModulation-=4
            blackBackground.set_alpha(alphaModulation)
    elif(gameSubstate==GAMEPLAY_PRELUDE):
        updateStageXFallingText(stage1Text)
    elif(gameSubstate==GAMEPLAY_STAGE1):
        if paused:
            if ( (keyboardMap[pygame.K_r])
                and (not prevKeyboardMap[pygame.K_p])):
                paused = False
        else:
            if ( (keyboardMap[pygame.K_p])
            and (not prevKeyboardMap[pygame.K_p])):
                paused = True 
        
        if ( (keyboardMap[pygame.K_q])
            and (not prevKeyboardMap[pygame.K_q])):
            interfaceState = MAINMENU
            menuSubstate = MENUFADEIN

        if paused: return

        if (keyboardMap[pygame.K_c]
        and (prevKeyboardMap[pygame.K_c] != keyboardMap[pygame.K_c])):
            collisionsShown = not collisionsShown;

        # (Later include all the update logic in its own function)

        # Update entity controllers
        updatePlayerControl(player, keyboardMap, enemies, 0, SCRW)

        # Update AIs
        
        updateLobotomite(player, tstEnemy1)
        #updateLobotomite(player, tstEnemy2)
        #updateLobotomite(player, tstEnemy3)
        #updateLobotomite(player, tstEnemy4)
        
        updateShooter(player, shooter)

        # Update entity behaviour 
        player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)#, arrowSystem)

        # Update enemy behaviour
        #for e in enemies:
        #    e.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW, arrowSystem)

        tstEnemy1.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)
        shooter.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW, arrowSystem)

        arrowSystem.update(0, SCRW)

def renderGame():
    global gameSubstate

    global stageTextPhase 
    global stageTextSpeed
    global stageTextAcceleration
    global stageTextX
    global stageTextY
    global stageTextMaxY

    # Clear screen
    screen.fill(BLACK)
    
    if(gameSubstate==GAMEFADEIN):
        # Render background
        bgScale = (SCRW, SCRH)
        scaledBg = pygame.transform.scale(background, bgScale)
        screen.blit(scaledBg, (0,0))

        screen.blit(blackBackground, (0,0))

    elif(gameSubstate==GAMEPLAY_PRELUDE):
        bgScale = (SCRW, SCRH)
        scaledBg = pygame.transform.scale(background, bgScale)
        screen.blit(scaledBg, (0,0))

        screen.blit(stage1Text,
                    (stageTextX, stageTextY))

    elif(gameSubstate==GAMEPLAY_STAGE1):
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
        objTypeArr.append(RENDEROBJ_RIKU)
        #objTypeArr.append(RENDEROBJ_RANGEDTIER1)  
        
        objArr.append(tstEnemy1)
        objTypeArr.append(RENDEROBJ_MELEETIER1)

        '''
        objArr.append(tstEnemy1)
        objTypeArr.append(RENDEROBJ_MELEETIER1)
        objArr.append(tstEnemy2)
        objTypeArr.append(RENDEROBJ_MELEETIER2)
        objArr.append(tstEnemy3)
        objTypeArr.append(RENDEROBJ_MELEETIER3)
        objArr.append(tstEnemy4)
        objTypeArr.append(RENDEROBJ_MELEETIER4)
        '''

        objArr.append(shooter)
        objTypeArr.append(RENDEROBJ_RANGEDTIER1)

        for a in arrowSystem.arrows:
            objArr.append(a)
            objTypeArr.append(RENDEROBJ_ARROW)

        renderObjectsByPseudoZ(screen, objArr, objTypeArr, animationAtlas, collisionsShown, font)

        debugText = font.render("In development...", False, WHITE)
        scaledDebugText = pygame.transform.scale_by(debugText, scaleFactor)
        screen.blit(debugText, (10, SCRH-scaledDebugText.get_height()))

        if paused:

            #darkRect = pygame.rect.Rect(0, 0, SCRW, SCRH)
            screen.blit(blackBackground,
                        (0,0))    

            pauseText1 = font.render("PAUSED", False, WHITE)
            #scaledPausedText1 = pygame.transform.scale_by(pauseText1, scaleFactor)
            screen.blit(pauseText1, 
                        ((SCRW/2)-(pauseText1.get_width()/2), 
                        (SCRH/2)-(pauseText1.get_height()/2)))

            pauseText2 = font.render("Press 'r' to resume", False, WHITE)
            #scaledPausedText2 = pygame.transform.scale_by(pauseText2, scaleFactor)
            screen.blit(pauseText2, 
                        ((SCRW/2)-(pauseText2.get_width()/2), 
                        (SCRH/2)+(pauseText2.get_height()/(1.5))))
            pauseText3 = font.render("Press 'q' to quit", False, WHITE)
            screen.blit(pauseText3,
                        ((SCRW/2)-(pauseText2.get_width()/2), 
                        (SCRH/2)+(pauseText3.get_height()/(1.5) + pauseText2.get_height()/(1.5))))

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

    #global interfaceState

    while running:
        
        if(interfaceState==MAINMENU):
            ######## INPUT ########
            handleMainMenuInput()
            ######## UPDATE ########
            updateMainMenu()
            ######## RENDER ########
            renderMainMenu()

        if(interfaceState==SLIDESHOW_INTRO):
            ######## INPUT ########
            handleMainMenuInput()
            ######## UPDATE ########
            slideShowIntro.update()
            if(slideShowIntro.finishedSlideShow):
                interfaceState=GAME
                gameSubstate=GAMEFADEIN    
            ######## RENDER ########
            slideShowIntro.render(screen, font)

        if(interfaceState==GAME):   
            ######## INPUT ########
            handleGameInput()
            ######## UPDATE ########
            updateGame()
            ######## RENDER ########
            renderGame()
        # Control frame rate
        clock.tick(60)
    
    # Exit...
    pygame.quit()
    sys.exit()

