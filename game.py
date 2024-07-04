#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import math
from copy import deepcopy

class GameTreePlayer:
    
    def __init__(self):
        self.recursivecalls = 0
        # pass
    
    def FindBestAction(self,currentState):        
        # Input
        # bestAction = input("Take action (0-6) : ")
        # bestAction = int(bestAction)
        # return bestAction

        #  minimax algo
        # _, bestAction = self.minimax(currentState, 3, maxiplayer=True)
        # return bestAction

        #  alpha beta pruning
        _, bestAction = self.alphabeta_pruning(currentState, float('-inf'), float('inf'), 3, maxiplayer=True)
        return bestAction
    
    def checkwin(self,currentState,player):

        rows = 6
        cols = 7

        for row in range(rows):
            for col in range(cols - 3):
                if all(currentState[row][col + i] == player for i in range(4)):
                    return True

        for row in range(rows - 3):
            for col in range(cols):
                if all(currentState[row + i][col] == player for i in range(4)):
                    return True


        for row in range(rows - 3):
            for col in range(cols - 3):
                if all(currentState[row + i][col + i] == player for i in range(4)):
                    return True

        for row in range(rows - 3):
            for col in range(3, cols):
                if all(currentState[row + i][col - i] == player for i in range(4)):
                    return True

        return False
    
    #  Initial Evaluation Function
    # def evaluation_function(self,state):
    #     if self.checkwin(state, 2):
    #         return 1000 
    #     elif self.checkwin(state, 1):
    #         return -1000
    #     elif all(cell != 0 for row in state for cell in row):
    #         return 0
    #     else:
    #         return 500

    #  Modified Evaluation Function
    def evaluation_function(self,state):
        if self.checkwin(state, 2):
            return 1000 
        elif self.checkwin(state, 1):
            return -1000
        elif all(cell != 0 for row in state for cell in row):
            return 0
        else:
            return self.possible_winningpositions(state,2) - self.possible_winningpositions(state,1)
    
    # Move ordering Heuristic
    def move_ordering(self, state, action):
        return (
            self.positions_aftermove(state, action, player=2)
            + self.block_opponent(state, action)
        )
    
    # Possible Winning Positions after move
    def positions_aftermove(self, state, action, player):
         simulated_state = copy.deepcopy(state)
         row = 0
         for i in range(5, -1, -1):
            if state[i][action] == 0:
                row = i
                break
         simulated_state[row][action] = player

         return self.possible_winningpositions(simulated_state,player)
    
    # Positions in which opponent is blocked from winning after move
    def block_opponent(self,state,action):
        simulated_state = copy.deepcopy(state)
        row = 0
        for i in range(5, -1, -1):
          if state[i][action] == 0:
              row = i
              break
        simulated_state[row][action] = 2

        return self.possible_winningpositions(state,1) - self.possible_winningpositions(simulated_state,1)
        
    # Possible winning positions for a player
    # Winning position -> A player can still use those cells to win the game
    def possible_winningpositions(self, state, player):
        horizontal_wins = self.count_horizontal_wins(state, player)
        vertical_wins = self.count_vertical_wins(state, player)
        diagonal_up_wins = self.count_diagonal_up_wins(state, player)
        diagonal_down_wins = self.count_diagonal_down_wins(state, player)

        return horizontal_wins + vertical_wins + diagonal_up_wins + diagonal_down_wins

    def count_horizontal_wins(self, state, player):
        count = 0
        for row in range(6):
            for col in range(4):
                if state[row][col] != 3-player and all(state[row][col + i] == player or state[row][col + i] == 0 for i in range(1, 4)):
                    count += 1
        return count

    def count_vertical_wins(self, state, player):
        count = 0
        for row in range(3):
            for col in range(7):
                if state[row][col] != 3-player and all(state[row + i][col] == player or state[row + i][col] == 0 for i in range(1, 4)):
                    count += 1
        return count

    def count_diagonal_up_wins(self, state, player):
        count = 0
        for row in range(3):
            for col in range(4):
                if state[row][col] != 3-player and all(state[row + i][col + i] == player or state[row + i][col + i] == 0 for i in range(1, 4)):
                    count += 1
        return count

    def count_diagonal_down_wins(self, state, player):
        count = 0
        for row in range(3):
            for col in range(3, 7):
                if state[row][col] != 3-player and all(state[row + i][col - i] == player or state[row + i][col - i] == 0 for i in range(1, 4)):
                    count += 1
        return count

    
    def minimax(self, state, depth, maxiplayer):

        self.recursivecalls += 1

        if depth == 0 or self.checkwin(state, 1) or self.checkwin(state, 2):
            return self.evaluation_function(state), None

        valid_actions = [action for action in range(7) if state[0][action] == 0]

        # ordered_actions = valid_actions

        # move ordering heuristic
        ordered_actions = sorted(valid_actions, key=lambda action: self.move_ordering(state, action), reverse=True)

        if maxiplayer:
            max_val = -math.inf
            best_action = None

            for action in ordered_actions:
                new_state = self.perform_action(state, action, 2)
                value, _ = self.minimax(new_state, depth - 1, False)

                if value > max_val:
                    max_val = value
                    best_action = action

            return max_val, best_action

        else:
            min_val = math.inf
            best_action = None

            for action in ordered_actions:
                new_state = self.perform_action(state, action, 1)
                value, _ = self.minimax(new_state, depth - 1, True)

                if value < min_val:
                    min_val = value
                    best_action = action

            return min_val, best_action


    def alphabeta_pruning(self, state, alpha, beta, depth, maxiplayer):

        self.recursivecalls += 1

        if depth == 0 or self.checkwin(state,1) or self.checkwin(state,2):
            return self.evaluation_function(state), None

        valid_actions = [action for action in range(7) if state[0][action] == 0]

        # ordered_actions = valid_actions

        # move ordering heuristic
        ordered_actions = sorted(valid_actions, key=lambda action: self.move_ordering(state, action), reverse=True)

        if maxiplayer:
            max_val = -math.inf
            bestAction = None

            for action in ordered_actions:
                new_state = self.perform_action(state, action, 2)
                value, _  = self.alphabeta_pruning(new_state, alpha, beta, depth - 1, False)

                if value > max_val:
                    max_val = value
                    bestAction = action

                alpha = max(alpha, value)
                
                if alpha >= beta:
                    break

            return max_val, bestAction

        else: 
            min_val = math.inf
            bestAction = None

            for action in ordered_actions:
                new_state = self.perform_action(state, action, 1)
                value, _  = self.alphabeta_pruning(new_state, alpha, beta, depth - 1, True)

                if value < min_val:
                    min_val = value
                    bestAction = action

                beta = min(beta, value)

                if alpha >= beta:
                    break

            return min_val, bestAction
        

    def perform_action(self, state, action, player):
        new_state = [row[:] for row in state]  
        for row in range(5, -1, -1):
            if new_state[row][action] == 0:
                new_state[row][action] = player  
                break

        return new_state


def LoadTestcaseStateFromCSVfile():
    testcaseState = list()

    with open('testcase.csv', 'r') as read_obj: 
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
            
    return testcaseState


def PlayGame(games):

    total_wins_player1 = 0
    total_wins_player2 = 0
    total_moves = 0
    total_moves_win = 0
    total_calls = 0

    for game in range(games):
      fourConnect = FourConnect()
      fourConnect.PrintGameState()
      gameTree = GameTreePlayer()
      
      move=0
      while move<42: #At most 42 moves are possible
          if move%2 == 0: #Myopic player always moves first
              fourConnect.MyopicPlayerAction()
          else:
              currentState = fourConnect.GetCurrentState()
              gameTreeAction = gameTree.FindBestAction(currentState)
              fourConnect.GameTreePlayerAction(gameTreeAction)
              calls = gameTree.recursivecalls
              
          fourConnect.PrintGameState()
          move += 1
          if fourConnect.winner!=None:
              break
          
      total_moves += move
      total_calls += calls

      if fourConnect.winner==None:
          print("Game is drawn.")
      else:
          print("Winner : Player {0}\n".format(fourConnect.winner))
          if fourConnect.winner == 1:
              total_wins_player1 += 1
          elif fourConnect.winner == 2:
              total_wins_player2 += 1
              total_moves_win += move

      print("Moves : {0}".format(move))

    average_calls = total_calls / games
    average_moves = total_moves / games
    average_moves_win = 0
    if(total_wins_player2 != 0):
      average_moves_win = total_moves_win / total_wins_player2


    print("\nResults after playing {} games:".format(games))
    print("Total wins for Player 1: {}".format(total_wins_player1))
    print("Total wins for Player 2: {}".format(total_wins_player2))

    print("Average number of moves: {:.2f}".format(average_moves))
    print("Average number of moves per win(player 2): {:.2f}".format(average_moves_win))

    # print("Total number of recursive calls: {:.2f}".format(total_calls))
    # print("Average number of recursive calls: {:.2f}".format(average_calls))

def RunTestCase():
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
        
    print("Moves : {0}".format(move))
    

def main():
    
    PlayGame(50)    
    #RunTestCase()

if __name__=='__main__':
    main()