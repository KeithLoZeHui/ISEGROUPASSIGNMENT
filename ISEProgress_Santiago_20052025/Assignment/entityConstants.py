
MINSCALEFACTOR = 2.5
MAXSCALEFACTOR = 3
scaleFactor = MINSCALEFACTOR

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

