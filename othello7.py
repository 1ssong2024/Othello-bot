import sys; args = sys.argv[1:]
import math, time, re
startTime = time.process_time()
#globals
#strOthelloBoard = ""
alphabetList = [*"ABCDEFGH"]
indToAINote = {}
AINoteToInd = {}
posToMove = {}
HL = 10 #on supercomputer you can do 16 --> good balance btwn too many and not too many holes
vb = False

for i in range(64): #assigns alphabet value to each ind
    indToAINote[i] = alphabetList[i%8] + str(i//8 + 1)
    AINoteToInd[indToAINote[i]] = i

# make CS
def diagonalSets(pos):
    listDiag = []
    upperLeftRow = pos//8-pos%8
    upperLeftBound = upperLeftRow*8
    if upperLeftBound < 0: upperLeftBound = 0
    upperleft = [i for i in range(pos-9, upperLeftBound-1, -9)] #OK

    lowerLeftRow = pos//8+pos%8
    lowerLeftBound = lowerLeftRow*8
    if lowerLeftBound > 63: lowerLeftBound = 63
    lowerleft = [i for i in range(pos+7, lowerLeftBound + 1, 7)] #OK

    upperRightRow = pos//8-(7-pos)%8
    upperRightBound = upperRightRow*8
    if upperRightBound < 0: upperRightBound = 0
    upperright = [i for i in range(pos-7, upperRightBound, -7)]
    
    lowerRightRow = pos//8+(7-pos)%8
    lowerRightBound = lowerRightRow*8+9
    if lowerRightBound > 63: lowerRightBound = 63
    lowerright = [i for i in range(pos+9, lowerRightBound +1, 9)] #OK
    
    if upperleft: listDiag.append(upperleft)
    if lowerleft: listDiag.append(lowerleft)
    if upperright: listDiag.append(upperright)
    if lowerright: listDiag.append(lowerright)
    return listDiag

def verticalSets(pos):
    listVert = []
    topList = [i for i in range(pos-8, -1, -8)]
    if topList: listVert.append(topList)
    botList = [i for i in range(pos+8, 64, 8)]
    if botList: listVert.append(botList)
    return listVert

def horizSets(pos): #OK !
    listHoriz = []
    row = pos//8
    lowerBound = row*8
    upperBound = (row+1)*8 #upper bound not included in for-loop
    leftList = [i for i in range(pos-1, lowerBound-1, -1)] #OK
    if leftList: listHoriz.append(leftList)
    rightList = [i for i in range(pos+1, upperBound, 1)]
    if rightList: listHoriz.append(rightList)
    return listHoriz

for i in range(64):
    allPossibleCS = horizSets(i) + verticalSets(i) + diagonalSets(i) #listOfLists
    posToMove[i] = allPossibleCS


horiz0 = [num for num in range(1,8,1)]
vert0 = [num for num in range(8,62,8)]
diag0 = [num for num in range(9, 64, 9)]
# print(horiz0)
# print(vert0)
#cornerConn[0] = [horiz0, vert0, diag0] #top left
horiz7 = [num for num in range(6, -1, -1)]
vert7 = [num for num in range(15, 64, 8)]
diag7 = [num for num in range(14, 57, 7)]
#cornerConn[7] = [horiz7, vert7, diag7]
horiz56 = [num for num in range(57, 64, 1)]
vert56 = [num for num in range(48, -1, -8)]
diag56 = [num for num in range(49, 6, -7)]
#cornerConn[56] = [horiz56, vert56, diag56]
horiz63 = [num for num in range(62, 55, -1)]
vert63 = [num for num in range(55, 6, -8)]
diag63 = [num for num in range(54, -1, -9)]
#cornerConn[63] = [horiz63, vert63, diag63]

# othello board + indices
#  0  1  2  3  4  5  6  7
#  8  9 10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31 
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49 50 51 52 53 54 55
# 56 57 58 59 60 61 62 63

def makeBoard(i):
    if i:
        strOthelloBoard = i
    else:
        strOthelloBoard = '.'*27 + 'OX......XO' + '.'*27
    return strOthelloBoard


def reformatArgs(args):
    #print(args)
    global vb
    argList = [] #board, toPlay, 
    board = ""
    token = ""
    HL = 0
    moveList = []
    for arg in args:
        if len(arg) == 64 and arg[2] in "xXoO.":
            board = arg.upper()
        elif arg in "xXoO":
            token = arg.upper()
        elif "HL" in arg:
            HL = arg[2:]
        elif "V" in arg or "v" in arg:
            vb = True;
        else:
            moveList.append(arg)
    if board: 
        argList.append(board)
    else: 
        argList.append('.'*27 + 'OX......XO' + '.'*27)
    if token: 
        argList.append(token)
    else: 
        argList.append("XO"[board.count(".")%2])
    rml = []
    if moveList:
        for move in moveList:
            if len(move) > 3:
                moveStr = "".join(moveList)
                rml = [moveStr[i] + moveStr[i+1] for i in range(0, len(move)-1, 2)]
            else: 
                rml.append(move)
    moveList = [int(move) if not "_" in move else int(move[1]) for move in rml] 
    argList.append(moveList)
    if HL:
        argList.append(int(HL))
    else:
        argList.append(11)
    #print(argList)
    return argList


def display2D(board):
    for rowPos in range(0, 64, 8):
        print(board[rowPos: rowPos+8])

#logic code
def findMoves(brd, tkn):
    brd = brd.upper()
    tkn = tkn.upper()
    enmy = "X" if tkn == "O" else "O"
    return possible_moves(brd, tkn, enmy)

def possible_moves(board, token, enemy):
    possmoves = set()
    for ind, peice in enumerate(board):
        if peice == token: #if it is something you are looking to place
            for sublist in posToMove[ind]: # posToMove returns a list of list, of sets of diagonal, horizantal, and vertical
                for index in sublist: #looks at CS indices
                    if board[index] == enemy:
                        continue
                    if board[index] == token:
                        break
                    if board[index] == "." and index != sublist[0]: #found a placeable index
                        possmoves.add(index)
                        break
                    else:
                        break
    return possmoves

def makeMove(brd, tkn, mv):
    brd = brd.upper()
    tkn = tkn.upper()
    enmy = "X" if tkn == "O" else "O"
    #possMoves = possible_moves(brd, tkn, enmy)
    return next_move(brd, tkn, mv)

def next_move(board, token, pos):
    for subList in posToMove[pos]:
        for ind, CSindex in enumerate(subList):
            if board[CSindex] == ".": break
            if board[CSindex] == token:
                if not token in subList[:ind] and not "." in subList[:ind]:
                    board = flippzs(board, subList[:ind] + [pos], token)
                break
    return board

def flippzs(board, posList, sym):
    for pos in posList:
        board = board[:pos] + sym + board[pos+1:]
    return board

def editBoard(board, posList, sym):
    for pos in posList:
        if board[pos] == ".":
            board = board[:pos] + sym + board[pos+1:]
    return board

def snapShot(possMoves, toPlay, strOthelloBoard, move = -1):
    toCatch = "X" if toPlay == "O" else "O"
    possMoves = possible_moves(strOthelloBoard, toPlay, toCatch)
    if possMoves:
        board = editBoard(strOthelloBoard, possMoves, "*")
        if move > -1: 
            board = board[:move] + toCatch.lower() + board[move+1:]
        display2D(board)
        board = board.upper()
        print(strOthelloBoard + " " + str(strOthelloBoard.count("X")) + "/" + str(strOthelloBoard.count("O")))
        print("Possible moves for " + toPlay + ": " + str(sorted([*possMoves]))[1:-1:])
    else:
        toPlay, toCatch = toCatch, toPlay #switch turns
        possMoves = possible_moves(strOthelloBoard, toPlay, toCatch) #find poss moves for next player
        board = editBoard(strOthelloBoard, possMoves, "*")
        if move > -1: 
            board = board[:move] + toCatch.lower() + board[move+1:]
        display2D(board)
        print(strOthelloBoard + " " + str(strOthelloBoard.count("X")) + "/" + str(strOthelloBoard.count("O")))
        if possMoves:
            print("Possible moves for " + toPlay + ": " + str(sorted([*possMoves]))[1:-1:])
        else:
            print("No moves possible")

def move_and_display(possMoves, toPlay, toCatch, strOthelloBoard, inputArg):
    if vb: snapShot(possMoves, toPlay, strOthelloBoard)
    for move in inputArg[2]: # M:1 T:1 RE, M:1 T:0 E:1 RT, M:-1 T:0 E:1 RE,  M:-1 T:1 E:0 RT. set next move at the end
        if move > -1:
            if not possMoves:
                toPlay, toCatch = toCatch, toPlay #switch turns
                possMoves = possible_moves(strOthelloBoard, toPlay, toCatch) #find poss moves for next player
            strOthelloBoard = next_move(strOthelloBoard, toPlay, move) # move
            if vb or move == inputArg[2][-1]: print(toPlay.lower() + " plays to " + str(move)) 
            toPlay, toCatch = toCatch, toPlay #switch turns
            possMoves = possible_moves(strOthelloBoard, toPlay, toCatch) #find poss moves for next player
            if not possMoves:
                toPlay, toCatch = toCatch, toPlay #switch turns
                possMoves = possible_moves(strOthelloBoard, toPlay, toCatch) #find poss moves for next player
        if vb: snapShot(possMoves, toPlay, strOthelloBoard, move)
    if not possible_moves(strOthelloBoard, toPlay, toCatch):
        toPlay, toCatch = toCatch, toPlay #switch turns
        possMoves = possible_moves(strOthelloBoard, toPlay, toCatch) #find poss moves for next player
    return strOthelloBoard, toPlay, toCatch

def updateStats(key, val):
   global STATS
   if key in STATS:
      STATS[key] += val
   else:
      STATS[key] = val

#def negamaxR(brd, tkn, dotLeft, upd, lbd):
   
CACHE = {}

def midgameAB(brd, tkn, lbd, ubd, counter):
    eTkn = "X" if tkn == "O" else "O"
    key = brd + " " + tkn
    keytkn = key + "TKN"
    keyetkn = key + "ETKN"
    if keytkn in CACHE:
      PM = CACHE[keytkn]
    else:
      CACHE[keytkn] = PM = possible_moves(brd, tkn, eTkn)
    if keyetkn in CACHE:
      EPM = CACHE[keyetkn]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    else:
      CACHE[keyetkn] = EPM = possible_moves(brd, eTkn, tkn) 
    if not PM and not EPM:
        return [0]
    if counter < 1:
       return [len(PM)*100+brd.count(tkn)]
    if not PM and EPM:
        nm = midgameAB(brd, eTkn, -ubd, -lbd, counter-1)
        return [-nm[0]]
    bestSoFar = [lbd-1]
    for mv in PM:
        newBrd = next_move(brd, tkn, mv)
        nm = midgameAB(newBrd, eTkn, -ubd, -lbd, counter-1)
        score = -nm[0] 
        if score < lbd: 
            continue
        if score > ubd:   
            return [score]
        bestSoFar = [score] +nm[1:] + [mv]
        lbd = score + 1
    return bestSoFar
    
def negamax(brd, tkn, dotLeft, lbd, ubd):
    eTkn = "X" if tkn == "O" else "O"
    if dotLeft == 0:
        return [brd.count(tkn) - brd.count(eTkn)]
    key = brd + " " + tkn
    keytkn = key + "TKN"
    keyetkn = key + "ETKN"
    if key in CACHE: 
      return CACHE[key]
    if keytkn in CACHE:
      PM = CACHE[keytkn]
    else:
      CACHE[keytkn] = PM = possible_moves(brd, tkn, eTkn)
    if keyetkn in CACHE:
      EPM = CACHE[keyetkn]
    else:
      CACHE[keyetkn] = EPM = possible_moves(brd, eTkn, tkn)
    if not PM and not EPM:
        return [brd.count(tkn) - brd.count(eTkn)]
    if not PM and EPM:
        key = brd + " " + eTkn
        nm = negamax(brd, eTkn, dotLeft, -ubd, -lbd)
        return [-nm[0]] + nm[1:] + [-1] 
    bestSoFar = [lbd-1]
    for mv in PM:
        newBrd = next_move(brd, tkn, mv)
        key = newBrd + " " + eTkn
        nm = negamax(newBrd, eTkn, dotLeft-1, -ubd, -lbd)
        score = -nm[0]
        if score < lbd: 
            continue
        if score > ubd:   
            return [score]
        #if -nm[0] > bestSoFar[0]:
        bestSoFar = [score] +nm[1:] + [mv]
        lbd = score + 1
    return bestSoFar

# nm = negamax("xxxxxxo.xxxxxo..xxooooooxoxxooooxoxxooooxxxoxoooxxo.oxooxooooooo".upper(), "X", "xxxxxxo.xxxxxo..xxooooooxoxxooooxoxxooooxxxoxoooxxo.oxooxooooooo".count("."), -1000, 1000)
# print(nm)

def quickMove(board, token):
    global HL, CACHE
    if not board:
      HL = token
      return
    if board == '.'*27 + 'OX......XO' + '.'*27:
      CACHE = {}
    board = board.upper()
    token = token.upper()
    enemy = "X" if token == "O" else "O"
    fm = qmHelper(board, token, enemy)
    dotcount = board.count(".")
    if dotcount >= HL and dotcount < 35:
        dotLeft = board.count(".")
        nm = midgameAB(board, token, -10000, 10000, 5)
       # print("Negamax score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
        return nm[-1]
    if dotcount < HL:
        dotLeft = board.count(".")
        nm = negamax(board, token, dotLeft, -100, 100)
       # print("Negamax score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
        return nm[-1]
    return fm
def qmHelper(board, token, enemy):
    possMoves = possible_moves(board, token, enemy)  
    if {0, 7, 56, 63} & possMoves: return [*{0, 7, 56, 63} & possMoves][0] #corner
    if board[0] == token: 
        for i in horiz0:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[:i]: return i
                else: break
        for i in vert0:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[0:i:8]: return i
                else: break
    if board[7] == token:
        for i in horiz7:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[7:i:-1]: return i
                else: break
        for i in vert7:
            if board[i] == ".":
                if i in possMoves and (enemy + token) not in board[7:i:8]: return i
                else: break
    if board[56] == token:
        for i in horiz56:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[56:i+1]: return i
                else: break
        for i in vert56:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[56:i:-8]: return i
                else: break
    if board[63] == token:
        for i in horiz63:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[63:i:-1]: return i
                else: break
        for i in vert63:
            if board[i] == ".":
                if i in possMoves and (enemy+token) not in board[63:i:-8]: return i
                else: break
    if board[0:8:].count(".") == 1 and board[0:8:].index(".") in possMoves: return board[0:8:].index(".")
    if board[0:57:8].count(".") == 1 and board[0:57:8].index(".") in possMoves: return board[0:57:8].index(".")
    if board[56:64:].count(".") == 1 and board[56:64:].index(".") in possMoves: return board[56:64:].index(".")
    if board[7:64:8].count(".") == 1 and board[7:64:8].index(".") in possMoves: return board[7:64:8].index(".")
    if board[0] != token and possMoves-{9}: possMoves = possMoves-{9} 
    if board[7] != token and possMoves - {14}: possMoves = possMoves - {14} 
    if board[56] != token and possMoves-{49}: possMoves = possMoves-{49} 
    if board[63] != token and possMoves-{54}: possMoves = possMoves-{54} 
    if board[0] != token and ({8,1} & possMoves): #top left
        if possMoves-{1}: possMoves = possMoves-{1} 
        if possMoves-{8}: possMoves = possMoves-{8} 
    if board[7] != token and ({6,15} & possMoves): #top right
        if possMoves - {6}: possMoves = possMoves - {6} 
        if possMoves - {15}: possMoves = possMoves - {15} 
    if board[56] != token and ({48,57} & possMoves): #bot left
        if possMoves-{48}: possMoves = possMoves-{48} 
        if possMoves-{57}: possMoves = possMoves-{57} 
    if board[63] != token and ({55,62} & possMoves): #bot right
        if possMoves-{55}: possMoves = possMoves-{55} 
        if possMoves-{62}: possMoves = possMoves-{62} 
    
    return [*possMoves][0]
#print(quickMove(".....OOXX.OOOOOOXXOOOXOOXOXXXOO.XOOXOXOOXXOOOOOOXOOX....XO.X....", "X"))

def main():
    #if args:
     global HL
     inputArg = reformatArgs(args)
     strOthelloBoard = makeBoard(inputArg[0])
     toPlay = inputArg[1]
     HL = inputArg[3]
     toCatch = "X" if toPlay == "O" else "O"
     possMoves = possible_moves(strOthelloBoard, toPlay, toCatch)
     lastmove, toPlay, toCatch = move_and_display(possMoves, toPlay, toCatch, strOthelloBoard, inputArg)
     if possible_moves(lastmove, toPlay, toCatch):
         if not vb: snapShot(possMoves, toPlay, lastmove)
         if strOthelloBoard.count(".") < HL:
            dotLeft = strOthelloBoard.count(".")
            nm = negamax(strOthelloBoard, toPlay, dotLeft, -100, 100)
            mypref = nm[-1]
            print(f"The preferred move is: {mypref}")
            print("Negamax score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
         else:
            mypref = quickMove(lastmove, toPlay)
            print(f"The preferred move is: {mypref}")
            
   #  else:
#         strOthelloBoard = makeBoard("")
#         toPlay = "XO"[strOthelloBoard.count(".")%2]
#         toCatch = "OX"[strOthelloBoard.count(".")%2]
#         inputArg = [strOthelloBoard, toPlay, []]
#         #print(strOthelloBoard + " " + str(strOthelloBoard.count("X")) + "/" + str(strOthelloBoard.count("O")))
#         possMoves = possible_moves(strOthelloBoard, toPlay, toCatch)
#         move_and_display(possMoves, toPlay, toCatch, strOthelloBoard, inputArg)
# 
 
if __name__ == "__main__":main()

#Stephanie Song, P6, 2024