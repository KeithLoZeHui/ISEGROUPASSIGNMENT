import pygame
from meleeEnemy import *
from rangedEnemy import *

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
    def __init__(self, screenRef, enemyIndexes, spawnBatches):
        self.screenRef = screenRef
        self.enemyIndexes = enemyIndexes
        self.spawnBatches = spawnBatches
        self.spawnedEnemyCount = 0
        self.currentBatchID = 0

        self.enemyStats = [
            # Melee stats:
            [],
            [],
            [],
            [],
            
            # Ranged stats:
            [],
            [],
            [],
            []
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

        '''
        self.meleeEnemies_tier1 = []
        self.meleeEnemies_tier2 = []
        self.meleeEnemies_tier3 = []
        self.meleeEnemies_tier4 = []

        self.rangedEnemies_tier1 = []
        self.rangedEnemies_tier2 = []
        self.rangedEnemies_tier3 = []
        self.rangedEnemies_tier4 = []
        '''

    # Returns the enemy instances in this batch 
    def spawnNextBatch(self):
        
        if(self.currentBatchID > len(self.spawnBatches)):
            return

        currentBatch = self.spawnBatches[self.currentBatchID]
        for eTypeID in currentBatch:
            
            newEnemyStats = []
            # Deep copy the stats
            for s in self.enemyStats[eTypeID]:
                newEnemyStats.append(s)                

            self.enemies[eTypeID].append(

            )

            '''
            if(self.MELEE_TIER1==e):
                pass
            if(self.MELEE_TIER2==e):
                pass
            if(self.MELEE_TIER3==e):
                pass
            if(self.MELEE_TIER4==e):
                pass

            if(self.RANGED_TIER1==e):
                pass
            if(self.RANGED_TIER2==e):
                pass
            if(self.RANGED_TIER3==e):
                pass
            if(self.RANGED_TIER4==e):
                pass
            '''

