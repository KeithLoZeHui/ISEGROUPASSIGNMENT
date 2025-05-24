from utilsAI import *

class MeleeEnemyAI:
    
    DEFAULT_CHASEW_MIN = 120
    DEFAULT_CHASEW_MAX = 150
    DEFAULT_CHASEZ_MAX = AABB.PSEUDOZ_OVERLAP_MARGIN

    CHASING = 0
    ATTACKING = 1

    ATTACKCOOLDOWN = 1000
    
    def __init__(self, minChaseW, maxChaseW, maxChaseZ):
        self.currentState = self.CHASING
        self.minChaseW = minChaseW
        self.maxChaseW = maxChaseW
        self.maxChaseZ = maxChaseZ
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0

    def update(self, meleeBody, player, leftBound, rightBound):

        # Avoid interruption of these actions
        if(
            meleeBody.currentActionState==ActionState.DYING
            or meleeBody.currentActionState==ActionState.HURTING
            or meleeBody.currentActionState==ActionState.ATTACKING1
            or meleeBody.currentActionState==ActionState.ATTACKING2
            or meleeBody.currentActionState==ActionState.ATTACKING3 
            or meleeBody.currentActionState==ActionState.CHARGESHOOT
            or meleeBody.currentActionState==ActionState.SHOOT       
        ):
            return

        if(ActionState.DYING==player.currentActionState):
            return
        
        if(self.CHASING == self.currentState):
            chaseResult = chasePlayer(player, meleeBody, self.minChaseW, self.maxChaseW, self.maxChaseZ)
    
            if(IDLEDURINGCHASE==chaseResult):
                self.currentState = self.ATTACKING

        elif(self.ATTACKING == self.currentState):

            dx = getDx(player, meleeBody)
            dz = getDz(player, meleeBody) 
            if (abs(dx) > self.maxChaseW 
                or abs(dx) < self.minChaseW
                or abs(dz) > self.maxChaseZ):
                self.currentState=self.CHASING

            self.attackCooldownElapsed = pygame.time.get_ticks() - self.attackCooldownT0
            if(self.attackCooldownElapsed >= self.ATTACKCOOLDOWN):
                meleeAttackPlayerRandomly(player, meleeBody, leftBound, rightBound)
                self.attackCooldownElapsed = 0
                self.attackCooldownT0 = pygame.time.get_ticks()
            