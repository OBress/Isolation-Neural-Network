# https://neat-python.readthedocs.io/en/latest/xor_example.html
from Isolation import game
import pygame
import neat
import os
import time
import pickle
import numpy as np
import random

class IsolationGame:
    def __init__(self, window, width, height, visuals):
        self.game = game.Isolation(9, 9, window, visuals, width, height)
        self.board = self.game.board
        self.player1 = self.game.player1
        self.player2 = self.game.player2

    def test_ai(self, net):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.right_paddle.y, abs(
                self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            self.game.draw(draw_score=True)
            pygame.display.update()

    def train_ai(self, genome1, genome2, config):
    
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        valid_moves1 = self.board.get_moves(self.player1)
        
        while True:
            
            #------------------------------------ Player 1 ---------------------------------------------
            input_vector = self.board.grid.flatten()
            
            # Move then check win
            self.move_ai(input_vector, net1, genome1, self.player1, valid_moves1)
            
            # Only player 2 can lose after player 1
            valid_moves2 = self.board.get_moves(self.player2)
            if self.game.check_winner(self.player2, valid_moves2):
                self.calculate_fitness(genome1, genome2, self.game.turn+1)
                break
            
            self.game.turn = 1 if self.game.turn == 0 else 0
            
            
            #------------------------------------ Player 2 ------------------------------------
            input_vector = self.board.grid.flatten()
            
            # Move then check win
            self.move_ai(input_vector, net2, genome2, self.player2, valid_moves2)
    
            # Only player 1 can lose after player 2
            valid_moves1 = self.board.get_moves(self.player1)
            if self.game.check_winner(self.player1, valid_moves1):
                self.calculate_fitness(genome1, genome2, self.game.turn+1)
                break
            
            self.game.turn = 1 if self.game.turn == 0 else 0

    def move_ai(self, inputV, net, genome, player, vMoves=None):
        output = net.activate(inputV)
        move = self.translate_move(output, player)
        moves = vMoves if vMoves else self.board.get_moves(player)
        
        if not self.board.move(player, move, moves):
            genome.fitness -= 0.5
            if moves:
                self.board.move(player, list(moves)[0], moves)
        else:
            genome.fitness += 1
            
    def translate_move(self, output, player, num_directions=8):
        # Convert to direction
        directions = output[:num_directions]
        direction_index = np.argmax(directions)
        direction_mapping = [
                (-1, 0), (1, 0),  # Vertical
                (0, -1), (0, 1),  # Horizontal
                (-1, -1), (-1, 1),  # Diagonals
                (1, -1), (1, 1)
            ]
        direction = direction_mapping[direction_index]
        
        # Convert to distance
        distances = output[num_directions:]
        distance = np.argmax(distances)
        
        row, col = player.pos if player.pos else (4,4)
        nRow = int((row + (distance*direction[0])) / 10)
        nCol = int((col + (distance*direction[1])) / 10)
        return (nRow, nCol)

    def calculate_fitness(self, genome1, genome2, winner):
        # add winning bonus
        genome1.fitness += 5 if winner == 1 else -5
        genome2.fitness += 5 if winner == 2 else -5
        
        # print("Winner was:",winner)
        # print(self.board)
# -----
def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    width, height = 800, 800
    # win = pygame.display.set_mode((width, height))
    win = None
    # pygame.display.set_caption("Isolation")

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes)-1:
            break
        
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            
            iso = IsolationGame(win, width, height, visuals=False)
            force_quit = iso.train_ai(genome1, genome2, config)
            
            if force_quit:
                quit()


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-48')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer((10), filename_prefix='checkpoints/neat-'))

    winner = p.run(eval_genomes, 100)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    pong = PongGame(win, width, height)
    pong.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
    # test_best_network(config)
