# GOTO = jump
# GOSUB = call

init python:
    import math

# player variables:
define player = [Character(), Character()] # N$() is a string array of players' names
default savings = [0, 0] #the amount of money each player has, orininally SV
define carVal = [99,139] #[2], value of player's car, originally VL
define curCar = 1 # originally L, for some loops in original code
define lane = 1
define LT = [0,0] # the low time of each player

# car variables:
define gearRatios = [[-1,1,1.76,3.11,0,3.78],[-1,1,1.66,2.94,0,4.11]] # [2,5] placeholder,1st,2nd,3rd,4th(0 on 3-speed transmissions),rear-end ratio, origianlly L
define engineStats = [[85,4466.667,221,1,3800,160,2000,0,0], [103,4100,248,1,3800,196,1800,0,0]] # [2,9] various details, maybe related to the engine. hp,shifting RPM,cid,?,hp @,torque,torque @,?,?  orininally P
define weight = [[2791,0,0],[3355,0,0]] # [2,3] originally O
define D = [2.3,2.3]
define W = [5,5]
define numGears = [3,3] # originally N
define NTR = [3,3]
define desc = ["40 FORD DELUXE COUPE. THE FLATHEAD V8 SEEMS TO RUN GOOD. VERY MINOR RUST - PAINT A LITTLE FADED","49 PONTIAC CHIEFTAIN BUSINESS COUPE. THIS IS A RARE 8-CYLINDER MODEL. IT SHOWS WEAR BUT STILL RUNS OK"] # originally DSCR
define VLCD = [6,5]
define carYear = [40,50] # originally YR
define MFR = ["FF","PONT"] # manufacturer, is this the car manufacturer or the engine manufacturer?
define TR = ["",""]

# engine variables:
define NC = [1,1]
define NB = [2,2]
define CR = [6.3,6.5]
define CAM = ["S/F","S/F"]
define BRTH = [3,3]

# race variables:
define seconds = 0 # number of seconds into race, originally T
define tenthSec = 0 # originally T1, number of tenths of a second for the current second (T) of the race
define T2 = 0
define T3 = 0
define dispRPM = [0,0] # originally H
define rpm = 0 # originally R
define Q = [0,0]
define feetSec = [0.0,0.0] # originally S, FT IN FT/SEC
define maxAccel = [0,0] # originally B, max acceleration without burning
define distance = [0,0] # originally X, DISTANCE IN FT
define L14 = 0
define L13 = 0
define L24 = 0
define L23 = 0
define TR1 = ""
define TR2 = ""
define lowTime = 0 # originally LOT, lowest winning time
define M = [0,0]
define E = [0,0]
define WR = 0
define accel = 0 # originally A
define BW1 = 0
define BW2 = 0
define BW3 = 0
define BW4 = 0
define BURN1 = 0
define BURN2 = 0
define BURN3 = 0
define BURN4 = 0
define XX1 = 0.0
define PT1 = 0
define PT2 = 0
define racing = False

# winner variables
define WS = 0
define WIN1 = 0 # the win record of player 1
define WIN2 = 0 # the win record of player 2
define LWIN = 0 # the winning lane
define LWINT = 0 # the winning time
define playerWin = -1 # the player who won
define RVL = 0
define SWT12 = -1
define SWT13 = -1
define SWT14 = -1
define SWT15 = -1
define SWT16 = -1
define SWT17 = -1
define SWT18 = -1
define PV = [0,0]
define HIS = 0

# other variables:
define CL = 0 # not sure anything about this variable  10453 CL=CL+1
define round = 0 # originally ROUND
define race = 0
define phase = 0
define JOB = ""
define modsCost = 0 # originally MD
define L5W = 0.0
define TSAV = 0
define HS = [0,0]
define VLHLD = 0.0
define SM = ""
define MFGR = "" # this is for reading engines from files
define P1 = 0
define P3 = 0
define SP1 = 0
define SP3 = 0
define WP1 = 0
define raceLoop = 0

screen carloc1:
    imagemap:
        ground "carlocations1.png"
        idle "carlocations1 idle.png"
        hover "carlocations1 hover.png"

        hotspot (6, 2, 852, 351) clicked Call("disreputable")
        hotspot (5, 360, 854, 354) clicked Call("junkyard")

screen stats():
    hbox:
        # maybe incorporate label f11100
        $ m1 = str(savings[0])
        $ m2 = str(savings[1])
        text "[player[0]]: $[m1]"
        text "[player[1]]: $[m2]"

label start:
    while curCar > -1:
        $ hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        $ nm = renpy.input("Player in lane [lane], what is your name?") or "Player " + str(lane)
        $ c = renpy.input("[nm], choose your color (enter a hex value or leave blank for default)") or "#" + renpy.random.choice(hexes) + renpy.random.choice(hexes) + renpy.random.choice(hexes) + renpy.random.choice(hexes) + renpy.random.choice(hexes) + renpy.random.choice(hexes)
        $ player[curCar] = Character(nm, color=c)
        # the 'or' values are defaults

        $ curCar -= 1
        $ lane += 1

    scene bg room

    "What type of game do you want to play?"

    menu:
        "What type of game do you want to play?"

        "1 'stock' race":
            jump stock

        "full 5 phase game of 20 races":
            jump phase1

    return

label phase1:
    show screen stats

    $ phase += 1
    "Beginning Phase [phase]."

    "You each will start with $250."

    $ savings[0] += 250
    $ savings[1] += 250

    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 1

    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 2

    $ round += 1
    $ race += 1
    "Beginning Race #[round]"
    #call race  # race 3

    $ round += 1
    $ race += 1
    "Beginning Race #[round]"
    #call race  # race 4

    jump phase2

label phase2:
    $ phase += 1
    $ round = 0
    "Beginning Phase [phase]."

    "You will now swap lanes."
    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 1

    "End of Phase [phase]."

    jump phase3

label phase3:
    $ phase += 1
    $ round = 0
    "Beginning Phase [phase]."

    "You will now swap lanes."
    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 1

    "End of Phase [phase]."
    jump phase4

label phase4:
    $ phase += 1
    $ round = 0
    "Beginning Phase [phase]."

    "You will now swap lanes."
    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 1

    "End of Phase [phase]."
    jump phase5

label phase5:
    $ phase += 1
    $ round = 0
    "Beginning Phase [phase]."

    "You will now swap lanes."
    $ round += 1
    $ race += 1
    call chooseCarMod
    "Beginning Race #[round]"
    call race  # race 1

    "End of Phase [phase]."
    "End of game."
    return
