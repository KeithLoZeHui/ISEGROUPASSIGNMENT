from fighter import *
from arrowSystem import *

class RangedEnemy(Fighter):

    RATTACK1ANIM_ID = 11+1 # Right attack 1
    LATTACK1ANIM_ID = RATTACK1ANIM_ID+1 # Left attack 1
    RATTACK2ANIM_ID = LATTACK1ANIM_ID+1 # Right attack 2
    LATTACK2ANIM_ID = RATTACK2ANIM_ID+1 # Left attack 2
    RATTACK3ANIM_ID = LATTACK2ANIM_ID+1 # Right attack 3 
    LATTACK3ANIM_ID = RATTACK3ANIM_ID+1 # Left attack 3

    RSHOOTCHARGEANIM_ID = LATTACK3ANIM_ID+1 
    LSHOOTCHARGEANIM_ID = RSHOOTCHARGEANIM_ID+1
    RSHOOTANIM_ID = LSHOOTCHARGEANIM_ID+1
    LSHOOTANIM_ID = RSHOOTANIM_ID+1
    RARROW_ID = LSHOOTANIM_ID+1
    LARROW_ID = RARROW_ID+1

    ATTACK2_COOLDOWN = 1000/4
    ATTACK3_COOLDOWN = 300 #1000/2

    CHARGEDELAY = 1000
    POSTSHOOTDELAY = 500
    SHOOT_COOLDOWN = 1000

    SP_RECOVERY_PERUPDATE = 0.5

    # CHANGE THIS!!
    ATTACK2_SPDRAIN = 15
    ATTACK3_SPDRAIN = 35

    # CHANGE THIS!!
    ATTACK1_DP = 15
    ATTACK2_DP = 25
    ATTACK3_DP = 55

    DEF_ARROW_DP = 10

    # CHANGE THIS !!
    ATTACK1_KNOCKBACK = 10
    ATTACK2_KNOCKBACK = 20
    ATTACK3_KNOCKBACK = 60

    def __init__(self, xPos, yPos, hp, sp, maxHp, maxSp):
        super().__init__(xPos, yPos, hp, sp, maxHp, maxSp)
        self.setHitbox(AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1]))
        self.renderbox = AABB(xPos, yPos, ARCHER_ANIM_DIMS[0][0], ARCHER_ANIM_DIMS[0][1])

        self.currentActionState = ActionState.IDLE
        self.attackFinished = False
        self.attackCoolingDown = False
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0 #pygame.time.get_ticks()
        self.lastAttack=0
        self.alreadyShot = False

    def __init__(self, xPos, yPos, hp, sp, maxHp, maxSp, tier):
        super().__init__(xPos, yPos, hp, sp, maxHp, maxSp)
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

    def update(self, lowerYBound, upperYBound, leftBound, rightBound, arrowSystem):
        
        if(self.attackCoolingDown):
            self.attackCooldownElapsed = (pygame.time.get_ticks() 
            - self.attackCooldownT0)

            if(2==self.lastAttack):
                if(self.attackCooldownElapsed >= self.ATTACK2_COOLDOWN):
                    self.attackCoolingDown = False
                    self.attackCooldownElapsed = 0
            elif(3==self.lastAttack):
                if(self.attackCooldownElapsed >= self.ATTACK3_COOLDOWN):
                    self.attackCoolingDown = False
                    self.attackCooldownElapsed = 0
            elif(4==self.lastAttack):
                if(self.attackCooldownElapsed >= self.CHARGEDELAY):
                    self.attackCoolingDown = False
                    self.attackCooldownElapsed = 0
                    self.lastAttack=5 # 5 is for shooting
                # Return to avoid other events modifying the action state
                else: return    
            elif(5==self.lastAttack):
                if(self.attackCooldownElapsed >= self.POSTSHOOTDELAY):
                    self.attackCoolingDown = False
                    self.attackCooldownElapsed = 0
                else: return

        super().update(lowerYBound, upperYBound, leftBound, rightBound)

        # Update stamina recovery
        if(self.currentActionState == ActionState.IDLE
           or self.currentActionState == ActionState.MOVING and not self.isRunning):
            if(self.sp < self.maxSp):
                self.sp += self.SP_RECOVERY_PERUPDATE
            else:
                # Force this to avoid SP to be bigger
                # than its maximum value
                self.sp = self.maxSp        


        if(self.currentActionState==ActionState.ATTACKING1):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LATTACK1ANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RATTACK1ANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            # If last frame passed, go back to idle state
            if(self.attackFinished):
                self.currentActionState = ActionState.IDLE
                self.attackbox = AABB(0,0,0,0)
            else:
                self.animations[self.currentAnimationID].update()

        if(self.currentActionState==ActionState.ATTACKING2):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LATTACK2ANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RATTACK2ANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            # If last frame passed, go back to idle state
            if(self.attackFinished):
                self.currentActionState = ActionState.IDLE
                self.attackCoolingDown = True
                self.attackbox = AABB(0,0,0,0)
                self.attackCooldownT0 = pygame.time.get_ticks() 
                self.attackFinished=False
            else:
                self.animations[self.currentAnimationID].update()

        if(self.currentActionState==ActionState.ATTACKING3):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LATTACK3ANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RATTACK3ANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            # If last frame passed, go back to idle state
            if(self.attackFinished):
                self.currentActionState = ActionState.IDLE
                self.attackCoolingDown = True
                self.attackbox = AABB(0,0,0,0)
                self.attackCooldownT0 = pygame.time.get_ticks() 
                self.attackFinished=False
            else:
                self.animations[self.currentAnimationID].update()

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
                    arrowXOffset = -ARROW_DIMENSIONS[0]
                elif(self.lastDirection == Direction.EAST):
                    arrowDirection=1
                    arrowXOffset = ARROW_DIMENSIONS[0]

                arrow = Arrow(self.hitbox.x+arrowXOffset, self.hitbox.y+ARROW_RENDER_YCORRECTION, 
                              arrowDirection, self.DEF_ARROW_DP)
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

    # SP drain: 0
    # DP dealt: 15 
    def attack1(self, enemies : list, leftBound, rightBound):
        if(self.attackCoolingDown): return

        self.lastAttack=1

        # Generate attack box        
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)

        # Check attack collision (naive, but still ok)
        for e in enemies:
            if(self.attackbox.overlaps(e.hitbox)
            and e.currentActionState != ActionState.DYING):
                # Apply damage
                e.hurt(self.ATTACK1_DP)

                # Apply knockback
                if(self.lastDirection == Direction.WEST):
                    e.forceXTranslate(-self.ATTACK1_KNOCKBACK, leftBound, rightBound)
                elif(self.lastDirection == Direction.EAST):
                    e.forceXTranslate(self.ATTACK1_KNOCKBACK, leftBound, rightBound)

        self.currentActionState = ActionState.ATTACKING1
        
        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK1ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK1ANIM_ID

        self.animations[self.currentAnimationID].reset()

    # SP drain: 15
    # DP dealt: 25
    def attack2(self, enemies : list, leftBound, rightBound):
        if(self.attackCoolingDown): return
        
        # Check and substract stamina
        if(self.sp < self.ATTACK2_SPDRAIN):
            return

        self.sp -= self.ATTACK2_SPDRAIN 

        self.lastAttack=2

        # Generate attack box
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)

        # Check attack collision (naive, but still ok)
        for e in enemies:
            if(self.attackbox.overlaps(e.hitbox)
            and e.currentActionState != ActionState.DYING):
                # Apply damage
                e.hurt(self.ATTACK2_DP)

                # Apply knockback
                if(self.lastDirection == Direction.WEST):
                    e.forceXTranslate(-self.ATTACK2_KNOCKBACK, leftBound, rightBound)
                elif(self.lastDirection == Direction.EAST):
                    e.forceXTranslate(self.ATTACK2_KNOCKBACK, leftBound, rightBound)

        self.currentActionState = ActionState.ATTACKING2

        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK2ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK2ANIM_ID

        self.animations[self.currentAnimationID].reset()

    # SP drain: 35
    # DP dealt: 55
    def attack3(self, enemies : list, leftBound, rightBound):
        if(self.attackCoolingDown): return

        # Check and substract stamina
        if(self.sp < self.ATTACK3_SPDRAIN):
            return

        self.sp -= self.ATTACK3_SPDRAIN 

        self.lastAttack=3

        # Generate attack box        
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)

        # Check attack collision (naive, but still ok)
        for e in enemies:
            if(self.attackbox.overlaps(e.hitbox)
            and e.currentActionState != ActionState.DYING):
                # Apply damage
                e.hurt(self.ATTACK3_DP)

                # Apply knockback
                if(self.lastDirection == Direction.WEST):
                    e.forceXTranslate(-self.ATTACK3_KNOCKBACK, leftBound, rightBound)
                elif(self.lastDirection == Direction.EAST):
                    e.forceXTranslate(self.ATTACK3_KNOCKBACK, leftBound, rightBound)

        self.currentActionState = ActionState.ATTACKING3

        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK3ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK3ANIM_ID

        self.animations[self.currentAnimationID].reset()


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
