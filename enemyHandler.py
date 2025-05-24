import pygame
from meleeEnemy import *
from rangedEnemy import *
import random
import copy

class EnemySpawnBatch:
    # 'enemyIndexes' -> Contains the indexes of the enemies
    # spawned in this batch
    # 'spawnSides' -> Parallel to 'enemyIndexes', each item tells 
    # if the enemy spawns on the left (-1) or on the right (1) 
    def __init__(self, enemyIndexes, spawnSides):
        self.enemyIndexes=enemyIndexes
        self.spawnSides=spawnSides

class EnemyHandler:

    MELEE_TIER1 = 0
    MELEE_TIER2 = 1
    MELEE_TIER3 = 2
    MELEE_TIER4 = 3

    RANGED_TIER1 = 4
    RANGED_TIER2 = 5
    RANGED_TIER3 = 6
    RANGED_TIER4 = 7

    FINAL_BOSS = 8

    # 'enemyIndexes' -> Contains the indexes of the enemies
    # that can be spawned by this spawner
    # 'spawnBatches' -> Contains the batches that will
    # be spawned used, in order
    def __init__(self, screenRef, spawnBatches):
        self.screenRef = screenRef
        #self.enemyIndexes = enemyIndexes
        self.spawnBatches = spawnBatches
        self.spawnedEnemyCount = 0
        self.currentBatchID = 0
        self.noMoreBatches = False

        # STATS FORMAT:
        self.enemyStats = [
            # Melee stats:
            #[hp, sp, dp, moveSpeed, blockMulti] 
            [80, 80, 10, 1.0, None],
            [100, 100, 20, 1.0, None],
            [150, 100, 20, 1.1, None],
            [200, 100, 25, 1.2, 0.65],
            
            # Ranged stats:
            # [hp, sp, dp, moveSpeed, meleeSwing]
            [60, 80, 20, 0.9, None],
            [90, 100, 25, 0.9, None],
            [110, 100, 30, 1.0, None],
            [150, 100, 40, 1.1, 10]
        ]

        self.enemies = [
            [], # Tier 1 melee
            [], # Tier 2 melee
            [], # Tier 3 melee
            [], # Tier 4 melee

            [], # Tier 1 ranged
            [], # Tier 2 ranged 
            [], # Tier 3 ranged
            []  # Tier 4 ranged 
        ]

    # Returns the enemy instances in this batch 
    def spawnNextBatch(self, minX, maxX, minY, maxY):
        
        print("Spawning next batch")

        if(self.currentBatchID == len(self.spawnBatches)):
            self.noMoreBatches=True
            return

        currentBatch = self.spawnBatches[self.currentBatchID]
        i = 0
        for eTypeID in currentBatch.enemyIndexes:
            
            # Deep copy the stats
            newEnemyStats = []
            for s in self.enemyStats[eTypeID]:
                newEnemyStats.append(copy.deepcopy(s))                

            spawnSide = currentBatch.spawnSides[i] 
            i+=1
            
            xPos = maxX if 1==spawnSide else minX
            yPos = random.randint(int(minY), int(maxY))

            hp = newEnemyStats[0] 
            sp = newEnemyStats[1]
            maxHp = newEnemyStats[0] 
            maxSp = newEnemyStats[1]
            tier = eTypeID if eTypeID <= self.MELEE_TIER4 else eTypeID-self.MELEE_TIER4
            
            if eTypeID <= self.MELEE_TIER4:
                self.enemies[eTypeID].append(
                    MeleeEnemy(
                        xPos,
                        yPos,
                        hp, 
                        sp,
                        maxHp,
                        maxSp,
                        tier
                    )
                )
            elif eTypeID >= self.RANGED_TIER1:
                self.enemies[eTypeID].append(
                    RangedEnemy(
                        xPos,
                        yPos,
                        hp,
                        sp,
                        maxHp,
                        maxSp,
                        tier
                    )
                )
            self.spawnedEnemyCount += 1

        # Update batch ID
        if(self.currentBatchID < len(self.spawnBatches)):
            self.currentBatchID+=1

    # Get the array for an specific enemy type
    def getEnemyArray(self, enemyType):
        if(enemyType < self.MELEE_TIER1
        or enemyType > self.RANGED_TIER4):
            return []
        else:
            return self.enemies[enemyType]

    def getAllEnemyArraysConcat(self):
        concatEnemies = []
        for eArr in self.enemies:
            concatEnemies += eArr
        return concatEnemies

    def getAllMeleeEnemies(self):
        meleeEnemies = []
        for i in range(self.MELEE_TIER1, self.MELEE_TIER4+1):
            meleeEnemies+=self.enemies[i]
        return meleeEnemies

    def getAllRangedEnemies(self):
        rangedEnemies = []
        for i in range(self.RANGED_TIER1, self.RANGED_TIER4+1):
            rangedEnemies+=self.enemies[i]
        return rangedEnemies

    def applyFunctionToEnemyArray(self, enemyType, function):
        targetArr = self.getEnemyArray(enemyType)
        if [] != targetArr:
            function(targetArr)

    def countAliveEnemies(self):
        nAlive = 0
        for eArr in self.enemies:
            for e in eArr:
                if(e.currentActionState!=ActionState.DYING):
                    nAlive+=1
        return nAlive
    
    def countDeadEnemies(self):
        nDead = 0
        for eArr in self.enemies:
            for e in eArr:
                if(e.currentActionState==ActionState.DYING):
                    nDead+=1
        return nDead

    def removeDeadEnemies(self):
        for i in range(0, len(self.enemies)):
            newArr = []
            for e in self.enemies[i]:
                if not (
                    # Dying:
                    e.currentActionState == ActionState.DYING
                    # Animation on the last frame:
                    and (e.animations[e.currentAnimationID].currentFrame 
                    == e.animations[e.currentAnimationID].nFrames-1)
                ):
                    newArr.append(e)
            self.enemies[i]=newArr # Replace array

    def getCurrentNOfenemies(self):
        lenCount = 0
        for i in self.enemies:
            lenCount+=len(i)
        return lenCount
