from entityConstants import *
from fighter import *
import copy

class Splatter:
    def __init__(self, xPos, yPos, animation, fighter):
        self.xPos = xPos
        self.yPos = yPos

        # Doesn't really need a hitbox, but the entity renderer needs 
        # this for the 2.5 rendering
        self.hitbox = AABB(xPos, yPos, SPLATTER_ANIM_DIMS[0], SPLATTER_ANIM_DIMS[1])
        self.hitbox.pseudoZ = fighter.hitbox.y + fighter.hitbox.h # Pseudo z correction


        self.animation = copy.deepcopy(animation)
        
class SplatterSystem:

    def __init__(self):
        self.splatterAnimation = Animation(0,0)
        self.splatterArr = []

    def __init__(self, splatterAnimation):
        self.splatterAnimation = copy.deepcopy(splatterAnimation)
        self.splatterArr = []

    def update(self):
        newSplatters = []
        for s in self.splatterArr:
            if(s.animation.currentFrame != s.animation.nFrames-1):
                newSplatters.append(s)
            s.animation.update()
        self.splatterArr = newSplatters

    def generateSplatter(self, xPos, yPos, fighter):
        self.splatterArr.append(Splatter(xPos, yPos, copy.deepcopy(self.splatterAnimation), fighter))
