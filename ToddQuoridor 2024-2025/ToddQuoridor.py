#Quoridor Minimax
import heapq
from heapq import heappop, heappush
import pygame
import keyboard
import time
from pathlib import Path
import sys

#display
def updateBoard(screen, walls, ppos, apos, lmove, turn, pwalls, awalls):
    pygame.event.pump()
    screen.fill((255, 255, 255))
    makeBoard(screen)
    drawTiles(screen, walls)
    drawHighlight(screen, lmove, ppos, apos, turn)
    drawPawns(screen, ppos, apos)
    drawWallsCount(screen, pwalls, awalls)
    drawInstructions(screen)
    pygame.display.flip()
    pygame.event.pump()
def makeBoard(screen):
    for i in range(9):
        drawX, drawY = 0, 600
        drawX += (i + 1) * 50 + 25
        drawY -= 50 + 55
        pygame.draw.rect(screen, (255, 200, 200), (drawX, drawY, 40, 40), width=0)
    for i in range(9):
        drawX, drawY = 0, 600
        drawX += (i + 1) * 50 + 25
        drawY -= 9 * 50 + 55
        pygame.draw.rect(screen, (200, 200, 255), (drawX, drawY, 40, 40), width=0)
    drawY = 95
    for i in range(9):
        drawX = 75
        for j in range(9):
            pygame.draw.rect(screen, (0, 0, 0), (drawX, drawY, 40, 40), 1)
            drawX += 50
        drawY += 50
def drawTiles(screen, walls):
    for i in range(len(walls)):
        if not walls[i] is None:
            drawX, drawY = 0, 600
            drawX += walls[i][0] * 50 + 65
            drawY -= walls[i][1] * 50 + 65
            if walls[i][2] == 1:
                pygame.draw.rect(screen, (100, 100, 100), (drawX - 40, drawY, 90, 10), 0)
            if walls[i][2] == 2:
                pygame.draw.rect(screen, (100, 100, 100), (drawX, drawY - 40, 10, 90), 0)
        else:
            pass
def drawPawns(screen, ppos, apos):
    px = ppos[0] * 50 + 45
    py = 600 - (ppos[1] * 50 + 35)
    ax = apos[0] * 50 + 45
    ay = 600 - (apos[1] * 50 + 35)
    if ppos == apos:
        px += 5
        py += 5
        ax -= 5
        ay -= 5
    pygame.draw.circle(screen, (0, 0, 225), (px, py), 10)
    pygame.draw.circle(screen, (255, 0, 0), (ax, ay), 10)
def drawHighlight(screen, lmove, ppos, apos, turn):
    #print(lmove)
    if lmove == None:
        return
    if isinstance(lmove, str):
        if turn == "alg":
            #print("alg move")
            drawX, drawY = 0, 600
            drawX += apos[0] * 50 + 30
            drawY -= apos[1] * 50 + 50
            pygame.draw.rect(screen, (0, 255, 0), (drawX, drawY, 30, 30), width=3)
        else:
            #print("player move")
            drawX, drawY = 0, 600
            drawX += ppos[0] * 50 + 30
            drawY -= ppos[1] * 50 + 50
            pygame.draw.rect(screen, (0, 255, 0), (drawX, drawY, 30, 30), width=3)
    else:
        #print("WALLLLL")
        drawX, drawY = 0, 600
        drawX += int(lmove[0]) * 50 + 65
        drawY -= int(lmove[1]) * 50 + 65
        if int(lmove[2]) == 1:
            pygame.draw.rect(screen, (0, 255, 0), (drawX - 40, drawY, 90, 10), 2)
        if int(lmove[2]) == 2:
            pygame.draw.rect(screen, (0, 255, 0), (drawX, drawY - 40, 10, 90), 2)
def highlightPossibleMove(screen, walls, pos, ppos, apos, lmove, pwalls, awalls):
    updateBoard(screen, walls, ppos, apos, lmove, "alg", pwalls, awalls)
    px = pos[0] * 50 + 45
    py = 600 - (pos[1] * 50 + 35)
    pygame.draw.circle(screen, (112, 112, 255), (px, py), 10)
    pygame.display.flip()
def highlightPossibleWall(screen, walls, nwall, ppos, apos, lmove, possible, pwalls, awalls):
    updateBoard(screen, walls, ppos, apos, lmove, "alg", pwalls, awalls)
    drawX, drawY = 0, 600
    drawX += nwall[0] * 50 + 65
    drawY -= nwall[1] * 50 + 65
    color = ()
    if possible:
        color = (150, 150, 150)
    else:
        color = (255, 150, 150)
    if nwall[2] == 1:
        pygame.draw.rect(screen, color, (drawX - 40, drawY, 90, 10), 0)
    if nwall[2] == 2:
        pygame.draw.rect(screen, color, (drawX, drawY - 40, 10, 90), 0)
    pygame.display.flip()
def drawTexts(screen, sTexts):
    for i in sTexts:
        text = i[0].render(i[1], i[2], i[3])
        textRect = text.get_rect()
        if i[4] == "c":
            textRect.center = i[5]
        elif i[4] == "l":
            textRect.left = i[5][0]
            textRect.centery = i[5][1]
        elif i[4] == "lb":
            textRect.left = i[5][0]
            textRect.bottom = i[5][1]
        elif i[4] == "r":
            textRect.right = i[5][0]
            textRect.centery = i[5][1]
        elif i[4] == "rb":
            textRect.right = i[5][0]
            textRect.bottom = i[5][1]
        screen.blit(text, textRect)
def showWinner(screen, pos, walls, ppos, apos, lmove, turn, pwalls, awalls):
    updateBoard(screen, walls, ppos, apos, lmove, turn, pwalls, awalls)
    for _ in range(5):
        drawX, drawY = 0, 600
        drawX += pos[0] * 50 + 25
        drawY -= pos[1] * 50 + 55
        pygame.draw.rect(screen, (0, 255, 0), (drawX, drawY, 40, 40), width=0)
        pygame.display.flip()
        time.sleep(0.2)
        updateBoard(screen, walls, ppos, apos, lmove, turn, pwalls, awalls)
        time.sleep(0.2)
    time.sleep(1)
def drawWallsCount(screen, pwalls, awalls):
    texts = []
    if isinstance(pwalls, int): texts.append([pygame.font.SysFont("Bahnschrift", 20), str(pwalls) + " walls", True, (0, 0, 255), "c", (100, 550)])
    if isinstance(awalls, int): texts.append([pygame.font.SysFont("Bahnschrift", 20), str(awalls) + " walls", True, (255, 0, 0), "c", (500, 75)])
    drawTexts(screen, texts)
def drawInstructions(screen):
    dGray = (100, 100, 100)
    texts = [
        [pygame.font.SysFont("Bahnschrift", 12), 'W: Switch to movement mode', True, dGray, "l", (10, 10)],
        [pygame.font.SysFont("Bahnschrift", 12), 'Q: Switch to walls mode', True, dGray, "l", (10, 25)],
        [pygame.font.SysFont("Bahnschrift", 12), 'R: Rotate Wall', True, dGray, "l", (10, 40)],
        [pygame.font.SysFont("Bahnschrift", 12), 'Space: Confirm', True, dGray, "l", (10, 55)],
        [pygame.font.SysFont("Bahnschrift", 12), 'Use arrow keys to move', True, dGray, "l", (10, 70)],
    ]
    for i in texts: drawTexts(screen, texts)

#human input
def humanMove(bx, by, walls, ppos, apos, screen, lmove, pwalls, turn, awalls):
    #print("It is now the players move.")
    moved = False
    mode = "move"
    while moved == False:
        if mode == "move":
            mode, ppos, walls, lmove = tryMove(bx, by, walls, ppos, apos, screen, lmove, turn, pwalls, awalls)
        elif mode == "wall":
            if pwalls > 0:
                mode, ppos, walls, lmove = tryWall(bx, by, walls, ppos, apos, screen, lmove, pwalls, awalls)
            else:
                pass #make 0 walls flash red
        elif mode == "esc":
            return ppos, walls, lmove, pwalls, "esc"
        else:
            moved = True
    #print(f"Alg is now at {apos}, you are now at {ppos}, and the walls are {walls}")
    if mode == "placed":
        pwalls -= 1
        #print(f"You place one wall, you are now at {pwalls}")
    return ppos, walls, lmove, pwalls, None
def tryMove(bx, by, walls, ppos, apos, screen, lmove, turn, pwalls, awalls):
    #print("Movement Mode")
    movements = validMovements(bx, by, walls, ppos)
    move = None
    if turn == "p1":
        if "up" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] + 1), ppos, apos, lmove, pwalls, awalls)
            move = "up"
        elif "down" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] - 1), ppos, apos, lmove, pwalls, awalls)
            move = "down"
        elif "left" in movements:
            highlightPossibleMove(screen, walls, (ppos[0] - 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "left"
        else:
            highlightPossibleMove(screen, walls, (ppos[0] + 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "right"
    if turn == "p2":
        if "down" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] - 1), ppos, apos, lmove, pwalls, awalls)
            move = "down"
        elif "up" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] + 1), ppos, apos, lmove, pwalls, awalls)
            move = "up"
        elif "left" in movements:
            highlightPossibleMove(screen, walls, (ppos[0] - 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "left"
        else:
            highlightPossibleMove(screen, walls, (ppos[0] + 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "right"
    while not any(keyboard.is_pressed(key) for key in [" ", "q", "down", "up", "right", "left", "esc"]):
        pygame.event.pump()
    key = keyboard.read_key()
    while key != "space":
        if key == "q":
            return "wall", ppos, walls, lmove
        if key == "up" and "up" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] + 1), ppos, apos, lmove, pwalls, awalls)
            move = "up"
        if key == "down" and "down" in movements:
            highlightPossibleMove(screen, walls, (ppos[0], ppos[1] - 1), ppos, apos, lmove, pwalls, awalls)
            move = "down"
        if key == "left" and "left" in movements:
            highlightPossibleMove(screen, walls, (ppos[0] - 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "left"
        if key == "right" and "right" in movements:
            highlightPossibleMove(screen, walls, (ppos[0] + 1, ppos[1]), ppos, apos, lmove, pwalls, awalls)
            move = "right"
        if key == "esc":
            return "esc", ppos, walls, None
        while not any(keyboard.is_pressed(key) for key in [" ", "q", "down", "up", "right", "left", "esc"]):
            pygame.event.pump()
        key = keyboard.read_key()
        while any(keyboard.is_pressed(key) for key in [" ", "q", "down", "up", "right", "left", "esc"]):
            pygame.event.pump()
    if move == "up":
        ppos = (ppos[0], ppos[1] + 1)
    if move == "down":
        ppos = (ppos[0], ppos[1] - 1)
    if move == "left":
        ppos = (ppos[0] - 1, ppos[1])
    if move == "right":
        ppos = (ppos[0] + 1, ppos[1])
    return "moved", ppos, walls, move
def tryWall(bx, by, walls, ppos, apos, screen, lmove, pwalls, awalls):
    #print("Wall mode")
    powalls = getAllMoves(bx, by, walls, ppos, apos, 1, 1)
    for i in range(4): powalls.pop(0)
    wallIsValid = False
    x = 1
    y = 1
    r = 1
    while wallIsValid == False:
        if [x, y, r] in powalls:
            wallIsValid = True
        else:
            if r == 1:
                r = 2
            elif x != 8:
                x += 1
                r = 1
            else:
                x = 1
                y += 1
                r = 1
    nwall = [x, y, r]
    highlightPossibleWall(screen, walls, nwall, ppos, apos, lmove, True, pwalls, awalls)
    while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
        pygame.event.pump()
    key = keyboard.read_key()
    possible = True
    while key != "space" or not possible:
        if key == "w":
            return "move", ppos, walls, lmove
        if key == "up":
            nwall[1] += 1
        if key == "down":
            nwall[1] -= 1
        if key == "left":
            nwall[0] -= 1
        if key == "right":
            nwall[0] += 1
        if key == "r":
            if nwall[2] == 1:
                nwall[2] = 2
            else:
                nwall[2] = 1
        if key == "esc":
            return "esc", ppos, walls, nwall
        possible = nwall in powalls and makeGraph(bx, by, walls + nwall) != float('inf')
        highlightPossibleWall(screen, walls, nwall, ppos, apos, lmove, possible, pwalls, awalls)
        while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
        key = keyboard.read_key()
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
    walls.append(nwall)
    return "placed", ppos, walls, nwall

#logic
def getAllMoves(bx, by, walls, pos, opos, endy, wallc, mmdb=None):
    possible = validMovements(bx, by, walls, pos)
    """if not mmdb == None and mmdb[0] == walls:
        if mmdb[1] == "up":
            possible.remove("down")
        elif mmdb[1] == "down":
            possible.remove("up")
        elif mmdb[1] == "left":
            possible.remove("right")
        elif mmdb[1] == "right":
            possible.remove("left")"""
    powalls = []

    if wallc > 0:
        for i in range(1, bx):
            for j in range(1, by):
                if not [i, j, 1] in walls and not [i, j, 2] in walls:
                    #vertical walls
                    if not [i - 1, j, 1] in walls and not [i + 1, j, 1] in walls:
                        nwalls = walls.copy()
                        nwalls.append([i, j, 1])
                        
                        #find out if there is a valid path
                        reach = dijkstra(bx, by, nwalls, opos, endy)
                        reachable = reach < float("inf")

                        #validate move
                        if reachable:
                            powalls.append([i, j, 1])

                    #horizontal walls
                    if not [i, j - 1, 2] in walls and not [i, j + 1, 2] in walls:
                        nwalls = walls.copy()
                        nwalls.append([i, j, 2])
                        
                        #find out if there is a valid path
                        reach = dijkstra(bx, by, nwalls, opos, endy)
                        reachable = reach < float("inf")
                        
                        #validate move
                        if reachable:
                            powalls.append([i, j, 2])
                    
                    if not [2, 1, 1] in walls or [1, 1, 2] in walls: #debug
                        nwalls = walls.copy()
                        nwalls.append([1, 1, 1])
                        reach = dijkstra(bx, by, nwalls, opos, endy)
                        reachable = reach < float("inf")
                        if reachable:
                            powalls.append([1, 1, 1])
                    
    #move ordering (none rn)
    powalls = sorted(powalls, key=lambda x: x[2])
    possible += powalls
    return possible
def isGameOver(bx, by, pos, opos, aendy, pendy):
    if pos[1] == aendy:
        return True, "algorithm"
    elif opos[1] == pendy:
        return True, "player"
    else:
        return False, "Nobody"
def validMovements(bx, by, walls, pos):
    px, py = pos
    valid = []

    if not py == by and not [px, py, 1] in walls and not [px - 1, py, 1] in walls:
        valid.append("up")
    if not py == 1 and not [px, py - 1, 1] in walls and not [px - 1, py - 1, 1] in walls:
        valid.append("down")
    if not px == 1 and not [px - 1, py, 2] in walls and not [px - 1, py - 1, 2] in walls:
        valid.append("left")
    if not px == bx and not [px, py, 2] in walls and not [px, py - 1, 2] in walls:
        valid.append("right")

    return valid
def dijkstra(bx, by, walls, start, endy):
    """
    Dijkstra-based pathfinding that stops early if reaching any cell in the goal row.
    Uses graph and priority queue to minimize distances.
    
    Function is my original code rewritten by chatGPT to run smother
    """
    # Build the graph
    graph = makeGraph(bx, by, walls)
    
    # Initialize the Dijkstra variables
    prev = {v: None for v in graph.keys()}
    vis = {v: False for v in graph.keys()}
    dists = {v: float("inf") for v in graph.keys()}
    dists[start] = 0
    
    # Initialize the priority queue
    unpq = [(0, start)]
    heapq.heapify(unpq)
    
    # Start Dijkstra's algorithm
    while unpq:
        rem_dist, rem = heapq.heappop(unpq)
        vis[rem] = True

        # If we reach any cell in the goal row, stop early
        x, y = rem
        if y == endy:
            return rem_dist
        
        # Visit neighbors and update distances
        for edge in graph[rem]:
            if vis[edge]:
                continue
            ndist = rem_dist + 1
            if ndist < dists[edge]:
                dists[edge] = ndist
                prev[edge] = rem
                heapq.heappush(unpq, (ndist, edge))
    
    return float("inf")  # No path found
def evalBoard(bx, by, walls, apos, ppos, aendy, pendy, turns, awalls, pwalls):
    if apos[1] == aendy:
        return float("inf")
    if ppos[1] == pendy:
        return -float("inf")
    
    ourBest = dijkstra(bx, by, walls, apos, aendy)
    theirBest = dijkstra(bx, by, walls, ppos, pendy)
    score = (theirBest - ourBest) + ((awalls - pwalls) * 4)

    return score
def makeGraph(bx, by, walls):
    #solve maze
    graph = {}
    for i in range(1, bx + 1):
        for j in range(1, by + 1):
            cell = (i, j)
            dirs = validMovements(bx, by, walls, cell)
            
            if cell not in graph:
                graph[cell] = []
            
            if "up" in dirs:
                graph[cell].append((i, j + 1))
            if "down" in dirs:
                graph[cell].append((i, j - 1))
            if "left" in dirs:
                graph[cell].append((i - 1, j))
            if "right" in dirs:
                graph[cell].append((i + 1, j))
    return graph

#minimax
def minimax(depth, maxiPlayer, bx, by, walls, apos, ppos, aendy, pendy, alpha, beta, turns, awalls, pwalls, mmdb):
    directions = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    
    #check if game is over
    ieval = evalBoard(bx, by, walls, apos, ppos, aendy, pendy, turns, awalls, pwalls)
    if depth <= 0 or abs(ieval) == float("inf"):
        return ieval, None

    #case if algorithm turn
    if maxiPlayer:
        maxEval = -float("inf")
        bestMove = None
        
        if depth == 0.5: awalls = 0
        
        for i in getAllMoves(bx, by, walls, apos, ppos, pendy, awalls, mmdb):
            
            nwalls = walls.copy()
            npos = (apos[0], apos[1])
            
            if isinstance(i, str):
                dx, dy = directions[i]
                npos = (npos[0] + dx, npos[1] + dy)
            else:
                nwalls.append(i)

            eval, _ = minimax(depth - 1, False, bx, by, nwalls, npos, ppos, aendy, pendy, alpha, beta, turns, awalls, pwalls, mmdb)
            
            if eval > maxEval:
                maxEval = eval
                bestMove = i
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return maxEval, bestMove

    else:
        minEval = float("inf")
        bestMove = None
        
        if depth == 0.5: pwalls = 0
        
        for i in getAllMoves(bx, by, walls, ppos, apos, aendy, pwalls, mmdb):
            
            nwalls = walls.copy()
            npos = (ppos[0], ppos[1])
            
            if isinstance(i, str):
                dx, dy = directions[i]
                npos = (npos[0] + dx, npos[1] + dy)
            else:
                nwalls.append(i)

            eval, _ = minimax(depth - 1, True, bx, by, nwalls, apos, npos, aendy, pendy, alpha, beta, turns, awalls, pwalls, mmdb)
            
            if eval < minEval:
                minEval = eval
                bestMove = i
            
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return minEval, bestMove
def makeMove(depth, bx, by, walls, pos, opos, aendy, pendy, turns, awalls, pwalls, mmdb):
    moves = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    
    #get algorithm move
    miniM = minimax(depth, True, bx, by, walls, pos, opos, aendy, pendy, -float('inf'), float('inf'), turns, awalls, pwalls, mmdb)
    #print(f"Eval of {miniM[0]}")
    #update board
    if isinstance(miniM[1], str):
        pos = (moves[miniM[1]][0] + pos[0], pos[1])
        pos = (pos[0], moves[miniM[1]][1] + pos[1])
        #print(f"I move {miniM[1]}")
    else:
        if not isinstance is None: walls.append(miniM[1])
        #print(f"I place a wall at {miniM[1]}")
        if not isinstance is None: awalls -= 1
        #print(f"Algorithm places one wall at {miniM[1]}, they are now at {awalls}")
    
    #debug
    #print(f"Alg is now at {pos}, you are now at {opos}, and the walls are {walls}")
    return pos, walls, miniM[1], awalls

#game
def vsAlg(depth, screen):
    #init variables
    gameOver, running, boardSizeX, boardSizeY, ppos, apos, walls, moves, lmove, pwalls, awalls, turns, winner, esc = False, True, 9, 9, (5, 1), (5, 9), [], {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}, False, 10, 10, 1, "Nobody", None
    
    updateBoard(screen, walls, ppos, apos, None, None, pwalls, awalls)
    
    mmdb = None
    
    #main logic loop
    while running:
        #make algorithm move
        if not gameOver:
            apos, walls, lmove, awalls = makeMove(depth, boardSizeX, boardSizeY, walls, apos, ppos, 1, 9, turns, awalls, pwalls, mmdb)
            gameOver, winner = isGameOver(boardSizeX, boardSizeY, apos, ppos, 1, 9)
            updateBoard(screen, walls, ppos, apos, lmove, "alg", pwalls, awalls)
            
            mmdb = [walls, lmove]
        
        #make players move
        if not gameOver:
            ppos, walls, lmove, pwalls, esc = humanMove(boardSizeX, boardSizeY, walls, ppos, apos, screen, lmove, pwalls, "p1", awalls)
            gameOver, winner = isGameOver(boardSizeX, boardSizeY, apos, ppos, 1, 9)
            updateBoard(screen, walls, ppos, apos, lmove, "play", pwalls, awalls)
        
        if esc == "esc": return
        
        turns += 1
        
        #exit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if gameOver:
            running = False
    if winner == "player":
        showWinner(screen, ppos, walls, ppos, apos, lmove, "player", pwalls, awalls)
    else:
        showWinner(screen, apos, walls, ppos, apos, lmove, "alg", pwalls, awalls)
def vsPlayer(screen):
    #init variables
    gameOver, running, boardSizeX, boardSizeY, ppos, apos, walls, moves, lmove, pwalls, awalls, turns, winner = False, True, 9, 9, (5, 1), (5, 9), [], {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}, None, 10, 10, 1, "Nobody"
    
    updateBoard(screen, walls, ppos, apos, None, None)
    
    #main logic loop
    while running:
        
        #make player1 move
        if not gameOver:
            ppos, walls, lmove, pwalls = humanMove(boardSizeX, boardSizeY, walls, ppos, apos, screen, lmove, pwalls, "p1")
            gameOver, winner = isGameOver(boardSizeX, boardSizeY, apos, ppos, 1, 9)
            updateBoard(screen, walls, ppos, apos, lmove, "play")
        
        #make player2 move
        if not gameOver:
            apos, walls, lmove, awalls = humanMove(boardSizeX, boardSizeY, walls, apos, ppos, screen, lmove, pwalls, "p2")
            gameOver, winner = isGameOver(boardSizeX, boardSizeY, apos, ppos, 1, 9)
            updateBoard(screen, walls, ppos, apos, lmove, "alg")
        
        
        turns += 1
        
        #exit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if gameOver:
            running = False
    if winner == "player":
        showWinner(screen, ppos, walls, ppos, apos, lmove, "player")
    else:
        showWinner(screen, apos, walls, ppos, apos, lmove, "alg")

#slides
def rules(screen):
    lGray = (100, 100, 100)
    gray = (50, 50, 50)
    dGray = (25, 25, 25)
    
    """
    Quoridor: (Show image of actual game) ###
    Quoridor is a turn-based strategy game
    played on a 9x9 board. Players start on
    opposite sides of the board, and on each
    turn can move to an adjacent tile or
    place a wall.
    
    Objective: (Show virtual board) ###
    First player to reach the other's
    side of the board wins the game.
    
    Walls: (Show a board state) ###
    Each wall is two spaces long and must be placed
    inbetween tiles. Each player starts the game
    with 10 walls and once they are placed they
    cannot be moved. Players cannot jump over
    walls and must walk around them.
    
    Placement (Show a wall being dissalowed from being placed ontop of another wall): 2 frames ###
    Walls can be placed either vertically or
    horizontally and cannot be placed ontop
    of other walls.
    
    Placement (Show a wall being dissalowed from being placed to box an opponent) 2 frames ###
    Players are not allowed to place walls
    that make the opponents path to their
    victory row impossible to reach
    
    Controls (show switching between wall and move mode with the keys being pressed): 2 frames ###
    To switch between moving and placing
    walls, press w and q respectively.
    
    Arrows (show player changing movement options with arrow keys shown): 4 frames ###
    To move your player or put a wall in
    place use the arrow keys.
    
    Rotation (show a wall being rotated with r key shown): 2 frames ###
    To rotate a wall press R.
    """
    
    slides = [
        { #what is love
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Quoridor', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'Quoridor is a turn-based strategy game', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), 'played on a 9x9 board. Players start on', True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'opposite sides of the board, and on each', True, lGray, "c", (300, 190)],
                [pygame.font.SysFont("Bahnschrift", 20), 'turn can move to an adjacent space or', True, lGray, "c", (300, 220)],
                [pygame.font.SysFont("Bahnschrift", 20), 'place a wall.', True, lGray, "c", (300, 250)],
            ],
                    "images": [
                ["assets//qba 2.jfif", (188, 300)]
            ],
                    "gifs": [
                
            ],
        },

        { #objective
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Objective', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), "First player to reach the other's", True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'side of the board wins the game.', True, lGray, "c", (300, 190)],
                [pygame.font.SysFont("Bahnschrift", 16), '<- Blue victory row', True, (0, 0, 255), "l", (386, 312)],
                [pygame.font.SysFont("Bahnschrift", 16), 'Red victory row ->', True, (255, 0, 0), "r", (214, 462)],
            ],
                    "images": [
                ["assets//board.png", (214, 300)],
            ],
                    "gifs": [
                
            ],
        },
        
        {
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Walls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'Each wall is two spaces long and must be placed', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), 'inbetween tiles. Each player starts the game', True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'with 10 walls and once they are placed they', True, lGray, "c", (300, 190)],
                [pygame.font.SysFont("Bahnschrift", 20), 'cannot be moved. Players cannot jump over', True, lGray, "c", (300, 220)],
                [pygame.font.SysFont("Bahnschrift", 20), 'walls and must walk around them.', True, lGray, "c", (300, 250)],
            ],
                    "images": [
                    
            ],
                    "gifs": [
                ["assets//walls1.png", "assets//walls2.png", "assets//walls3.png", "assets//walls4.png", (187, 300), (186, 300), (187, 300), (188, 300)]
            ],
        },
        { #no overlap
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Walls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'Walls can be placed either vertically or', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), 'horizontally and cannot be placed ontop', True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'of other walls.', True, lGray, "c", (300, 190)],
            ],
                    "images": [
                
            ],
                    "gifs": [
                ["assets//nooverlap1.png", "assets//nooverlap2.png", (223, 250), (223, 249)],
            ],
        },
        { #nobox
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Walls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'Players are not allowed to place walls', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), "that make the opponent's path to their", True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'victory row impossible to reach', True, lGray, "c", (300, 190)],
            ],
                    "images": [
                ["assets//nofullbox.png", (200, 300)]
            ],
                    "gifs": [
                #boxing in player
            ],
        },
        { #pp
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Passing Pawns', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), "If you move into an occupied square", True, lGray, "c", (300, 160)],
                [pygame.font.SysFont("Bahnschrift", 20), 'your pawns will sit next to eachother', True, lGray, "c", (300, 190)],
            ],
                    "images": [
                ["assets//passingpawns.png", (186, 250)]
            ],
                    "gifs": [
                
            ],
        },
        { #change modes
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Controls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'To switch between moving and placing walls', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), 'walls, press w(movement) and q(walls).', True, lGray, "c", (300, 160)],
            ],
                    "images": [
                
            ],
                    "gifs": [
                ["assets//keyboard1.png", "assets//keyboard2.png", (50, 250), (50, 250)]
            ],
        },
        { #move
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Controls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'To control the movement of walls', True, lGray, "c", (300, 130)],
                [pygame.font.SysFont("Bahnschrift", 20), 'and pawns use the arrow keys.', True, lGray, "c", (300, 160)],
            ],
                    "images": [
                
            ],
                    "gifs": [
                ["assets//move1.png", "assets//move2.png", "assets//move3.png", "assets//move4.png", (188, 250), (188, 249), (188, 250), (188, 250)]
            ],
        },
        { #rotate
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 48), 'Controls', True, dGray, "c", (300, 50)],
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to continue', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'To rotate a wall press R.', True, lGray, "c", (300, 130)],
            ],
                    "images": [
                
            ],
                    "gifs": [
                ["assets//rotate1.png", "assets//rotate2.png", (225, 250), (224, 250)]
            ],
        },
        { #gl
                    "text": [
                [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to exit', True, gray, "c", (300, 550)],
                [pygame.font.SysFont("Bahnschrift", 20), 'Good luck, and have fun!', True, lGray, "c", (300, 250)],
            ],
                    "images": [
                
            ],
                    "gifs": [
                
            ],
        },
    ]
    
    if hasattr(sys, "_MEIPASS"):
        current_dir = Path(sys._MEIPASS)
    else:
        current_dir = Path(__file__).resolve().parent
    
    frame = 0
    timer = time.time()
    for i in slides:
        while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            screen.fill((255,255,255))
            if len(i["images"]) != 0:
                for j in i["images"]:
                    screen.blit(pygame.image.load(str(current_dir / j[0])).convert_alpha(), j[1])
            current_time = time.time()
            if current_time - timer >= 0.52: #0.52
                frame += 1
                timer = current_time
            if i["gifs"]:
                for gif in i["gifs"]:
                    if not gif:
                        continue
                    num_frames = len(gif) // 2
                    if num_frames == 0:
                        continue  # skip empty gifs
                    index = frame % num_frames
                    path = gif[index]
                    pos = gif[index + num_frames]
                    image = pygame.image.load(str(current_dir / path)).convert_alpha()
                    screen.blit(image, pos)
            drawTexts(screen, i["text"])
            pygame.display.flip()
            pygame.event.pump()
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            if keyboard.is_pressed("esc"):
                return
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
def settings(screen, difficulty):
    
    red = (255, 0, 0)
    gray = (50, 50, 50)
    dGray = (25, 25, 25)
    lGray = (100, 100, 100)
    
    texts = [
        [pygame.font.SysFont("Bahnschrift", 48), 'Settings', True, dGray, "c", (300, 50)],
        [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to exit', True, gray, "c", (300, 550)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Difficulty[                                     ]', True, lGray, "l", (165, 250)],
    ]
    
    rexts = [
        [pygame.font.SysFont("Bahnschrift", 12), '1(Fastest)', True, lGray, "l", (235, 250)],
        [pygame.font.SysFont("Bahnschrift", 12), '2', True, lGray, "l", (290, 250)],
        [pygame.font.SysFont("Bahnschrift", 12), '3', True, lGray, "l", (300, 250)],
        [pygame.font.SysFont("Bahnschrift", 12), '4', True, lGray, "l", (310, 250)],
        [pygame.font.SysFont("Bahnschrift", 12), '5(Smartest)', True, lGray, "l", (320, 250)],
    ]
    
    key = None
    cursor = difficulty - 1
    
    screen.fill((255,255,255))
    nTexts = [item.copy() for item in rexts]
    nTexts[cursor][3] = red
    drawTexts(screen, texts)
    drawTexts(screen, nTexts)
    pygame.display.flip()
    
    while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
        pygame.event.pump()
    key = keyboard.read_key()
    while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
        pygame.event.pump()
    
    while not key == "space" or key == "esc":
        
        if key == "left":
            if cursor != 0:
                cursor -= 1
            else:
                cursor = 4
        if key == "right":
            if cursor != 4:
                cursor += 1
            else:
                cursor = 0
        if key == "esc":
                return
        
        screen.fill((255,255,255))
        nTexts = [item.copy() for item in rexts]
        nTexts[cursor][3] = red
        drawTexts(screen, texts)
        drawTexts(screen, nTexts)
        pygame.display.flip()
        
        while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
        key = keyboard.read_key()
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
        
    difficulty = cursor + 1
    return difficulty
def credits(screen):
    lGray = (100, 100, 100)
    gray = (50, 50, 50)
    dGray = (25, 25, 25)
    texts = [
        [pygame.font.SysFont("Bahnschrift", 48), 'Credits', True, dGray, "c", (300, 50)],
        [pygame.font.SysFont("Bahnschrift", 28), 'Press Space to exit', True, gray, "c", (300, 550)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Developer', True, gray, "c", (150, 100)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Benjamin Sullivan', True, lGray, "c", (150, 120)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Development Help', True, gray, "c", (150, 170)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Xavier Bradford', True, lGray, "c", (150, 190)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Jack Ellingwood', True, lGray, "c", (150, 210)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Algorithm Inspiration', True, gray, "c", (150, 260)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Sebastian Lague', True, lGray, "c", (150, 280)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Mentor', True, gray, "c", (150, 330)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Eric Kawamoto', True, lGray, "c", (150, 350)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Playtesters', True, gray, "c", (450, 100)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Amos Varney', True, lGray, "c", (450, 120)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Elise Sullivan', True, lGray, "c", (450, 140)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Gabriel Hoy', True, lGray, "c", (450, 160)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Gideon Varney', True, lGray, "c", (450, 180)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Jeffrey Sullivan', True, lGray, "c", (450, 200)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Luke Sullivan', True, lGray, "c", (450, 220)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Matthew Dyer', True, lGray, "c", (450, 240)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Nicholas Sullivan', True, lGray, "c", (450, 260)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Scarlet Quimi', True, lGray, "c", (450, 280)],
        
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Presentation Feedback', True, gray, "c", (450, 330)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Elise Sullivan', True, lGray, "c", (450, 350)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Jeffrey Sullivan', True, lGray, "c", (450, 370)],
        
        [pygame.font.SysFont("Bahnschrift", 24), 'Artistic Consultant', True, gray, "c", (450, 420)],
        [pygame.font.SysFont("Bahnschrift", 16), 'Elise Sullivan', True, lGray, "c", (450, 440)],
    ]
    
    screen.fill((255,255,255))
    drawTexts(screen, texts)
    pygame.display.flip()
    
    while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
    while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

#main
def main():
    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill((255,255,255))
    pygame.display.set_caption('Minimax Quoridor')
    
    vlgray = (220, 220, 220)
    gray = (50, 50, 50)
    lGray = (100, 100, 100)
    red = (255, 0, 0)
    
    sTexts = [
        [pygame.font.SysFont("BahnschriftB", 48), 'Todd Quoridor Algorithm', True, gray, "c", (300, 50)],
        [pygame.font.SysFont("BahnschriftB", 24), 'By Benjamin Sullivan', True, gray, "c", (300, 75)],
        [pygame.font.SysFont("Bahnschrift", 12), 'Use arrow keys to select', True, lGray, "l", (10, 560)],
        [pygame.font.SysFont("Bahnschrift", 12), 'Use space to confirm', True, lGray, "l", (10, 580)],
    ]
    
    texts = [
        [pygame.font.SysFont("Bahnschrift", 20), 'Play vs Algorithm', True, lGray, "c", (300, 200)],
        [pygame.font.SysFont("Bahnschrift", 20), 'Play vs Player (coming soon!)', True, vlgray, "c", (300, 225)],
        [pygame.font.SysFont("Bahnschrift", 20), 'Tutorial', True, lGray, "c", (300, 250)],
        [pygame.font.SysFont("Bahnschrift", 20), 'Credits', True, lGray, "c", (300, 275)],
        [pygame.font.SysFont("Bahnschrift", 20), 'Settings', True, lGray, "c", (300, 300)],
        [pygame.font.SysFont("Bahnschrift", 20), 'Exit', True, lGray, "c", (300, 325)],
    ]
    
    difficulty = 3
    
    cursor = 0
    running = True
    while running:
        
        screen.fill((255,255,255))
        nTexts = [item.copy() for item in texts]
        nTexts[cursor][3] = red
        drawTexts(screen, sTexts)
        drawTexts(screen, nTexts)
        pygame.display.flip()
        
        while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
        key = keyboard.read_key()
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()
        
        while key != "space":
            if key == "up":
                if cursor != 0:
                    cursor -= 1
                else:
                    cursor = len(nTexts) - 1
                if cursor == 1: cursor = 0
            if key == "down":
                if cursor != len(nTexts) - 1:
                    cursor += 1
                else:
                    cursor = 0
                if cursor == 1: cursor = 2
            if key == "esc":
                return
            
            nTexts = [item.copy() for item in texts]
            nTexts[cursor][3] = red
            
            screen.fill((255,255,255))
            drawTexts(screen, sTexts)
            drawTexts(screen, nTexts)
            pygame.display.flip()
            
            while not any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
                pygame.event.pump()
            key = keyboard.read_key()
            while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
                pygame.event.pump()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
                pygame.event.pump()
        
        if cursor == 0: vsAlg(round(difficulty / 2, 1), screen)
        elif cursor == 1: vsPlayer(screen)
        elif cursor == 2: rules(screen)
        elif cursor == 3: credits(screen)
        elif cursor == 4: difficulty = settings(screen, difficulty)
        else: running = False
        
        while any(keyboard.is_pressed(key) for key in [" ", "w", "down", "up", "right", "left", "r", "esc"]):
            pygame.event.pump()

main()