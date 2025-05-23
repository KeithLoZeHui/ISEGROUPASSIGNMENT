from meleeEnemy import *

# Test AI controller for chasing the player
def chasePlayer(player, npc):
    
    # Make sure these actions arent interrumpted
    if(npc.currentActionState == ActionState.DYING
    or npc.currentActionState == ActionState.HURTING): 
        return

    maxRangeW = 150
    minRangeW = 120

    # Calculation of x direction
    dx = player.hitbox.x - npc.hitbox.x
    xDirection = (
        0 if (abs(dx)<=maxRangeW) or 0==dx 
        else (-1 if 0>dx 
                else 1)
        )
    
    # If closer than the minimum range, 
    # make the npc take distance
    if abs(dx)<=minRangeW:
        if(npc.lastDirection == Direction.EAST):
            xDirection = 1 
        elif(npc.lastDirection == Direction.WEST):
            xDirection = -1

    # Calculation of y direction 
    dz = player.hitbox.pseudoZ - npc.hitbox.pseudoZ
    yDirection = 0 if 0==dz else (1 if dz>0 else -1)


    # Apply chasing movement
    if(0==xDirection and 0==yDirection):
        npc.forceActionState(ActionState.IDLE)
    else:
        npc.setXMove(xDirection)
        npc.setYMove(yDirection)

def attackPlayer(player, npc):
    pass

class MeleeAI:
    def __init__():
        pass

def updateMeleeAI(meleeAI):
    pass