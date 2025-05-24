from meleeEnemy import *
import random

MOVEDDURINGCHASE = True
IDLEDURINGCHASE  = False

def getDx(player, npc):
    return player.hitbox.x - npc.hitbox.x

def getDz(player, npc):
    return player.hitbox.pseudoZ - npc.hitbox.pseudoZ

def getXChaseDirection(dx, maxRangeW):
    #dx = getDx(player, npc) #player.hitbox.x - npc.hitbox.x
    return (
        0 if (abs(dx)<=maxRangeW) or 0==dx 
        else (-1 if 0>dx 
                else 1)
    )

def getYChaseDirection(dz, maxRangeZ):
    #dz = getDz(player, npc)#player.hitbox.pseudoZ - npc.hitbox.pseudoZ
    yDirection = 0
    if abs(dz)>=maxRangeZ:
        yDirection = 0 if 0==dz else (1 if dz>0 else -1)
    return yDirection

# AI controller for chasing the player
# Returns 'True' if the npc moved to chase the player,
# 'False' if the is too close and didn't move
def chasePlayer(player, npc, minRangeW, maxRangeW, maxRangeZ):
    
    # Make sure these actions arent interrumpted
    if(npc.currentActionState == ActionState.DYING
    or npc.currentActionState == ActionState.HURTING): 
        return

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

ATTACK1 = 0

def meleeAttackPlayerRandomly(player, npc, leftBound, rightBound):

    # 3 possible attacks
    attackType = random.randint(1, 3)

    print(attackType)

    if(1==attackType):
        npc.attack1([player], leftBound, rightBound)
    elif(2==attackType):
        npc.attack2([player], leftBound, rightBound)
    elif(3==attackType):
        npc.attack3([player], leftBound, rightBound)