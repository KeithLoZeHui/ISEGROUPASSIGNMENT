from fighter import *
from entityConstants import *

class Riku(Fighter):

    def __init__(self, xPos, yPos, hp, sp, dpMulti, blockMulti, maxHp, maxSp):
        super().__init__(xPos, yPos, hp, sp, dpMulti, blockMulti, maxHp, maxSp)
        self.setHitbox(AABB(xPos, yPos, CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1]))
        self.renderbox = AABB(xPos, yPos, CAPTAIN_ANIM_DIMS[1][0], CAPTAIN_ANIM_DIMS[1][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0

    def update(self, lowerYBound, upperYBound, leftBound, rightBound, splatterSystem):
        super().update(lowerYBound, upperYBound, leftBound, rightBound, splatterSystem)

