import random
import datetime
import copy

class Team35:

	def __init__(self):
		self.one_value = 5
		self.two_value = 10
		self.twohalf_value = 50
		self.three_value = 100
		self.ALPHA = -100000000
		self.BETA = 100000000
		self.dict = {}
		self.lenght = 0
		self.HIGH_POS = [(0,0),(1,1),(2,2),(1,2),(2,1)]
		self.LOW_POS = [(0,1),(1,0),(1,2),(2,1)]

		self.timeLimit = datetime.timedelta(seconds = 23)
		self.begin = 0
		self.WIN_UTILITY = 1000000
		self.cell_win = 1000
		self.bonus = 0
		self.opp_bonus = 0
		self.won1 = False
		self.won2 = False
		self.player = 1



	def minimax(self,old_move, depth, max_depth, bonus , alpha, beta, isMax, p_board, p_block, flag1, flag2, best_node):
		if datetime.datetime.utcnow() - self.begin > self.timeLimit:
			return (-111,(-1,-1))
		terminal_state = p_board.find_terminal_state()
		if terminal_state[1] == 'WON' :
			if terminal_state[0] == flag1 :
				return (self.WIN_UTILITY,old_move)
			if terminal_state[0] == flag2 :
				return (-self.WIN_UTILITY,old_move)

		if depth==max_depth:
			utility = self.check_utility_box(p_block,p_board)


			if flag1 == 'o':
				return (-utility,old_move)

			return (utility,old_move)
		else:
			children_list = p_board.find_valid_move_cells(old_move)

			random.shuffle(children_list)
			if len(children_list) == 0:
				utility = self.check_utility_box(p_block,p_board)

				if flag1 == 'o':
					return (-utility,old_move)
				return (utility,old_move)

			for child in children_list:

				if isMax:
					status,self.won1=p_board.update(old_move,child,flag1)
				else:
					status,self.won2=p_board.update(old_move,child,flag2)

				if self.won1 == True and self.bonus <= 1:
					self.bonus += 1
				elif self.won2 == True and self.opp_bonus <= 1:
					#isMax = False
					self.opp_bonus += 1
					
				if isMax:
					if self.won1 and bonus == False:
						score = self.minimax (child,depth+1,max_depth,True,alpha,beta,True,p_board,p_block,flag1,flag2,best_node)
					else:
						score = self.minimax (child,depth+1,max_depth,False,alpha,beta,False,p_board,p_block,flag1,flag2,best_node)
					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
						p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
						return (-111,(-1,-1))
					if (score[0] > alpha):
						alpha = score[0]
						best_node = child
				else:
					if self.won2 and bonus == False:
						score = self.minimax (child,depth+1,max_depth,True,alpha,beta,False,p_board,p_block,flag1,flag2,best_node)
					else:
						score = self.minimax (child,depth+1,max_depth,False,alpha,beta,True,p_board,p_block,flag1,flag2,best_node)

					if datetime.datetime.utcnow() - self.begin > self.timeLimit:
						p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
						p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
						return (-111,(-1,-1))
					if (score[0] < beta):
						beta = score[0]
						best_node = child

				p_board.big_boards_status[child[0]][child[1]][child[2]] = '-'
				p_board.small_boards_status[child[0]][child[1]/3][child[2]/3] = '-'
				if (alpha >= beta):
					break
			if isMax:
				return (alpha, best_node)
			else:
				return(beta, best_node)


	def check_utility_box(self,block,board):
		ans = 0
		for z in range(2):
			ans += 100*self.block_utility(board.small_boards_status[z],1,'x')
			ans -= 100*self.block_utility(board.small_boards_status[z],1,'o')

			temp_block = []
			for i in range(0,3):
				for j in range(0,3):
					if(board.small_boards_status[z][i][j] == '-'):
						temp_block = [[board.big_boards_status[z][3*i+k][3*j+l] for l in range(0,3)] for k in range(0,3)]
			 			ans += self.block_utility(temp_block,1,'x')
			 			ans -= self.block_utility(temp_block,1,'o')
					elif(board.small_boards_status[z][i][j] == 'x'):
						ans += self.cell_win
					elif(board.small_boards_status[z][i][j] == 'o'):
						ans -= self.cell_win
		return ans


	def move(self,board,old_move,flag1) :
		self.timeLimit = datetime.timedelta(seconds = 23)
		self.begin = 0
		self.begin = datetime.datetime.utcnow()
		temp_board = copy.deepcopy(board)

		if flag1 == 'x' :
			flag2 = 'o'
			self.player = 1
		else :
			flag2 = 'x'
			self.player = 0

		maxDepth = 3
		while datetime.datetime.utcnow() - self.begin < self.timeLimit:
			(g,g_node) = self.minimax(old_move,False,maxDepth,0,self.ALPHA,self.BETA,True,temp_board, (1,1), flag1, flag2, (7,7))
			if g != -111 :
				best_node = g_node
			maxDepth += 1
		return best_node

	def block_utility(self,block,value,flag):
		self.bonus=1
		self.opp_bonus=1
		block_1 = tuple([tuple(block[i]) for i in range(3)])

		ans = 0
		if (block_1, flag) not in self.dict:
			for pos in self.HIGH_POS:
				if block[pos[0]][pos[1]]==flag:
					ans += value*2

			for pos in self.LOW_POS:
				if block[pos[0]][pos[1]]==flag:
					ans += value

			if flag == 'x':
				flag2 = 'o'
			else:
				flag2 = 'x'
			for row in range(3):
				countflag = 0
				opponentflag = 0
				for col in range(3):
					if(block[row][col] == flag):
						countflag += 1
					elif((block[row][col] == flag2) or (block[row][col] == 'd')):
						opponentflag += 1
					if opponentflag == 0:
						if countflag == 2:
							ans += value*self.two_value
						elif countflag == 3:
							ans = value*self.three_value
					elif opponentflag == 1:
						if countflag == 2:
							ans -= value*self.twohalf_value
					elif opponentflag == 2:
						if countflag == 1:
							ans += value*self.three_value
					elif opponentflag == 3:
						if countflag == 0:
							ans = -value*self.three_value


				for col in range(3):
					countflag = 0
					opponentflag = 0
					for row in range(3):
						if(block[row][col] == flag):
							countflag += 1
						elif((block[row][col] == flag2) or (block[row][col] == 'd')):
							opponentflag += 1
						if opponentflag == 0:
							if countflag == 2:
								ans += value*self.two_value
							elif countflag == 3:
								ans = value*self.three_value
								self.bonus=1
						elif opponentflag == 1:
							if countflag == 2:
								ans -= value*self.twohalf_value
						elif opponentflag == 2:
							if countflag == 1:
								ans += value*self.three_value
						elif opponentflag == 3:
							if countflag == 0:
								ans = -value*self.three_value

				countflag = 0
				opponentflag = 0
				for diag in range(3):
					if(block[diag][diag] == flag):
						countflag += 1
					elif((block[diag][diag] == flag2) or (block[diag][diag] == 'd')):
						opponentflag += 1
					if opponentflag == 0:
						if countflag == 2:
							ans += value*self.two_value
						elif countflag == 3:
							ans = value*self.three_value
					elif opponentflag == 1:
						if countflag == 2:
							ans -= value*self.twohalf_value
					elif opponentflag == 2:
						if countflag == 1:
							ans += value*self.three_value
					elif opponentflag == 3:
						if countflag == 0:
							ans = -value*self.three_value
				countflag = 0
				opponentflag = 0
				for diag in range(3):
					if(block[diag][2-diag] == flag):
						countflag += 1
					elif((block[diag][2-diag] == flag2) or (block[diag][2-diag] == 'd')):
						opponentflag += 1
					if opponentflag == 0:
						if countflag == 2:
							ans += value*self.two_value
						elif countflag == 3:
							ans = value*self.three_value
					elif opponentflag == 1:
						if countflag == 2:
							ans -= value*self.twohalf_value
					elif opponentflag == 2:
						if countflag == 1:
							ans += value*self.three_value
					elif opponentflag == 3:
						if countflag == 0:
							ans = -value*self.three_value
				self.dict[(block_1, flag)] = ans
				return self.dict[(block_1, flag)]
		else :
			return self.dict[(block_1, flag)]
