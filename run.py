
''' Monopoly-Command Line - V.01

- Bugfixes will be ongoing at this point, especially in
interactor.py
- Args:

	:players: number of players (technically no limite at the moment,
				really shouldn't be more than 5)
	:turns: number of turns
	:mode: game mode; default, worth
'''

import argparse
from monopoly import Monopoly


def command_line():
	desc = '''  	 _____________________________________________________
	|     M     O     N     O     P     O     L     Y     |
	 -----------------------------------------------------

	This is a command-line interpretation of Hasbro's famous
	board game, Monopoly. This is intended to be a personal project,
	so no party is profiting in any way from this creation. Enjoy!'''

	parser = argparse.ArgumentParser(version='0.1',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=desc)

	parser.add_argument('-players', type=int, dest='players',
						help="Number of Players", default=3)

	parser.add_argument('-turns', type=int, dest='turns',
						help="Number of Turns (default 50)", default=50)

	mode_help = ''' 'default' is a last-man-standing style, where the only
				player not bankrupt wins. 'worth' selects winner based on highest
				net worth. '''

	parser.add_argument('-mode', type=str, dest='mode',
						help=mode_help, default='default')

	return parser.parse_args()

if __name__ == '__main__':

	args = command_line()

	monopoly = Monopoly(args.players)
	monopoly.setup()
	monopoly.play(args.turns, args.mode)
