from enum import Enum
from animation import Animation
from entityConstants import *

import pygame
import sys
import os
import copy

# Action states
class ActionState(Enum):
    IDLE = 0
    MOVING = 1
    JUMPING = 2 # (?)
    #ACST_ATTACKING = 3
    BLOCKING = 4
    HURTING = 5
    DYING = 6
    ATTACKING1 = 7
    ATTACKING2 = 8
    ATTACKING3 = 9
    CHARGESHOOT = 10
    SHOOT = 11

class Direction(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    NONE = 8

gravity = 1

# Axis Aligned Bounding Box (AABB)
class AABB:

    PSEUDOZ_OVERLAP_MARGIN = 10

    def __init__(self, x, y, w, h):
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        
        # Represents the depth position,
        # in a pseudo 3d environment,
        # at the 'feet' level
        self.pseudoZ = y+h

    def overlaps(self, other) -> bool:
        selfMinX = self.x
        selfMaxX = self.x+self.w
        selfMinY = self.y
        selfMaxY = self.y+self.h
        
        otherMinX = other.x
        otherMaxX = other.x+other.w
        otherMinY = other.y
        otherMaxY = other.y+other.h

        return (
            # X overlap
            (selfMinX <= otherMaxX and
            selfMaxX >= otherMinX) 
            and
            # Y overlap
            (selfMinY <= otherMaxY and
            selfMaxY >= otherMinY)
            and
            (abs(self.pseudoZ-other.pseudoZ) <= self.PSEUDOZ_OVERLAP_MARGIN) 
        )

class Fighter:

    DEFAULT_WALK_SPEED = 2
    DEFAULT_RUN_SPEED = 2
    DEFAULT_JUMP_SPEED = 3
    DEFAULT_SP_RECOVERY = 0.8

    DEFAULT_RIDLEANIM_ID = 0  # Idle right
    DEFAULT_LIDLEANIM_ID = 1  # Idle left
    DEFAULT_RWALKANIM_ID = 2 # Right walk
    DEFAULT_LWALKANIM_ID = 3 # Left walk
    DEFAULT_RRUNANIM_ID = 4 # Right run
    DEFAULT_LRUNANIM_ID = 5 # Left run
    DEFAULT_RBLOCKANIM_ID = 6 # Right block
    DEFAULT_LBLOCKANIM_ID = 7 # Left block
    DEFAULT_RHURTANIM_ID = 8 # Right hurt
    DEFAULT_LHURTANIM_ID = 9 # Left hurt
    DEFAULT_RDEATHANIM_ID = 10 # Right death
    DEFAULT_LDEATHANIM_ID = 11 # Left death

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

    ATTACK2_SPDRAIN = 15
    ATTACK3_SPDRAIN = 35

    ATTACK1_DP = 15
    ATTACK2_DP = 25
    ATTACK3_DP = 55

    DEF_ARROW_DP = 30

    ATTACK1_KNOCKBACK = 10
    ATTACK2_KNOCKBACK = 20
    ATTACK3_KNOCKBACK = 60

    ATTACK1_HITFRAME = 2
    ATTACK2_HITFRAME = 3
    ATTACK3_HITFRAME = 2
    
    def __init__(self, xPos, yPos, hp, sp, dpMulti, blockMulti, maxHp, maxSp):
        #self.xPos = xPos
        #self.yPos = yPos
        
        self.xVelocity = 0
        self.yVelocity = 0
        self.lastDirection = Direction.EAST
        self.hp=hp
        self.sp=sp
        self.dpMulti = dpMulti
        self.blockMulti = blockMulti
        self.maxHp=maxHp
        self.maxSp=maxSp
        self.walkSpeed = Fighter.DEFAULT_WALK_SPEED
        self.runSpeed = Fighter.DEFAULT_RUN_SPEED
        self.currentActionState = ActionState.IDLE

        self.currentAnimationID = 0
        #self.currentFrameID = 0
        self.animations = []

        self.isRunning = False
        self.isExhausted = False

        self.enemies = []

        self.hitbox = AABB(xPos, yPos, 0, 0)
        self.renderbox = AABB(xPos, yPos, 0, 0)
        self.attackbox = AABB(xPos, yPos, 0, 0)

    def addAnimation(self, animation):
        self.animations.append(
            Animation(
                copy.deepcopy(animation.milisPerFrames), 
                copy.deepcopy(animation.nFrames)
                )
            )

    def setAnimationAt(self, animation, animationID):
        self.animations[animationID] = animation

    def setHitbox(self, hb : AABB):
        self.hitbox = hb

    def attack(self, attackID):
        self.currentActionState = ActionState.ACST_ATTACKING

    def block(self):
        self.currentActionState = ActionState.BLOCKING
        if(Direction.WEST == self.lastDirection):       
            self.currentAnimationID = self.DEFAULT_LBLOCKANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.DEFAULT_RBLOCKANIM_ID
        self.animations[self.currentAnimationID].reset()        
    
    def forceActionState(self, actionState : ActionState):
        self.currentActionState = actionState

    def forceXTranslate(self, xtranslate, leftBound, rightBound):
        # Update x position
        if(
            (self.hitbox.x + self.xVelocity >= leftBound)
            and (self.hitbox.x + self.xVelocity <= rightBound - self.hitbox.w) 
        ):
            self.renderbox.x += xtranslate
            self.hitbox.x += xtranslate

    def forceYTranslate(self, ytranslate, lowerYBound, upperYBound):
        # Update y position
        if(
            (self.hitbox.y + self.yVelocity >= (upperYBound-self.hitbox.h))
            and (self.hitbox.y + self.yVelocity <= lowerYBound-self.hitbox.h)
        ):
            self.renderbox.y += ytranslate
            self.hitbox.y += ytranslate
            self.hitbox.pseudoZ += ytranslate

    # direction: 1 for right, -1 for left
    def setXMove(self, direction : int):
        # Return if values are invalid
        if(1!=direction and -1!=direction and 0!=direction):
            return

        if(self.isRunning):
            if -1==direction:
                self.currentAnimationID = self.DEFAULT_LRUNANIM_ID 
            elif 1==direction:
                self.DEFAULT_RRUNANIM_ID
        else:
            if -1==direction:
                self.currentAnimationID = self.DEFAULT_LWALKANIM_ID 
            elif 1==direction:
                self.DEFAULT_RWALKANIM_ID 
        
        if(-1==direction):
            self.lastDirection = Direction.WEST
        elif(1==direction):
            self.lastDirection = Direction.EAST
        else:
            self.lastDirection = self.lastDirection

        #self.lastDirection = Direction.WEST if -1==direction else Direction.EAST

        if self.isRunning:
            self.xVelocity = direction*(self.runSpeed) 
        else:
            self.xVelocity = direction*(self.walkSpeed)
        
        if(0!=direction):
            self.currentActionState = ActionState.MOVING

        #else:
        #    self.xVelocity=0
        #    self.currentActionState = ActionState.ACST_IDLE

    # direction: 1 for south, -1 for north
    def setYMove(self, direction):
        # Return if values are invalid
        if(1!=direction and -1!=direction and 0!=direction):
            return

        #self.currentAnimationID = self.DEFAULT_LWALKANIM_ID if -1==direction else self.DEFAULT_RWALKANIM_ID 
        #self.lastDirection = Direction.WEST if -1==direction else Direction.EAST        

        if self.isRunning:
            self.yVelocity = direction*(self.runSpeed) 
        else:
            self.yVelocity = direction*(self.walkSpeed)
        
        if(0!=direction):
            self.currentActionState = ActionState.MOVING
        #else:
        #    self.yVelocity=0
        #    self.currentActionState = ActionState.ACST_IDLE

    # lowerBound, upperBound -> vertical movement bounds
    # leftBound, rightBound -> horizontal movement bounds
    def update(self, lowerYBound, upperYBound, leftBound, rightBound, splatterSystem):

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

        # Update stamina recovery
        if(self.currentActionState == ActionState.IDLE
           or self.currentActionState == ActionState.MOVING and not self.isRunning):
            if(self.sp < self.maxSp):
                self.sp += self.SP_RECOVERY_PERUPDATE
            else:
                # Force this to avoid SP to be bigger
                # than its maximum value
                self.sp = self.maxSp        

        # Idle logic
        if(self.currentActionState==ActionState.IDLE):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_LIDLEANIM_ID 
                self.animations[self.DEFAULT_LIDLEANIM_ID].update()
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_RIDLEANIM_ID
                self.animations[self.DEFAULT_RIDLEANIM_ID].update()
        
        # Moving logic
        if(self.currentActionState==ActionState.MOVING):

            if(Direction.WEST == self.lastDirection):
                if(not self.isRunning):
                    self.currentAnimationID = self.DEFAULT_LWALKANIM_ID 
                else:
                    self.currentAnimationID = self.DEFAULT_LRUNANIM_ID
                #self.animations[self.DEFAULT_LWALKANIM_ID].update()
            elif(Direction.EAST == self.lastDirection):
                if(not self.isRunning):
                    self.currentAnimationID = self.DEFAULT_RWALKANIM_ID
                else:
                    self.currentAnimationID = self.DEFAULT_RRUNANIM_ID
                #self.animations[self.DEFAULT_RWALKANIM_ID].update()

            self.animations[self.currentAnimationID].update()

            # Update x position
            nextX = self.hitbox.x + self.xVelocity
            if(
                (nextX > leftBound)
                and (nextX < rightBound - self.hitbox.w) 
            ):
                self.renderbox.x += self.xVelocity
                self.hitbox.x += self.xVelocity
            
            # Correct X collisions:
            if not (self.hitbox.x > leftBound):
                self.renderbox.x = leftBound
                self.hitbox.x = leftBound
            elif not (self.hitbox.x < rightBound - self.hitbox.w):
                self.renderbox.x = rightBound - self.hitbox.w
                self.hitbox.x = rightBound - self.hitbox.w

            # Update y position
            nextY = self.hitbox.y + self.yVelocity
            if(
                (nextY > (upperYBound-self.hitbox.h))
                and (nextY < lowerYBound-self.hitbox.h)
            ):
                self.renderbox.y += self.yVelocity
                self.hitbox.y += self.yVelocity
                self.hitbox.pseudoZ += self.yVelocity

            # Correct Y collisions
            if not (self.hitbox.y > (upperYBound-self.hitbox.h)):
                self.renderbox.y = (upperYBound-self.hitbox.h)
                self.hitbox.y = (upperYBound-self.hitbox.h)
            elif not (self.hitbox.y < lowerYBound-self.hitbox.h):
                self.renderbox.y = lowerYBound-self.hitbox.h
                self.hitbox.y = lowerYBound-self.hitbox.h

        # Blocking logic
        if(self.currentActionState==ActionState.BLOCKING):
            
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_LBLOCKANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_RBLOCKANIM_ID

            currentAnimation = self.animations[self.currentAnimationID]

            # If on the last frame, do not update
            if(not currentAnimation.currentFrame==currentAnimation.nFrames-1):            
                self.animations[self.currentAnimationID].update()

        # Hurting logic
        if(self.currentActionState==ActionState.HURTING):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_LHURTANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_RHURTANIM_ID

            currentHurtAnimation = self.animations[self.currentAnimationID] 

            currentHurtAnimation.update() 

            # Do this AFTER update()
            if(currentHurtAnimation.currentFrame == currentHurtAnimation.nFrames-1):
                self.currentActionState = ActionState.IDLE

        # Dying logic
        if(self.currentActionState==ActionState.DYING):

            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_LDEATHANIM_ID            

            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.DEFAULT_RDEATHANIM_ID
                #currentAnimation = self.animations[self.DEFAULT_RDEATHANIM_ID]

            currentAnimation = self.animations[self.currentAnimationID]
            # If on the last frame, do not update
            if(not currentAnimation.currentFrame==currentAnimation.nFrames-1):
                self.animations[self.currentAnimationID].update()
        
        if(self.currentActionState==ActionState.ATTACKING1):
            if(Direction.WEST == self.lastDirection):
                self.currentAnimationID = self.LATTACK1ANIM_ID
            elif(Direction.EAST == self.lastDirection):
                self.currentAnimationID = self.RATTACK1ANIM_ID
            
            currentAnimation = self.animations[self.currentAnimationID]

            collisionResult = self.checkAttackCollision(
                self.enemies, leftBound, rightBound, 
                self.ATTACK1_DP*self.dpMulti, # Make sure to implement the dpMulti
                self.ATTACK1_KNOCKBACK,
                self.ATTACK1_HITFRAME, splatterSystem)

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            #self.attackFinished = self.attackFinished or collisionResult 

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

            collisionResult = self.checkAttackCollision(
                self.enemies, leftBound, rightBound, 
                self.ATTACK2_DP*self.dpMulti, # Make sure to implement the dpMulti 
                self.ATTACK2_KNOCKBACK,
                self.ATTACK2_HITFRAME, splatterSystem)

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            #self.attackFinished = self.attackFinished or collisionResult 

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

            collisionResult = self.checkAttackCollision(
                self.enemies, leftBound, rightBound, 
                self.ATTACK3_DP*self.dpMulti, # Make sure to implement the dpMulti 
                self.ATTACK3_KNOCKBACK,
                self.ATTACK3_HITFRAME, splatterSystem)

            self.attackFinished = (
                currentAnimation.currentFrame == currentAnimation.nFrames-1
            ) 

            #self.attackFinished = self.attackFinished or collisionResult 

            # If last frame passed, go back to idle state
            if(self.attackFinished):
                self.currentActionState = ActionState.IDLE
                self.attackCoolingDown = True
                self.attackbox = AABB(0,0,0,0)
                self.attackCooldownT0 = pygame.time.get_ticks() 
                self.attackFinished=False
            else:
                self.animations[self.currentAnimationID].update()

        '''
        if(self.currentActionState==ActionState.ACST_JUMPING):
            
            if(self.yPos+self.hitbox.h >= floor):
                self.currentActionState = ActionState.ACST_IDLE

            # Update gravity acceleration
            self.yVelocity += gravity #GRAVITY
            print(f'velocity = {self.yVelocity}')
            
            # Update main position
            self.yPos += self.yVelocity

            # Upadate hitbox position
            self.hitbox.y += self.yVelocity
        '''
    
    def toggleRun(self):
        self.isRunning = not self.isRunning

    def jump(self):
        self.currentActionState = ActionState.JUMPING
        self.yVelocity = -self.DEFAULT_JUMP_SPEED

    def hurt(self, damage, splatterSystem):
        self.currentActionState = ActionState.HURTING

        if damage < self.hp:
            self.hp -= damage
        else:
            self.die()
            #self.currentActionState = ActionState.DYING
        # Generate splatter

        splatterSystem.generateSplatter(
            self.hitbox.x+(self.hitbox.w/2),
            self.hitbox.y+(self.hitbox.h/2)-(SPLATTER_ANIM_DIMS[1]/2),
            self
        )

        self.animations[self.currentAnimationID].reset()

    def die(self):
        self.currentActionState = ActionState.DYING
        if(Direction.WEST == self.lastDirection):       
            self.currentAnimationID = self.DEFAULT_LDEATHANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.DEFAULT_RDEATHANIM_ID
        self.animations[self.currentAnimationID].reset()

    def getCurrentAnimationID(self):
        return self.currentActionID
    
    def getCurrentAnimationFrame(self):
        return self.animations[self.currentAnimationID].getCurrentFrame()

    # Check attack collision (naive approach, but still ok)
    # 'hitFrame' -> the animation frame from where the 
    # # damage is applied in case of collision  
    def checkAttackCollision(self, enemies, 
                             leftBound, rightBound,
                             damage, knockback,
                             hitFrame, splatterSystem):
        
        selfCurrentAnimation = self.animations[self.currentAnimationID]
        for e in enemies:
            if(self.attackbox.overlaps(e.hitbox)
            and e.currentActionState != ActionState.DYING
            and selfCurrentAnimation.currentFrame == hitFrame
            # Avoid the extra damage within sub-fram time:
            and selfCurrentAnimation.previousFrame!=selfCurrentAnimation.currentFrame
            ):                
                # Apply damage

                # Check if the target is blocking
                if(ActionState.BLOCKING==e.currentActionState
                   
                   # Ensure the blockign and attacking directions 
                   # are opposite:
                   and (   
                        (self.lastDirection==Direction.EAST
                        and e.lastDirection==Direction.WEST) 
                        or
                        (self.lastDirection==Direction.WEST
                        and e.lastDirection==Direction.EAST)
                   )
                ):  
                    # Diminish the damage by the block multi
                    e.hurt(damage*e.blockMulti, splatterSystem)
                    print("Blocked multi applied")
                else:    
                    # Apply normal damage
                    e.hurt(damage, splatterSystem)
                    print("Normal damage")

                # Apply knockback
                if(self.lastDirection == Direction.WEST):
                    e.forceXTranslate(
                        -knockback,#-self.ATTACK1_KNOCKBACK, 
                        leftBound, 
                        rightBound)

                elif(self.lastDirection == Direction.EAST):
                    e.forceXTranslate(
                        knockback, #self.ATTACK1_KNOCKBACK, 
                        leftBound, 
                        rightBound)
                
                return True # If collided
        
        return False # If not collided

    # SP drain: 0
    # DP dealt: 15 
    def attack1(self, enemies : list, leftBound, rightBound):
        self.enemies = enemies
        
        if(self.attackCoolingDown): return

        self.lastAttack=1

        self.currentActionState = ActionState.ATTACKING1
        
        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK1ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK1ANIM_ID

        self.animations[self.currentAnimationID].reset()

        # Generate attack box        
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)

        '''
        self.checkAttackCollision(
            enemies, leftBound, rightBound, 
            self.ATTACK1_DP, self.ATTACK1_KNOCKBACK,
            self.ATTACK1_HITFRAME)
        '''

    # SP drain: 15
    # DP dealt: 25
    def attack2(self, enemies : list, leftBound, rightBound):
        self.enemies = enemies
        
        if(self.attackCoolingDown): return
        
        # Check and substract stamina
        if(self.sp < self.ATTACK2_SPDRAIN):
            return

        self.sp -= self.ATTACK2_SPDRAIN 

        self.lastAttack=2


        self.currentActionState = ActionState.ATTACKING2

        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK2ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK2ANIM_ID

        self.animations[self.currentAnimationID].reset()

        # Generate attack box
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)
        
        '''
        self.checkAttackCollision(
            enemies, leftBound, rightBound, 
            self.ATTACK2_DP, self.ATTACK2_KNOCKBACK,
            self.ATTACK2_HITFRAME)
        '''

    # SP drain: 35
    # DP dealt: 55
    def attack3(self, enemies : list, leftBound, rightBound):
        self.enemies = enemies

        if(self.attackCoolingDown): return

        # Check and substract stamina
        if(self.sp < self.ATTACK3_SPDRAIN):
            return

        self.sp -= self.ATTACK3_SPDRAIN 

        self.lastAttack=3

        self.currentActionState = ActionState.ATTACKING3

        if(Direction.WEST == self.lastDirection):
            self.currentAnimationID = self.LATTACK3ANIM_ID
        elif(Direction.EAST == self.lastDirection):
            self.currentAnimationID = self.RATTACK3ANIM_ID

        self.animations[self.currentAnimationID].reset()

        # Generate attack box        
        attackBoxW = self.hitbox.w/2
        attackBoxH = self.hitbox.h
        attackBoxX = (self.hitbox.x-attackBoxW
            if (self.lastDirection == Direction.WEST)
            else self.hitbox.x+self.hitbox.w)
        attackBoxY = self.hitbox.y
        
        self.attackbox = AABB(attackBoxX, attackBoxY, attackBoxW, attackBoxH)
        '''
        self.checkAttackCollision(
            enemies, leftBound, rightBound, 
            self.ATTACK3_DP, self.ATTACK3_KNOCKBACK,
            self.ATTACK3_HITFRAME)
        '''


    # Abstract function, leave this here
    # for it to be implemented by RangedEnemy
    def shoot(self):
        pass