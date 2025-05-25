from meleeEnemy import *
import random

MOVEDDURINGCHASE = True
IDLEDURINGCHASE  = False

def getDx(player, npc):
    return player.hitbox.x - npc.hitbox.x

def getDz(player, npc):
    return player.hitbox.pseudoZ - npc.hitbox.pseudoZ

def getXChaseDirection(dx, maxRangeW):
    return (
        0 if (abs(dx)<=maxRangeW) or 0==dx 
        else (-1 if 0>dx 
                else 1)
    )

def getYChaseDirection(dz, maxRangeZ):
    yDirection = 0
    if abs(dz)>=maxRangeZ:
        yDirection = 0 if 0==dz else (1 if dz>0 else -1)
    return yDirection

def getXRelocationDirection(dx, maxRangeW):
    return (
        0 if (abs(dx)<=maxRangeW) or 0==dx 
        else (1 if 0>dx 
                else -1)
    )

def getYRelocationDirection(dz, maxRangeZ):
    yDirection = 0
    if abs(dz)>=maxRangeZ:
        yDirection = 0 if 0==dz else (1 if dz>0 else -1)
    return yDirection

# AI controller for chasing the player
# Returns 'True' if the npc moved to chase the player,
# 'False' if the is too close and didn't move
def chasePlayer(player, npc, minRangeW, maxRangeW, maxRangeZ):
    
    # Make sure these actions arent interrumpted
    #if(npc.currentActionState == ActionState.DYING
    #or npc.currentActionState == ActionState.HURTING): 
    #    return

    # Calculation of x direction
    dx = getDx(player, npc)
    xDirection = getXChaseDirection(dx, maxRangeW)
   
    # If closer than the minimum range, 
    # make the npc take distance
    if abs(dx)<=minRangeW:
        if(npc.lastDirection == Direction.EAST):
            xDirection = 1 
        elif(npc.lastDirection == Direction.WEST):
            xDirection = -1

    # Calculation of y direction
    dz = getDz(player, npc)
    yDirection = getYChaseDirection(dz, maxRangeZ)

    # Apply chasing movement
    if(0==xDirection and 0==yDirection):
        npc.forceActionState(ActionState.IDLE)
    else:
        npc.setXMove(xDirection)
        npc.setYMove(yDirection)

    # Set direction towards player when 'idle chasing'
    if(0==xDirection and 0==yDirection):
        if(dx<0):
            npc.lastDirection = Direction.WEST
        elif(dx>0):
            npc.lastDirection = Direction.EAST

    # If there's a move in at least one axis, 
    # there was a chase move
    return (
        xDirection!=0 # There was a move in X
        or yDirection!=0 # There was a move in Y
    )

def relocateFromPlayer(player, npc, minRangeW, maxRangeW, maxRangeZ, leftBound, rightBound):

    # Calculation of x direction
    dx = getDx(player, npc)
    xDirection = getXChaseDirection(dx, maxRangeW) #getXRelocationDirection(dx, maxRangeW)

    # Calculation of y direction
    dz = getDz(player, npc)
    yDirection = getYChaseDirection(dz, maxRangeZ)#getYRelocationDirection(dz, maxRangeZ)
    
    # If closer than the minimum range, 
    # make the npc take distance
    if abs(dx)<=minRangeW:
        xDirection = -1*xDirection
    
    # Apply relocation movement
    if(0==xDirection and 0==yDirection):
        npc.forceActionState(ActionState.IDLE)
    else:
        # If not enough x space to relocate, just set to 'idle relocating'
        if(
            not (npc.hitbox.x+(xDirection*npc.xVelocity) <= leftBound or
            npc.hitbox.x+(xDirection*npc.xVelocity) >= rightBound)
        ):
            npc.setXMove(xDirection)
        else:
            xDirection = 0

        npc.setYMove(yDirection)

    # Set direction towards player when 'idle relocation'
    if(0==xDirection and 0==yDirection):
        if(dx<0):
            npc.lastDirection = Direction.WEST
        elif(dx>0):
            npc.lastDirection = Direction.EAST

    # If there's a move in at least one axis, 
    # there was a chase move
    return (
        xDirection!=0 # There was a move in X
        or yDirection!=0 # There was a move in Y
    )

def meleeAttackPlayerRandomly(player, npc, leftBound, rightBound):

    # 3 possible attacks
    attackType = random.randint(1, 3)

    if(1==attackType):
        npc.attack1([player], leftBound, rightBound)
    elif(2==attackType):
        npc.attack2([player], leftBound, rightBound)
    elif(3==attackType):
        npc.attack3([player], leftBound, rightBound)
