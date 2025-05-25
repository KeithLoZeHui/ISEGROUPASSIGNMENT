from fighter import *
from entityConstants import *

class MeleeEnemy(Fighter):

    def __init__(self, xPos, yPos, hp, sp, dpMulti, blockMulti,  maxHp, maxSp):
        super().__init__(xPos, yPos, hp, sp, dpMulti, blockMulti,  maxHp, maxSp)
        self.hitbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.renderbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.tier = 0

    def __init__(self, xPos, yPos, hp, sp, dpMulti, blockMulti, maxHp, maxSp, tier):
        super().__init__(xPos, yPos, hp, sp, dpMulti, blockMulti, maxHp, maxSp)
        self.hitbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.renderbox = AABB(xPos, yPos, SAMURAI_ANIM_DIMS[1][0], SAMURAI_ANIM_DIMS[1][1])
        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.tier = tier
    
    def update(self, lowerYBound, upperYBound, leftBound, rightBound, splatterSystem):

        super().update(lowerYBound, upperYBound, leftBound, rightBound, splatterSystem)

    # Override to no behaviour
    # (Melee Enemies shouldn't block)
    def block(self):
        pass
