from fighter import *
from entityConstants import *

class MeleeEnemy(Fighter):
    
    RATTACK1ANIM_ID = 11+1 # Right attack 1
    LATTACK1ANIM_ID = RATTACK1ANIM_ID+1 # Left attack 1
    RATTACK2ANIM_ID = LATTACK1ANIM_ID+1 # Right attack 2
    LATTACK2ANIM_ID = RATTACK2ANIM_ID+1 # Left attack 2
    RATTACK3ANIM_ID = LATTACK2ANIM_ID+1 # Right attack 3 
    LATTACK3ANIM_ID = RATTACK3ANIM_ID+1 # Left attack 3

    def __init__(self, xPos, yPos, hp, sp, maxHp, maxSp):
        super().__init__(xPos, yPos, hp, sp, maxHp, maxSp)
        self.hitbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.renderbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.tier = 0

    def __init__(self, xPos, yPos, hp, sp, maxHp, maxSp, tier):
        super().__init__(xPos, yPos, hp, sp, maxHp, maxSp)
        self.hitbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.renderbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.tier = tier
