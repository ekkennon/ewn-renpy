label chooseCarMod:
    # pre race 1 should now be complete (aside from typical debugging)
    # pre race 2 should start at line 15000
    # pre race 3 should start at line 16000
    # pre race 4 should start at line 17000 and should include line 12900 (use diff checker)

    $ curCar = phase % 2
    while curCar == 1 or curCar == 0:
        $ nw = savings[curCar] + carVal[curCar]
        if numGears[curCar] > 0:
            if curCar == 0:
                player[0] "YOU ARE CURRENTLY DRIVING A  [engineStats[0][0]] HP [desc[0]]."
                player[0] "YOU HAVE $[savings[0]] IN SAVINGS. THE CAR IS NOW VALUED AT $[carVal[0]]"
                player[0] "YOUR NET WORTH IS $[nw] AND YOU HAVE WON [WIN1] RACES"
            elif curCar == 1:
                player[1] "YOU ARE CURRENTLY DRIVING A [engineStats[1][0]] HP [desc[1]]"
                player[1] "YOU HAVE $[savings[1]] IN SAVINGS; THE CAR IS NOW VALUED AT $[carVal[1]]"
                player[1] "YOUR NET WORTH IS $[nw] AND YOU HAVE WON [WIN2] RACES"

        $ lookAvail = False # this is true on race 1 and after race 2
        $ modsAvail = False # this is true after race 1, this should remain false when the car has no mods available - later races
        $ raceAvail = False # this is true when the player has a working car (after race 1)

        if numGears[curCar] == 0: # if current player has no car
            $ lookAvail = True

        if race > 1:
            $ modsAvail = True
            $ raceAvail = True

        if race > 2:
            $ lookAvail = True

        menu:
            "Considering where you bought your cars, both of them could probably use some work."

            "Look at used cars" if lookAvail:
                call chooseCar

            "Make modifications" if modsAvail:
                call modifications

            "Race the car 'As Is'" if raceAvail: # I'm ready to race
                "The race will begin shortly."

        if phase % 2 == 0:
            $ curCar += 1
        elif phase % 2 == 1:
            $ curCar -= 1
    return

label chooseCar:
    # Phase 1:
        # family and friends cars (USED50FA.DG1 & USED50FB.DG1)
        # various junkers and jalopies (this could include cars that start out broken where label carCheck will be used) (JUNK0CAR.DG1)
        # front row of a junkyard (JUNK1.DG1 & JUNK2.DG1)
        # back row of a disreputable used car lot (USED50-A.DG1 & USED50-B.DG1)
    # Phase 2:
        # newspaper want ads (USED54-B.DG1)
        # various transportation cars (JUNK0CAT.DG1)
        # descent used cars (USED54-A.DG1)
        # (USED54-C.DG1 & USED54-D.DG1)
    # Phase 3:
        # 55-A
        # 56-A
        # 57-a
        # 58-A
    # Phase 4:
        # 59-A
        # 60-A
        # 61-A
        # 62-A
    # Phase 5:
        # 63-A
        # 64-A
        # 65-A
        # hotrods

    if carVal[curCar] > 0:
        call f16150 # sell current car

    $ curFile = renpy.file("cars/carslist" + str(phase) + str(stage) + str(curCar) + ".dg1")
    $ lines = curFile.read().splitlines()

    $ car1 = ""
    while lines > 0 and car1 == "":
        $ car1 = renpy.random.choice(lines)
        $ cardets = car1.split(",")
        $ lines.remove(car1)
        if savings[curCar] < cardets[3]: # if the player can't afford the car
            if cardets[18] < FINYR: # car is too old to be financed
                $ car1 = ""

    $ desc1 = cardets[4] + " " + cardets[5] + " " + cardets[6]
    $ car2 = ""
    while lines > 0 and car2 == "":
        $ car2 = renpy.random.choice(lines)
        $ cardets = car2.split(",")
        $ lines.remove(car2)
        if savings[curCar] < cardets[3]: # if the player can't afford the car
            if cardets[18] < FINYR: # car is too old to be financed
                $ car2 = ""

    $ desc2 = cardets[4] + " " + cardets[5] + " " + cardets[6]
    $ car3 = ""
    while lines > 0 and car3 == "":
        $ car3 = renpy.random.choice(lines)
        $ cardets = car3.split(",")
        $ lines.remove(car3)
        if savings[curCar] < cardets[3]: # if the player can't afford the car
            if cardets[18] < FINYR: # car is too old to be financed
                $ car3 = ""

    $ desc3 = cardets[4] + " " + cardets[5] + " " + cardets[6]
    $ car4 = ""
    while lines > 0 and car4 == "":
        $ car4 = renpy.random.choice(lines)
        $ cardets = car4.split(",")
        $ lines.remove(car4)
        if savings[curCar] < cardets[3]: # if the player can't afford the car
            if cardets[18] < FINYR: # car is too old to be financed
                $ car4 = ""
    $ desc4 = cardets[4] + " " + cardets[5] + " " + cardets[6]

    menu:
        "Which car would you like?"

        "[desc1]" if car1:
            $ cardets = car1.split(",")
        "[desc2]" if car2:
            $ cardets = car2.split(",")
        "[desc3]" if car3:
            $ cardets = car3.split(",")
        "[desc4]" if car4:
            $ cardets = car4.split(",")

label assignCar:
    $ engineStats[curCar][0] = int(cardets[1])
    $ engineStats[curCar][2] = int(cardets[2])
    $ weight[curCar][0] = int(cardets[7])
    $ D[curCar] = float(cardets[8])
    $ W[curCar] = float(cardets[9])
    $ numGears[curCar] = int(cardets[10])
    $ NTR[curCar] = numGears[curCar]
    $ desc[curCar] = cardets[4] + cardets[5] + cardets[6]
    $ gearRatios[curCar][4] = float(cardets[11])
    $ gearRatios[curCar][3] = float(cardets[12])
    $ gearRatios[curCar][2] = float(cardets[13])
    $ gearRatios[curCar][1] = float(cardets[14])
    $ gearRatios[curCar][5] = float(cardets[15])
    $ VLCD[curCar] = int(cardets[17])
    $ carYear[curCar] = int(cardets[18])
    $ savings[curCar] = savings[curCar] - int(cardets[3])
    $ carVal[curCar] = int(cardets[3])
    $ MFR[curCar] = cardets[16]
    $ NTR[curCar] = numGears[curCar]
    $ TR[curCar] = cardets[19] or ""

    $ curFile = renpy.file("cars/engines.dg1")
    $ lines = curFile.read().splitlines()

    $ engNum = 0 # compare this (lines 10210 - 10480) with lines 10810 - 10895 in P1X (both P1X and P1T have the same 10210 - 10480)
    while engineStats[curCar][1] == 0: # while this car has no engine
        $ engine = lines[engNum]
        $ engine = engine.split(",")
        if engine[0] == MFR[curCar] and int(engine[3]) == engineStats[curCar][2] and int(engine[1]) == engineStats[curCar][0]:
            $ engineStats[curCar][3] = int(engine[4])
            $ engineStats[curCar][4] = float(engine[5])
            $ engineStats[curCar][5] = float(engine[6])
            $ engineStats[curCar][6] = float(engine[7])
            $ NC[curCar] = int(engine[8])
            $ NB[curCar] = int(engine[9])
            $ CR[curCar] = float(engine[10])
            $ CAM[curCar] = engine[11]
            $ BRTH[curCar] = int(engine[12])
            $ engineStats[curCar][1] = float(engine[2])
        $ engNum += 1

label carCheck:# check for modifications needed on car immediately after purchasing (P1X)
    if engineStats[curCar][0] == 0:
        jump f14260
    else:
        call f10210
    return

label modifications:
    if stage == 5:#2:
        $ modsCost = 5
        $ savings[curCar] = savings[curCar] + 100 # why does their money increase for wanting mods?
        call f15065
    elif stage < 5:#== 3:
        $ FINYR = 54
        $ modsCost = 5
        $ savings[curCar] = savings[curCar] + 100
        call f16010

    if stage == 6:#4:
        jump f17010
    return

label f10010:
    #REM: CHEV TRANSMISSION RATIOS
    "       PLEASE INPUT THE 1ST GEAR RATIO OF THE TRANSMISSION OF YOUR CHOICE (line f10010)"#:INPUT L(L,4)

label f10020:
    if gearRatios[curCar][4] == 2.94:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][2] = 1.68
        $ gearRatios[curCar][3] = 2.94
    elif gearRatios[curCar][4] == 3.06:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][3] = 1.63
        $ gearRatios[curCar][2] = 1.05
        $ gearRatios[curCar][1] = 1
        $ weight[curCar][0] = weight[curCar][0] + 150
    elif gearRatios[curCar][4] == 2.85:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.35
        $ gearRatios[curCar][3] = 2.02
        $ weight[curCar][0] = weight[curCar][0] + 25
    elif gearRatios[curCar][4] == 2.47:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][2] = 1.53
        $ gearRatios[curCar][3] = 2.47
    elif gearRatios[curCar][4] == 2.58:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][2] = 1.48
        $ gearRatios[curCar][3] = 2.58
    elif gearRatios[curCar][4] == 3.62:
        $ numGears[curCar] = 2
        $ gearRatios[curCar][2] = 1.1
        $ gearRatios[curCar][3] = 3.62 # original code has this as index 2 but should it be index 3? line 10060
        $ weight[curCar][0] = weight[curCar][0] + 95
        $ TR[curCar] = "PG"
    elif gearRatios[curCar][4] == 3.96:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.53
        $ gearRatios[curCar][3] = 2.63
        $ weight[curCar][0] = weight[curCar][0] + 198
        $ TR[curCar] = "HYD"
    elif gearRatios[curCar][4] == 3.97:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.33
        $ gearRatios[curCar][3] = 2.23
        $ weight[curCar][0] = weight[curCar][0] + 198
        $ TR[curCar] = "HYD"
    elif gearRatios[curCar][4] == 2.5:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][2] = 1.55
        $ gearRatios[curCar][3] = 2.5
        $ weight[curCar][0] = weight[curCar][0] + 125
        $ TR[curCar] = "TH"
    elif gearRatios[curCar][4] == 2.21:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][2] = 1.33
        $ gearRatios[curCar][3] = 2.21
    elif gearRatios[curCar][4] == 2.2:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.31
        $ gearRatios[curCar][3] = 1.64
        $ weight[curCar][0] = weight[curCar][0] + 25
    elif gearRatios[curCar][4] == 2.54:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.66
        $ gearRatios[curCar][3] = 1.91
        $ weight[curCar][0] = weight[curCar][0] + 25
    elif gearRatios[curCar][4] == 2.56:
        $ numGears[curCar] = 4
        $ gearRatios[curCar][2] = 1.48
        $ gearRatios[curCar][3] = 1.91
        $ weight[curCar][0] = weight[curCar][0] + 25
    elif gearRatios[curCar][4] == 2.65:
        $ numGears[curCar] = 3
        $ gearRatios[curCar][1] = 1
        $ gearRatios[curCar][2] = 1.51
        $ gearRatios[curCar][3] = 2.65
    elif gearRatios[curCar][4] == 2.39:
        $ gearRatios[curCar][3] = 2.39
        $ gearRatios[curCar][2] = 1.53
        $ numGears[curCar] = 3
    if gearRatios[curCar][2] == 0:
        jump f10010
    if gearRatios[curCar][1] == 0:
        $ gearRatios[curCar][1] = 1
    return

label f10210:
    #REM: GET ENGINE DATA
    $ SM = MFR[curCar]
    if engineStats[curCar][2] == 999:
        $ SM[curCar] = ""
        jump f10210

label f10235:
    $ SP1 = engineStats[curCar][0]
    $ SP3 = engineStats[curCar][2]
    if SM == "LIST":
        jump f10450
    if SM == MFGR:
        jump f10420
    else:
        jump f10500

label f10420:
    if SP3 == P3:
        jump f10430
    else:
        jump f10500

label f10430:
    if SP1 == P1:
        jump f10440
    else:
        jump f10500

label f10440:
    $ engineStats[curCar][0] = P1
    $ engineStats[curCar][1] = P2
    $ engineStats[curCar][2] = P3
    $ engineStats[curCar][3] = P4
    $ engineStats[curCar][4] = P5
    $ engineStats[curCar][5] = P6
    $ engineStats[curCar][6] = P7
    $ NC[curCar] = NC
    $ NB[curCar] = NB
    $ CR[curCar] = CR
    $ CAM[curCar] = CAM
    $ BRTH[curCar] = BRTH

label f10450:
    "MFGR [MFGR], DISP=[P3], HP=[P1] @ [P5], TORQUE=[P6] @ [P7]"
    if engineStats[curCar][4] == 0:
        jump f10460
    $ CL = CL + 1
    return

label f10460:
    $ LL = LL + 1
    if LL < 23:
        jump f10500
    $ LL = 1

label f10500:
    if engineStats[curCar][4] > 0:
        return
    "YOU CHOSE AN INELLIGIBLE HP/DISPLACEMENT COMBINATION - TRY AGAIN"
    $ engineStats[curCar][0] = 0
    $ engineStats[curCar][2] = 0
    jump f10210

label f12100:
    #REM:  INCREASE VALUE OF JUNKERS

label f12105:
    if stage == 3:
        $ VLX = 150
    else:
        $ VLX = 100

label f12110:
    if carVal[curCar] > engineStats[curCar][0]:
        return

label f12120:
    if carVal(curCar) > VLX:
        return

label f12130:
    if engineStats[curCar][0] > 100:
        $ carVal[curCar] = carVal[curCar] * 2
    else:
        $ carVal[curCar] = engineStats[curCar][0]

label f12140:
    return

label f12205:
    if MFR(curCar) == "MOPAR":
        if N[curCar] < 4:
            jump f12250
        player[curCar] "You have blown first gear on the old 4-speed."
        "Your options are to avoid first gear or buy the available 3-speed."
        "Another transmission will cost $50.  Enter 'B' to buy (if 'B' goto f12225)"#;I$
        $ numGears[curCar] = 3
        $ gearRatios[curCar][4] = 0
        if engineStats[curCar][0] > 135:
            jump f12270
        else:
            return

label f12225:
    $ gearRatios[curCar][4] = 0
    $ gearRatios[curCar][3] = 2.67
    $ gearRatios[curCar][2] = 1.55
    $ numGears[curCar] = 3
    $ SV[curCar] = SV[curCar] - 50
    if engineStats[curCar][0] > 135:
        jump f12270
    else:
        return

label f12250:
    if gearRatios[curCar][3] < 2.5:
        jump f12255
    if engineStats[curCar][0] > 135:
        jump f12270
    else:
        return

label f12255:
    player[curCar] "Your clutch is gone.  It will cost you $50 to replace it."#;N$(L)
    "You have no alternative; press enter to continue"#;I$
    $ SV[curCar] = SV[curCar] - 50
    if engineStats[curCar][0] < 136:
        return

label f12270:
    if engineStats[curCar][4] < 3500:
        return
    if engineStats[curCar][1] < 4100:
        return
    "You have pushed the old straight 8 beyond its limits."
    "It is going to blow up soon.  Perhaps you should consider selling."
    if stage == 2:
        $ engineStats[curCar][0] = 2
    else:
        $ engineStats[curCar][0] = 135
    return

label f12400:
    if stage == 3:
        jump f12500

label f12410:
    if VLCD[curCar] > 4:
        jump f12450

label f12420:
    if MFR[curCar] == "FF":
        jump f12450

label f12430:
    if carYear[curCar] < 46:
        $ VLPCT = .6
    else:
        $ VLPCT = .9

label f12440:
    return

label f12450:
    if carYear[curCar] < 46:
        $ VLPCT = .8
    else:
        $ VLPCT = .9
    if VLCD[curCar] > 6:
        $ VLPCT = VLPCT + .1
    if VLCD[curCar] > 7:
        $ VLPCT = VLPCT + .1
    if VLCD[curCar] > 8:
        $ VLPCT = VLPCT + .1
    return

label f12500:
    if VLCD[curCar] > 4:
        jump f12550
    if MFR[curCar]) == "FF":
        jump f12550
    if YR[curCar] > 48:
        $ VLPCT = .9
    if YR[curCar] < 49:
        $ VLPCT = .6
    if YR[curCar] < 46:
        $ VLPCT = .3
    jump f12560

label f12550:
    $ VLPCT = .9

label f12560:
    if VLCD[curCar] < 4:
        $ VLPCT = VLPCT - .1
    if VLCD[curCar] > 6:
        $ VLPCT = VLPCT + .1
    if VLCD[curCar] > 7:
        $ VLPCT = VLPCT + .1
    if VLCD[curCar] > 8:
        $ VLPCT = VLPCT + .1
    return

label f14280:
    if VLCD[curCar] < 2:
        call f21000

label f14300:
    if engineStats[curCar][0] > 0:
        jump f14500

label f14310:
    player[curCar] "Since your car won't even run, you'd better look into buying an engine."

label f14320:
    call f14350

label f14330:
    jump f14500

label f14350:
    #OPEN "I",#1,"junk0ENG.DG1

label f14360:
    #WHILE NOT EOF(1)

    # loop to find engine ?

label f14365:
    #INPUT#1,P1,P3,PR,DESC1$,O,MFGR$,MFGS$

label f14370:
    if MFR[curCar] == MFGS:
        jump f14380

label f14375:
    jump f14390

label f14380:
    player[curCar] "[P1] HP, [P3] CID, WILL COST YOU $[PR]"

label f14381:
    if O == 0:
        jump f14385

label f14383:
    "THE ADDED WEIGHT OF THIS ENGINE WILL BE [O] POUNDS"

label f14385:
    "[DESC1]"

label f14388:
    "PRESS ENTER FOR NEXT ENGINE"

label f14390:
    #WEND

label f14400:
    #CLOSE #1

label f14410:
    "INPUT THE HORSEPOWER OF THE ENGINE YOU WANT"
    # P1W

label f14420:
    #OPEN "I",#1,"junk0ENG.DG1

label f14425:
    #WHILE NOT EOF(1)

    # loop to assign engine

label f14430:
    #INPUT#1,P1,P3,PR,DESC1$,O,MFGR$,MFGS$

label f14435:
    if MFR[curCar] == MFGS:
        jump f14440
    else:
        jump f14490

label f14440:
    if P1W == P1:
        jump f14450
    else:
        jump f14490

label f14450:
    $ engineStats[curCar][0] = P1
    $ MFR[curCar] = MFGR
    $ weight[curCar][0] = weight[curCar][0] + O # probably a variable read from the file

label f14460:
    $ engineStats[curCar][2] = P3
    $ SV[curCar] = SV[curCar] - PR

label f14470:
    $ VL[curCar] = VL[curCar] + (P1 * .5) + (P3 * .2) - (O * .1) # probably a variable read from the file

label f14490:
    #WEND

label f14495:
    #CLOSE #1

label f14497:
    call f10200

label f14498:
    #call f12030

label f14499:
    return

label f14500:
    #REM

label f14510:
    if numGears[curCar] > 0:
        jump f14550

label f14520:
    player[curCar] "WHEN YOU TRY TO DRIVE THE CAR, YOU FIND THE CLUTCH IS OUT"

label f14530:
    $ cost = engineStats[curCar][0] / 3
    player[curCar] "IT WILL COST YOU $[cost] TO REPLACE IT"

label f14535:
    #INPUT "PRESS ENTER TO CONTINUE";I$

label f14540:
    $ SV[curCar] = SV[curCar] - engineStats[curCar][0] / 3

label f14542:
    $ VL[curCar] = VL[curCar] + 20

label f14545:
    #call f12030

label f14550:
    if numGears[curCar] < 3:
        call f14560

label f14555:
    jump f14800

label f14560:
    if numGears[curCar] = 1:
        jump f14600

label f14562:
    if YR[curCar] > 49:
        return

label f14565:
    $ cost = engineStats[curCar][2] / 9
    player[curCar] "YOUR TRANSMISSION CRUNCHES IN FIRST GEAR.  IT WILL COST YOU $[cost] TO REBUILD    IT NOW - OR YOU CAN LOOK FOR ANOTHER TRANSMISSION"

label f14570:
    player[curCar] "DO YOU WANT TO REBUILD (R) OR LOOK FOR ANOTHER TRANSMISSION (L) (if L: jump f14600)"

label f14580:
    #if I$="L":jump f14600

label f14585:
    $ SV[curCar] = SV[curCar] - gearRatios[curCar][3] / 9

label f14590:
    $ numGears[curCar] = 3
    $ VL[curCar] = VL[curCar] + 10

label f14595:
    jump f14795

label f14600:
    #REM

label f14605:
    if YR[curCar] > 49:
        return

label f14610:
    #OPEN "I",#1,"junk0-TR.DG1

label f14620:
    #WHILE NOT EOF(1)

label f14630:
    #INPUT#1,N(3),L(3,1),L(3,2),L(3,3),L(3,4),DESC1$,O,MFGR$,PR,L(3,5)

    # read in variable tempN rather than N(3)
    # need to use tempL[] rather than L(3,?)

label f14640:
    if MFR[curCar] = MFGR:
        jump f14660

label f14650:
    jump f14690

label f14660:
    player[curCar] "[DESC1], [tempN] SPEED, LOW GEAR = [tempL[tempN]], WILL COST YOU $[PR]"

label f14665:
    if O = 0:
        jump f14690

label f14670:
    player[curCar] "THE ADDED WEIGHT OF THIS TRANSMISSION WILL BE [O] POUNDS"

label f14690:
    #WEND

label f14700:
    #CLOSE #1

label f14710:
    player[curCar] "INPUT THE LOW GEAR RATIO OF THE TRANSMISSION YOU WANT"
    # LLW

label f14720:
    #OPEN "I",#1,"junk0-TR.DG1

label f14725:
    #WHILE NOT EOF(1)

label f14730:
    #INPUT#1,N(3),L(3,1),L(3,2),L(3,3),L(3,4),DESC1$,O,MFGR$,PR,L(3,5)

    # read in variable tempN rather than N(3)

label f14735:
    if MFR[curCar] = MFGR:
        jump f14740
    else:
        jump f14790

label f14740:
    if tempL[tempN] = LLW:
        jump f14750
    else:
        jump f14790

label f14745:
    $ O[curCar][0] = O[curCar][0] + O

label f14750:
    $ gearRatios[curCar][1] = tempL[1]
    $ gearRatios[curCar][2] = tempL[2]
    $ gearRatios[curCar][3] = tempL[3]
    $ gearRatios[curCar][4] = tempL[4]

label f14755:
    if tempL[5] > 0:
        $ gearRatios[curCar][5] = tempL[5]

label f14760:
    $ numGears[curCar] = tempN
    $ SV[curCar] = SV[curCar] - PR

label f14770:
    if numGears[curCar] = 4:
        $ VL[curCar] = VL[curCar] + 50
    else:
        $ VL[curCar] = VL[curCar] + 20

label f14790:
    #WEND

label f14792:
    #CLOSE #1

label f14795:
    #call f12030

label f14799:
    return

label f15065:
    if engineStats[curCar][2] == 323: # the car is broke and needs a repair
        call f12205

label f15110:
    #player[curCar] "\        \ YOU HAVE $[SV[curCar]] TO MODIFY YOUR [DSCR[curCar]] - COST IS $[MD] PER HP."
    player[curCar] "TO MODIFY YOUR Car the COST IS $[modsCost] PER HP."

label f15120:
    #player[curCar] "YOU HAVE [P[curCar][0]] HP AND $[SV[curCar]]"
    #stats line

    #player[curCar] "ENTER 'N' TO SKIP MODIFICATIONS THIS TIME. (if 'N' jump f15520, if 'Y' jump f15150)"

label f15150:
    #OPEN "I",#1,"ENGINEX3"
    #"if the player wants modifications, read from file ENGINEX3. (line 15150)"

label f15160:
    #"curCar=[curCar], MFR=[MFR[1]], preSM=[SM]"
    $ SM = MFR[curCar]
    #"postSM=[SM]"

label f15170:
    if SM == "":
        #INPUT "MANUFACTURER";SM$
        "this should never be reached (f15170)"

label f15180:
    #"curCar=[curCar]"
    $ SP3 = engineStats[curCar][2]
    #"it seems the player's car looked at for SM was not the same as the player's car looked at for SP3"
    #"curCar=[curCar], SM=[SM], SP3=[SP3]"
    #$ SP1 = engineStats[curCar][0] # this was added for this game because the original code (P1T) line 15190 doesn't make sense to me why it would work

label f15190:
    # this line is in the original code (P1T) but it doesn't make sense to me why it works in the game and it doesn't work here.
    $ SP1 = 0
    "read from file and output engine options to player (f15190)"
    $ curFile = renpy.file("cars/engines.dg1")
    $ lines = curFile.read().splitlines()

    $ engineCount = -1
    $ engNum = 0
    #"EO00[engineOptions[0][0]], EO01[engineOptions[0][1]], EO02[engineOptions[0][2]], EO03[engineOptions[0][3]], EO04[engineOptions[0][4]], EO10[engineOptions[1][0]], EO11[engineOptions[1][1]], EO12[engineOptions[1][2]], EO13[engineOptions[1][3]], EO14[engineOptions[1][4]]"
    while engNum < len(lines) and engineCount < 4:
        #"engine number: [engNum]"
        $ engine = lines[engNum]
        $ engine = engine.split(",")
        call f15220
        $ engNum += 1

    if engineCount == -1:
        "no engines available"
        jump f15460
    else:
        menu:
            "Which engine would you like?"

            "[engineOptions[0][0]]":
                $ engdets = engineOptions[1][0]
            "[engineOptions[0][1]]" if engineCount > 0:
                $ engdets = engineOptions[1][1]
            "[engineOptions[0][2]]" if engineCount > 1:
                $ engdets = engineOptions[1][2]
            "[engineOptions[0][3]]" if engineCount > 2:
                $ engdets = engineOptions[1][3]
            "[engineOptions[0][4]]" if engineCount > 3:
                $ engdets = engineOptions[1][4]

    jump f15390

label f15220:
    if SM == engine[0]:
        #"SM=[SM]"
        #"f15220 - Current1 CID = [engineStats[1][2]], this CID = [engine[3]]"
        #"f15220 - Current2/0 CID = [engineStats[0][2]], this CID = [engine[3]]"
        jump f15230
    else:
        return

label f15230:
    if SP3 > 0:
        #"SP3=[SP3]"
        jump f15240
    else:
        jump f15270

label f15240:
    if SP3 == int(engine[3]):
        #"f15240 - CID=[SP3]"
        jump f15250
    else:
        #"P3=[engine[3]]"
        return

label f15250:
    if SP1 > 0:
        jump f15260
    else:
        jump f15270

label f15260:
    if SP1 == int(engine[1]):
        jump f15270
    else:
        return

label f15270:
    #"number of engines = [engineCount]"


label f15280:
    #$ LL = LL + 1

label f15290:
    #if LL < 23:
        #return

label f15310:
    #$ LL = 1
    #return

label f15340:
    #player[curCar] "WHAT IS THE EXACT HORSEPOWER YOU WANT (WP1 is the HP entered by the player)"

label f15345:
    #if WP1 == 0:
        #jump f15420

label f15350:
    $ WORK1 = int(engine[1]) - engineStats[curCar][0]

label f15360:
    $ WORK2 = WORK1 * modsCost

label f15370:
    if WORK2 > 0:
        $ WORK3 = savings[curCar] - WORK2
    else:
        return

label f15380:
    if WORK3 > 0:
        $ engineCount += 1
        #", EC [engineCount]"
        #"MFGR [engine[0]]"
        #", DISP=[engine[3]]"
        #", HP=[engine[1]]"
        #" @ [engine[5]]"
        #", TORQUE=[engine[6]]"
        #" @ [engine[7]]"
        #" will cost $[WORK2]"
        #if engineCount == 0:
            #"EO [engineOptions[0][0]]"
        #elif engineCount == 1:
            #"EO [engineOptions[0][1]]"
        #elif engineCount == 2:
            #"EO [engineOptions[0][2]]"
        #elif engineCount == 3:
            #"EO [engineOptions[0][3]]"
        #elif engineCount == 4:
            #"EO [engineOptions[0][4]]"
        #player[curCar] "YOU CAN'T AFFORD THAT - TRY AGAIN (f15380)"
        #jump f15340
        $ engineOptions[0][engineCount] = "HP=" + engine[1] + " @ " + engine[5] + ", TORQUE=" + engine[6] + " @ " + engine[7] + " will cost $" + str(WORK2)
        $ engineOptions[1][engineCount] = engine
    return

label f15390:
    $ engineOptions = [["","","","",""],["","","","",""]]
    #$ engdets = engdets.split(",")
    #$ cardets = car1.split(",")
    #player[curCar] "YOU CAN INCREASE TO [WP1] HP - IT WILL LEAVE YOU WITH $[WORK3]"
    #"the price needs to be displayed to the player (f15390)"

label f15400:
    #player[curCar] "ENTER 'Y' TO CONFIRM MODIFICATION (if 'Y' jump f15430, if 'N' jump f15420)"

label f15420:
    #"line 15420"
    #player[curCar] "YOU OPTED NOT TO MODIFY AT THIS TIME"
    #jump f15520

label f15430:
    $ engineStats[curCar][0] = int(engdets[1])
    $ savings[curCar] = WORK3
    $ carVal[curCar] = carVal[curCar] + (WORK1 * 2)
    $ engineStats[curCar][3] = int(engdets[4])
    $ engineStats[curCar][4] = float(engdets[5])
    $ engineStats[curCar][5] = float(engdets[6])
    $ engineStats[curCar][6] = float(engdets[7])
    $ NC[curCar] = int(engdets[8])
    $ NB[curCar] = int(engdets[9])
    $ CR[curCar] = float(engdets[10])
    $ CAM[curCar] = engdets[11]
    $ BRTH[curCar] = int(engdets[12])
    $ engineStats[curCar][1] = float(engdets[2])
    $ engineStats[curCar][2] = int(engdets[3])

label f15440:
    player[curCar] "MODIFICATIONS COMPLETE"#; HP = [engineStats[curCar][0]], CASH = $[savings[curCar]], CAR IS WORTH $[carVal[curCar]]"

label f15460:
    #$ engineStats[curCar][1] = 0
    #$ engineStats[curCar][4] = 0
    #$ engineStats[curCar][5] = 0
    #$ engineStats[curCar][6] = 0

    #call f10200
    #call f8900

label f15520:
    #"line 15520"
    #NEXT PL
    return

label f16010:
    #FOR PL=1 TO 2
    #$ curCar = 0
    #call f16014
    #$ curCar = 1

label f16014:
    #$ FINYR = 54

label f16015:
    #$ modsCost = 5

label f16020:
    #$ savings[curCar] = savings[curCar] + 100

label f16030:
    if engineStats[curCar][2] < 229:
        jump f16040

label f16033:
    if engineStats[curCar][2] == 323:
        call f12200

label f16035:
    if engineStats[curCar][0] < 95:
        jump f16060
    else:
        call f12100
        jump f16130

label f16040:
    if engineStats[curCar][2] > 207:
        jump f16042

label f16041:
    if engineStats[curCar][0] < 74:
        jump f16060
    else:
        call f12100
        jump f16130

label f16042:
    if engineStats[curCar][0] < 78:
        jump f16060
    call f12100
    jump f16130

label f16060:
    player[curCar] "You have blown your engine.  You knew when you bought it that it"

label f16062:
    player[curCar] "needed work.  Now you have no choice."

label f16065:
    $ engineStats[curCar][0] = 0
    #call f12030

label f16080:
    player[curCar] "YOU CAN LOOK AT USED CARS (L) OR MODIFY/REBUILD (M) (if 'L' jump f16150, if 'M' jump f16315)"
    jump f16150
    jump f16220 # i don't see how this would ever be reached, originally line 16125

label f16130:
    #player[curCar] "You now have $[savings[curCar]]."

label f16131:
    #player[curCar] "YOU CAN LOOK AT USED CARS (L), MODIFY YOUR CAR (M), OR RACE IT AS IS (R) (if 'L' jump f16150, if 'M' jump f16315, if 'R' jump f16740)"
    jump f16315

label f16150:
    call f12400

label f16165:
    $ WORK1 = (VLPCT * carVal[curCar]) + (engineStats[curCar][0] * .1) - ( weight[curCar][0] * .005)

label f16175:
    player[curCar] "\        \-YOU HAVE BEEN OFFERED $[WORK1] FOR YOUR car."#[desc[curCar]]"

label f16180:
    player[curCar] "YOU FIGURE THIS IS MUCH MORE THAN YOU COULD GET AS A TRADE-IN"

label f16185:
    player[curCar] "IF YOU ARE SERIOUS ABOUT BUYING ANOTHER CAR, YOU'D BETTER SELL IT NOW (Y/N) (if 'Y' jump f16195, if 'N' jump f16131)"

label f16195:
    $ savings[curCar] = savings[curCar] + WORK1

label f16200:
    $ carVal[curCar] = 0
    return

label f16205:
    #player[curCar] "\        \ YOU HAVE $[savings[curCar]] TO SPEND"

label f16220:
    #player[curCar] "\        \ YOU ARE GOING TO BUY A CAR; YOU HAVE $[savings[curCar]]"

label f16222:
    player[curCar] "CHOOSE FROM DECENT USED CARS (U) OR NEWSPAPER WANT ADS (W)"

label f16225:
    if IP == "W":
        #OPEN "I",#1,"USED54-B.DG1"
        "for want adds use file USED54-B.DG1 (line 16225)"
    else:
        #OPEN "I",#1,"USED54-A.DG1"
        "for used cars use file USED54-A.DG1 (line 16225)"
    call f11300

label f16275:
    player[curCar] "INPUT THE NUMBER OF THE CAR YOU WANT OR '0' TO PASS"

label f16277:
    if CN[curCar] > 0:
        jump f16280

label f16278:
    $ carVal[curCar] = WORK1
    $ savings[curCar] = savings[curCar] - WORK1
    jump f16315

label f16280:
    if IP = "W":
        #OPEN "I",#1,"USED54-B.DG1"
        "for W cars use file USED54-B.DG1 (line 16280)"
    else:
        #OPEN "I",#1,"USED54-A.DG1"
        "for NOT W cars use file USED54-A.DG1 (line 16280)"
    call f11400
    call f10200

label f16315:
    #call f12030
    if savings[curCar] < 0:
        jump f16740

label f16318:
    player[curCar] "YOU MAY HAVE THE OPPORTUNITY TO MAKE AN ENGINE SWAP-TO LOOK, ENTER (Y/N) (if 'Y' jump f16325, if 'N' jump f16525)"

label f16325:
    #OPEN "I",#1,"BOLTIN-Z.DG1"
    "line 16325, use file BOLTIN-Z.DG1"
    $ HX = 0

label f16336:
    if C1 > stage:
        jump f16375

label f16340:
    if MFGR = MFR[curCar]:
        jump f16345
    else:
        jump f16375

label f16345:
    if OLD = engineStats[curCar][2]:
        jump f16350
    else:
        jump f16375

label f16350:
    $ HX = HP

label f16355:
    player[curCar]"YOU CAN BUY A [HP] HP [NW] FOR $[C2] "

label f16375:
    if HX = 0:
        jump f16380
    else:
        jump f16385

label f16380:
    player[curCar] "NO FURTHER ENGINE SWAPS AVAILABLE AT THIS TIME"
    jump f16525

label f16385:
    player[curCar] "INPUT THE HP YOU DESIRE (SP1 is the requested HP)"

label f16386:
    if SP1 = 0:
        jump f16525

label f16390:
    #OPEN "I",#1,"BOLTIN-Z.DG1"
    "hp change uses file BOLTIN-Z.DG1 (line 16390)"
    $ HX = 0

label f16405:
    if MFGR = MFR[curCar]:
        jump f16410
    else:
        jump f16465

label f16410:
    if OLD = engineStats[curCar][2]:
        jump f16415
    else:
        jump f16465

label f16415:
    if HP = SP1:
        jump f16420
    else:
        jump f16465

label f16420:
    $ NWH = NW
    $ HPH = HP
    $ C1H = C1
    $ C2H = C2
    $ VLHLD = VLOLD

label f16465:
    player[curCar] "IT WILL COST YOU $[C2H] ; YOU CAN GET SOME HELP INSTALLING IT."

label f16470:
    if VLHLD == 0:
        $ VLHLD = engineStats[curCar][0] * .85

label f16475:
    player[curCar] "YOU CAN SELL YOUR OLD ENGINE FOR $[VLHLD]"

label f16480:
    player[curCar] "DO YOU WANT TO MAKE THIS SWAP (Y/N) (if 'Y' jump f16490, if 'N' jump f16525)"

label f16490:
    $ savings[curCar] = savings[curCar] - C2H + VLHLD

label f16495:
    $ carVal[curCar] = carVal[curCar] + (C1H * .65)

label f16500:
    $ engineStats[curCar][2] = NWH
    $ engineStats[curCar][0] = HPH
    $ engineStats[curCar][4] = 0
    $ engineStats[curCar][5] = 0
    $ engineStats[curCar][6] = 0
    $ engineStats[curCar][1] = 0

    call f10200
    call f8900

label f16510:
    player[curCar] "YOU NOW HAVE A [engineStats[curCar][0]] HP [engineStats[curCar][2]] CID [desc[curCar]]"

label f16515:
    player[curCar] "YOUR SAVINGS IS $[savings[curCar]] AND YOUR CAR IS WORTH $[carVal[curCar]]"

label f16525:
    if savings[curCar] < 0:
        jump f16740

label f16540:
    player[curCar] "\        \ YOU HAVE $[savings[curCar]] TO MODIFY YOUR [desc[curCar]] - COST IS $[modsCost] PER HP."

label f16545:
    player[curCar] "YOU HAVE [engineStats[curCar][1]] HP AND $[savings[curCar]]"
    player[curCar] "ENTER 'N' TO SKIP MODIFICATIONS THIS TIME (if 'Y' jump f16560, if 'N' jump f16740)"

label f16560:
    #OPEN "I",#1,"ENGINEX3"
    "modifications use file ENGINEX3 (line 16560)"

label f16565:
    $ SM = MFR[curCar]

label f16570:
    if SM == "":
        # THEN INPUT "MANUFACTURER";SM$
        "line 16570"

label f16575:
    $ SP3 = engineStats[curCar][2]

label f16580:
    $ SP1 = 0

label f16595:
    if SM == MFGR:
        jump f16600
    else:
        jump f16655

label f16600:
    if SP3 > 0:
        jump f16605
    else:
        jump f16620

label f16605:
    if SP3 == P3:
        jump f16610
    else:
        jump f16655

label f16610:
    if SP1 > 0:
        jump f16615
    else:
        jump f16620

label f16615:
    if SP1 == P1:
        jump f16620
    else:
        jump f16655

label f16620:
    player[curCar] "MFGR [MFGR], DISP=[P3], HP=[P1] @ [P5], TORQUE=[P6] @ [P7]"

label f16625:
    $ LL = LL + 1

label f16630:
    if LL < 23:
        jump f16655

label f16640:
    $ LL = 1

label f16655:
    player[curCar] "WHAT IS THE EXACT HORSEPOWER YOU WANT (WP1 is the requested HP)"

label f16658:
    if WP1 == 0:
        jump f16695

label f16660:
    $ WORK1 = WP1 - engineStats[curCar][0]

label f16665:
    $ WORK2 = WORK1 * modsCost

label f16670:
    $ WORK3 = savings[curCar] - WORK2

label f16675:
    if WORK3 < 0:
        player[curCar] "YOU CAN'T AFFORD THAT - TRY AGAIN"
        jump f16655

label f16680:
    player[curCar] "YOU CAN INCREASE TO [WP1] HP - IT WILL LEAVE YOU WITH $[WORK3]"

label f16685:
    player[curCar] "ENTER 'Y' TO CONFIRM MODIFICATION (if 'Y' jump f16700, if 'N' jump f16695)"

label f16695:
    "line 16695"
    player[curCar] "YOU OPTED NOT TO MODIFY AT THIS TIME"
    jump f16740

label f16700:
    $ engineStats[curCar][0] = WP1
    $ savings[curCar] = WORK3
    $ carVal[curCar] = carVal[curCar] + (WORK1 * 2)

label f16705:
    player[curCar] "MODIFICATIONS COMPLETE; HP = [engineStats[curCar][0]], CASH = $[savings[curCar]], CAR IS WORTH $[carVal[curCar]]"

label f16715:
    $ engineStats[curCar][1] = 0
    $ engineStats[curCar][4] = 0
    $ engineStats[curCar][5] = 0
    $ engineStats[curCar][6] = 0

    call f10200
    call f8900
    call f12020

label f16740:
    #REM
    #NEXT PL
    return
    jump f890
    jump f16525

label f17010:
    #FOR PL=1 TO 2
    $ curCar = 0
    call f17014
    $ curCar = 1

label f17014:
    $ FINYR = 54

label f17017:
    if engineStats[curCar][2] == 323:
        call f12200
    else:
        call f12100

label f17020:
    if MFR[curCar] == "FF":
        $ modsCost = 5
    else:
        $ modsCost = 6

label f17021:
    if engineStats[curCar][0] < 160:
        $ modsCost = 5

label f17030:
    $ savings[curCar] = savings[curCar] + 100

label f17110:
    player[curCar] "YOU CAN LOOK AT USED CARS (L), MODIFY YOUR CAR (M), OR RACE IT AS IS (R) (if 'L' jump f17170, if 'M' jump f17490, if 'R' return)"

label f17170:
    call f12400
    $ WORK1 = (VLPCT * carVal[curCar]) + (engineStats[curCar][0] * .1)

label f17200:
    player[curCar] "\        \-YOU HAVE BEEN OFFERED $[WORK1] FOR YOUR [desc[curCar]]"

label f17210:
    player[curCar] "YOU FIGURE THIS IS MUCH MORE THAN YOU COULD GET AS A TRADE-IN"

label f17220:
    player[curCar] "IF YOU ARE SERIOUS ABOUT BUYING ANOTHER CAR, YOU'D BETTER SELL IT NOW (Y/N) (if 'Y' jump f17240, if 'N' jump f17110)"

label f17240:
    $ savings[curCar] = savings[curCar] + WORK1

label f17250:
    $ carVal[curCar] = 0

label f17290:
    player[curCar] "\        \ YOU ARE GOING TO BUY A CAR; YOU HAVE $[savings[curCar)]]"

label f17300:
    if curCar == 0:
        # THEN OPEN "I", #1,"USED54-C.DG1"
        "car will come from file USED54-C.DG1"

label f17310:
    if curCar == 1:
        # THEN OPEN "I",#1,"USED54-D.DG1"
        "car will come from file USED54-D.DG1"
    call f11300

label f17400:
    player[curCar] "INPUT THE NUMBER OF THE CAR YOU WANT OR '0' TO PASS, as [CN[curCar]]"

label f17405:
    if CN[curCar] > 0:
        jump f17410

label f17406:
    $ savings[curCar] = savings[curCar] - WORK1
    $ carVal[curCar] = WORK1
    jump f17475

label f17410:
    if curCar == 0:
        #OPEN "I",#1,"USED54-C.DG1"
        "car will come from file USED54-C.DG1"

label f17420:
    if curCar == 1:
        #OPEN "I",#1,"USED54-D.DG1"
        "car will come from file USED54-D.DG1"
    call f11400
    call f10200

label f17475:
    #CLS
    #call f12030

label f17490:
    if savings[curCar] < 1:
        return

label f17495:
    player[curCar] "YOU MAY HAVE THE OPPORTUNITY TO MAKE AN ENGINE SWAP-TO LOOK, ENTER (Y/N) (if 'N' jump f17840, if 'Y' jump f17510)"

label f17510:
    #OPEN "I",#1,"BOLTIN-Z.DG1"
    "use file BOLTIN-Z.DG1 for engine swap"
    $ HX = 0

label f17535:
    if C1 > stage:
        jump f17610

label f17540:
    if MFGR == MFR[curCar]:
        jump f17550
    else:
        jump f17610

label f17550:
    if OLD == engineStats[curCar][2]:
        jump f17560
    else:
        jump f17610

label f17560:
    $ HX = HP

label f17570:
    player[curCar] "YOU CAN BUY A [HP] HP [NW] FOR $[C2]"

label f17610:
    if HX == 0:
        jump f17620
    else:
        jump f17630

label f17620:
    player[curCar] "NO FURTHER ENGINE SWAPS AVAILABLE AT THIS TIME"
    jump f17840

label f17630:
    player[curCar] "INPUT THE HP YOU DESIRE (SP1 is the desired HP)"

label f17635:
    if SP1 == 0:
        jump f17840

label f17640:
    #OPEN "I",#1,"BOLTIN-Z.DG1"
    "hp change uses file BOLTIN-Z.DG1"
    $ HX = 0

label f17670:
    if MFGR == MFR[curCar]:
        jump f17680
    else:
        jump f17730

label f17680:
    if OLD == engineStats[curCar][2]:
        jump f17690
    else:
        jump f17730

label f17690:
    if HP == SP1:
        jump f17700
    else:
        jump f17730

label f17700:
    $ NWH = NW
    $ HPH = HP
    $ C1H = C1
    $ C2H = C2
    $ VLHLD = VLOLD

label f17730:
    player[curCar] "IT WILL COST YOU $[C2H] ; YOU CAN GET SOME HELP INSTALLING IT."

label f17740:
    if VLHLD = 0:
        $ VLHLD = engineStats[curCar][0] * .85

label f17750:
    player[curCar] "YOU CAN SELL YOUR OLD ENGINE FOR $[VLHLD]"

label f17760:
    player[curCar] "DO YOU WANT TO MAKE THIS SWAP (Y/N) (if 'Y' jump f17780, if 'N' jump f17840)"

label f17780:
    $ savings[curCar] = savings[curCar] - C2H + VLHLD

label f17790:
    $ carVal[curCar] = carVal[curCar] + (C1H * .65)

label f17800:
    $ engineStats[curCar][2] = NWH
    $ engineStats[curCar][0] = HPH
    $ engineStats[curCar][4] = 0
    $ engineStats[curCar][5] = 0
    $ engineStats[curCar][6] = 0
    $ engineStats[curCar][1] = 0

    call f10200
    call f8900

label f17820:
    player[curCar] "YOU NOW HAVE A [engineStats[curCar][0]] HP [engineStats[curCar][2]] CID [desc]"

label f17830:
    player[curCar] "YOUR SAVINGS IS $[savings[curCar]] AND YOUR CAR IS WORTH $[carVal[curCar]]"

label f17840:
    if savings[curCar] < 1:
        return

label f17850:
    player[curCar] "\        \ YOU HAVE $[savings[curCar]] TO MODIFY YOUR [desc] - COST IS $[modsCost] PER HP."

label f17860:
    player[curCar] "ENTER 'N' TO SKIP MODIFICATIONS THIS TIME (if 'N' return, if 'Y' jump f17870)"

label f17870:
    player[curCar] "YOU HAVE [engineStats[curCar][0]] HP AND $[savings[curCar]]"

label f17890:
    #OPEN "I",#1,"ENGINEX3"
    "file for modifications is ENGINEX3"

label f17900:
    $ SM = MFR[curCar]

label f17910:
    if SM = "":
        #INPUT "MANUFACTURER";SM$
        "line 17910"

label f17920:
    $ SP3 = engineStats[curCar][2]

label f17930:
    $ SP1 = 0

label f17960:
    if SM == MFGR:
        jump f17970
    else:
        jump f18080

label f17970:
    if SP3 > 0:
        jump f17980
    else:
        jump f18010

label f17980:
    if SP3 == P3:
        jump f17990
    else:
        jump f18080

label f17990:
    if SP1 > 0:
        jump f18000
    else:
        jump f18010

label f18000:
    if SP1 == P1:
        jump f18010
    else:
        jump f18080

label f18010:
    player[curCar] "MFGR [MFGR], DISP=[P3], HP=[P1] @ [P5], TORQUE=[P6] @ [P7]"

label f18020:
    $ LL = LL + 1

label f18030:
    if LL < 23:
        jump f18080

label f18050:
    $ LL = 1

label f18080:
    player[curCar] "WHAT IS THE EXACT HORSEPOWER YOU WANT (WP1 is requested HP)"

label f18085:
    if WP1 == 0:
        return

label f18090:
    $ WORK1 = WP1 - engineStats[curCar][0]

label f18100:
    $ WORK2 = WORK1 * modsCost

label f18110:
    $ WORK3 = savings[curCar] - WORK2

label f18120:
    if WORK3 < 0:
        player[curCar] "YOU CAN'T AFFORD THAT - TRY AGAIN"
        jump f18080

label f18130:
    player[curCar] "YOU CAN INCREASE TO [WP1] HP - IT WILL LEAVE YOU WITH $[WORK3]"

label f18140:
    player[curCar] "ENTER 'Y' TO CONFIRM MODIFICATION (if 'Y' jump f18170, if 'N' jump f18160)"

label f18160:
    "line 18160"
    player[curCar] "YOU OPTED NOT TO MODIFY AT THIS TIME"
    return

label f18170:
    $ engineStats[curCar][0] = WP1
    $ savings[curCar] = WORK3
    $ carVal[curCar] = carVal[curCar] + (WORK1 * 2)

label f18180:
    player[curCar] "MODIFICATIONS COMPLETE; HP = [engineStats[curCar][0]], CASH = $[savings[curCar]], CAR IS WORTH $[carVal[curCar]]"

label f18200:
    $ engineStats[curCar][1] = 0
    $ engineStats[curCar][4] = 0
    $ engineStats[curCar][5] = 0
    $ engineStats[curCar][6] = 0

    call f10200
    call f8900
    call f12020
    return
