from riku import *

def updatePlayerControl(player : Riku, keyboardMap : list, enemies : list, leftBound, rightBound):

    # Handle key down

    # "Resurrection"
    if(keyboardMap[pygame.K_r] 
       and player.currentActionState==ActionState.DYING):
        player.forceActionState(ActionState.IDLE)

    # Avoid interruption of these actions
    if(
        player.currentActionState==ActionState.DYING
        or player.currentActionState==ActionState.HURTING
        or player.currentActionState==ActionState.ATTACKING1
        or player.currentActionState==ActionState.ATTACKING2
        or player.currentActionState==ActionState.ATTACKING3 
        or player.currentActionState==ActionState.CHARGESHOOT
        or player.currentActionState==ActionState.SHOOT       
    ):
        return
    
    # Test kill switch
    if keyboardMap[pygame.K_g]:
        if(not player.currentActionState==ActionState.DYING):
            player.die()
        return

    # Test hurt switch
    if keyboardMap[pygame.K_h]:
        if(not player.currentActionState==ActionState.HURTING):
            player.hurt(1)
        return

    #if(player.currentActionState==ActionState.ACST_HURTING):
    #    hurtAnimation = player.animations[player.currentAnimationID]
    #    if(hurtAnimation.currentframe == hurtAnimation.nFrames-1):
    #        player.forceActionState(ActionState.ACST_IDLE)
    #else:
    #    return

    if keyboardMap[pygame.K_b]:
        if (not player.currentActionState==ActionState.BLOCKING):
            player.block()
        return

    if keyboardMap[pygame.K_i]:
        player.isRunning = True

    if keyboardMap[pygame.K_j]:
        if(not player.currentActionState==ActionState.ATTACKING1):
            player.attack1(enemies, leftBound, rightBound)
        return 

    if keyboardMap[pygame.K_k]:
        if(not player.currentActionState==ActionState.ATTACKING2):
            player.attack2(enemies, leftBound, rightBound)
        return

    if keyboardMap[pygame.K_l]:
        if(not player.currentActionState==ActionState.ATTACKING3):
            player.attack3(enemies, leftBound, rightBound)
        return

    # TEST ONLY: Shoot key
    if keyboardMap[pygame.K_o]:
        if(not (player.currentActionState==ActionState.CHARGESHOOT
           or player.currentActionState==ActionState.SHOOT)):
            player.shoot()
        return

    if keyboardMap[pygame.K_w]: player.setYMove(-1)
    if keyboardMap[pygame.K_s]: player.setYMove(1)

    if keyboardMap[pygame.K_a]: player.setXMove(-1)
    if keyboardMap[pygame.K_d]: player.setXMove(1)

    if keyboardMap[pygame.K_SPACE]: pass
        #if(not prevKeyboardMap[pygame.K_SPACE]):
        #    f.jump() #f.toggleRun()
        #f.forceActionState(fighter.ActionState.ACST_JUMPING)

    # Handle key releases
    if not keyboardMap[pygame.K_i]:
        player.isRunning = False

    if not(keyboardMap[pygame.K_w] or keyboardMap[pygame.K_s]): 
        player.setYMove(0)
    if not(keyboardMap[pygame.K_a] or keyboardMap[pygame.K_d]): 
        player.setXMove(0)

    if not(keyboardMap[pygame.K_w] or keyboardMap[pygame.K_s]
        or keyboardMap[pygame.K_a] or keyboardMap[pygame.K_d]):
        player.forceActionState(ActionState.IDLE)

    if(player.currentActionState==ActionState.BLOCKING):
        if(not keyboardMap[pygame.K_b]):
            player.forceActionState(ActionState.IDLE)
        return


        