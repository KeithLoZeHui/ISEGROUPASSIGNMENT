from entityConstants import *
from fighter import *
import copy

class Arrow:
    def __init__(self, x, y, direction, damage):
        self.hitbox = AABB(x, y, ARROW_DIMENSIONS[0], ARROW_DIMENSIONS[1])
        self.direction = direction
        self.damage = damage

class ArrowSystem:

    MAX_ARROWS = 10
    MAX_VULNERABLE_ENTITIES = 10
    DEF_ARROW_SPEED = 10

    def __init__(self):
        #self.nArrows = 0
        #self.nVentities = 0
        self.arrows = []
        self.vulnerableEntities = []

    def update(self, leftXbound, rightXbound):
        if self.arrows == []: return
        
        #arrCounter = 0
        for a in self.arrows:

            # Check collisions (naive algorithm, but still works)
            for e in self.vulnerableEntities:
                if(a.hitbox.overlaps(e.hitbox)):
                    
                    # Deflection logic
                    if(e.currentActionState == ActionState.BLOCKING
                    and 0==e.animations[e.currentAnimationID].currentFrame):
                        a.direction = -a.direction
                        print("Arrow deflected!")
                    else: # Damage logic
                        e.hurt(a.damage)
                        a.direction = 0
                        print("Arrow hit!")

            # Check if out of bounds
            if(a.hitbox.x+a.hitbox.w <= leftXbound
            or a.hitbox.x >= rightXbound):
                # Set arrow direction to 0 to eliminate it 
                a.direction = 0

            # Update position
            if(0 != a.direction):
                a.hitbox.x += self.DEF_ARROW_SPEED*a.direction
            
            #arrCounter += 1

        # Delete 0 direction arrows
        oldArrows = [a for a in self.arrows]
        self.arrows = []
        for i in range(0, len(oldArrows)):
            if(oldArrows[i].direction != 0):
                self.arrows.append(oldArrows[i])

    def addArrow(self, newArrow):

        if(len(self.arrows) < self.MAX_ARROWS):
            self.arrows.append(newArrow)
            #self.nArrows+=1

    def addVulnerableEntity(self, entity):
        if(len(self.vulnerableEntities) < self.MAX_VULNERABLE_ENTITIES):
            self.vulnerableEntities.append(entity)
            print("Added vulnerable entity")
        