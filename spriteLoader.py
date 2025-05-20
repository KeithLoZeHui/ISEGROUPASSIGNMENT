import pygame
#import sys
import os
from spritesheet import *
from entityConstants import *

# Level 0 file hierarchy
BASERESOURCEDIR = "resources"

# Level 1 file hierarchy
RIKURESOURCEDIR = "Riku"
TIER1RESOURCEDIR = "Tier1"
TIER2RESOURCEDIR = "Tier2"
TIER3RESOURCEDIR = "Tier3"
TIER4RESOURCEDIR = "Tier4"
BOSSRESOURCEDIR = "Boss"

# Level 2 file hierarchy
MELEERESOURCEDIR = "Melee"
RANGEDRESOURCEDIR = "Ranged"

# Background loading
def loadBackground():
    backgroundLoc = os.path.join(BASERESOURCEDIR, "background.png")
    background = pygame.image.load(backgroundLoc).convert_alpha()
    return background

# Riku sprites loading 
def loadRikuSprites():
        
    rikuSublocations = [
            "IdleRight.png", "IdleLeft.png",
            "WalkRight.png", "WalkLeft.png",
            "RunRight.png", "RunLeft.png",
            "BlockRight.png", "BlockLeft.png",
            "HurtRight.png", "HurtLeft.png",
            "DeadRight.png", "DeadLeft.png",
            "Attack1Right.png", "Attack1Left.png",
            "Attack2Right.png", "Attack2Left.png",
            "Attack3Right.png", "Attack3Left.png"
    ]

    rikuLocations = []

    for sl in rikuSublocations:
        rikuLocations.append(
            os.path.join(BASERESOURCEDIR, RIKURESOURCEDIR, sl)
        )

    animationNframes = [
        5, # Idle right
        5, # Idle left
        9, # Walk right
        9, # Walk left
        8, # Run right
        8, # Run left
        2, # Block right
        2, # Block left
        2, # Hurt right
        2, # Hurt left
        6, # Dead right
        6, # Dead left
        4, # Attack 1 right
        4, # Attack 1 left
        5, # Attack 2 right
        5, # Attack 2 left
        4, # Attack 3 right
        4, # Attack 3 left
    ]

    rikuAnimationsData = []

    # works as iterator inside the SAMURAI_ANIM_DIMS_RAW
    animType = 0 

    # works as iterator inside the meleeTier1locations
    animationLoadCounter = 0

    for i in range(0, len(rikuLocations)):
        
        if(2==animationLoadCounter):
            animType+=1
            animationLoadCounter=0

        #print(f"SPRITE RAW DIMENSIONS = {CAPTAIN_ANIM_DIMS_RAW[animType]}")

        # Even means its a 'right' animation
        # (Array starts from 0, 0%2 == 0) 
        if 0==i%2:
            rikuAnimationsData.append(
                getSpritesheetAsSpriteArr(
                    rikuLocations[i],
                    CAPTAIN_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                    CAPTAIN_ANIM_DIMS_RAW[animType][1], # Sprite Height
                    CAPTAIN_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                    CAPTAIN_ANIM_DIMS_RAW[animType][1] # Sheet height
                )
            )
        else:
            rikuAnimationsData.append(
                getSpritesheetAsSpriteArr(
                    rikuLocations[i],
                    CAPTAIN_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                    CAPTAIN_ANIM_DIMS_RAW[animType][1], # Sprite Height
                    CAPTAIN_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                    CAPTAIN_ANIM_DIMS_RAW[animType][1] # Sheet height
                )[::-1] # Reverse frames, because its a 'left' animation
            )

        animationLoadCounter+=1

    
    return rikuAnimationsData

########### TIER 1 SPRITES LOADING ###########

def loadMeleeSprites(tier : int):
    
    meleeTier1Sublocations = [
            "IdleRight.png", "IdleLeft.png",
            "WalkRight.png", "WalkLeft.png",
            "RunRight.png", "RunLeft.png",
            "BlockRight.png", "BlockLeft.png",
            "HurtRight.png", "HurtLeft.png",
            "DeadRight.png", "DeadLeft.png",
            "Attack1Right.png", "Attack1Left.png",
            "Attack2Right.png", "Attack2Left.png",
            "Attack3Right.png", "Attack3Left.png"
    ]

    meleeTier1locations = []

    tierDir = ""
    if(1==tier):
        tierDir = TIER1RESOURCEDIR
    elif(2==tier):
        tierDir = TIER2RESOURCEDIR
    elif(3==tier):
        tierDir = TIER3RESOURCEDIR
    elif(4==tier):
        tierDir = TIER4RESOURCEDIR

    for sl in meleeTier1Sublocations:
        meleeTier1locations.append(
            os.path.join(BASERESOURCEDIR, tierDir, MELEERESOURCEDIR, sl)
        )

    animationNframes = [
        6, # Idle right
        6, # Idle left
        9, # Walk right
        9, # Walk left
        8, # Run right
        8, # Run left
        2, # Block right
        2, # Block left
        2, # Hurt right
        2, # Hurt left
        6, # Dead right
        6, # Dead left
        4, # Attack 1 right
        4, # Attack 1 left
        5, # Attack 2 right
        5, # Attack 2 left
        4, # Attack 3 right
        4, # Attack 3 left
    ]

    meleeTier1AnimationsData = []

    # works as iterator inside the SAMURAI_ANIM_DIMS_RAW
    animType = 0 

    # works as iterator inside the meleeTier1locations
    animationLoadCounter = 0

    for i in range(0, len(meleeTier1locations)):
        
        if(2==animationLoadCounter):
            animType+=1
            animationLoadCounter=0

        #print(f"SPRITE RAW DIMENSIONS = {SAMURAI_ANIM_DIMS_RAW[animType]}")

        # Even means its a 'right' animation
        # (Array starts from 0, 0%2 == 0) 
        if 0==i%2:
            meleeTier1AnimationsData.append(
                getSpritesheetAsSpriteArr(
                    meleeTier1locations[i],
                    SAMURAI_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                    SAMURAI_ANIM_DIMS_RAW[animType][1], # Sprite Height
                    SAMURAI_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                    SAMURAI_ANIM_DIMS_RAW[animType][1] # Sheet height
                )
            )
        else:
            meleeTier1AnimationsData.append(
                getSpritesheetAsSpriteArr(
                    meleeTier1locations[i],
                    SAMURAI_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                    SAMURAI_ANIM_DIMS_RAW[animType][1], # Sprite Height
                    SAMURAI_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                    SAMURAI_ANIM_DIMS_RAW[animType][1] # Sheet height
                )[::-1] # Reverse frames, because its a 'left' animation
            )

        animationLoadCounter+=1
    
    return meleeTier1AnimationsData

def loadRangedTier1Sprites():

    ranged1Sublocations = [
            "IdleRight.png", "IdleLeft.png",
            "WalkRight.png", "WalkLeft.png",
            "RunRight.png", "RunLeft.png",
            "", "", # No blocking animation
            "HurtRight.png", "HurtLeft.png",
            "DeadRight.png", "DeadLeft.png",
            "Attack1Right.png", "Attack1Left.png",
            "Attack2Right.png", "Attack2Left.png",
            "Attack3Right.png", "Attack3Left.png",
            "ShotChargeRight.png", "ShotChargeLeft.png",
            "ShotRight.png", "ShotLeft.png",
            "ArrowRight.png", "ArrowLeft.png"
    ]

    rangedTier1locations = []

    for sl in ranged1Sublocations:
        if ""==sl:
            rangedTier1locations.append("")
        else:
            rangedTier1locations.append(
                os.path.join(BASERESOURCEDIR, TIER1RESOURCEDIR, RANGEDRESOURCEDIR, sl)
            )

    animationNframes = [
        9, # Idle right
        9, # Idle left
        8, # Walk right
        8, # Walk left
        8, # Run right
        8, # Run left
        0, # Block right
        0, # Block left
        3, # Hurt right
        3, # Hurt left
        5, # Dead right
        5, # Dead left
        5, # Attack 1 right
        5, # Attack 1 left
        5, # Attack 2 right
        5, # Attack 2 left
        5, # Attack 3 right
        5, # Attack 3 left
        11, # Shot charge right
        11, # Shot charge left
        3,  # Shot right
        3,  # Shot left
        1,  # Arrow right (not really an animation)
        1,  # Arrow left (not really an animation)
    ]

    rangedTier1AnimationsData = []

    # works as iterator inside the SAMURAI_ANIM_DIMS_RAW
    animType = 0 

    # works as iterator inside the meleeTier1locations
    animationLoadCounter = 0

    for i in range(0, len(rangedTier1locations)):
        
        if(2==animationLoadCounter):
            animType+=1
            animationLoadCounter=0

        #print(f"SPRITE RAW DIMENSIONS = {ARCHER_ANIM_DIMS_RAW[animType]}")
        
        if("" == rangedTier1locations[i]):
            rangedTier1AnimationsData.append(None)
        else:
            # Even means its a 'right' animation
            # (Array starts from 0, 0%2 == 0) 
            if 0==i%2:
                rangedTier1AnimationsData.append(
                    getSpritesheetAsSpriteArr(
                        rangedTier1locations[i],
                        ARCHER_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                        ARCHER_ANIM_DIMS_RAW[animType][1], # Sprite Height
                        ARCHER_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                        ARCHER_ANIM_DIMS_RAW[animType][1] # Sheet height
                    )
                )
            else:
                rangedTier1AnimationsData.append(
                    getSpritesheetAsSpriteArr(
                        rangedTier1locations[i],
                        ARCHER_ANIM_DIMS_RAW[animType][0], # Sprite Width 
                        ARCHER_ANIM_DIMS_RAW[animType][1], # Sprite Height
                        ARCHER_ANIM_DIMS_RAW[animType][0]*animationNframes[i], # Sheet width
                        ARCHER_ANIM_DIMS_RAW[animType][1] # Sheet height
                    )[::-1] # Reverse frames, because its a 'left' animation
                )

        animationLoadCounter+=1
    
    return rangedTier1AnimationsData

