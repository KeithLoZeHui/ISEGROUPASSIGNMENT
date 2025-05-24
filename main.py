import pygame
import sys
import os

from entityConstants import * 
from colorConstants import * 
from animation import *
from riku import *
from meleeEnemy import *
from rangedEnemy import *
from spritesheet import *
from playerController import *
from meleeEnemyAI import *
from rangedAIs import *
from spriteLoader import*
from entityRenderer import *
from slideShow import *
from enemyHandler import *

import copy

##############################################################################
#####################       RESOURCE LOADING          ########################
##############################################################################

SCRW = 1760
SCRH = 990
RIKUMAXHP = 200
RIKUMAXSP = 100
INITIALHP = RIKUMAXHP 
INITIALSP = RIKUMAXSP

# Y boundaries of the fight 'arena'
UPPERYBOUND = (SCRH/4)*3+40 
LOWERYBOUND = SCRH - 10

RIKUINITIALX = (SCRW/2)-(CAPTAIN_ANIM_DIMS[1][0]/2)
RIKUINITIALY = LOWERYBOUND-CAPTAIN_ANIM_DIMS[1][1]

player = Riku(RIKUINITIALX, RIKUINITIALY, INITIALHP, INITIALSP, RIKUMAXHP, RIKUMAXSP)
player.walkSpeed = 2
player.runSpeed = 4

# Initialize Pygame
pygame.init()

# Initialize display
screen = pygame.display.set_mode((SCRW, SCRH))
pygame.display.set_caption("百の剣 | Hyaku-no-Ken (Hundred Blades)")

# Initialize black background for fade effects
blackBackground = pygame.Surface((SCRW, SCRH), flags=0, depth=32, masks=pygame.Color(BLACK))
blackBackground.set_alpha(255/2)

# Initialize mixer
pygame.mixer.init()

BGM_MAINMENU = "MainMenu.wav"
BGM_INTROSLIDESHOW = "IntroSlideShow.wav"
BGM_MIDGAME = "MidGame.wav"

DEFAULT_BGM_VOLUME = 0.5
bgmVolume = DEFAULT_BGM_VOLUME

# Load and set background music
def loadAndSetBGM(musicName):
    try:
        pygame.mixer.music.load(os.path.join("resources", musicName))
        pygame.mixer.music.set_volume(bgmVolume)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except pygame.error as e:
        print(f"Couldn't load music: {e}")
        sys.exit()

# Lower the BGM volume by 1%
def fadeOutBGMVolume():
    global bgmVolume
    bgmVolume-= 0.01 if bgmVolume >= 0.0 else 0.0
    pygame.mixer.music.set_volume(bgmVolume)

def fadeInBGMVolume():
    global bgmVolume
    bgmVolume+= 0.01 if bgmVolume <= DEFAULT_BGM_VOLUME else 0.0
    pygame.mixer.music.set_volume(bgmVolume)

# Creation of animation objects: These are just
# logical representations of each animation, without
# any image data inside them. Their current index is then 
# used to access the 'animationsData' array below 

meleeAnimations = [
    Animation(
        copy.deepcopy(a[0]), 
        copy.deepcopy(a[1])
    ) for a in MELEE_ANIMATIONS_SETUP]
archerAnimations = [
    Animation(
        copy.deepcopy(a[0]), 
        copy.deepcopy(a[1])
    ) for a in RANGED_ANIMATIONS_SETUP]

# Load the background picture
background = loadBackground()

# Load the intro slide show images
introSlideshowImages = loadIntroSlideImages()

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
for a in meleeAnimations:
    player.addAnimation(a)

def updateMeleeEnemyAnimations(meleeArr):
    for e in meleeArr:
        for a in meleeAnimations:
            e.addAnimation(a)

def updateRangedEnemyAnimations(rangedArr):
    for e in rangedArr:
        for a in archerAnimations:
            e.addAnimation(a)

##############################################################################
##############################################################################



########################################################################
# KEYBOARD LOGIC

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


########################################################################

# Application states
MAINMENU = 0
SLIDESHOW_INTRO = 1
GAME = 2
PAUSE = 3
SLIDESHOW_OUTRO = 4

interfaceState = GAME
#MAINMENU

##############################################################################
############################    MAIN MENU   ##################################
##############################################################################

# Menu substates
MENUFADEIN = 0
MENUIDLE = 1
MENUFADEOUT = 2

# Set main menu music as default
loadAndSetBGM(BGM_MAINMENU)

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
    global bgmVolume

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
            bgmVolume = DEFAULT_BGM_VOLUME
            loadAndSetBGM(BGM_INTROSLIDESHOW)
        else:
            fadeOutBGMVolume()
            alphaModulation -=4    
            titleJap.set_alpha(alphaModulation)
            titleLatin.set_alpha(alphaModulation)
            menuText1.set_alpha(alphaModulation)

        print("titleJapAlpha = ", alphaModulation)
        print("menuText1Alpha = ", alphaModulation)

def renderMainMenuBackground():
    bgScale = (SCRW, SCRH)
    scaledBg = pygame.transform.scale(introSlideshowImages[0], bgScale)
    screen.blit(scaledBg, (0,0))

def renderMainMenu():

    screen.fill(BLACK)

    renderMainMenuBackground()

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

##############################################################################
##############################################################################

##############################################################################
########################    INTRO SLIDESHOW    ###############################
##############################################################################

placeHolderImage = pygame.surface.Surface((400,400))
placeHolderImage.fill((BLUE))
placeHolderImage.set_alpha(255)

slides = [
    Slide(  
         introSlideshowImages[0], 
          ["Japan, 1590 — The Final Fires of the Sengoku Era"],
          2500, 
          5000, 
          2500
    ),
    Slide(  
        introSlideshowImages[1], 
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
        introSlideshowImages[2], 
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
        introSlideshowImages[3], 
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
        introSlideshowImages[4], 
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
        introSlideshowImages[5], 
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

##############################################################################
##############################################################################

##############################################################################
###########################    GAMEPLAY   ####################################
##############################################################################

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
GAMEPLAY_PAUSE = 12

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

stageFinishDelayT0 = -1
stageFinishDelayElapsed = 0
STAGEFINISHDELAY = 2000

enemyHandlerStage1 = EnemyHandler (
    screen,
    [
        EnemySpawnBatch(
            [EnemyHandler.MELEE_TIER1, EnemyHandler.RANGED_TIER1],
            [-1, 1]
        ),
        EnemySpawnBatch (
            [EnemyHandler.RANGED_TIER1, EnemyHandler.RANGED_TIER1],
            [-1, 1]
        ),
        EnemySpawnBatch (
            [EnemyHandler.RANGED_TIER1, EnemyHandler.RANGED_TIER1, EnemyHandler.MELEE_TIER1, EnemyHandler.MELEE_TIER1],
            [-1, 1, -1, 1]
        )
    ]
)

'''
        EnemySpawnBatch (
            [EnemyHandler.MELEE_TIER1, EnemyHandler.MELEE_TIER1],
            [-1, 1]
        ),
        EnemySpawnBatch (
            [EnemyHandler.MELEE_TIER2, EnemyHandler.MELEE_TIER2],
            [-1, 1]
        ),
        EnemySpawnBatch (
            [EnemyHandler.MELEE_TIER3, EnemyHandler.MELEE_TIER3],
            [-1, 1]
        ),
        EnemySpawnBatch (
            [EnemyHandler.MELEE_TIER4, EnemyHandler.MELEE_TIER4],
            [-1, 1]
        )
'''

arrowSystem = ArrowSystem()
for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.MELEE_TIER1):
    arrowSystem.addVulnerableEntity(e)
arrowSystem.addVulnerableEntity(player)


def resetFallingTextState():
    global stageTextPhase
    global stageTextSpeed
    global stageTextY
    global stageTextStallT0
    global stageTextStallElapsed

    stageTextPhase = STAGETEXT_GOINGDOWN
    stageTextSpeed = 9.9
    stageTextY = 0
    stageTextStallT0 = 0
    stageTextStallElapsed = 0

def updateStageXFallingText(textToRender, nextSubState):
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
                #stageTextStallElapsed
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
                gameSubstate=nextSubState
                blackBackground.set_alpha(255/2) # set for pause menu
            else:
                stageTextSpeed-=stageTextAcceleration
                stageTextY-=stageTextSpeed    

def updateEnemySpawning(enemyHandler):

    global stageFinishDelayElapsed
    global stageFinishDelayT0
    global gameSubstate 
    global meleeAIs
    global rangedAIs

    nAliveEnemies = enemyHandler.countAliveEnemies()
    if(0==nAliveEnemies):
        if(enemyHandler.noMoreBatches):
            # Start the delay timer
            if(-1==stageFinishDelayT0):
                stageFinishDelayT0=pygame.time.get_ticks()
            
            # Update the delay timer
            stageFinishDelayElapsed = pygame.time.get_ticks() - stageFinishDelayT0

            if(stageFinishDelayElapsed>=STAGEFINISHDELAY):                    
                enemyHandler.removeDeadEnemies()
                meleeAIs = []
                rangedAIs = []

                resetFallingTextState()
                gameSubstate=GAMEPLAY_INTERLUDE1

                # Reset the delay timer:
                stageFinishDelayElapsed = 0
                stageFinishDelayT0=-1 
        else:
            enemyHandler.spawnNextBatch(
                0-SAMURAI_ANIM_DIMS[0][0], # left bound - enemy W 
                SCRW, # right bound
                UPPERYBOUND-SAMURAI_ANIM_DIMS[0][1],
                LOWERYBOUND-ARCHER_ANIM_DIMS[0][1]
            )

            for t in range(EnemyHandler.MELEE_TIER1, EnemyHandler.MELEE_TIER4+1): 
                # Update melee animations
                enemyHandler.applyFunctionToEnemyArray(t, updateMeleeEnemyAnimations)

                # Update melee AIs
                meleeAIs.append(
                    MeleeEnemyAI(
                        MeleeEnemyAI.DEFAULT_CHASEW_MIN,
                        MeleeEnemyAI.DEFAULT_CHASEW_MAX,
                        MeleeEnemyAI.DEFAULT_CHASEZ_MAX
                    ))

            # Update ranged animations
            for t in range(EnemyHandler.RANGED_TIER1, EnemyHandler.RANGED_TIER4):
                enemyHandler.applyFunctionToEnemyArray(t, updateRangedEnemyAnimations)

def checkPause():
    global gameSubstate

    # Check if pause button was pressed
    if ((keyboardMap[pygame.K_p])
    and (not prevKeyboardMap[pygame.K_p])):
        gameSubstate=GAMEPLAY_PAUSE
        return 
    
def checkCollisionsActivated():
    global collisionsShown

    # Check if collisions are activated
    if (keyboardMap[pygame.K_c]
    and (prevKeyboardMap[pygame.K_c] != keyboardMap[pygame.K_c])):
        collisionsShown = not collisionsShown;

meleeAIs = []
rangedAIs = []

def updateAIs(player, meleeEnemies, rangedEnemies, leftBound, rightBound):
    global meleeAIs
    global rangedAIs    

    for i in range(0, len(meleeEnemies)):
        meleeAIs[i].update(meleeEnemies[i], player, leftBound, rightBound)

    for i in range(0, len(rangedEnemies)):
        # dont do this yet, implement ranged AIs first ....    
        #rangedAIs[i].update(rangedEnemies[i], player)
        pass

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

    global stageFinishDelayElapsed
    global stageFinishDelayT0 

    global bgmVolume

    if(gameSubstate==GAMEFADEIN):
        if(0>=alphaModulation):
            gameSubstate=GAMEPLAY_PRELUDE
            bgmVolume=DEFAULT_BGM_VOLUME
            loadAndSetBGM(BGM_MIDGAME)
        else:
            fadeOutBGMVolume()
            alphaModulation-=4
            blackBackground.set_alpha(alphaModulation)
    
    elif(gameSubstate==GAMEPLAY_PRELUDE):
        updateStageXFallingText(stage1Text,GAMEPLAY_STAGE1)
        
        # Update just to show the idle animation
        player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)

    elif(gameSubstate==GAMEPLAY_STAGE1):

        checkPause()

        checkCollisionsActivated()
        
        # Update enemy spawning 
        updateEnemySpawning(enemyHandlerStage1)

        meleeEnemies = enemyHandlerStage1.getAllMeleeEnemies()
        rangedEnemies = enemyHandlerStage1.getAllRangedEnemies()
        allEnemies = meleeEnemies+rangedEnemies

        # Update player controller
        updatePlayerControl(
            player, 
            keyboardMap, 
            allEnemies,
            0, 
            SCRW
        )

        # Update AI controllers
        updateAIs(player, meleeEnemies, rangedEnemies, 0, SCRW)

        # Update entity behaviour 
        player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)#, arrowSystem)

        # Update melee enemy behaviour
        for e in meleeEnemies:
            e.update(
                LOWERYBOUND, 
                UPPERYBOUND, 
                0-(SAMURAI_ANIM_DIMS[0][0]*2), 
                SCRW+(SAMURAI_ANIM_DIMS[0][0]*2))

        # Update ranged enemy behaviour
        for e in rangedEnemies:
            e.update(
                LOWERYBOUND, 
                UPPERYBOUND, 
                0-(SAMURAI_ANIM_DIMS[0][0]*2), 
                SCRW+(SAMURAI_ANIM_DIMS[0][0]*2),
                arrowSystem)

        arrowSystem.update(0, SCRW)

    elif(gameSubstate==GAMEPLAY_INTERLUDE1):
        updateStageXFallingText(stage2Text,GAMEPLAY_STAGE2)
        
        # Update entity behaviour 
        player.update(LOWERYBOUND, UPPERYBOUND, 0, SCRW)

    elif(gameSubstate==GAMEPLAY_STAGE2):

        pass
    elif(gameSubstate==GAMEPLAY_INTERLUDE2):
        
        pass
    elif(gameSubstate==GAMEPLAY_STAGE3):
        
        pass
    elif(gameSubstate==GAMEPLAY_INTERLUDE3):
        
        pass
    elif(gameSubstate==GAMEPLAY_PAUSE):
        if ((keyboardMap[pygame.K_r])
        and (not prevKeyboardMap[pygame.K_p])):
            gameSubstate=GAMEPLAY_STAGE1
        else:
            if ((keyboardMap[pygame.K_q])
            and (not prevKeyboardMap[pygame.K_q])):
                interfaceState = MAINMENU
                menuSubstate = MENUFADEIN

def renderBackground():
    bgScale = (SCRW, SCRH)
    scaledBg = pygame.transform.scale(background, bgScale)
    screen.blit(scaledBg, (0,0))

def renderAllEntities(statusBarsShown):
    objArr = []
    objTypeArr = []
        
    objArr.append(player)
    objTypeArr.append(RENDEROBJ_RIKU)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.MELEE_TIER1):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_MELEETIER1)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.MELEE_TIER2):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_MELEETIER2)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.MELEE_TIER3):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_MELEETIER3)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.MELEE_TIER4):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_MELEETIER4)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.RANGED_TIER1):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_RANGEDTIER1)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.RANGED_TIER2):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_RANGEDTIER2)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.RANGED_TIER3):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_RANGEDTIER3)

    for e in enemyHandlerStage1.getEnemyArray(EnemyHandler.RANGED_TIER4):
        objArr.append(e)
        objTypeArr.append(RENDEROBJ_RANGEDTIER4)

    for a in arrowSystem.arrows:
        objArr.append(a)
        objTypeArr.append(RENDEROBJ_ARROW)

    # Render all entities ordered by pseudo Z: Provides the 2.5D / Pseudo 3D illusion
    renderObjectsByPseudoZ(screen, objArr, objTypeArr, animationAtlas, collisionsShown, font, statusBarsShown)

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
        renderBackground()
        screen.blit(blackBackground, (0,0))

    elif(gameSubstate==GAMEPLAY_PRELUDE):
        renderBackground()
        screen.blit(stage1Text,
                    (stageTextX, stageTextY))

        renderAllEntities(False)

    elif(gameSubstate==GAMEPLAY_STAGE1):
        renderBackground()

        # Draw the y boundaries
        if collisionsShown:
            pygame.draw.line(screen, WHITE, (0, UPPERYBOUND), (SCRW, UPPERYBOUND))
            pygame.draw.line(screen, WHITE, (0, LOWERYBOUND), (SCRW, LOWERYBOUND))

        renderAllEntities(True)
            
    elif(gameSubstate==GAMEPLAY_INTERLUDE1):
        renderBackground()
        screen.blit(stage2Text,
                (stageTextX, stageTextY))
        
        renderAllEntities(False)

    elif(gameSubstate==GAMEPLAY_STAGE2):
        renderBackground()
        # Draw the y boundaries
        
        if collisionsShown:
            pygame.draw.line(screen, WHITE, (0, UPPERYBOUND), (SCRW, UPPERYBOUND))
            pygame.draw.line(screen, WHITE, (0, LOWERYBOUND), (SCRW, LOWERYBOUND))
        
        renderAllEntities(True)

    elif(gameSubstate==GAMEPLAY_INTERLUDE2):
        renderBackground()
        screen.blit(stage2Text,
                (stageTextX, stageTextY))
    elif(gameSubstate==GAMEPLAY_STAGE3):
        pass
    elif(gameSubstate==GAMEPLAY_INTERLUDE3):
        renderBackground()
        screen.blit(stage2Text,
                (stageTextX, stageTextY))
        
    elif(gameSubstate==GAMEPLAY_PAUSE):
        renderBackground()

        renderAllEntities(False)

        screen.blit(blackBackground,
                    (0,0))    

        pauseText1 = font.render("PAUSED", False, WHITE)
        screen.blit(pauseText1, 
                    ((SCRW/2)-(pauseText1.get_width()/2), 
                    (SCRH/2)-(pauseText1.get_height()/2)))

        pauseText2 = font.render("Press 'r' to resume", False, WHITE)
        screen.blit(pauseText2, 
                    ((SCRW/2)-(pauseText2.get_width()/2), 
                    (SCRH/2)+(pauseText2.get_height()/(1.5))))
        pauseText3 = font.render("Press 'q' to quit", False, WHITE)
        screen.blit(pauseText3,
                    ((SCRW/2)-(pauseText2.get_width()/2), 
                    (SCRH/2)+(pauseText3.get_height()/(1.5) + pauseText2.get_height()/(1.5))))

    # Update display
    pygame.display.flip()

##############################################################################
##############################################################################

##############################################################################
#########################     ENTRY POINT       ##############################
##############################################################################

running = True
clock = pygame.time.Clock()

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
                #fadeOutBGMVolume()
                #if(bgmVolume<=0):
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
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

##############################################################################
##############################################################################