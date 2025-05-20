from riku import *
from entityConstants import *
from colorConstants import *
from math import * 

def renderCollisionBoxes(screen, player, collisionsShown):
    # Draw the player's hitbox
    if collisionsShown:
        hitbox_rect = pygame.Rect(player.hitbox.x, player.hitbox.y, player.hitbox.w, player.hitbox.h)
        pygame.draw.rect(screen, GREEN, hitbox_rect, 2)  # Green outline

    # Draw the player's attack box
    if collisionsShown:
        attackboxRect = pygame.Rect(player.attackbox.x, player.attackbox.y, player.attackbox.w, player.attackbox.h)
        pygame.draw.rect(screen, RED, attackboxRect, 2) # Red outline

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
            coolDownFillW = (player.attackCooldownElapsed / coolDownTime) * coolDownW
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


def applyRangedEnemyRenderCorrections(rangedEnemy, renderCorrections):
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

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]

    #print("X correction = ", renderCorrectionX)
    #print("Y correction = ", renderCorrectionY)
    
    # Apply render corrections for player walk (On X and Y)
    if(rangedEnemy.DEFAULT_RWALKANIM_ID == rangedEnemy.currentAnimationID
       or rangedEnemy.DEFAULT_LWALKANIM_ID == rangedEnemy.currentAnimationID):
        #rangedEnemy.renderbox.y += renderCorrectionY
        if(rangedEnemy.DEFAULT_LWALKANIM_ID == rangedEnemy.currentAnimationID):
            rangedEnemy.renderbox.x -= renderCorrectionX 

    # Apply render correction for player run (only on Y)
    if( 
        rangedEnemy.DEFAULT_RRUNANIM_ID == rangedEnemy.currentAnimationID  
    ):
        rangedEnemy.renderbox.y += renderCorrectionY
    if(   
       rangedEnemy.DEFAULT_LRUNANIM_ID == rangedEnemy.currentAnimationID
    ):
        rangedEnemy.renderbox.y += renderCorrectionY
        rangedEnemy.renderbox.x -= renderCorrectionX

    # Apply render correction for player death (On X and Y)
    if(rangedEnemy.DEFAULT_RDEATHANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.y += renderCorrectionY
        #rangedEnemy.renderbox.x += renderCorrectionX

    if(rangedEnemy.DEFAULT_LDEATHANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x -= renderCorrectionX
        rangedEnemy.renderbox.y += renderCorrectionY

    # Apply render correction for player attack 1 (Only on X)
    if(rangedEnemy.LATTACK1ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x -= renderCorrectionX

    # Apply render correction for player attack 2 (On X and Y)
    if(rangedEnemy.LATTACK2ANIM_ID == rangedEnemy.currentAnimationID
        or rangedEnemy.RATTACK2ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.y -= renderCorrectionY
        if(rangedEnemy.LATTACK2ANIM_ID == rangedEnemy.currentAnimationID):
            rangedEnemy.renderbox.x -= renderCorrectionX 

    # Apply render correction for player attack 3 (Only on X)
    if(rangedEnemy.LATTACK3ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x -= renderCorrectionX

def revertRangedEnemyRenderCorrections(rangedEnemy, renderCorrections):
    # Convert from an animation index to a render correction index
    indexRatio = float((rangedEnemy.LATTACK3ANIM_ID+1)/len(renderCorrections))
    renderCorrectionID = (
        int(floor(float(rangedEnemy.currentAnimationID)/indexRatio))
    )

    renderCorrectionX = renderCorrections[renderCorrectionID][0]
    renderCorrectionY = renderCorrections[renderCorrectionID][1]

    # Revert render corrections
    if(rangedEnemy.DEFAULT_RWALKANIM_ID == rangedEnemy.currentAnimationID
       or rangedEnemy.DEFAULT_LWALKANIM_ID == rangedEnemy.currentAnimationID):
        #rangedEnemy.renderbox.y -= renderCorrectionY
        if(rangedEnemy.DEFAULT_LWALKANIM_ID == rangedEnemy.currentAnimationID):
            rangedEnemy.renderbox.x += renderCorrectionX 

    if(#rangedEnemy.DEFAULT_LRUNANIM_ID == rangedEnemy.currentAnimationID or 
        rangedEnemy.DEFAULT_RRUNANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.y -= renderCorrectionY
    if(   
       rangedEnemy.DEFAULT_LRUNANIM_ID == rangedEnemy.currentAnimationID
    ):
        rangedEnemy.renderbox.y -= renderCorrectionY
        rangedEnemy.renderbox.x += renderCorrectionX


    if(rangedEnemy.DEFAULT_RDEATHANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.y -= renderCorrectionY
        #rangedEnemy.renderbox.x -= renderCorrectionX

    if(rangedEnemy.DEFAULT_LDEATHANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x += renderCorrectionX
        rangedEnemy.renderbox.y -= renderCorrectionY

    if(rangedEnemy.LATTACK1ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x += renderCorrectionX 

    if(rangedEnemy.LATTACK2ANIM_ID == rangedEnemy.currentAnimationID
        or rangedEnemy.RATTACK2ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.y += renderCorrectionY 
        if(rangedEnemy.LATTACK2ANIM_ID == rangedEnemy.currentAnimationID):
            rangedEnemy.renderbox.x += renderCorrectionX 

    if(rangedEnemy.LATTACK3ANIM_ID == rangedEnemy.currentAnimationID):
        rangedEnemy.renderbox.x += renderCorrectionX 

    

def renderRiku(screen, player : Riku, animationsData : list, collisionsShown : bool, renderCorrections : list):
    
    renderCollisionBoxes(screen, player, collisionsShown)

    # Scale and Render the character
    targetFrame = animationsData[player.currentAnimationID][player.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyRikuRenderCorrections(player, renderCorrections)

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (player.renderbox.x, player.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertRikuRenderCorrections(player, renderCorrections)

    renderStatusBars(screen, player)

def renderMeleeEnemy(screen, meleeEnemy, animationsData, collisionsShown, renderCorrections):

    renderCollisionBoxes(screen, meleeEnemy, collisionsShown)

    # Scale and Render the character
    targetFrame = animationsData[meleeEnemy.currentAnimationID][meleeEnemy.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyMeleeEnemyRenderCorrections(meleeEnemy, renderCorrections)

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (meleeEnemy.renderbox.x, meleeEnemy.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertMeleeEnemyRenderCorrections(meleeEnemy, renderCorrections)

    renderStatusBars(screen, meleeEnemy)

def renderRangedEnemy(screen, rangedEnemy, animationsData, collisionsShown, renderCorrections):

    renderCollisionBoxes(screen, rangedEnemy, collisionsShown)

    # Scale and Render the character
    targetFrame = animationsData[rangedEnemy.currentAnimationID][rangedEnemy.getCurrentAnimationFrame()]
    scaledSize = (targetFrame.get_width()*scaleFactor, targetFrame.get_height()*scaleFactor)

    applyRangedEnemyRenderCorrections(rangedEnemy, renderCorrections)

    # Perform the actual rendering
    scaledMC = pygame.transform.scale(targetFrame, scaledSize)
    screen.blit(scaledMC, (rangedEnemy.renderbox.x, rangedEnemy.renderbox.y)) #(f.hitbox.x, f.hitbox.y))

    revertRangedEnemyRenderCorrections(rangedEnemy, renderCorrections)

    renderStatusBars(screen, rangedEnemy)


    