from rangedEnemy import *

# Testing AI...
def updateShooter(player, npc):

    # Make sure these actions arent interrumpted
    if(npc.currentActionState == ActionState.DYING
    or npc.currentActionState == ActionState.HURTING
    or npc.currentActionState == ActionState.CHARGESHOOT
    or npc.currentActionState == ActionState.SHOOT): 
        return
    

    npc.shoot()
    