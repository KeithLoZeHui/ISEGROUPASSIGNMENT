from utilsAI import *

class BossAI:

    DEFAULT_CHASEW_MIN = 120
    DEFAULT_CHASEW_MAX = 150
    DEFAULT_CHASEZ_MAX = AABB.PSEUDOZ_OVERLAP_MARGIN

    CHASING = 0
    ATTACKING = 1

    ATTACKCOOLDOWN = 1000

    DEFAULT_SHOOTW_MIN = 120*4
    DEFAULT_SHOOTW_MAX = 120*5
    DEFAULT_SHOOTZ_MAX = AABB.PSEUDOZ_OVERLAP_MARGIN

    RELOCATING = 0
    SHOOTING = 1

    SHOOTCOOLDOWN = 1000

    def __init__(self, minChaseW, maxChaseW, maxChaseZ,
                 minShootW, maxShootW, maxShootZ):
        self.currentState = self.CHASING
        self.minChaseW = minChaseW
        self.maxChaseW = maxChaseW
        self.maxChaseZ = maxChaseZ
        self.attackCooldownT0 = pygame.time.get_ticks()
        self.attackCooldownElapsed = 0
        self.minShootW = minShootW
        self.maxShootW = maxShootW
        self.maxShootZ = maxShootZ
        self.shootCooldownT0 = pygame.time.get_ticks()
        self.shootCooldownElapsed = 0
