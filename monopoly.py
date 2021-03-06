
''' Game Engine.
which intializes essential game elements, and
coordinates them. These elements include mechanics like turns,
as well as game state updates (like for rent or logs).
'''

from models import Board, Cards, Bank, Player
from models import DbInterface
from config import DEFAULT_TILES
from models import Interactor
from models import GameLogger
from colorama import Fore, Style


class Monopoly(object):
	''' This is the game engine.

		:num_players: - number of players in game (see command-line interface.)
		:turns: - number of turns in game (see command-line interface.)
		:board: - by default, Board object using standard tiles.
		:cards: - by default, Cards object using standard game cards.
	'''

	def __init__(self, num_players, board=Board(DEFAULT_TILES), cards=Cards()):
		self.num_players = num_players
		self.players = {}
		self.board = board
		self.bank = Bank(board, self.players)
		self.cards = cards
		self.turns = 0

	def setup(self):
		''' Factory method that sets up Player objects, and essential
		in-game elements e.g. the game logger. '''

		print Style.BRIGHT + Fore.WHITE + "\nWelcome to command-line Monopoly! Let's set your game up.\n"
		# creates all players
		for player in range(1, self.num_players + 1):
			name = raw_input("What's your name player? > ")
			self.players[name] = Player(name, self.board, self.cards)

		# includes name of other players, for future interaction purposes
		for player in self.players.values():
			player.others = [other for other in self.players.values()
							if other != player]
			print "Player %s has been added to game." % (player.name)

		self.cards.shuffle_cards()

		# set up interactor
		Interactor.players = self.players
		Interactor.board = self.board
		Interactor.bank = self.bank
		Interactor.cards = self.cards
		Interactor.db = DbInterface()
		print 'Interactor Initialized!'

		# set up game logger
		GameLogger.players = self.players
		GameLogger.player_logs = {p: [] for p in self.players}
		print 'Game logger initialized!'
		return "Setup complete"

	def turn(self):
		''' Advances game state - orchestrates a turn for each player using
		the Player.roll_dice() method.'''

		for player in self.players.values():
			print "\n%s, it's your turn now!" % player.name
			player.inspect_self()

			current_location = player.roll_dice(self.board, self.bank)
			if current_location is not None:
				player.interact(current_location, self.board, self.bank)

			if player.money < 0:
				pass
			# bankrupcty protocol
			player.check_monopoly()
			self.bank.update_all_rents(self.players)
			GameLogger.push_public_logs()

		msg = "\n -- End of Turn %s. \n" % self.turns
		GameLogger.add_log(msg=msg)
		self.turns += 1
		return

	def play(self, turns, mode):
		''' Runs the game, following setup, for a duration specified by
		the command-line argument, 't' (50 by default).'''

		for _ in range(turns):
			self.turn()
		self.summary()
		self.select_winner(mode)
		return

	def select_winner(self, mode='default'):
		''' After the game ends, process who the game winners are based on
		requirements set by game mode. '''

		if mode == 'default':
			for player in self.players.values():
				if player._inplay is True:
					print "%s is the winner!" % player.name

		elif mode == 'worth':
			winner_worth = 0
			winner_name = None
			for player in self.players.values():
				if player.net_worth()[0] > winner_worth:
					winner_worth = player.net_worth()[0]
					winner_name = player.name
			print Fore.GREEN + Style.BRIGHT + "%s is the winner!" % winner_name

	def summary(self):
		''' Summary stats displayed following the game. '''

		print "_"*40
		print ' '*5, 'G A M E  S U M M A R Y', ' '*5
		print '%s turns have elapsed in this game.\n' % self.turns
		for player in self.players.values():
			print "Player: %s" % player.name
			print "Total Net Worth: $%s" % player.net_worth()[0]
			print "Money: $%s" % player.money
			print "%% Net Worth in Cash: %s" % player.net_worth()[1]
			print "%% Net Worth in Assets: %s" % player.net_worth()[2]
			print "Emergency Liquidity: $%s" % (player.net_worth()[0] * player.net_worth()[2])
			property_display = [p.name for p in player.properties.values()]
			print "Properties: %s" % property_display
			print "Monopolies: %s\n\n" % player.check_monopoly()
