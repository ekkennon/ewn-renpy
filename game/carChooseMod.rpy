
label chooseCarMod:
    $ curCar = phase % 2
    while curCar == 1 or curCar == 0:
        if curCar == 0:
            player[0] "YOU ARE CURRENTLY DRIVING A  [engineStats[0][0]] HP [desc[0]]."
            player[0] "YOU HAVE $[savings[0]] IN SAVINGS. THE CAR IS NOW VALUED AT $[carVal[0]]"
            $ nw = savings[0] + carVal[0]
            player[0] "YOUR NET WORTH IS $[nw] AND YOU HAVE WON [WIN1] RACES"
        elif curCar == 1:
            player[1] "YOU ARE CURRENTLY DRIVING A [engineStats[1][0]] HP [desc[1]]"
            player[1] "YOU HAVE $[savings[1]] IN SAVINGS; THE CAR IS NOW VALUED AT $[carVal[1]]"
            $ nw = savings[1] + carVal[1]
            player[1] "YOUR NET WORTH IS $[nw] AND YOU HAVE WON [WIN2] RACES"

        $ lookAvail = False # this is true on race 1 and after race 2
        $ modsAvail = False # this is true after race 1, this should remain false when the car has no mods available - later races
        $ raceAvail = False # this is true when the player has a working car (after race 1)

        if race == 1:
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

            "Make modifications" if  modsAvail:
                call modifications

            "Race the car 'As Is'" if raceAvail: # I'm ready to race
                "The race will begin shortly."

        if phase % 2 == 0:
            $ curCar += 1
        elif phase % 2 == 1:
            $ curCar -= 1
    return

label disreputable:
    player[curCar] "disreputable"

    return

label junkyard:
    player[curCar] "junkyard"

    return

label chooseCar:
    player[curCar] "You can choose your own car or you can have the computer randomly choose a car for you."
    player[curCar] "If you choose your own car it will cost more but it will be in better shape."
    player[curCar] "If you have the computer choose then the car will come from the front row of a junkyard (prices less than $50)"
    player[curCar] "If you want to choose your own car then the car will come from the back row of a disreputable used car lot (prices less than $200)"
    call screen carloc1

    return

label modifications:
    if round == 2:
        $ modsCost = 5
        $ savings[curCar] = savings[curCar] + 100 # why does their money increase for wanting mods?
        jump f15065
        #(if 'M' jump f15110)

    elif round == 3:
        jump f16010

    elif round == 4:
        jump f17010
    return

label f15065:
    if engineStats[curCar][2] == 323: # the car is broke and needs a repair
        if MFR(curCar) == "MOPAR":
            jump f12205

label f15110:
    #player[curCar] "\        \ YOU HAVE $[SV[curCar]] TO MODIFY YOUR [DSCR[curCar]] - COST IS $[MD] PER HP."
    player[curCar] "TO MODIFY YOUR Car the COST IS $[modsCost] PER HP."

label f15120:
    #player[curCar] "YOU HAVE [P[curCar][0]] HP AND $[SV[curCar]]"
    #stats line

    player[curCar] "ENTER 'N' TO SKIP MODIFICATIONS THIS TIME. (if 'N' jump f15520, if 'Y' jump f15150)"

label f15150:
    #OPEN "I",#1,"ENGINEX3"
    "if the player wants modifications, read from file ENGINEX3. (line 15150)"

label f15160:
    $ SM == MFR[curCar]

label f15170:
    if SM == "":
        #INPUT "MANUFACTURER";SM$
        "read the manufacturer from the file?"

label f15180:
    $ SP3 = engineStats[curCar][2]

label f15190:
    $ SP1 = 0

label f15220:
    if SM == MFGR:
        jump f15230
    else:
        jump f15340

label f15230:
    if SP3 > 0:
        jump f15240
    else:
        jump f15270

label f15240:
    if SP3 == P3:
        jump f15250
    else:
        jump f15340

label f15250:
    if SP1 > 0:
        jump f15260
    else:
        jump f15270

label f15260:
    if SP1 == P1:
        jump f15270
    else:
        jump f15340

label f15270:
    player[curCar] "MFGR [MFGR], DISP=[P3], HP=[P1] @ [P5], TORQUE=[P6] @ [P7]"

label f15280:
    $ LL = LL + 1

label f15290:
    if LL < 23:
        jump f15340

label f15310:
    $ LL = 1

label f15340:
    player[curCar] "WHAT IS THE EXACT HORSEPOWER YOU WANT (WP1 is the HP entered by the player)"

label f15345:
    if WP1 == 0:
        jump f15420

label f15350:
    $ WORK1 = WP1 - engineStats[curCar][0]

label f15360:
    $ WORK2 = WORK1 * modsCost

label f15370:
    $ WORK3 = savings[curCar] - WORK2

label f15380:
    if WORK3 < 0:
        PRINT "YOU CAN'T AFFORD THAT - TRY AGAIN"
        jump f15340

label f15390:
    player[curCar] "YOU CAN INCREASE TO [WP1] HP - IT WILL LEAVE YOU WITH $[WORK3]"

label f15400:
    player[curCar] "ENTER 'Y' TO CONFIRM MODIFICATION (if 'Y' jump f15430, if 'N' jump f15420)"

label f15420:
    #"line 15420"
    player[curCar] "YOU OPTED NOT TO MODIFY AT THIS TIME"
    jump f15520

label f15430:
    $ engineStats[curCar][0] = WP1
    $ savings[curCar] = WORK3
    $ carVal[curCar] = carVal[curCar] + (WORK1 * 2)

label f15440:
    player[curCar] "MODIFICATIONS COMPLETE; HP = [engineStats[curCar][0]], CASH = $[savings[curCar]], CAR IS WORTH $[carVal[curCar]]"

label f15460:
    $ engineStats[curCar][1] = 0
    $ engineStats[curCar][4] = 0
    $ engineStats[curCar][5] = 0
    $ engineStats[curCar][6] = 0

    call f10200
    call f8900

label f15520:
    #"line 15520"
    #NEXT PL
    return

label f16010:
    #FOR PL=1 TO 2
    $ curCar = 0
    call f16014
    $ curCar = 1

label f16014:
    $ FINYR = 54

label f16015:
    $ modsCost = 5

label f16020:
    $ savings[curCar] = savings[curCar] + 100

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
    call f12030

label f16080:
    player[curCar] "YOU CAN LOOK AT USED CARS (L) OR MODIFY/REBUILD (M) (if 'L' jump f16150, if 'M' jump f16315)"
    jump f16150
    jump f16220 # i don't see how this would ever be reached, originally line 16125

label f16130:
    player[curCar] "You now have $[savings[curCar]]."

label f16131:
    player[curCar] "YOU CAN LOOK AT USED CARS (L), MODIFY YOUR CAR (M), OR RACE IT AS IS (R) (if 'L' jump f16150, if 'M' jump f16315, if 'R' jump f16740)"

label f16150:
    call f12400

label f16165:
    $ WORK1 = (carValPCT * carVal[curCar]) + (engineStats[curCar][0] * .1) - ( weight[curCar][0] * .005)

label f16175:
    player[curCar] "\        \-YOU HAVE BEEN OFFERED $[WORK1] FOR YOUR [desc[curCar]]"

label f16180:
    player[curCar] "YOU FIGURE THIS IS MUCH MORE THAN YOU COULD GET AS A TRADE-IN"

label f16185:
    player[curCar] "IF YOU ARE SERIOUS ABOUT BUYING ANOTHER CAR, YOU'D BETTER SELL IT NOW (Y/N) (if 'Y' jump f16195, if 'N' jump f16131)"

label f16195:
    $ savings[curCar] = savings[curCar] + WORK1

label f16200:
    $ carVal[curCar] = 0

label f16205:
    player[curCar] "\        \ YOU HAVE $[savings[curCar]] TO SPEND"

label f16220:
    player[curCar] "\        \ YOU ARE GOING TO BUY A CAR; YOU HAVE $[savings[curCar]]"

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
    call f12030
    if savings[curCar] < 0:
        jump f16740

label f16318:
    player[curCar] "YOU MAY HAVE THE OPPORTUNITY TO MAKE AN ENGINE SWAP-TO LOOK, ENTER (Y/N) (if 'Y' jump f16325, if 'N' jump f16525)"

label f16325:
    #OPEN "I",#1,"BOLTIN-Z.DG1"
    "line 16325, use file BOLTIN-Z.DG1"
    $ HX = 0

label f16336:
    if C1 > round:
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
        PRINT "YOU CAN'T AFFORD THAT - TRY AGAIN"
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
    call f12030

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
    if C1 > round:
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
