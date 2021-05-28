label race:

    $ curCar = phase % 2
    $ lane = 1
    while curCar == 1 or curCar == 0:
        if TR[curCar] == "SLIP":
            $ TR[curCar] = ""
        if TR[curCar] == "PG":
            $ gearRatios[curCar][4] = 3.62
            call f10020
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
    if phase % 2 == 0:
        "[engineStats[0][0]] HP  [engineStats[0][2]] CI [weight[0][0]] LBS  [gearRatios[0][5]] | LOW TIME  [lowTime] | [engineStats[1][0]] HP  [engineStats[1][2]] CI [weight[1][0]] LBS  [gearRatios[1][5]]"
    elif phase % 2 == 1:
        "[engineStats[1][0]] HP  [engineStats[1][2]] CI [weight[1][0]] LBS  [gearRatios[1][5]] | LOW TIME  [lowTime] | [engineStats[0][0]] HP  [engineStats[0][2]] CI [weight[0][0]] LBS  [gearRatios[0][5]]"

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
            if phase % 2 == 0:
                "[mph1] MPH [distance[0]] FEET [dispRPM[0]] RPM ||     [seconds].[tenthSec][T2]     ||[mph2] MPH  [distance[1]] FEET [dispRPM[1]] RPM"
            elif phase % 2 == 1:
                "[mph2] MPH [distance[1]] FEET [dispRPM[1]] RPM ||     [seconds].[tenthSec][T2]     ||[mph1] MPH  [distance[0]] FEET [dispRPM[0]] RPM"

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

    $ seconds = 0
    $ tenthSec = 0
    $ raceLoop = 0
    $ T2 = 0
    $ dispRPM[0] = 0
    $ dispRPM[1] = 0
    $ rpm = 0
    $ Q[1] = 0
    $ Q[0] = 0
    $ feetSec[1] = 0
    $ feetSec[0] = 0
    $ maxAccel[1] = 0
    $ maxAccel[0] = 0
    $ distance[1] = 0
    $ distance[0] = 0
    $ engineStats[1][7] = 0
    $ engineStats[0][7] = 0
    $ weight[1][1] = 3355
    $ weight[0][1] = 2791
    $ BURN1 = 0
    $ BURN2 = 0
    $ BURN3 = 0
    $ BURN4 = 0
    $ E[0] = 0
    $ E[1] = 0
    $ accel = 0
    $ BW1 = 0
    $ BW2 = 0
    $ BW3 = 0
    $ BW4 = 0
    $ numGears[0] = 3
    $ numGears[1] = 3
    $ gearRatios = [[-1,1,1.76,3.11,0,3.78],[-1,1,1.66,2.94,0,4.11]]

    return

label f1260:
    $ tempE = 60 * E[curCar]
    $ tempD = math.pi * D[curCar]
    $ se = feetSec[curCar] * tempE
    $ rpm = se / tempD
    $ dispRPM[curCar] = rpm
    $ dispRPM[curCar] = rpm
    jump f2390

label f1360:
    if phase % 2 == 0:
        if curCar == 0:
            "STOPS BURNING AT  [distance[0]] FEET   ||     [seconds].[tenthSec][T2]     ||            [distance[1]] FEET"
        elif curCar == 1:
            "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2]     ||STOPS BURNING AT  [distance[1]] FEET"
    elif phase % 2 == 1:
        if curCar == 0:
            "           [distance[1]] FEET          ||     [seconds].[tenthSec][T2]     ||STOPS BURNING AT  [distance[0]] FEET"
        elif curCar == 1:
            "STOPS BURNING AT  [distance[1]] FEET   ||     [seconds].[tenthSec][T2]     ||            [distance[0]] FEET"

label f1380:
    $ Q[curCar] = 1
    jump f2610

label f1410:
    # new burnout routine
    # REM: BURN ACCEL
    $ accel = ((engineStats[curCar][0] + engineStats[curCar][2]) * (E[curCar] * (2.9 / D[curCar]))) / (( weight[curCar][0] / 12) + (feetSec[curCar] * .7))
    if accel > W[curCar] * 5:
        $ accel = W[curCar] * 4.5
    $ XX1 = 6000 * engineStats[curCar][0] / engineStats[curCar][2]
    if seconds < 2:
        $ accel = accel * 1.2 * 3000 /  weight[curCar][0]
    if dispRPM[curCar] > XX1 * .34:
        jump f1490

label f1470:
    $ feetSec[curCar] = feetSec[curCar] + accel * .037
    $ feetSec[curCar] = feetSec[curCar] + accel * ((dispRPM[curCar] / (5 * XX1 / 6)) * .025)
    jump f1540

label f1490:
    if dispRPM[curCar] > (5 * XX1 / 6):
        jump f1510

label f1500:
    $ feetSec[curCar] = feetSec[curCar] + accel * ((dispRPM[curCar] / (5 * XX1 / 6)) * .053)
    jump f1540

label f1510:
    if dispRPM[curCar] =< XX1:
        jump f1530

label f1520:
    $ feetSec[curCar] = feetSec[curCar] + accel * ((.049 * (XX1 / dispRPM[curCar])))
    jump f1560

label f1530:
    $ feetSec[curCar] = feetSec[curCar] + accel * ((.052 * ((5 * XX1 / 6) / dispRPM[curCar])))

label f1540:
    $ feetSec[curCar] = feetSec[curCar] + (accel * ((dispRPM[curCar] / XX1) * .053))

label f1560:
    if maxAccel[curCar] < 1 or maxAccel[curCar] > 1:
        jump f1590

label f1570:
    $ distance[curCar] = distance[curCar] + feetSec[curCar] * .075
    return

label f1590:
    $ distance[curCar] = distance[curCar] + feetSec[curCar] * .098
    return

label f1630:
    if distance[0] > distance[1]:
        jump f1780

    $ T3 = (distance[1] - 5280 / 4) / feetSec[1]
    $ seconds = seconds + (tenthSec / 10) - T3
    $ distance[1] = distance[1] - feetSec[1] * T3
    $ distance[0] = distance[0] - feetSec[0] * T3
    $ distance[1] = distance[1] - feetSec[1] * T3

    if phase % 2 == 0:
        "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2] --->||  LANE 2 WINNER"
        $ LWIN = 2 # the player in lane 2 won
    elif phase % 2 == 1:
        "       LANE  1   WINNER       ||<--- [seconds].[tenthSec][T2]     ||            [distance[0]] FEET"
        $ LWIN = 1
    $ racing = False
    $ raceLoop = 20
    $ playerWin = 1
    $ WS = feetSec[1] * 3600 / 5280
    $ WIN2 = WIN2 + 1
    $ LWINT = seconds
    $ mph1 = feetSec[0] * 3600 / 5280
    $ mph2 = feetSec[1] * 3600 / 5280
    if phase % 2 == 0:
        " [mph1] MPH    [dispRPM[0]] RPM       ||               ||   [mph2] MPH  [dispRPM[1]] RPM"
    elif phase % 2 == 1:
        " [mph2] MPH    [dispRPM[1]] RPM       ||               ||   [mph1] MPH  [dispRPM[0]] RPM"

label f1710:
    $ numGears[0] = NTR[0]
    $ numGears[1] = NTR[1]
    if phase % 2 == 0:
        $ gearRatios[0][4] = L14
        $ gearRatios[0][3] = L13
        $ gearRatios[1][4] = L24
        $ gearRatios[1][3] = L23
    elif phase % 2 == 1:
        $ gearRatios[0][4] = L24
        $ gearRatios[0][3] = L23
        $ gearRatios[1][4] = L14
        $ gearRatios[1][3] = L13
    $ TR[0] = TR1
    $ TR[1] = TR2

    jump f11000

label f1780:
    $ T3 = (distance[0] - 5280 / 4) / feetSec[0]
    $ seconds = seconds + (tenthSec / 10) - T3
    $ distance[0] = 5200 / 4
    $ distance[1] = distance[1] - feetSec[1] * T3
    $ distance[0] = distance[0] - feetSec[0] * T3
    if phase % 2 == 0:
        "       LANE  1   WINNER       ||<--- [seconds].[tenthSec][T2]     ||            [distance[1]] FEET"
        $ LWIN = 1
    elif phase % 2 == 1:
        "           [distance[1]] FEET          ||     [seconds].[tenthSec][T2] --->||  LANE 2 WINNER"
        $ LWIN = 2
    $ racing = False
    $ raceLoop = 20
    $ playerWin = 0
    $ mph1 = feetSec[0] * 3600 / 5280
    $ mph2 = feetSec[1] * 3600 / 5280
    if phase % 2 == 0:
        "[mph1] MPH  [dispRPM[0]] RPM          ||               ||    [mph2] MPH   [dispRPM[1]] RPM"
    elif phase % 2 == 1:
        "[mph2] MPH  [dispRPM[1]] RPM          ||               ||    [mph1] MPH   [dispRPM[0]] RPM"
    $ WS = feetSec[0] * 3600 / 5280
    $ WIN1 = WIN1 + 1
    $ LWINT = seconds
    jump f1710
    return

label f1970:
    if gearRatios[curCar][2] > 2.5:
        $ gearRatios[curCar][2] = gearRatios[curCar][2] - ((dispRPM[curCar] / (engineStats[curCar][4] - 500)) * (1.9 / gearRatios[curCar][2]) * .2)
    else:
        $ gearRatios[curCar][2] = gearRatios[curCar][2] - .02
        jump f2040 # this wasn't at this level but i believe it will only be executed in this situation

label f2010:
    if PGS[curCar] = 1:
        jump f2030
    $ PGS[curCar] = 1
    $ gearRatios[curCar][1] = 1.18

label f2030:
    if gearRatios[curCar][1] > 1.07:
        $ gearRatios[curCar][1] = gearRatios[curCar][1] - .001

label f2040:
    $ E[curCar] = gearRatios[curCar][numGears[curCar]] * gearRatios[curCar][5]
    return

label f2064:
    if dispRPM[0] == 0:
        call gears
        jump f2174
    call checkTR
    if dispRPM[curCar] < engineStats[curCar][1] * 1.0001:
        jump f1260
    if numGears[0] > 1:
        jump f2115
    if dispRPM[0] > (engineStats[0][1] * 1.07):
        jump f2190
    if numGears[0] == 1:
        jump f1260

label f2115:
    if distance[1] > 1320:
        jump f1780
    $ mph = 3600 * feetSec[0] / 5280
    if curCar == 0:
        if phase % 2 == 0:
            "SHIFTING - [dispRPM[0]] RPM, [mph] MPH  ||     [seconds].[tenthSec][T2]     ||            [distance[1]] FEET "
        elif phase % 2 == 1:
            "           [distance[1]] FEET          ||     [seconds].[tenthSec][T2]     ||SHIFTING - [dispRPM[0]] RPM, [mph] MPH "
    $ numGears[curCar] -= 1
    call gears

label f2174:
    if TR[curCar] != "":
        jump f2176
    if dispRPM[0] == 0:
        if E[0] < 11:
            $ TR[curCar] = "SLIP"

label f2176:
    if TR[curCar] == "SLIP":
        call f6000
    jump f1260

label f2190:
    $ mph = feetSec[0] * 3600 / 5280
    "CAR #1 OVERREVED AT [dispRPM[0]]RPM[distance[0]] FT.[mph] MPH"
    "CAR #1 -- GEAR =[numGears[0]] FINAL= [E[0]]  J=[curCar]"
    $ engineStats[0][0] = 0
    jump f1260

label f2224:
    if rpm == 0:
        call gears
        jump f2335
    call checkTR
    if dispRPM[curCar] < engineStats[curCar][1] * 1.0001:
        jump f1260
    if numGears[1] > 1:
        jump f2275
    if dispRPM[1] > (engineStats[1][1] * 1.07):
        jump f2350
    if numGears[1] == 1:
        jump f1260

label f2275:
    if distance[0] > 1320:
        jump f1780
    $ mph = 3600 * feetSec[1] / 5280
    if curCar == 1:
        if phase % 2 == 0:
            "           [distance[0]] FEET          ||     [seconds].[tenthSec][T2]     ||SHIFTING - [dispRPM[1]] RPM, [mph] MPH "
        elif phase % 2 == 1:
            "SHIFTING - [dispRPM[1]] RPM, [mph] MPH  ||     [seconds].[tenthSec][T2]     ||            [distance[0]] FEET "
    $ numGears[curCar] -= 1
    call gears

label f2335:
    if dispRPM[1] == 0:
        if E[1] < 11:
            $ TR[curCar] = "SLIP"
    if TR[curCar] == "SLIP":
        call f6000
    jump f1260

label f2350:
    $ mph = feetSec[1] * 3600 / 5280
    "CAR #2 OVERREVED AT [dispRPM[1]]RPM[distance[1]] FT.[mph] MPH"
    "CAR #2 -- GEAR =[numGears[1]] FINAL= [E[1]]  J=[curCar]"
    $ engineStats[1][0] = 0
    jump f1260

label f2390:
    if Q[curCar] <> 0:
        jump f1380
    if Q[curCar] <> 0:
        jump f1380
    $ BW1 = gearRatios[curCar][numGears[curCar]] * gearRatios[curCar][5]
    if BW1 > 11:
        jump f2500
    $ BW2 = 14 * (engineStats[curCar][0] + engineStats[curCar][2])
    $ BW3 = engineStats[curCar][0] / engineStats[curCar][2]
    $ BW4 = engineStats[curCar][2] /  weight[curCar][0] * .085
    if BW3 > BW4:
        jump f2470
    if distance[curCar] > (50 -  weight[curCar][0] / 100):
        jump f2470
    else:
        $ BURN1 = BW2 * BW4
    if seconds > 2:
        jump f2470
    else:
        jump f2510

label f2470:
    $ BURN1 = BW2 * BW3
    jump f2510

label f2500:
    $ BURN1 = (engineStats[curCar][0] + engineStats[curCar][2]) * 11

label f2510:
    $ BURN2 = BURN1 * 2.5 / D[curCar]
    $ BURN3 = (BURN2 -  weight[curCar][0]) / 100
    $ BURN4 = BURN3 - W[curCar]
    if TR[curCar] == "PG":
        jump f2560
    jump f2570

label f2560:
    $ BURN4 = (BURN3 - W[curCar]) / 3

label f2570:
    if BURN4 < feetSec[curCar]:
        jump f1360
    jump f1410

label f2610:
    # REM: NEW POWER & ACCEL ROUTINE
    # REM: GO TO 1610 FOR SPEED COMPUTE AFTER THIS RTN
    if dispRPM[curCar] > (1000 / engineStats[curCar][6]):
        jump f2650
    $ engineStats[curCar][7] = engineStats[curCar][6] * engineStats[curCar][5] / 1000 + engineStats[curCar][4] * engineStats[curCar][0] / 1000
    jump f2810

label f2650:
    if dispRPM[curCar] > engineStats[curCar][6]:
        jump f2710
    $ engineStats[curCar][7] = ((dispRPM[curCar] / engineStats[curCar][6]) * engineStats[curCar][5]) + ((dispRPM[curCar] / engineStats[curCar][4]) * engineStats[curCar][0])
    if TR[curCar] == "PG":
        jump f2810
    if engineStats[curCar][7] < engineStats[curCar][2] * 1.1:
        $ engineStats[curCar][7] = engineStats[curCar][2] * 1.1
    jump f2810

label f2710:
    if dispRPM[curCar] > engineStats[curCar][4]:
        jump f2760
    $ PT1 = engineStats[curCar][5] / engineStats[curCar][2]
    if PT1 > .95:
        $ PT1 = .95
    if PT1 < .8:
        $ PT1 = .8
    $ PT2 = 1 - PT1
    $ engineStats[curCar][7] = engineStats[curCar][5] - ((engineStats[curCar][5] * PT2) * (dispRPM[curCar] / engineStats[curCar][4]))
    $ engineStats[curCar][7] = engineStats[curCar][7] + (((dispRPM[curCar] / engineStats[curCar][4]) * (dispRPM[curCar] / engineStats[curCar][4])) * engineStats[curCar][0])
    jump f2810

label f2760:
    $ engineStats[curCar][7] = engineStats[curCar][5] - ((engineStats[curCar][5] * ((dispRPM[curCar] - engineStats[curCar][6]) / engineStats[curCar][6])) * ((engineStats[curCar][0] / engineStats[curCar][2] * (dispRPM[curCar] / (engineStats[curCar][6] * 1.2)))))
    $ engineStats[curCar][7] = engineStats[curCar][7] + (engineStats[curCar][0] - ((engineStats[curCar][0] * ((dispRPM[curCar] - engineStats[curCar][4]) / engineStats[curCar][4]))) * ((engineStats[curCar][0] / engineStats[curCar][2]) * .99))

label f2810:
    if feetSec[curCar] > 66:
        $ WR = .24 + (feetSec[curCar] / 1000)
    else:
        jump f2880
    if feetSec[curCar] > 99:
        $ WR = .45 + (feetSec[curCar] / 1000)
    if feetSec[curCar] > 119:
        $ WR = .55 + (feetSec[curCar] / 1000)
    if feetSec[curCar] > 138:
        $ WR = .65 + (feetSec[curCar] / 1000)
    if feetSec[curCar] > 147:
        $ WR = .75 + (feetSec[curCar] / 1000)
    if feetSec[curCar] > 157:
        $ WR = .85 + (feetSec[curCar] / 1000)
    if feetSec[curCar] > 169:
        $ WR = .95 + (feetSec[curCar] / 1000)

label f2880:
    if feetSec[curCar] <= 66:
        $ WR = .12 + (feetSec[curCar] / 1000)
    if engineStats[curCar][7] > (engineStats[curCar][2] * 1.5):
        jump f2910
    jump f2930

label f2910:
    $ accel = ((engineStats[curCar][7] *1.33) * (E[curCar] * (2.2 / D[curCar]))) / (( weight[curCar][0] / 8) + (feetSec[curCar] * WR))
    jump f2950

label f2930:
    $ accel = ((engineStats[curCar][7] + (engineStats[curCar][2] / 2)) * (E[curCar] * (2.2 / D[curCar]))) / (( weight[curCar][0] / 8) + (feetSec[curCar] * WR))

label f2950:
    $ feetSec[curCar] = feetSec[curCar] + accel * (.099 - (feetSec[curCar] * .00028))
    jump f1560

label f6000:
    #REM:SLIP RTN
    $ curNumGears = numGears[curCar]
    if weight[curCar][1] == 0:
        $ weight[curCar][1] = gearRatios[curCar][curNumGears]
    if dispRPM[curCar] == 0:
        $ gearRatios[curCar][curNumGears] = 11 / gearRatios[curCar][5]
    else:
        jump f6050
    $ E[curCar] = gearRatios[curCar][curNumGears] * gearRatios[curCar][5]
    if dispRPM[curCar] == 0:
        return

label f6050:
    $ curNumGears = numGears[curCar] # it is possible this doesn't need to be separate. maybe i just forgot how to write an array in python
    if dispRPM[curCar] < engineStats[curCar][6] / 3:
        $ gearRatios[curCar][curNumGears] = gearRatios[curCar][curNumGears] - .003
        jump f6065
    if dispRPM[curCar] < engineStats[curCar][6] - 100:
        $ gearRatios[curCar][curNumGears] = gearRatios[curCar][curNumGears] - .02
        jump f6065
    if dispRPM[curCar] < (engineStats[curCar][6] + engineStats[curCar][4]) / 2:
        $ gearRatios[curCar][curNumGears] = gearRatios[curCar][curNumGears] - .04
    else:
        $ gearRatios[curCar][curNumGears] = gearRatios[curCar][curNumGears] - .06

label f6065:
    $ curNumGears = numGears[curCar]
    if gearRatios[curCar][curNumGears] < weight[curCar][1] + .06:
        $ gearRatios[curCar][curNumGears] = weight[curCar][1]
        $ TR[curCar] = " "
    $ E[curCar] = gearRatios[curCar][curNumGears] * gearRatios[curCar][5]
    return

label f6100:
    #REM:TURBO HYDRO
    if numGears[curCar] < 3:
        return
    if TR[curCar] == "TH1":
        jump f6140
    $ TR[curCar] = "TH1"
    $ gearRatios[curCar][3] = 5.25
    return

label f6140:
    $ gearRatios[curCar][3] = gearRatios[curCar][3] - (dispRPM[curCar] / 10000)
    if gearRatios[curCar][3] > 2.5:
        jump f6160
    $ TR[curCar] = "TH2"
    $ gearRatios[curCar][3] = 2.5

label f6160:
    $ E[curCar] = gearRatios[curCar][numGears[curCar]] * gearRatios[curCar][5]
    return

label f6200:
    #REM: PG REVISION
    if numGears[curCar] == 1:
        jump f6250
    if gearRatios[curCar][2] == 1.89:
        jump f6290
    if dispRPM[curCar] > 1200:
        jump f6225
    $ gearRatios[curCar][2] = 3.82
    jump f6290

label f6225:
    $ gearRatios[curCar][2] = 1.82 + (2 - (2 * (dispRPM[curCar] / ((engineStats[curCar][6] + 5500) / 2))))
    if gearRatios[curCar][2] > 1.89:
        jump f6290
    $ gearRatios[curCar][2] = 1.89
    $ gearRatios[curCar][1] = 1
    jump f6290

label f6250:
    if gearRatios[curCar][1] == 1.05:
        jump f6290
    if gearRatios[curCar][1] == 1:
        $ gearRatios[curCar][1] = 1.18
    $ gearRatios[curCar][1] = gearRatios[curCar][1] - (dispRPM[curCar] / 120000) # this was 120000!
    if gearRatios[curCar][1] < 1.05:
        $ gearRatios[curCar][1] = 1.05

label f6290:
    $ E[curCar] = gearRatios[curCar][numGears[curCar]] * gearRatios[curCar][5]
    return

label f6300:
    #REM: HYD
    if weight[curCar][1] == 1:
        return
    if weight[curCar][1] == 4:
        jump f6335
    $ weight[curCar][2] = engineStats[curCar][1]
    if gearRatios[curCar][3] > 2.5:
        $ engineStats[curCar][1] = engineStats[curCar][6] * .8
    else:
        $ engineStats[curCar][1] = engineStats[curCar][6] * 1.19
    $ weight[curCar][1] = 4
    return

label f6335:
    if numGears[curCar] == 3:
        $ engineStats[curCar][1] = O[curCar][2]
    else:
        return
    $ weight[curCar][1] = 1
    return

label f10010:
    #REM: CHEV TRANSMISSION RATIOS
    "       PLEASE INPUT THE 1ST GEAR RATIO OF THE TRANSMISSION OF YOUR CHOICE (line f10010)"#:INPUT L(L,4)

label f10020:
    if gearRatios[[curCar][4]] == 2.94:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][2]] = 1.68
        $ gearRatios[[curCar][3]] = 2.94
    elif gearRatios[[curCar][4]] == 3.06:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][3]] = 1.63
        $ gearRatios[[curCar][2]] = 1.05
        $ gearRatios[[curCar][1]] = 1
        $ weight[[curCar][0]] = weight[[curCar][0]] + 150
    elif gearRatios[[curCar][4]] == 2.85:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.35
        $ gearRatios[[curCar][3]] = 2.02
        $ weight[[curCar][0]] = weight[[curCar][0]] + 25
    elif gearRatios[[curCar][4]] == 2.47:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][2]] = 1.53
        $ gearRatios[[curCar][3]] = 2.47
    elif gearRatios[[curCar][4]] == 2.58:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][2]] = 1.48
        $ gearRatios[[curCar][3]] = 2.58
    elif gearRatios[[curCar][4]] == 3.62:
        $ numGears[curCar] = 2
        $ gearRatios[[curCar][2]] = 1.1
        $ gearRatios[[curCar][3]] = 3.62 # original code has this as index 2 but should it be index 3? line 10060
        $ weight[[curCar][0]] = weight[[curCar][0]] + 95
        $ TR[curCar] = "PG"
    elif gearRatios[[curCar][4]] == 3.96:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.53
        $ gearRatios[[curCar][3]] = 2.63
        $ weight[[curCar][0]] = weight[[curCar][0]] + 198
        $ TR[curCar] = "HYD"
    elif gearRatios[[curCar][4]] == 3.97:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.33
        $ gearRatios[[curCar][3]] = 2.23
        $ weight[[curCar][0]] = weight[[curCar][0]] + 198
        $ TR[curCar] = "HYD"
    elif gearRatios[[curCar][4]] == 2.5:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][2]] = 1.55
        $ gearRatios[[curCar][3]] = 2.5
        $ weight[[curCar][0]] = weight[[curCar][0]] + 125
        $ TR[curCar] = "TH"
    elif gearRatios[[curCar][4]] == 2.21:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][2]] = 1.33
        $ gearRatios[[curCar][3]] = 2.21
    elif gearRatios[[curCar][4]] == 2.2:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.31
        $ gearRatios[[curCar][3]] = 1.64
        $ weight[[curCar][0]] = weight[[curCar][0]] + 25
    elif gearRatios[[curCar][4]] == 2.54:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.66
        $ gearRatios[[curCar][3]] = 1.91
        $ weight[[curCar][0]] = weight[[curCar][0]] + 25
    elif gearRatios[[curCar][4]] == 2.56:
        $ numGears[curCar] = 4
        $ gearRatios[[curCar][2]] = 1.48
        $ gearRatios[[curCar][3]] = 1.91
        $ weight[[curCar][0]] = weight[[curCar][0]] + 25
    elif gearRatios[[curCar][4]] == 2.65:
        $ numGears[curCar] = 3
        $ gearRatios[[curCar][1]] = 1
        $ gearRatios[[curCar][2]] = 1.51
        $ gearRatios[[curCar][3]] = 2.65
    elif gearRatios[[curCar][4]] == 2.39:
        $ gearRatios[[curCar][3]] = 2.39
        $ gearRatios[[curCar][2]] = 1.53
        $ numGears[curCar] = 3
    if gearRatios[[curCar][2]] == 0:
        jump f10010
    if gearRatios[[curCar][1]] == 0:
        $ gearRatios[[curCar][1]] = 1
    return

label f10210:
    #REM: GET ENGINE DATA
    $ SM = MFR[curCar]
    if engineStats[[curCar][2]] == 999:
        $ SM[curCar] = ""
    jump f10210

label f10235:
    $ SP1 = engineStats[[curCar][0]]
    $ SP3 = engineStats[[curCar][2]]
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
    $ engineStats[[curCar][0]] = P1
    $ engineStats[[curCar][1]] = P2
    $ engineStats[[curCar][2]] = P3
    $ engineStats[[curCar][3]] = P4
    $ engineStats[[curCar][4]] = P5
    $ engineStats[[curCar][5]] = P6
    $ engineStats[[curCar][6]] = P7
    $ NC[curCar] = NC
    $ NB[curCar] = NB
    $ CR[curCar] = CR
    $ CAM[curCar] = CAM
    $ BRTH[curCar] = BRTH

label f10450:
    "MFGR [MFGR], DISP=[P3], HP=[P1] @ [P5], TORQUE=[P6] @ [P7]"
    if engineStats[[curCar][4]] == 0:
        jump f10460
    $ CL = CL + 1
    return

label f10460:
    $ LL = LL + 1
    if LL < 23:
        jump f10500
    $ LL = 1

label f10500:
    if engineStats[[curCar][4]] > 0:
        return
    "YOU CHOSE AN INELLIGIBLE HP/DISPLACEMENT COMBINATION - TRY AGAIN"
    $ engineStats[[curCar][0]] = 0
    $ engineStats[[curCar][2]] = 0
    jump f10210

label f11000:
    call f11500
    $ RVL = 10
    player[playerWin] "Congratulations! You have won race [race]."
    if round == 1:
        return

    # maybe should only be done if round > 2
    if LWINT < lowTime:
        $ RVL = RVL + 10
    if round < 4:
        return

    # only continue if round == 4
    "lines 11064 to 11084, write WINNERS1.DG1"
    if SWT18 == -1:
        jump f11085
    if SWT17 == -1:
        jump f11085
    if SWT16 == -1:
        jump f11085
    if SWT15 == -1:
        jump f11085
    if SWT14 == -1:
        jump f11085
    if SWT13 == -1:
        jump f11085

label f11085:
    "lines 11085 to 11085, write P1-END.DG1"
    "END OF PHASE 1 - PRESS <ENTER> TO LOAD PHASE 2 OR 'E' TO END"
    "End of Phase 1."
    return

label f11500:
    call f11900
    if SWT18 > 0:
        "SWT18 [SWT18]"
        $ swt = player[SWT18]
        "FIRST PERSON UNDER 18 SECONDS IS [swt]"
    if SWT17 > 0:
        "SWT17 [SWT17]"
        $ swt = player[SWT17]
        "FIRST PERSON UNDER 17 SECONDS IS [swt]"
    if SWT16 > 0:
        "SWT16 [SWT16]"
        $ swt = player[SWT16]
        "FIRST PERSON UNDER 16 SECONDS IS [swt]"
    if SWT15 > 0:
        "SWT15 [SWT15]"
        $ swt = player[SWT15]
        "FIRST PERSON UNDER 15 SECONDS IS [swt]"
    if SWT14 > 0:
        "SWT14 [SWT14]"
        $ swt = player[SWT14]
        "FIRST PERSON UNDER 14 SECONDS IS [swt]"
    if SWT13 > 0:
        "SWT13 [SWT13]"
        $ swt = player[SWT13]
        "FIRST PERSON UNDER 13 SECONDS IS [swt]"
    if SWT12 > 0:
        "SWT12 [SWT12]"
        $ swt = player[SWT12]
        "FIRST PERSON UNDER 12 SECONDS IS [swt]"
    if WS > HIS:
        $ HIS = WS
        jump f11515
        $ PV[playerWin] = PV[playerWin] + .5
    if LWINT < lowTime:
        $ lowTime = LWINT
        jump f11515
        $ PV[playerWin] = PV[playerWin] + .5
    jump f11522

label f11515:
    $ carVal[playerWin] = carVal[playerWin] + RVL
    $ PV[playerWin] = PV[playerWin] + 1

label f11522:
    if HIS > HS[curCar]:
        $ HS[curCar] = HIS
        jump f11525
    if lowTime < LT[curCar]:
        $ LT[curCar] = lowTime
        jump f11525
    jump f11528

label f11525:
    $ carVal[playerWin] = carVal[playerWin] + RVL

label f11528:
    "END OF RACE [round]"
    return

label f11740:
    $ W[curCar] = 7
    $ savings[curCar] = savings[curCar] - 100
    player[curCar] "YOU HAVE CHEATER SLICKS AND A $[savings[curCar]] TO SPEND"
    if JOB[curCar] == "B":
        jump f11780
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
    if savings[curCar] < 0:
        return
    $ modsUpper = modsCost * 1.4
    player[curCar] "YOU HAVE $[savings[curCar]] AND A [gearRatios[curCar][5]] RATIO; ANOTHER RATIO WILL COST BETWEEN $[modsCost] AND $[modsUpper]."
    player[curCar] "DO YOU WANT TO CHANGE REAR END RATIOS? (if 'yes' jump f11830, if 'no' return)"

label f11830:
    player[curCar] "WHAT IS THE REAR END RATIO YOU WOULD LIKE? (line 11830)"
    if L5W < 4.69:
        jump f11892
    player[curCar] "[L5W] IS PRETTY HIGH FOR STREET USE - DO YOU WANT TO TRY ANOTHER?(Y/N) (if 'yes jump f11800, if 'no' jump f11880)"

label f11880:
    $ carVal[curCar] = carVal[curCar] - 50
    $ modsCost = modsCost * 1.3

label f11892:
    $ savings[curCar] = savings[curCar] - modsCost
    $ gearRatios[curCar][5] = L5W
    return

label f11900:
    if lowTime == 0:
        $ lowTime = 99.99
    if TSAV == 0:
        $ TSAV = 99.99
    if LWINT < lowTime:
        $ lowTime = LWINT
    if LWINT < TSAV:
        $ TSAV = LWINT
    else:
        return
    if SWT18 > 0:
        jump f11915
    if LWINT < 18:
        $ SWT18 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 50
        $ PV[playerWin] = PV[playerWin] + .5

label f11915:
    if SWT17 > 0:
        jump f11925
    if LWINT < 17:
        $ SWT17 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 75
        $ RVL = RVL + 25
        $ PV[playerWin] = PV[playerWin] + 1

label f11925:
    if SWT16 > 0:
        jump f11935
    if LWINT < 16:
        $ SWT16 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 75
        $ RVL = RVL + 25
        $ PV[playerWin] = PV[playerWin] + 1.3

label f11935:
    if SWT15 > 0:
        jump f11950
    if LWINT < 15:
        $ SWT15 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 100
        $ RVL = RVL + 50
        $ PV[playerWin] = PV[playerWin] + 1.8
    if LWINT > 14:
        return

label f11950:
    if SWT14 > 0:
        jump f11970
    if LWINT < 14:
        $ SWT14 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 125
        $ RVL = RVL + 100
        $ PV[playerWin] = PV[playerWin] + 2.1
    if LWINT > 13:
        return

label f11970:
    if SWT13 > 0:
        jump f11990
    if LWINT < 13:
        $ SWT13 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 150
        $ RVL = RVL + 150
        $ PV[playerWin] = PV[playerWin] + 3
    if LWINT > 12:
        return

label f11990:
    if SWT12 > 0:
        return
    if LWINT < 12:
        $ SWT12 = playerWin #LWIN
        $ carVal[playerWin] = carVal[playerWin] + 200
        $ RVL = RVL + 200
        $ PV[playerWin] = PV[playerWin] + 4
    return

label f12205:
    if N[curCar] < 4:
        jump f12250
    "&, you have blown first gear on the old 4-speed."#;N$(L)
    "Your options are to avoid first gear or buy the available 3-speed."
    "Another transmission will cost $50.  Enter 'B' to buy (if 'B' goto f12225)"#;I$
    $ numGears[curCar] = 3
    $ gearRatios[[curCar][4]] = 0
    if engineStats[[curCar][0]] > 135:
        jump f12270
    else:
        return

label f12225:
    $ gearRatios[[curCar][4]] = 0
    $ gearRatios[[curCar][3]] = 2.67
    $ gearRatios[[curCar][2]] = 1.55
    $ numGears[curCar] = 3
    $ SV[curCar] = SV[curCar] - 50
    if engineStats[[curCar][0]] > 135:
        jump f12270
    else:
        return

label f12250:
    if gearRatios[[curCar][3]] < 2.5:
        jump f12255
    if engineStats[[curCar][0]] > 135:
        jump f12270
    else:
        return

label f12255:
    player[curCar] "Your clutch is gone.  It will cost you $50 to replace it."#;N$(L)
    "You have no alternative; press enter to continue"#;I$
    $ SV[curCar] = SV[curCar] - 50
    if engineStats[[curCar][0]] < 136:
        return

label f12270:
    if engineStats[[curCar][4]] < 3500:
        return
    if engineStats[[curCar][1]] < 4100:
        return
    "You have pushed the old straight 8 beyond its limits."
    "It is going to blow up soon.  Perhaps you should consider selling."
    if round == 2:
        $ engineStats[[curCar][0]] = 2
    else:
        $ engineStats[[curCar][0]] = 135
    return
    if round == 3:
        jump f12500
    if VLCD[curCar] > 4:
        jump f12450
    if MFR[curCar] == "FF":
        jump f12450
    if carYear[curCar] < 46:
        $ VLPCT = .6
    else:
        $ VLPCT = .9
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
    "You will have to help the computer choose a car by supplying a 'seed' number."
    if CN[curCar] == 0:
        $ CN[curCar] = 10
    jump f14400
    if curCar == 1:
        "use file USED50-A.DG1"
    if curCar == 2:
        "use file USED50-B.DG1"
    call f11300
    if curCar == 1:
        "use file USED50-A.DG1"
    if curCar == 2:
        "use file USED50-B.DG1"
    call f11400

label f14255:
    call f10210
    jump f890

label f14400:
    if curCar == 1:
        "use file JUNK2.DG1"
    if curCar == 2:
        "use file JUNK1.DG1"
    call f11400
    jump f14255

label gears:
    if  numGears[curCar] == 4:
        $ E[curCar] = gearRatios[curCar][4] * gearRatios[curCar][5]
    elif  numGears[curCar] == 3:
        $ E[curCar] = gearRatios[curCar][3] * gearRatios[curCar][5]
    elif  numGears[curCar] == 2:
        $ E[curCar] = gearRatios[curCar][2] * gearRatios[curCar][5]
    elif  numGears[curCar] == 1:
        $ E[curCar] = gearRatios[curCar][1] * gearRatios[curCar][5]

    return

label checkTR:
    if TR[curCar] == "PG":
        call f6200
    if TR[curCar] == "TH1":
        call f6100
    if TR[curCar] == "SLIP":
        call f6000

    return
