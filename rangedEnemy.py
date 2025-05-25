from fighter import *
from arrowSystem import *

class RangedEnemy(Fighter):

    def __init__(self, xPos, yPos, hp, sp, dpMulti, bockMulti, maxHp, maxSp):
        super().__init__(xPos, yPos, hp, sp, dpMulti, bockMulti, maxHp, maxSp)
        self.setHitbox(AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
        self.renderbox = AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.alreadyShot = False

    def __init__(self, xPos, yPos, hp, sp, dpMulti, bockMulti, maxHp, maxSp, tier):
        super().__init__(xPos, yPos, hp, sp, dpMulti, bockMulti, maxHp, maxSp)
        self.setHitbox(AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
        self.renderbox = AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.alreadyShot = False
        self.tier=tier

    def update(self, lowerYBound, upperYBound, leftBound, rightBound, arrowSystem, splatterSystem):

        super().update(lowerYBound, upperYBound, leftBound, rightBound, splatterSystem)

        if(self.currentActionState==ActionState.SHOOT):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LSHOOTANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RSHOOTANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            # Generate Arrow hitbox here 
            if(currentAnimation.currentFrame == 0
            and not self.alreadyShot):
                arrowDirection = 0
                arrowXOffset = 0
                if(self.lastDirection == Direction.WEST):
                    arrowDirection=-1
                    arrowXOffset = -(ARROW_DIMENSIONS[0] + self.hitbox.w)
                elif(self.lastDirection == Direction.EAST):
                    arrowDirection=1
                    arrowXOffset = ARROW_DIMENSIONS[0]

                arrow = Arrow(self.hitbox.x+arrowXOffset, self.hitbox.y+ARROW_RENDER_YCORRECTION, 
                              arrowDirection, self.DEF_ARROW_DP*self.dpMulti)
                arrow.hitbox.pseudoZ = self.hitbox.y+self.hitbox.h
                arrowSystem.addArrow(arrow)
                self.alreadyShot = True

            # If last frame passed, go to idle state
            if(self.attackFinished):
                self.currentActionState = ActionState.IDLE
                self.attackCoolingDown = True
                self.attackbox = AABB(0,0,0,0)
                self.attackCooldownT0 = pygame.time.get_ticks() 
                self.attackFinished=False
                self.alreadyShot = False
            else:
                self.animations[self.currentAnimationID].update()

        if(self.currentActionState==ActionState.CHARGESHOOT):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LSHOOTCHARGEANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RSHOOTCHARGEANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 
            
            # If last frame passed, go to shoot state
            if(self.attackFinished):
                self.currentActionState = ActionState.SHOOT
                self.attackCoolingDown = True
                self.attackbox = AABB(0,0,0,0)
                self.attackCooldownT0 = pygame.time.get_ticks() 
                self.attackFinished=False
            else:
                self.animations[self.currentAnimationID].update()


    # Override to no behaviour
    # (Archers can't block)
    def block(self):
        pass

    def shoot(self):
        if(self.attackCoolingDown): return

        self.lastAttack=4

        # Initialize by charging the shoot, not by shooting
        self.currentActionState = ActionState.CHARGESHOOT

        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LSHOOTCHARGEANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RSHOOTCHARGEANIM_ID

        self.animations[self.currentAnimationID].reset()

        # animID+2 because we want to also reset the actual shoot animation 
        self.animations[self.currentAnimationID+2].reset()
