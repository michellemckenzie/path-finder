import copy

#this is the calling function that will process the initial state and then send it to be examined, and have operators applied to it
def rushhour(h, initial_state):

    if initial_state == []:
        print('No puzzle was provided. Ending now')
        return
    
    fn = blockingHeuristic(initial_state)
    gn = 0
    frontier = [(fn, initial_state, gn)]
    
    path, moves, statesExplored = statesearch(frontier, initial_state, h)
    path.reverse()

    for board in path:
        for row in board:
            print(row)
        print(' ')

    print('Moves: ' + str(moves))
    print('States explored ' + str(statesExplored))

#statesearch follows the A* algorithm and inserts nodes into a priority queue, then sorts by the f(n) value. It pops off the first node in the priority queue, checks to see if it is a winner, and if it's not it will apply operators to move vehicles around. Once the operators have been completed, generate f(n) and g(n) values, and distinguish if the new nodes are already in the priority queue, or have already been examined. Repeat this until there are no more nodes to evaluate, which means there is no solution, or until XX is in the correct position.
def statesearch(frontier, initial, h):
    seen = []
    linkedListTree = {}

    while frontier != []:
        firstNode = frontier.pop(0)
        front = firstNode[1]
        seen.append(front)

        if goalReached(front):
            path = generatePath(linkedListTree, front, initial)
            return path, len(path) - 1, len(seen)
        else:
            newNodes = generateNewStates(front)
            newKids = []

            #look through all of the new states we just generated and check to see if we have already seen them before
            for node in newNodes:
                gn = g(node, linkedListTree)
                if (h == 0):
                    fn = gn + blockingHeuristic(node)
                else:
                    fn = gn + myHeuristic(node, linkedListTree, front, initial, seen) 

                inFrontier = False
                for f in range(len(frontier)):
                    #we have found a state that's the same as the current front and the f(n) value is higher than what we just calculated, so let's replace it
                    if frontier[f][1] == node and frontier[f][0] > fn:
                        frontier.pop(f)
                        frontier.append((fn, node, gn))
                        inFrontier = True
                    elif frontier[f][1] == node:
                        inFrontier = True
                
                inSeen = False
                if node in seen:
                    inSeen = True
                
                if not inFrontier and not inSeen:
                    frontier.append((fn, node, gn))
                    newKids.append(node)

            #find the child's parent to create an element that will be inserted into the linked list
            parent = None
            for leaf in linkedListTree:
                for child in linkedListTree[leaf][1]:
                    if child == front:
                        parent = leaf
            if ' '.join(front) not in linkedListTree:
                #firstNode[2] = g(n), which we need for later calculations for a child's g(n)
                linkedListTree[' '.join(front)] = [parent, newKids, firstNode[2]]

    #if no solution was printed and we reach this point, the puzzle has not solution        
    print('The puzzle cannot be solved')
    return [], 0, 0

#this is the blocking heuristic from the homework prompt and it returns g(n) = 0 if XX is in the correct spot, else it returns the amount of cars in the way + 1
def blockingHeuristic(n):
    if n[2][4] == 'X' and n[2][5] == 'X':
        return 0
    
    index = n[2].rfind('X') + 2

    blocking = 1

    for i in range(index,6):
        if n[2][i] != '-':
            blocking += 1

    return blocking

#my heuristic immediately prints the path once it finds XX in the correct spot and does not bother returning the g(n) value for the target goal to keep looking otherwise, if XX is not in the right spot, estimate how many cars are still in the way
def myHeuristic(n, linkedListTree, front, initial, seen):
    if n[2][4] == 'X' and n[2][5] == 'X':
        path = generatePath(linkedListTree,front,initial)
        moves = len(path)
        path.reverse()
        for board in path:
            for row in board:
                print(row)
            print(' ')

        print('Moves: ' + str(moves))
        print('States explored ' + str(len(seen)))
        exit()
    
    index = n[2].rfind('X') + 2
    blocking = 1

    for i in range(index,6):
        if n[2][i] != '-':
            blocking += 1

    return blocking

#return the value of the child's parent's g(n) + 1
def g(node, linkedListTree):
    for leaf in linkedListTree:
        for child in linkedListTree[leaf][1]:
            if child == node:
                return 1 + linkedListTree[leaf][2]  
    return 0


#go through all the possible operators for each vehicle, and return a list of newly generated states
def generateNewStates(currState):
    newStates = []

    newStates.extend(left(currState))
    newStates.extend(right(currState))
    newStates.extend(up(currState))
    newStates.extend(down(currState))

    newStates = filter(None, newStates)
    return newStates

#this function will check to see if there is a horizontal vehicle in the row
#and will check to see if there is an empty space to the left to move to
def left(vehicles):
    newBoards = []

    for row in range (6):
        col = 0
        while col < 6:
            if vehicles[row][col] != "-" and 0 < col < 5 and vehicles[row][col+1] == vehicles[row][col] and vehicles[row][col-1] == '-':
                moveTo = - 1

                #the vehicle is 3 spaces long
                if col < 4 and vehicles[row][col+2] == vehicles[row][col]:
                    openSpace = col + 2
                #the vehicle is 2 spaces long
                else:
                    openSpace = col + 1

                newList = createNewHorizontalBoard(vehicles, row, col, moveTo, openSpace)
                newBoards.append(newList)
                col += openSpace
            else:
                col += 1
    return newBoards

#this function will check to see if there is a horizontal vehicle in the row
#and will check to see if there is an empty space to the right to move to
def right(vehicles):
    newBoards = []

    for row in range (6):
        col = 0
        while col < 6:
            moveTo = 0

            if vehicles[row][col] != "-" and col < 4 and vehicles[row][col+1] == vehicles[row][col]:
                #the vehicle is 3 spaces long
                if col < 3 and vehicles[row][col+2] == vehicles[row][col] and vehicles[row][col+3] == '-':
                    moveTo = 3
                #the vehicle is 2 spaces long
                elif vehicles[row][col+2] == '-':
                    moveTo = 2
                    
                if moveTo == 2 or moveTo == 3:
                    openSpace = col
                    newList = createNewHorizontalBoard(vehicles, row, col, moveTo, openSpace)
                    newBoards.append(newList)
                    col += moveTo

            col += 1
    return newBoards

#create a list of the row that is being modified so that we can change the characters
#then create a deep copy of the original board, set the row to the new modified row, and return the deep copy
#that is the new horizontally moved board 
def createNewHorizontalBoard (vehicles, row, col, moveTo, openSpace):
    newRow = list(vehicles[row])
    newRow[col+moveTo] = vehicles[row][col]
    newRow[openSpace] = '-'

    newList = copy.deepcopy(vehicles)
    newList[row] = ''.join(newRow)
    return newList

#this function will check to see if there is a vertical vehicle in the column
#and will check to see if there is an empty space to above to move to
def up(vehicles):
    newBoards = []
    moved = []

    for row in range(6):
        for col in range (6):
            if vehicles[row][col] not in moved and vehicles[row][col] != "-" and 0 < row < 5 and vehicles[row+1][col] == vehicles[row][col] and vehicles[row-1][col] == '-':
                moveTo = - 1

                if row < 4 and vehicles[row+2][col] == vehicles[row][col]:
                    openSpace = row + 2
                else:
                    openSpace = row + 1

                moved.append(vehicles[row][col])
                newList = createNewVerticalBoard(vehicles, row, col, moveTo, openSpace)
                newBoards.append(newList)
    return newBoards

#this function will check to see if there is a vertical vehicle in the column
#and will check to see if there is an empty space to below to move to
def down(vehicles):
    newBoards = []
    moved = []

    for row in range (6):
        for col in range(6):
            moveTo = 0

            if vehicles[row][col] not in moved and vehicles[row][col] != "-" and row < 4 and vehicles[row+1][col] == vehicles[row][col]:
                if row < 3 and vehicles[row+2][col] == vehicles[row][col] and vehicles[row+3][col] == '-':
                    moveTo = 3
                elif vehicles[row+2][col] == '-':
                    moveTo = 2
                    
                if moveTo == 2 or moveTo == 3:
                    openSpace = row
                    newList = createNewVerticalBoard(vehicles, row, col, moveTo, openSpace)
                    newBoards.append(newList)
                    moved.append(vehicles[row][col])
    return newBoards

#create lists of the rows that are being modified so that we can change the characters
#then create a deep copy of the original board, set the rows to the new modified rows, and return the deep copy
#that is the new vertically moved board 
def createNewVerticalBoard(vehicles, row, col, moveTo, openSpace):
    newOccupiedRow = list(vehicles[row+moveTo])
    newOpenRow = list(vehicles[openSpace])

    newOccupiedRow[col] = vehicles[row][col]
    newOpenRow[col] = '-'

    newList = copy.deepcopy(vehicles)
    newList[row+moveTo] = ''.join(newOccupiedRow)
    newList[openSpace] = ''.join(newOpenRow)
    return newList

#if XX is in the two far right spaces of the third row, we have won the puzzle
def goalReached(node):
    if node[2][4] == "X" and node[2][5] == "X":
        return True
    return False

#This function traverses through a linked list to create the most optimal path
#by finding the child's parent, and appending that to the path, and so on
#and so forth until it reaches the initial state. Then it returns.
def generatePath(linkedListTree, front, initial):
    path = [front]
    current = front
    
    while True:
        for leaf in linkedListTree:
            for child in linkedListTree[leaf][1]:
                #if the current node matches someone's child
                if child == current:
                    #set current to the parent of the child
                    current = leaf.split(' ')
                    path.append(current)
                    #once we reach the initial node we have completed the path
                    if current == initial:
                        return path

#rushhour(0,["--B---","--B---","XXB---","--AA--","------","------"])
rushhour(0, ["---O--","---O--","XX-O--","PQQQ--","P-----","P-----"])
#rushhour(1, ["OOOP--","--AP--","XXAP--","Q-----","QGGCCD","Q----D"])
#rushhour(1, ["--OPPP","--O--A","XXO--A","-CC--Q","-----Q","--RRRQ"])
#rushhour(1, ["-ABBO-","-ACDO-","XXCDO-","PJFGG-","PJFH--","PIIH--"])
#rushhour(0, ['OOO--P','-----P','--AXXP','--ABCC','D-EBFF','D-EQQQ'])
