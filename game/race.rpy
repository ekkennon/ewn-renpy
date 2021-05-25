label race:

    if TR[0] == "SLIP":
        $ TR[0] = ""
    if TR[1] == "SLIP":
        $ TR[1] = ""

    $ curCar = phase % 2
    $ lane = 1
    while curCar == 1 or curCar == 0:
        if TR[curCar] == "PG":
            $ gearRatios[curCar][3] = 3.62
            "call f10020"
        $ hp = engineStats[curCar][0]
        $ hpat = engineStats[curCar][4]
        $ torque = engineStats[curCar][5]
        $ torqueat = engineStats[curCar][6]
        $ disp = engineStats[curCar][2]
        $ shift = engineStats[curCar][1]
        player[curCar] "HP = [hp]  @ [hpat]  TORQUE = [torque] @ [torqueat]  DISP = [disp]"
        player[curCar] "LANE [lane] IS PROGRAMMED TO SHIFT AT [shift] RPM" # 932 (I changed the shift calculation from the original, did not work as well when the number started as a decimal)
        "player has the option to change Shifting RPM - lines 960 to 1000"
        if phase % 2 == 0:
            $ curCar += 1
        elif phase % 2 == 1:
            $ curCar -= 1
        $ lane += 1
    $ curCar = phase % 2

    "THIS IS A TEST OF MACHINES--BOTH DRIVERS ARE EQUAL"
    "[engineStats[0][0]] HP  [engineStats[0][2]] CI [weight[0][0]] LBS  [gearRatios[0][4]] | LOW TIME  [lowTime] | [engineStats[1][0]] HP  [engineStats[1][2]] CI [weight[1][0]] LBS  [gearRatios[1][4]]"

    while curCar  == 1 or curCar == 0:
        $ engineStats[curCar][7] = engineStats[curCar][0]
        if engineStats[curCar][3] == 0:
            $ engineStats[curCar][3] = 1

        $ engineStats[curCar][0] = engineStats[curCar][0] * engineStats[curCar][3]
        $ M[curCar] = ( weight[curCar][0] * 1.5 + engineStats[curCar][0] + engineStats[curCar][2] + (D[curCar] * W[curCar])) / 33
        $ maxAccel[curCar] = 15 + 28 * W[curCar] * D[curCar] / ((W[curCar] + 6) * (D[curCar] + 1))
        if phase % 2 == 0:
            $ curCar += 1
        elif phase % 2 == 1:
            $ curCar -= 1
    $ curCar = phase % 2

    $ racing = True
    while racing: # each second of the race
        if seconds > 0:
            $ mph1 = feetSec[0] * 3600 / 5280
            $ mph2 = 3600 * feetSec[1] / 5280
            "[mph1] MPH [distance[0]] FEET [dispRPM[0]] RPM ||     [seconds].[tenthSec][T2]     ||[mph2] MPH  [distance[1]] FEET [dispRPM[1]] RPM"

        while raceLoop < 20: # each player's tenth of a second
            $ curCar = raceLoop % 2 # will this continue to work correctly with other parts of the game starting at $ curCar = phase % 2

            if TR[curCar] == "TH":
                call f6100

            if TR[curCar] == "HYD":
                call f6300

            if curCar == 0:
                call f2064
            elif curCar == 1:
                call f2224

                # REM: TEST FOR FINISH
                if distance[0] >= 1320 or distance[1] >= 1320:
                    call f1630 # should this be jump instead

            $ tenthSec += curCar
            $ raceLoop += 1

        $ tenthSec = 0
        $ raceLoop = 0
        $ seconds += 1

    return

label f1260:
    # player[J] "line 1260"
    $ tempE = 60 * E[curCar]
    $ tempD = math.pi * D[curCar] # 3.14159
    $ se = feetSec[curCar] * tempE
    $ rpm = se / tempD
    # "R:[R] = se:[se], tempE:[tempE]"

label f1270:
    # player[J] "line 1270"
    $ dispRPM[curCar] = rpm
    #if J == 1:
        #$ H[1] = R
        # "H(2) = [H[1]]"

label f1280:
    # player[J] "line 1280"
    $ dispRPM[curCar] = rpm
    #if J == 0:
        #$ H[0] = R
        # "H(1) = [H[0]]"

label f1300:
    # player[J] "line 1300"
    jump f2390

label f1320:
    if Q[curCar] <> 0:
        jump f2610

label f1330:
    if rpm == 0:
        jump f1410

label f1340:
    if tenthSec < (engineStats[curCar][0] * 2 + engineStats[curCar][2]) * E[curCar] * .001 * (engineStats[curCar][8] / 2) / ( weight[curCar][0] * .8):
        jump f1410

label f1350:
    if tenthSec < (engineStats[curCar][0] * 2 + engineStats[curCar][2]) * E[curCar] * .001 * (engineStats[curCar][8] / 2) / ( weight[curCar][0] * .8):
        jump f1410

label f1360:
    # player[J] "line 1360"
    if curCar == 0:
        "STOPS BURNING AT  [distance[0]] FEET   ||     [seconds].[tenthSec][T2]     ||            [distance[1]] FEET"
    elif curCar == 1:
        "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2]     ||STOPS BURNING AT  [distance[1]] FEET"

label f1380:
    # player[J] "line 1380"
    $ Q[curCar] = 1
    jump f2610

label f1410:
    # new burnout routine
    # REM: BURN ACCEL
    $ accel = ((engineStats[curCar][0] + engineStats[curCar][2]) * (E[curCar] * (2.9 / D[curCar]))) / (( weight[curCar][0] / 12) + (feetSec[curCar] * .7))

label f1440:
    # player[J] "line 1440"
    if accel > W[curCar] * 5:
        $ accel = W[curCar] * 4.5

label f1450:
    # player[J] "line 1450"
    $ XX1 = 6000 * engineStats[curCar][0] / engineStats[curCar][2]

label f1455:
    # player[J] "line 1455"
    if seconds < 2:
        $ accel = accel * 1.2 * 3000 /  weight[curCar][0]

label f1460:
    # player[J] "line 1460"
    if dispRPM[curCar] > XX1 * .34:
        jump f1490
    else:
        jump f1470

label f1470:
    # player[J] "line 1470"
    $ feetSec[curCar] = feetSec[curCar] + accel * .037

label f1480:
    # player[J] "line 1480"
    $ feetSec[curCar] = feetSec[curCar] + accel * ((dispRPM[curCar] / (5 * XX1 / 6)) * .025)
    jump f1540

label f1490:
    # player[J] "line 1490"
    if dispRPM[curCar] > (5 * XX1 / 6):
        jump f1510
    else:
        jump f1500

label f1500:
    # player[J] "line 1500"
    $ feetSec[curCar] = feetSec[curCar] + accel * ((dispRPM[curCar] / (5 * XX1 / 6)) * .053)
    jump f1540

label f1510:
    # player[J] "line 1510"
    if dispRPM[curCar] > XX1:
        jump f1520
    else:
        jump f1530

label f1520:
    # player[J] "line 1520"
    $ feetSec[curCar] = feetSec[curCar] + accel * ((.049 * (XX1 / dispRPM[curCar])))
    jump f1560

label f1530:
    # player[J] "line 1530"
    $ feetSec[curCar] = feetSec[curCar] + accel * ((.052 * ((5 * XX1 / 6) / dispRPM[curCar])))

label f1540:
    # player[J] "line 1540"
    $ feetSec[curCar] = feetSec[curCar] + (accel * ((dispRPM[curCar] / XX1) * .053))

label f1560:
    # player[J] "line 1560"
    if maxAccel[curCar] == 1:
        jump f1570
    else:
        jump f1590

label f1570:
    $ distance[curCar] = distance[curCar] + feetSec[curCar] * .075
    return

label f1590:
    # player[J] "line 1590"
    $ distance[curCar] = distance[curCar] + feetSec[curCar] * .098
    return

label f1630:
    #"line 1630"
    #"X(1) = [X[0]], X(2) = [X[1]]"
    if distance[0] > distance[1]:
        jump f1780

label f1640:
    $ T3 = (distance[1] - 5280 / 4) / feetSec[1]

label f1650:
    $ seconds = seconds + (tenthSec / 10) - T3

label f1660:
    $ distance[1] = distance[1] - feetSec[1] * T3

label f1670:
    $ distance[0] = distance[0] - feetSec[0] * T3

label f1680:
    "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2] --->||  LANE 2 WINNER"
    $ racing = False
    $ raceLoop = 20

label f1682:
    $ WS = feetSec[1] * 3600 / 5280

label f1684:
    $ WIN2 = WIN2 + 1

label f1685:
    $ LWIN = 2 # the player in lane 2 won

    if phase % 2 == 0:
        $ playerWin = 1
    elif phase % 2 == 1:
        $ playerWin = 0

    $ LWINT = seconds

label f1690:
    $ mph1 = feetSec[0] * 3600 / 5280
    $ mph2 = feetSec[1] * 3600 / 5280
    " [mph1] MPH    [dispRPM[0]] RPM       ||               ||   [mph2] MPH  [dispRPM[1]] RPM"

label f1710:
    #$ round = round + 1
    #$ race += 1

label f1720:
    $  numGears[0] = NTR[0]
    $  numGears[1] = NTR[1]
    $ gearRatios[0][3] = L14
    $ gearRatios[0][2] = L13
    $ gearRatios[1][3] = L24
    $ gearRatios[1][2] = L23
    $ TR[0] = TR1
    $ TR[1] = TR2
    #$ X[0] = 0
    #$ X[1] = 0

    jump f11000

label f1780:
    #"line 1780"
    $ T3 = (distance[0] - 5280 / 4) / feetSec[0]

label f1790:
    #"line 1790"
    $ seconds = seconds + (tenthSec / 10) - T3

label f1800:
    #"line 1800"
    $ distance[0] = 5200 / 4

label f1810:
    #"line 1810"
    $ distance[1] = distance[1] - feetSec[1] * T3

label f1820:
    #"line 1820"
    "       LANE  1   WINNER       ||<--- [seconds].[tenthSec][T2]     ||            [distance[1]] FEET"
    $ racing = False
    $ raceLoop = 20

label f1830:
    $ mph1 = feetSec[0] * 3600 / 5280
    $ mph2 = feetSec[1] * 3600 / 5280
    "[mph1] MPH  [dispRPM[0]] RPM          ||               ||    [mph2] MPH   [dispRPM[1]] RPM"

label f1832:
    $ WS = feetSec[0] * 3600 / 5280

label f1834:
    $ WIN1 = WIN1 + 1

label f1835:
    $ LWIN = 1 # the player in lane 1 won
    $ playerWin = phase % 2
    $ LWINT = seconds
    jump f1710
    return

label f1920:
    # REM: POWERGLIDE
    if  numGears[curCar] = 1:
        jump f2010

label f1930:
    if gearRatios[curCar][1] < 1.89:
        jump f2040

label f1940:
    if dispRPM[curCar] > ((engineStats[curCar][4] + engineStats[curCar][6]) / 3):
        jump f1970
    else:
        $ gearRatios[curCar][1] = gearRatios[curCar][1] - ((dispRPM[curCar] / 200000) / (88 / feetSec[curCar]))
        jump f2040 # this wasn't at this level but i believe it will only be called in this situation

label f1970:
    if gearRatios[curCar][1] > 2.5:
        $ gearRatios[curCar][1] = gearRatios[curCar][1] - ((dispRPM[curCar] / (engineStats[curCar][4] - 500)) * (1.9 / gearRatios[curCar][1]) * .2)
    else:
        $ gearRatios[curCar][1] = gearRatios[curCar][1] - .02
        jump f2040 # this wasn't at this level but i believe it will only be called in this situation

label f2010:
    if PGS[curCar] = 1:
        jump f2030

label f2020:
    $ PGS[curCar] = 1
    $ gearRatios[curCar][1] = 1.18

label f2030:
    if gearRatios[curCar][1] > 1.07:
        $ gearRatios[curCar][1] = gearRatios[curCar][1] - .001

label f2040:
    $ E[curCar] = gearRatios[curCar][ numGears[curCar]] * gearRatios[curCar][5]
    return

label f2064:
    if dispRPM[0] == 0:
        call gears
        jump f2174

label f2070:
    if TR[curCar] == "PG":
        call f6200

label f2072:
    if TR[curCar] == "TH1":
        call f6100

label f2075:
    if TR[curCar] == "SLIP":
        call f6000

label f2080:
    if dispRPM[curCar] < engineStats[curCar][1] * 1.0001:
        jump f1260

label f2090:
    if  numGears[0] > 1:
        jump f2115

label f2100:
    # player[J] "line 2100"
    if dispRPM[0] > (engineStats[0][1] * 1.07):
        # "H(1) = [H[0]]"
        jump f2190

label f2110:
    # player[J] "line 2110"
    if  numGears[0] == 1:
        jump f1260

label f2115:
    #player[curCar] "line 2115"
    if distance[1] > 1320:
        jump f1780

label f2120:
    # player[J] "line 2120"
    if curCar == 0:
        $ mph = feetSec[0] * 3600 / 5280
        "SHIFTING - [dispRPM[0]] RPM, [mph] MPH  ||     [seconds].[tenthSec][T2]     ||            [distance[1]] FEET "

label f2130:
    # player[J] "line 2130"
    $  numGears[0] =  numGears[0] - 1
    call gears

label f2174:
    # player[J] "line 2174"
    if TR[curCar] != "":
        jump f2176

label f2175:
    # player[J] "line 2175"
    if dispRPM[0] == 0:
        if E[0] < 11:
            $ TR[curCar] = "SLIP"

label f2176:
    # player[J] "line 2176"
    if TR[curCar] == "SLIP":
        call f6000
    jump f1260

label f2190:
    # player[J] "line 2190"
    $ mph = feetSec[0] * 3600 / 5280
    "CAR #1 OVERREVED AT [dispRPM[0]]RPM[distance[0]] FT.[mph] MPH"

label f2200:
    # player[J] "line 2200"
    $ engineStats[0][0] = 0
    jump f1260

label f2224:
    if rpm == 0:
        call gears
        jump f2335

label f2230:
    if TR[curCar] == "PG":
        call f6200

label f2232:
    if TR[curCar] == "TH1":
        call f6100

label f2235:
    if TR[curCar] == "SLIP":
        call f6000

label f2240:
    if dispRPM[curCar] < engineStats[curCar][1] * 1.0001:
        jump f1260

label f2250:
    if  numGears[1] > 1:
        jump f2275

label f2260:
    # player[J] "line 2260"
    if dispRPM[1] > (engineStats[1][1] * 1.07):
        $ ans = engineStats[1][1] * 1.07
        "H(2)[dispRPM[1]] > P(2,1)[engineStats[1][1]]; (ans[ans])"
        jump f2350

label f2270:
    # player[J] "line 2270"
    if  numGears[1] == 1:
        jump f1260

label f2275:
    #player[J] "line 2275"
    if distance[0] > 1320:
        jump f1780

label f2280:
    # player[J] "line 2280"
    if curCar == 1:
        $ mph = 3600 * feetSec[1] / 5280
        "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2]     ||SHIFTING - [dispRPM[1]] RPM, [mph] MPH "

label f2290:
    # player[J] "line 2290"
    $  numGears[1] =  numGears[1] - 1
    call gears

label f2335:
    # player[J] "line 2335"
    if dispRPM[1] == 0:
        if E[1] < 11:
            $ TR[curCar] = "SLIP"

label f2336:
    # player[J] "line 2336"
    if TR[curCar] == "SLIP":
        call f6000

label f2340:
    # player[J] "line 2340"
    jump f1260

label f2350:
    $ mph = feetSec[1] * 3600 / 5280
    "CAR #2 OVERREVED AT [dispRPM[1]]RPM[distance[1]] FT.[mph] MPH"

label f2360:
    "CAR #2 -- GEAR =[ numGears[1]] FINAL= [E[1]]  J=[curCar]"

label f2370:
    $ engineStats[1][0] = 0
    jump f1260

label f2390:
    # player[J] "line 2390"
    if Q[curCar] <> 0:
        jump f1380

label f2400:
    # player[J] "line 2400"
    if Q[curCar] <> 0:
        jump f1380

label f2410:
    # player[J] "line 2410"
    $ tempN =  numGears[curCar] - 1
    # "BW1 = [L[0][2]] * [L[0][4]]"
    $ BW1 = gearRatios[curCar][tempN] * gearRatios[curCar][4]

label f2420:
    # player[J] "line 2420"
    # "BW1 = [BW1]"
    if BW1 > 11:
        jump f2500

label f2430:
    # player[J] "line 2430"
    $ BW2 = 14 * (engineStats[curCar][0] + engineStats[curCar][2])
    $ BW3 = engineStats[curCar][0] / engineStats[curCar][2]
    $ BW4 = engineStats[curCar][2] /  weight[curCar][0] * .085

label f2440:
    # player[J] "line 2440"
    if BW3 > BW4:
        jump f2470

label f2450:
    # player[J] "line 2450"
    if distance[curCar] > (50 -  weight[curCar][0] / 100):
        jump f2470
    else:
        $ BURN1 = BW2 * BW4

label f2460:
    # player[J] "line 2460"
    if T > 2:
        jump f2470
    else:
        jump f2510

label f2470:
    $ BURN1 = BW2 * BW3
    jump f2510

label f2500:
    # player[J] "line 2500"
    # WAS BURN1=(P(J,1)+P(J,3))*(L(J,N(J))*L(J,5))
    $ BURN1 = (engineStats[curCar][0] + engineStats[curCar][2]) * 11

label f2510:
    # player[J] "line 2510"
    $ BURN2 = BURN1 * 2.5 / D[curCar]

label f2520:
    # player[J] "line 2520"
    # "BURN2 [BURN2] - O(1,1) [O[0][0]]"
    $ BURN3 = (BURN2 -  weight[curCar][0]) / 100

label f2530:
    # player[J] "line 2530"
    # "BURN3 [BURN3] - W(1) [W[1]]"
    $ BURN4 = BURN3 - W[curCar]

label f2540:
    # player[J] "line 2540"
    if TR[curCar] == "PG":
        jump f2560
    jump f2570

label f2560:
    $ BURN4 = (BURN3 - W[curCar]) / 3

label f2570:
    # player[J] "BURN4 [BURN4] < S(1) [S[0]]"
    # player[J] "line 2570"
    if BURN4 < feetSec[curCar]:
        jump f1360
    jump f1410

label f2610:
    # player[J] "line 2610"
    # REM: NEW POWER & ACCEL ROUTINE
    # REM: GO TO 1610 FOR SPEED COMPUTE AFTER THIS RTN
    if dispRPM[curCar] > (1000 / engineStats[curCar][6]):
        jump f2650

label f2620:
    # player[J] "line 2620"
    $ engineStats[curCar][7] = engineStats[curCar][6] * engineStats[curCar][5] / 1000 + engineStats[curCar][4] * engineStats[curCar][0] / 1000
    jump f2810

label f2650:
    # player[J] "line 2650"
    if dispRPM[curCar] > engineStats[curCar][6]:
        jump f2710

label f2660:
    # player[J] "line 2660"
    $ engineStats[curCar][7] = ((dispRPM[curCar] / engineStats[curCar][6]) * engineStats[curCar][5]) + ((dispRPM[curCar] / engineStats[curCar][4]) * engineStats[curCar][0])

label f2670:
    # player[J] "line 2670"
    if TR[curCar] == "PG":
        jump f2810

label f2680:
    # player[J] "line 2680"
    if engineStats[curCar][7] < engineStats[curCar][2] * 1.1:
        $ engineStats[curCar][7] = engineStats[curCar][2] * 1.1
    jump f2810

label f2710:
    # player[J] "line 2710"
    if dispRPM[curCar] > engineStats[curCar][4]:
        jump f2760

label f2720:
    # player[J] "line 2720"
    $ PT1 = engineStats[curCar][5] / engineStats[curCar][2]

label f2721:
    # player[J] "line 2721"
    if PT1 > .95:
        $ PT1 = .95

label f2722:
    # player[J] "line 2722"
    if PT1 < .8:
        $ PT1 = .8

label f2723:
    # player[J] "line 2723"
    $ PT2 = 1 - PT1

label f2725:
    # player[J] "line 2725"
    $ engineStats[curCar][7] = engineStats[curCar][5] - ((engineStats[curCar][5] * PT2) * (dispRPM[curCar] / engineStats[curCar][4]))

label f2730:
    # player[J] "line 2730"
    $ engineStats[curCar][7] = engineStats[curCar][7] + (((dispRPM[curCar] / engineStats[curCar][4]) * (dispRPM[curCar] / engineStats[curCar][4])) * engineStats[curCar][0])
    jump f2810

label f2760:
    # player[J] "line 2760"
    $ engineStats[curCar][7] = engineStats[curCar][5] - ((engineStats[curCar][5] * ((dispRPM[curCar] - engineStats[curCar][6]) / engineStats[curCar][6])) * ((engineStats[curCar][0] / engineStats[curCar][2] * (dispRPM[curCar] / (engineStats[curCar][6] * 1.2)))))

label f2770:
    # player[J] "line 2770"
    $ engineStats[curCar][7] = engineStats[curCar][7] + (engineStats[curCar][0] - ((engineStats[curCar][0] * ((dispRPM[curCar] - engineStats[curCar][4]) / engineStats[curCar][4]))) * ((engineStats[curCar][0] / engineStats[curCar][2]) * .99))

label f2810:
    # player[J] "line 2810"
    if feetSec[curCar] > 66:
        $ WR = .24 + (feetSec[curCar] / 1000)
    else:
        jump f2880

label f2820:
    # player[J] "line 2820"
    if feetSec[curCar] > 99:
        $ WR = .45 + (feetSec[curCar] / 1000)

label f2830:
    # player[J] "line 2830"
    if feetSec[curCar] > 119:
        $ WR = .55 + (feetSec[curCar] / 1000)

label f2840:
    # player[J] "line 2840"
    if feetSec[curCar] > 138:
        $ WR = .65 + (feetSec[curCar] / 1000)

label f2850:
    # player[J] "line 2850"
    if feetSec[curCar] > 147:
        $ WR = .75 + (feetSec[curCar] / 1000)

label f2860:
    # player[J] "line 2860"
    if feetSec[curCar] > 157:
        $ WR = .85 + (feetSec[curCar] / 1000)

label f2870:
    # player[J] "line 2870"
    if feetSec[curCar] > 169:
        $ WR = .95 + (feetSec[curCar] / 1000)

label f2880:
    # player[J] "line 2880"
    if feetSec[curCar] <= 66:
        $ WR = .12 + (feetSec[curCar] / 1000)

label f2890:
    # player[J] "line 2890"
    if engineStats[curCar][7] > (engineStats[curCar][2] * 1.5):
        jump f2910
    jump f2930

label f2910:
    # player[J] "line 2910"
    $ accel = ((engineStats[curCar][7] *1.33) * (E[curCar] * (2.2 / D[curCar]))) / (( weight[curCar][0] / 8) + (feetSec[curCar] * WR))
    jump f2950

label f2930:
    # player[J] "line 2930"
    $ accel = ((engineStats[curCar][7] + (engineStats[curCar][2] / 2)) * (E[curCar] * (2.2 / D[curCar]))) / (( weight[curCar][0] / 8) + (feetSec[curCar] * WR))

label f2950:
    # player[J] "line 2950"
    $ feetSec[curCar] = feetSec[curCar] + accel * (.099 - (feetSec[curCar] * .00028))
    jump f1560

label f11000:
    call f11500
    $ RVL = 10

    player[playerWin] "Congratulations! You have won race [race]."

    if round == 1:
        return

label f11025: # maybe should only be done if round > 2
    if LWINT < lowTime:
        $ RVL = RVL + 10
    if round < 4:
        return

label f11064:# only continue if round == 4
    # OPEN "O",#1,"WINNERS1.DG1"
    "lines 11064 to 11084, write WINNERS1.DG1"

label f11072:
    if SWT18 == -1:
        jump f11085
    # else:WRITE #1,18,SWT18

label f11074:
    if SWT17 == -1:
        jump f11085
    # else:WRITE #1,17,SWT17

label f11076:
    if SWT16 == -1:
        jump f11085
    # else:WRITE #1,16,SWT16

label f11078:
    if SWT15 == -1:
        jump f11085
    # else:WRITE #1,15,SWT15

label f11080:
    if SWT14 == -1:
        jump f11085
    # else:WRITE #1,14,SWT14

label f11082:
    if SWT13 == -1:
        jump f11085
    # else:WRITE #1,13,SWT13

label f11085:
    # OPEN "O",#1,"P1-END.DG1"
    "lines 11085 to 11085, write P1-END.DG1"

label f11096:
    # INPUT "END OF PHASE 1 - PRESS <ENTER> TO LOAD PHASE 2 OR 'E' TO END";I$
    "End of Phase 1."
    return

label f11100:
    # PRINT N$(PL)
    $ curCar = phase % 2
    # these seem to not be used anywhere and should be moved to the stats screen

label f11110:
    player[curCar] "  YOU HAVE $[savings[curCar]] IN SAVINGS; THE CAR IS NOW VALUED AT $[carVal[curCar]]"

label f11120:
    player[curCar] "  YOUR NET WORTH IS $[savings[curCar]]+[carVal[curCar]]"
    return

label f11500:
    call f11900

label f11501:
    if SWT18 > 0:
        "FIRST PERSON UNDER 18 SECONDS IS [player[SWT18]]"

label f11502:
    if SWT17 > 0:
        "FIRST PERSON UNDER 17 SECONDS IS [player[SWT17]]"

label f11504:
    if SWT16 > 0:
        "FIRST PERSON UNDER 16 SECONDS IS [player[SWT16]]"

label f11505:
    if SWT15 > 0:
        "FIRST PERSON UNDER 15 SECONDS IS [player[SWT15]]"

label f11507:
    if SWT14 > 0:
        "FIRST PERSON UNDER 14 SECONDS IS [player[SWT14]]"

label f11508:
    if SWT13 > 0:
        "FIRST PERSON UNDER 13 SECONDS IS [player[SWT13]]"

label f11509:
    if SWT12 > 0:
        "FIRST PERSON UNDER 12 SECONDS IS [player[SWT12]]"

label f11512:
    if WS > HIS:
        $ HIS = WS
        jump f11515
        $ PV[playerWin] = PV[playerWin] + .5

label f11513:
    if LWINT < lowTime:
        $ lowTime = LWINT
        jump f11515
        $ PV[playerWin] = PV[playerWin] + .5
    jump f11522

label f11515:
    $ carVal[playerWin] = carVal[playerWin] + RVL

label f11516:
    $ PV[playerWin] = PV[playerWin] + 1

label f11522:
    if HIS > HS[curCar]:
        $ HS[curCar] = HIS
        jump f11525

label f11523:
    if lowTime < LT[curCar]:
        $ LT[curCar] = lowTime
        jump f11525
    jump f11528

label f11525:
    $ carVal[playerWin] = carVal[playerWin] + RVL

label f11528:
    "END OF RACE [round]"
    return

label f11700:
    if W[curCar]>6.99:
        # RETURN
        return

label f11702:
    if savings[curCar]<=100:
        # RETURN
        return

label f11705:
    player[curCar] "YOU WILL HAVE THE OPTION OF CHANGING YOUR REAR END RATIO AND YOU CAN BUY A      PAIR OF 'CHEATER SLICKS'."

label f11710:
    player[curCar] "YOU CAN BUY CHEATER SLICKS FOR $100"

label f11720:
    player[curCar] "DO YOU WANT TO BUY THEM NOW? (if 'yes' jump f11800, if 'no' jump f11740)"

label f11740:
    $ W[curCar] = 7
    $ savings[curCar] = savings[curCar] - 100

label f11750:
    player[curCar] "YOU HAVE CHEATER SLICKS AND A $[savings[curCar]] TO SPEND"

label f11760:
    if JOB[curCar] == "B":
        jump f11780

label f11770:
    if JOB[curCar] == "D":
        jump f11780
    else:
        jump f11790

label f11780:
    $ modsCost = 60
    jump f11800

label f11790:
    $ modsCost = 125

label f11800:
    $ modsCost = 125

label f11802:
    if savings[curCar] < 0:
        return

label f11805:
    $ modsUpper = modsCost * 1.4
    player[curCar] "YOU HAVE $[savings[curCar]] AND A [gearRatios[curCar][4]] RATIO; ANOTHER RATIO WILL COST BETWEEN $[modsCost] AND $[modsUpper]."

label f11810:
    player[curCar] "DO YOU WANT TO CHANGE REAR END RATIOS? (if 'yes' jump f11830, if 'no' return)"

label f11830:
    player[curCar] "WHAT IS THE REAR END RATIO YOU WOULD LIKE? (line 11830)"

label f11840:
    if L5W < 4.69:
        jump f11892

label f11850:
    player[curCar] "[L5W] IS PRETTY HIGH FOR STREET USE - DO YOU WANT TO TRY ANOTHER?(Y/N) (if 'yes jump f11800, if 'no' jump f11880)"

label f11870:
    if I == "Y":
        jump f11800

label f11880:
    $ carVal[curCar] = carVal[curCar] - 50

label f11890:
    $ modsCost = modsCost * 1.3

label f11892:
    $ savings[curCar] = savings[curCar] - modsCost

label f11895:
    $ gearRatios[curCar][4] = L5W
    return

label f11900:
    if lowTime == 0:
        $ lowTime = 99.99

label f11901:
    if TSAV == 0:
        $ TSAV = 99.99

label f11902:
    if LWINT < lowTime:
        $ lowTime = LWINT

label f11905:
    if LWINT < TSAV:
        $ TSAV = LWINT
    else:
        return

label f11910:
    if SWT18 > 0:
        jump f11915

label f11912:
    if LWINT < 18:
        $ SWT18 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 50
        $ PV[playerWin] = PV[playerWin] + .5

label f11915:
    if SWT17 > 0:
        jump f11925

label f11920:
    if LWINT < 17:
        $ SWT17 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 75
        $ RVL = RVL + 25
        $ PV[playerWin] = PV[playerWin] + 1

label f11925:
    if SWT16 > 0:
        jump f11935

label f11930:
    if LWINT < 16:
        $ SWT16 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 75
        $ RVL = RVL + 25
        $ PV[playerWin] = PV[playerWin] + 1.3

label f11935:
    if SWT15 > 0:
        jump f11950

label f11940:
    if LWINT < 15:
        $ SWT15 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 100
        $ RVL = RVL + 50
        $ PV[playerWin] = PV[playerWin] + 1.8

label f11945:
    if LWINT > 14:
        return

label f11950:
    if SWT14 > 0:
        jump f11970

label f11955:
    if LWINT < 14:
        $ SWT14 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 125
        $ RVL = RVL + 100
        $ PV[playerWin] = PV[playerWin] + 2.1

label f11960:
    if LWINT > 13:
        return

label f11970:
    if SWT13 > 0:
        jump f11990

label f11975:
    if LWINT < 13:
        $ SWT13 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 150
        $ RVL = RVL + 150
        $ PV[playerWin] = PV[playerWin] + 3

label f11980:
    if LWINT > 12:
        return

label f11990:
    if SWT12 > 0:
        return

label f11992:
    if LWINT < 12:
        $ SWT12 = LWIN
        $ carVal[playerWin] = carVal[playerWin] + 200
        $ RVL = RVL + 200
        $ PV[playerWin] = PV[playerWin] + 4
    return

label gears:
    if  numGears[curCar] == 4:
        $ E[curCar] = gearRatios[curCar][3] * gearRatios[curCar][4]
    elif  numGears[curCar] == 3:
        $ E[curCar] = gearRatios[curCar][2] * gearRatios[curCar][4]
    elif  numGears[curCar] == 2:
        $ E[curCar] = gearRatios[curCar][1] * gearRatios[curCar][4]
    elif  numGears[curCar] == 1:
        $ E[curCar] = gearRatios[curCar][0] * gearRatios[curCar][4]

    return
