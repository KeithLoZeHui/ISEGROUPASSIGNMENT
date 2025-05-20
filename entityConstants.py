
MINSCALEFACTOR = 2.5
MAXSCALEFACTOR = 3
scaleFactor = MINSCALEFACTOR

# Describes the time and number of 
# frames for each melee animation
MELEE_ANIMATIONS_SETUP = [
    (1000/5, 5), # idleLeftAnimation
    (1000/5, 5), # idleRightAnimation

    (1000/9, 9), # walkLeftAnimation
    (1000/9, 9), # walkRightAnimation

    (1000/8, 8), # runLeftAnimation
    (1000/8, 8), # runRightAnimation

    (100/2, 2), # blockLeftAnimation
    (100/2, 2), # blockRightAnimation 

    (100/2, 2), # hurtLeftAnimation
    (100/2, 2), # hurtRightAnimation

    (800/6, 6), # deadLeftAnimation
    (800/6, 6), # deadRightAnimation

    (400/4, 4), # attack1LeftAnimation
    (400/4, 4), # attack1RightAnimation 

    (400/5, 5), # attack2LeftAnimation
    (400/5, 5), # attack2RightAnimation

    (400/4, 4), # attack3LeftAnimation
    (400/4, 4)  # attack3RightAnimation
]

RANGED_ANIMATIONS_SETUP = [
    (1000/5, 9), # idleLeftAnimation
    (1000/5, 9), # idleRightAnimation

    (1000/9, 8), # walkLeftAnimation
    (1000/9, 8), # walkRightAnimation

    (1000/8, 8), # runLeftAnimation
    (1000/8, 8), # runRightAnimation

    (0, 0), # blockLeftAnimation
    (0, 0), # blockRightAnimation 

    (100/2, 3), # hurtLeftAnimation
    (100/2, 3), # hurtRightAnimation

    (800/6, 5), # deadLeftAnimation
    (800/6, 5), # deadRightAnimation

    (400/4, 5), # attack1LeftAnimation
    (400/4, 5), # attack1RightAnimation 

    (400/5, 5), # attack2LeftAnimation
    (400/5, 5), # attack2RightAnimation

    (400/4, 5), # attack3LeftAnimation
    (400/4, 5),  # attack3RightAnimation

    (1000/11, 11), # Shot charge left animation
    (1000/11, 11), # Shot charge right animation

    (500/3, 3), # Shot left animation
    (500/3, 3), # Shot right animation

    (1000, 1), # Arrow (not an animation)
    (1000, 1), # Arrow (not an animation)
]


############# CAPTAIN (RIKU/PLAYER) CONSTANTS #############

CAPTAIN_ANIM_DIMS_RAW = [
    [57, 93], # Idle
    [59, 94], # Walk
    [58, 88], # Run
    [55, 93], # Block
    [55, 93], # Hurt
    [88, 91], # Dead
    [100, 93], # Attack 1
    [100, 107], # Attack 2
    [96, 90] # Attack 3
]

CAPTAIN_ANIM_DIMS = [
    (d[0]*scaleFactor, d[1]*scaleFactor)
    for d in CAPTAIN_ANIM_DIMS_RAW
]

#print("SCALED DIMENSIONS:\n",CAPTAIN_ANIM_DIMS)

CAPTAIN_RENDER_CORRECTIONS = [
    # abs(Idle - animation[i])
    [
        abs(CAPTAIN_ANIM_DIMS[0][0] - CAPTAIN_ANIM_DIMS[i][0]),
        abs(CAPTAIN_ANIM_DIMS[0][1] - CAPTAIN_ANIM_DIMS[i][1])
    ]
    for i in range(0, len(CAPTAIN_ANIM_DIMS))
]

#print("RENDER CORRECTIONS:\n",CAPTAIN_RENDER_CORRECTIONS)

############# SAMURAI (MELEE DEFAULT) CONSTANTS #############

SAMURAI_ANIM_DIMS_RAW = [
    [58, 70], # Idle
    [59, 70], # Walk
    [56, 67], # Run
    [54, 70], # Block
    [57, 69], # Hurt
    [62, 67], # Dead
    [100, 67], # Attack 1
    [90, 105], # Attack 2
    [100, 71]  # Attack 3
]

SAMURAI_ANIM_DIMS = [
    (d[0]*scaleFactor, d[1]*scaleFactor) 
    for d in SAMURAI_ANIM_DIMS_RAW
]

SAMURAI_RENDER_CORRECTIONS = [
    # abs(Idle - animation[i]) 
    (
        abs(SAMURAI_ANIM_DIMS[0][0] - SAMURAI_ANIM_DIMS[i][0]),
        abs(SAMURAI_ANIM_DIMS[0][1] - SAMURAI_ANIM_DIMS[i][1])
    )
    for i in range(0, len(SAMURAI_ANIM_DIMS))
]

############# ARCHER (RANGED DEFAULT & BOSS) CONSTANTS ############# 

ARCHER_ANIM_DIMS_RAW = [
    [48, 104],  # Idle
    [104, 72],  # Walk
    [104, 74],  # Run
    [0,0,],     # Block (No block...)
    [104, 70],  # Hurt
    [121, 71],  # Dead
    [98, 70],   # Attack 1
    [104, 101], # Attack 2
    [116, 73],  # Attack 3
    [93, 115],  # Short Charge
    [93, 115],  # Shot
    [52, 7],    # Arrow
]


ARCHER_ANIM_DIMS = [
    (d[0]*scaleFactor, d[1]*scaleFactor)
    for d in ARCHER_ANIM_DIMS_RAW
]


ARCHER_RENDER_CORRECTIONS = [
    # abs(Idle - animation[i]) 
    (
        abs(ARCHER_ANIM_DIMS[0][0] - ARCHER_ANIM_DIMS[i][0]),
        abs(ARCHER_ANIM_DIMS[0][1] - ARCHER_ANIM_DIMS[i][1])
    )
    for i in range(0, len(ARCHER_ANIM_DIMS))
]

ARROW_DIMENSIONS = ARCHER_ANIM_DIMS[11]
#ARROW_RENDER_XCORRECTION = (ARCHER_ANIM_DIMS[10][0]/2)
ARROW_RENDER_YCORRECTION = (ARCHER_ANIM_DIMS[10][1]/2)-(ARROW_DIMENSIONS[1])

#ARROW_RENDER_CORRECTION = [
#    [ARCHER_ANIM_DIMS[0] ,], # Right direction
#    [ ,]  # Left direction
#]

#print(ARCHER_RENDER_CORRECTIONS)

ARCHER_RENDER_CORRECTION_XMASK = [
    # Idle
    0,
    0,
    # Walk
    -0.5, 
    -0.5,
    # Run
    -0.5,
    -0.5,
    # Block (not used)
    0,    
    0,
    # Hurt
    -0.5, 
    -0.5,
    # Dead
    -0.5, 
    -0.5,
    # Attack 1
    0, 
    -1,
    # Attack 2
    0,
    -1,
    # Attack 3
    0,
    -1,
    # Shot charge
    0,
    -1,
    # Shot
    0,
    -1,
    # Arrow
    0,
    0,
]

ARCHER_RENDER_CORRECTION_YMASK = [
    # Idle
    0,
    0,
    # Walk
    1,
    1,
    # Run
    1,
    1,
    # Block (not used)
    0,
    0,
    # Hurt
    1,
    1,
    # Dead
    1,
    1,
    # Attack 1
    1,
    1,
    # Attack 2
    1,
    1,
    # Attack3
    1,
    1,
    # Shot Charge
    -1,
    -1,
    # Shot
    -1,
    -1,
    # Arrow
    0,
    0,
]