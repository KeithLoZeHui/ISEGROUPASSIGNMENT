from riku import *
from arrowSystem import *
from entityConstants import *
from colorConstants import *
from math import * 

def renderEntityCollisionBoxes(screen, player, collisionsShown):
    if collisionsShown:
        
        # Draw the player's hitbox
        hitbox_rect = pygame.Rect(player.hitbox.x, player.hitbox.y, player.hitbox.w, player.hitbox.h)
        pygame.draw.rect(screen, GREEN, hitbox_rect, 2)  # Green outline

        # Draw the players pseudoZ
        pygame.draw.line(screen, BLUE,
                         (player.hitbox.x-10, player.hitbox.pseudoZ),
                         (player.hitbox.x+player.hitbox.w+10, player.hitbox.pseudoZ),
                         2)

        # Draw the player's render box
        renderboxRect = pygame.Rect(player.renderbox.x, player.renderbox.y, player.renderbox.w, player.renderbox.h)
        pygame.draw.rect(screen, YELLOW, renderboxRect, 2) # Yellow outline

        # Draw the player's attack box
        attackboxRect = pygame.Rect(player.attackbox.x, player.attackbox.y, player.attackbox.w, player.attackbox.h)
        pygame.draw.rect(screen, RED, attackboxRect, 2) # Red outline

def renderArrowCollisionBox(screen, arrow, collisionsShown):
    if collisionsShown:
        # Draw the arrow's attack box
        attackboxRect = pygame.Rect(arrow.hitbox.x, arrow.hitbox.y, arrow.hitbox.w, arrow.hitbox.h)
        pygame.draw.rect(screen, RED, attackboxRect, 2) # Red outline

        # Draw the arrow's pseudoZ
        pygame.draw.line(screen, BLUE,
                         (arrow.hitbox.x-10, arrow.hitbox.pseudoZ),
                         (arrow.hitbox.x+arrow.hitbox.w+10, arrow.hitbox.pseudoZ),
                         2)

def renderStatusBars(screen, player):
    if(not player.currentActionState == ActionState.DYING):

        # Render the cooldown bar (if available)
        if player.attackCoolingDown:
            coolDownW = player.hitbox.w
            coolDownH = 10
            coolDownX = player.hitbox.x
            coolDownY = player.hitbox.y - (3*coolDownH)-(2*2)

            coolDownTime = 0

            if 2 == player.lastAttack:
                coolDownTime = player.ATTACK2_COOLDOWN
            if 3 == player.lastAttack:
                coolDownTime = player.ATTACK3_COOLDOWN

            # Draw cooldown bar fill
            coolDownFactor = (player.attackCooldownElapsed / coolDownTime) if coolDownTime > 0 else 0 
            coolDownFillW = coolDownFactor * coolDownW
            pygame.draw.rect(screen, WHITE, (coolDownX, coolDownY, coolDownFillW-4, coolDownH))

        # Render the player's health bar
        healthBarW = player.hitbox.w
        healthBarH = 10
        healthBarX = player.hitbox.x
        healthBarY = player.hitbox.y-(2*healthBarH)-2
        font = pygame.font.Font(None, 18)

        # Draw health text
        healthText = font.render(f"HP:", True, WHITE)
        screen.blit(healthText, (healthBarX-30, healthBarY))

        # Draw health bar fill
        healthFillW = (player.hp / player.maxHp) * healthBarW
        healthColor = (GREEN if player.hp > (player.maxHp/2) 
                        else YELLOW 
                        if player.hp < (player.maxHp/2) and player.hp > (player.maxHp/4)  
                        else RED)
        pygame.draw.rect(screen, healthColor, (healthBarX, healthBarY, healthFillW-4, healthBarH))

        # Render the player's stamina bar
        staminaBarW = player.hitbox.w
        staminaBarH = healthBarH
        staminaBarX = player.hitbox.x
        staminaBarY = player.hitbox.y-staminaBarH

        # Draw stamina text
        staminaText = font.render(f"SP:", True, WHITE)
        screen.blit(staminaText, (staminaBarX-30, staminaBarY))

        # Draw stamina bar fill
        staminaFillW = (player.sp / player.maxSp) * staminaBarW
        staminaColor = BLUE
        pygame.draw.rect(screen, staminaColor, (staminaBarX, staminaBarY, staminaFillW-4, staminaBarH))

def applyRikuRenderCorrections(riku, renderCorrections):
    # Render correction: Given that the animations vary in resolutions,
    # it is necessary to align all of them around a common coordinate.
    # The 'render correction' is a transformation for aligning animations
    # with obvious resolution discrepancies with the rest of the animations 

    # Apply render corrections

    # Convert from an animation index to a render correction index
    indexRatio = float((riku.LATTACK3ANIM_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(riku.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]

    #print("X correction = ", renderCorrectionX)
    #print("Y correction = ", renderCorrectionY)
    
    # Apply render correction for player run (only on Y)
    if(riku.DEFAULT_RRUNANIM_ID == riku.currentAnimationID
       or riku.DEFAULT_LRUNANIM_ID == riku.currentAnimationID):
        riku.renderbox.y += renderCorrectionY

    # Apply render correction for player death (Only on X)
    if(riku.DEFAULT_LDEATHANIM_ID == riku.currentAnimationID):
        riku.renderbox.x -= renderCorrectionX

    # Apply render correction for player attack 1 (Only on X)
    if(riku.LATTACK1ANIM_ID == riku.currentAnimationID):
        riku.renderbox.x -= renderCorrectionX

    # Apply render correction for player attack 2 (On X and Y)
    if(riku.LATTACK2ANIM_ID == riku.currentAnimationID
        or riku.RATTACK2ANIM_ID == riku.currentAnimationID):
        riku.renderbox.y -= renderCorrectionY
        if(riku.LATTACK2ANIM_ID == riku.currentAnimationID):
            riku.renderbox.x -= renderCorrectionX 

    # Apply render correction for player attack 3 (Only on X)
    if(riku.LATTACK3ANIM_ID == riku.currentAnimationID):
        riku.renderbox.x -= renderCorrectionX

def revertRikuRenderCorrections(riku, renderCorrections):
    # Convert from an animation index to a render correction index
    indexRatio = float((riku.LATTACK3ANIM_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(riku.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]

    # Revert render corrections
    if(riku.LATTACK1ANIM_ID == riku.currentAnimationID):
        riku.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK1_RENDERCORRECTION[0]

    if(riku.LATTACK2ANIM_ID == riku.currentAnimationID
        or riku.RATTACK2ANIM_ID == riku.currentAnimationID):
        riku.renderbox.y += renderCorrectionY #CAPTAIN_ATTACK2_RENDERCORRECTION[1]
        if(riku.LATTACK2ANIM_ID == riku.currentAnimationID):
            riku.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK2_RENDERCORRECTION[0]

    if(riku.LATTACK3ANIM_ID == riku.currentAnimationID):
        riku.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK3_RENDERCORRECTION[0]

    if(riku.DEFAULT_LDEATHANIM_ID == riku.currentAnimationID):
        riku.renderbox.x += renderCorrectionX #CAPTAIN_DEADANIM_RENDERCORRECTION[0]
    
    if(riku.DEFAULT_RRUNANIM_ID == riku.currentAnimationID
       or riku.DEFAULT_LRUNANIM_ID == riku.currentAnimationID):
        riku.renderbox.y -= renderCorrectionY

def applyMeleeEnemyRenderCorrections(meleeEnemy, renderCorrections):
    # Render correction: Given that the animations vary in resolutions,
    # it is necessary to align all of them around a common coordinate.
    # The 'render correction' is a transformation for aligning animations
    # with obvious resolution discrepancies with the rest of the animations 

    # Apply render corrections

    # Convert from an animation index to a render correction index
    indexRatio = float((meleeEnemy.LATTACK3ANIM_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(meleeEnemy.currentAnimationID)/indexRatio))
    )

    #print(renderCorrectionID)

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]

    #print("X correction = ", renderCorrectionX)
    #print("Y correction = ", renderCorrectionY)
    
    # Apply render correction for player run (only on Y)
    if(meleeEnemy.DEFAULT_RRUNANIM_ID == meleeEnemy.currentAnimationID
       or meleeEnemy.DEFAULT_LRUNANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.y += renderCorrectionY

    # Apply render correction for player death (Only on X)
    if(meleeEnemy.DEFAULT_LDEATHANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x -= renderCorrectionX

    # Apply render correction for player attack 1 (Only on X)
    if(meleeEnemy.LATTACK1ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x -= renderCorrectionX

    # Apply render correction for player attack 2 (On X and Y)
    if(meleeEnemy.LATTACK2ANIM_ID == meleeEnemy.currentAnimationID
        or meleeEnemy.RATTACK2ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.y -= renderCorrectionY
        if(meleeEnemy.LATTACK2ANIM_ID == meleeEnemy.currentAnimationID):
            meleeEnemy.renderbox.x -= renderCorrectionX 

    # Apply render correction for player attack 3 (Only on X)
    if(meleeEnemy.LATTACK3ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x -= renderCorrectionX

def revertMeleeEnemyRenderCorrections(meleeEnemy, renderCorrections):
    # Convert from an animation index to a render correction index
    indexRatio = float((meleeEnemy.LATTACK3ANIM_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(meleeEnemy.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]
    
    # Revert render corrections
    if(meleeEnemy.LATTACK1ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK1_RENDERCORRECTION[0]

    if(meleeEnemy.LATTACK2ANIM_ID == meleeEnemy.currentAnimationID
        or meleeEnemy.RATTACK2ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.y += renderCorrectionY #CAPTAIN_ATTACK2_RENDERCORRECTION[1]
        if(meleeEnemy.LATTACK2ANIM_ID == meleeEnemy.currentAnimationID):
            meleeEnemy.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK2_RENDERCORRECTION[0]

    if(meleeEnemy.LATTACK3ANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x += renderCorrectionX #CAPTAIN_ATTACK3_RENDERCORRECTION[0]

    if(meleeEnemy.DEFAULT_LDEATHANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.x += renderCorrectionX #CAPTAIN_DEADANIM_RENDERCORRECTION[0]
    
    if(meleeEnemy.DEFAULT_RRUNANIM_ID == meleeEnemy.currentAnimationID
       or meleeEnemy.DEFAULT_LRUNANIM_ID == meleeEnemy.currentAnimationID):
        meleeEnemy.renderbox.y -= renderCorrectionY


def applyRangedEnemyRenderCorrections(rangedEnemy, renderCorrections, renderCorrectionXMask, renderCorrectionYMask):
    # Render correction: Given that the animations vary in resolutions,
    # it is necessary to align all of them around a common coordinate.
    # The 'render correction' is a transformation for aligning animations
    # with obvious resolution discrepancies with the rest of the animations 

    # Apply render corrections

    # Convert from an animation index to a render correction index
    indexRatio = float((rangedEnemy.LARROW_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(rangedEnemy.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]*renderCorrectionXMask[rangedEnemy.currentAnimationID]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]*renderCorrectionYMask[rangedEnemy.currentAnimationID]

    #print("X correction = ", renderCorrectionX)
    #print("Y correction = ", renderCorrectionY)
    
    #print(f"Y correction when applying correction: {renderCorrectionY}")

    # Apply render corrections for player walk (On X and Y)
    rangedEnemy.renderbox.x += renderCorrectionX
    rangedEnemy.renderbox.y += renderCorrectionY


def revertRangedEnemyRenderCorrections(rangedEnemy, renderCorrections, renderCorrectionXMask, renderCorrectionYMask):
    # Convert from an animation index to a render correction index
    indexRatio = float((rangedEnemy.LARROW_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(rangedEnemy.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]*renderCorrectionXMask[rangedEnemy.currentAnimationID]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]*renderCorrectionYMask[rangedEnemy.currentAnimationID]

    #print(f"Y correction when reverting correction: {renderCorrectionY}")

    # Revert render corrections
    rangedEnemy.renderbox.x -= renderCorrectionX
    rangedEnemy.renderbox.y -= renderCorrectionY

def renderRiku(screen, player : Riku, animationsData : list, collisionsShown : bool):
    
    renderEntityCollisionBoxes(screen, player, collisionsShown)

    # Scale and Render the character
    targetFrame = animationsData[player.currentAnimationID][player.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyRikuRenderCorrections(player, CAPTAIN_RENDER_CORRECTIONS)

    player.renderbox.w = scaledSize[0]
    player.renderbox.h = scaledSize[1]

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (player.renderbox.x, player.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertRikuRenderCorrections(player, CAPTAIN_RENDER_CORRECTIONS)

    renderStatusBars(screen, player)

def renderMeleeEnemy(screen, meleeEnemy, animationsData, collisionsShown): #, renderCorrections):

    renderEntityCollisionBoxes(screen, meleeEnemy, collisionsShown)

    # Scale and Render the character
    targetFrame = animationsData[meleeEnemy.currentAnimationID][meleeEnemy.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyMeleeEnemyRenderCorrections(meleeEnemy, SAMURAI_RENDER_CORRECTIONS)#renderCorrections)

    meleeEnemy.renderbox.w = scaledSize[0]
    meleeEnemy.renderbox.h = scaledSize[1]

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (meleeEnemy.renderbox.x, meleeEnemy.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertMeleeEnemyRenderCorrections(meleeEnemy, SAMURAI_RENDER_CORRECTIONS) #renderCorrections)

    renderStatusBars(screen, meleeEnemy)

def renderRangedEnemy(screen, rangedEnemy, animationsData, collisionsShown):

    # Scale and Render the character
    targetFrame = animationsData[rangedEnemy.currentAnimationID][rangedEnemy.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyRangedEnemyRenderCorrections(rangedEnemy, ARCHER_RENDER_CORRECTIONS, ARCHER_RENDER_CORRECTION_XMASK, ARCHER_RENDER_CORRECTION_YMASK)

    rangedEnemy.renderbox.w = scaledSize[0]
    rangedEnemy.renderbox.h = scaledSize[1]

    renderEntityCollisionBoxes(screen, rangedEnemy, collisionsShown)

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (rangedEnemy.renderbox.x, rangedEnemy.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertRangedEnemyRenderCorrections(rangedEnemy, ARCHER_RENDER_CORRECTIONS, ARCHER_RENDER_CORRECTION_XMASK, ARCHER_RENDER_CORRECTION_YMASK)

    renderStatusBars(screen, rangedEnemy)

def renderArrow(screen, arrow, collisionsShown, leftArrowSprite, rightArrowSprite):
            renderArrowCollisionBox(screen, arrow, collisionsShown)
            
            targetFrame = leftArrowSprite if -1 == arrow.direction else rightArrowSprite
            scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

            # Perform the actual rendering
            scaledArrow = pygame.transform.scale(targetFrame, scaledSize)
            screen.blit(scaledArrow, (arrow.hitbox.x, arrow.hitbox.y))

def renderArrows(screen, arrowSystem, collisionsShown, leftArrowSprite, rightArrowSprite):

    if arrowSystem.arrows != []:
        arrowArr = arrowSystem.arrows

        for i in range(0, len(arrowArr)):

            renderArrowCollisionBox(screen, arrowArr[i], collisionsShown)

            
            targetFrame = leftArrowSprite if -1 == arrowArr[i].direction else rightArrowSprite


            scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

            # Perform the actual rendering
            scaledArrow = pygame.transform.scale(targetFrame, scaledSize)
            screen.blit(scaledArrow, (arrowArr[i].hitbox.x, arrowArr[i].hitbox.y))

RENDEROBJ_RIKU = 0

RENDEROBJ_MELEETIER1 = 1 
RENDEROBJ_MELEETIER2 = 2
RENDEROBJ_MELEETIER3 = 3
RENDEROBJ_MELEETIER4 = 4

RENDEROBJ_RANGEDTIER1 = 5 
RENDEROBJ_RANGEDTIER2 = 6
RENDEROBJ_RANGEDTIER3 = 7
RENDEROBJ_RANGEDTIER4 = 8

RENDEROBJ_ARROW = 9

# Objects can be fighters, arrows, particles
def renderObjectsByPseudoZ(screen, objArr, objTypeArr, animationAtlas, collisionsShown):
    
    # Create a parallel list containing the 'pseudoZ' dimension: 
    zArr = [o.hitbox.pseudoZ for o in objArr]

    # Sort the objArr ascending by 'pseudoZ' (use bubble sort)
    nObjs = len(objArr)
    for i in range(nObjs):
        for j in range(0, nObjs-i-1):
            if(zArr[j] > zArr[j+1]):
                # Swap on the 3 arrays in parallel 
                zArr[j], zArr[j+1] = zArr[j+1], zArr[j]
                objArr[j], objArr[j+1] = objArr[j+1], objArr[j]
                objTypeArr[j], objTypeArr[j+1] = objTypeArr[j+1], objTypeArr[j]

    # Render each object
    for i in range(nObjs):

        if(RENDEROBJ_RIKU==objTypeArr[i]):
            renderRiku(screen, objArr[i], animationAtlas[RENDEROBJ_RIKU], collisionsShown)

        elif(RENDEROBJ_MELEETIER1==objTypeArr[i]):
            renderMeleeEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_MELEETIER1], collisionsShown)
        elif(RENDEROBJ_MELEETIER2==objTypeArr[i]):
            renderMeleeEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_MELEETIER2], collisionsShown)
        elif(RENDEROBJ_MELEETIER3==objTypeArr[i]):
            renderMeleeEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_MELEETIER2], collisionsShown)
        elif(RENDEROBJ_MELEETIER1==objTypeArr[i]):
            renderMeleeEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_MELEETIER2], collisionsShown)
    
        elif(RENDEROBJ_RANGEDTIER1==objTypeArr[i]):
            renderRangedEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_RANGEDTIER1], collisionsShown)
        elif(RENDEROBJ_RANGEDTIER2==objTypeArr[i]):
            renderRangedEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_RANGEDTIER2], collisionsShown)
        elif(RENDEROBJ_RANGEDTIER3==objTypeArr[i]):
            renderRangedEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_RANGEDTIER3], collisionsShown)
        elif(RENDEROBJ_RANGEDTIER4==objTypeArr[i]):
            renderRangedEnemy(screen, objArr[i], animationAtlas[RENDEROBJ_RANGEDTIER4], collisionsShown)

        elif(RENDEROBJ_ARROW==objTypeArr[i]):
            renderArrow(screen, objArr[i], collisionsShown, animationAtlas[RENDEROBJ_ARROW][1], animationAtlas[RENDEROBJ_ARROW][0])

        if(RENDEROBJ_ARROW!=objTypeArr[i]):
            #renderEntityCollisionBoxes(screen, objArr[i], collisionsShown)
            pass
        else:
            renderArrowCollisionBox(screen, objArr[i], collisionsShown)