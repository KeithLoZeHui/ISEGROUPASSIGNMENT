from enum import Enum
from animation import Animation
import pygame
import sys
import os

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

    def __init__(self, xPos, yPos, hp, sp, maxHp, maxSp):
        #self.xPos = xPos
        #self.yPos = yPos
        
        self.xVelocity = 0
        self.yVelocity = 0
        self.lastDirection = Direction.EAST
        self.hp=hp
        self.sp=sp
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

        self.hitbox = AABB(xPos, yPos, 0, 0)
        self.renderbox = AABB(xPos, yPos, 0, 0)
        self.attackbox = AABB(xPos, yPos, 0, 0)

    def addAnimation(self, animation):
        self.animations.append(Animation(animation.milisPerFrames, animation.nFrames))

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
    def update(self, lowerYBound, upperYBound, leftBound, rightBound):
        
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
            if(
                (self.hitbox.x + self.xVelocity >= leftBound)
                and (self.hitbox.x + self.xVelocity <= rightBound - self.hitbox.w) 
            ):
                self.renderbox.x += self.xVelocity
                self.hitbox.x += self.xVelocity

            #scaledHeight = self.hitbox.h*scaleFactor;

            # Update y position
            if(
                (self.hitbox.y + self.yVelocity >= (upperYBound-self.hitbox.h))
                and (self.hitbox.y + self.yVelocity <= lowerYBound-self.hitbox.h)
            ):
                self.renderbox.y += self.yVelocity
                self.hitbox.y += self.yVelocity
                self.hitbox.pseudoZ += self.yVelocity

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

    def hurt(self, damage):
        self.currentActionState = ActionState.HURTING

        if damage < self.hp:
            self.hp -= damage
        else:
            self.currentActionState = ActionState.DYING

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
    
    # Abstract function, leave this here
    # for it to be implemented by RangedEnemy
    def shoot(self):
        pass