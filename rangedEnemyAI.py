from utilsAI import *

class RangedEnemyAI:
    
    DEFAULT_SHOOTW_MIN = 120*4
    DEFAULT_SHOOTW_MAX = 120*5
    DEFAULT_SHOOTZ_MAX = AABB.PSEUDOZ_OVERLAP_MARGIN

    RELOCATING = 0
    SHOOTING = 1
    
    SHOOTCOOLDOWN = 1000

    def __init__(self, minShootW, maxShootW, maxShootZ):
        self.currentState = self.RELOCATING
        self.minShootW = minShootW
        self.maxShootW = maxShootW
        self.maxShootZ = maxShootZ
        self.shootCooldownT0 = pygame.time.get_ticks()
        self.shootCooldownElapsed = 0

    def update(self, rangedBody, player, leftBound, rightBound):
        # Avoid interruption of these actions
        if(
            rangedBody.currentActionState==ActionState.DYING
            or rangedBody.currentActionState==ActionState.HURTING 
            or rangedBody.currentActionState==ActionState.CHARGESHOOT
            or rangedBody.currentActionState==ActionState.SHOOT       
        ):
            return
        
        if(ActionState.DYING==player.currentActionState):
            return

        if(self.RELOCATING == self.currentState):
            relocationResult = chasePlayer(player, rangedBody, self.minShootW, self.maxShootW, self.maxShootZ) #, leftBound, rightBound)
            # relocateFromPlayer(player, rangedBody, self.minShootW, 
            #                   self.maxShootW, self.maxShootZ, leftBound, rightBound)
            
            if(IDLEDURINGCHASE == relocationResult):
                self.currentState = self.SHOOTING

        elif(self.SHOOTING == self.currentState):
            dx = getDx(player, rangedBody)
            dz = getDz(player, rangedBody) 
            if (abs(dx) > self.maxShootW 
                or abs(dx) < self.minShootW
                or abs(dz) > self.maxShootZ):
                self.currentState=self.RELOCATING

            self.shootCooldownElapsed = pygame.time.get_ticks() - self.shootCooldownT0
            if(self.shootCooldownElapsed >= self.SHOOTCOOLDOWN):
                #meleeAttackPlayerRandomly(player, rangedBody, leftBound, rightBound)
                rangedBody.shoot()
                self.shootCooldownElapsed = 0
                self.shootCooldownT0 = pygame.time.get_ticks()

        
