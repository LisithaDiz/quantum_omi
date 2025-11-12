from collections import namedtuple
import pygame
import random
import sys
from pygame.locals import KEYDOWN

from qiskit import QuantumCircuit, Aer, execute

import ctypes

ctypes.windll.user32.SetProcessDPIAware()
pygame.mixer.init()
CardTuple = namedtuple('Card', ['value', 'suit'])
card_values = [7, 8, 9, 10, 11, 12, 13, 14]
card_suits = ['C', 'D', 'H', 'S']
TITLE_STRING = 'Quantum Omi'
FPS = 120
HEIGHT = 1080
WIDTH = 1920
BG_COLOR = (33, 124, 66)
GAME_FONT = 'graphics/fonts/BrownieStencil-vmrPE.ttf'

P1_C1 = (20, (HEIGHT / 3))
P1_C2 = (80, (HEIGHT / 3))

P2_C1 = (1920, (HEIGHT / 3))
P2_C2 = (1920, (HEIGHT / 3))

value_dict = {
    'J': 11,
    'Q': 12,
    'K': 13,
    '14': 14,  # Ace

    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10
}


class Card:
    def __init__(self, input_value, input_suit):
        self.animation_start_time = pygame.time.get_ticks()

        self.selected_cards = []
        self.animation_complete = False
        self.uuid = None
        self.position = None
        self.hovered = False
        self.start_position = (0, 1080)
        self.orig_position = self.start_position
        self.data = CardTuple(value=input_value, suit=input_suit)
        self.id = f"{self.data.value}{self.data.suit}"
        self.img = f"graphics/cards/{self.id}.png"
        blit_pos = (0, 0)
        self.card_rotation_angle = random.uniform(-3, 3)

        self.card_img = pygame.image.load(self.img)
        self.card_img = pygame.transform.scale(self.card_img,
                                               (self.card_img.get_width() * 3.5, self.card_img.get_height() * 3.5))
        self.card_rot = pygame.transform.rotate(self.card_img, self.card_rotation_angle)
        self.card_bounding_rect = self.card_rot.get_bounding_rect()
        self.card_surf = pygame.Surface(self.card_bounding_rect.size, pygame.SRCALPHA)

        self.card_img_1 = pygame.image.load(self.img)
        self.card_img_1 = pygame.transform.scale(self.card_img_1,
                                                 (self.card_img_1.get_width() * 2, self.card_img_1.get_height() * 2))
        self.card_rot_1 = pygame.transform.rotate(self.card_img_1, self.card_rotation_angle)
        self.card_bounding_rect_1 = self.card_rot_1.get_bounding_rect()
        self.card_surf_1 = pygame.Surface(self.card_bounding_rect_1.size, pygame.SRCALPHA)

        self.card_surf.blit(self.card_rot, blit_pos)
        self.card_y = (P1_C1[1] - self.card_surf.get_height() // 5) + random.randint(-20, 20)

        self.card_surf_1.blit(self.card_rot_1, blit_pos)
        self.card_y_1 = (P1_C1[1] - self.card_surf_1.get_height() // 2) + random.randint(-20, 20)


class Player:
    def __init__(self):
        self.ask_for_swapping = False
        self.want_swap = False
        self.cards = []
        self.player_mark = 0
        self.player_id = 0

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)


def quantum_random_number(num_bits=4):
    circuit = QuantumCircuit(num_bits, num_bits)
    circuit.h(range(num_bits))
    circuit.measure(range(num_bits), range(num_bits))

    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=1).result()
    counts = result.get_counts(circuit)

    random_number = int(list(counts.keys())[0], 2)
    return random_number


def shuffle_deck_quantum(deck):
    num_cards = len(deck)
    quantum_order = [quantum_random_number(num_bits=num_cards.bit_length()) for _ in range(num_cards)]
    sorted_indices = sorted(range(len(quantum_order)), key=quantum_order.__getitem__)
    shuffled_deck = [deck[i] for i in sorted_indices]
    return shuffled_deck


def distribute_cards(players, deck):
    shuffled_deck = shuffle_deck_quantum(deck)
    cards_per_player = len(shuffled_deck) // len(players)
    for i, player in enumerate(players):
        player.cards = shuffled_deck[i * cards_per_player: (i + 1) * cards_per_player]


def generate_deck():
    fresh_deck = []
    for cv in card_values:
        for cs in card_suits:
            fresh_deck.append(Card(cv, cs))
    return fresh_deck


def get_trump_suit():
    return random.choice(card_suits)


def get_winner(trick, trump_suit):
    winner = trick[0]
    for card in trick[1:]:
        if card.data.suit == trump_suit and winner.data.suit != trump_suit:
            winner = card
        elif card.data.suit == winner.data.suit and card.data.value > winner.data.value:
            winner = card
    return winner


def rearrange_player_list(player_list, first_player):
    max_index = player_list.index(player_list[first_player])
    rearranged_list = player_list[max_index:] + player_list[:max_index]
    return rearranged_list


class Hand:
    def __init__(self, first_player):
        self.winner_index = None
        self.copy_selected_cards = []
        self.selected_card = None
        self.selected_cards = []
        self.screen_width, self.screen_height = WIDTH, HEIGHT
        self.display_surfaces = [pygame.Surface((self.screen_width, self.screen_height)) for _ in range(4)]
        self.current_player_index = 0
        self.team_1_mark = 0
        self.team_2_mark = 0
        self.k = 0

        self.winner = None
        self.font = pygame.font.Font(GAME_FONT, 120)
        self.win_rotation_angle = random.uniform(-10, 10)

        self.player_list = [Player() for _ in range(4)]

        ##############################################################################################################################
        # define function to perfrom Quantum Superdense communication
        def superdense_transfer(card_transferer, card_trasnferee):
            print()

        def superdense_communication(index):
            protocol = QuantumCircuit(2)

            # Prepare ebit used for superdense coding
            protocol.h(0)
            protocol.cx(0, 1)
            protocol.barrier()

            # Alice's operations
            if index[0] == "1":
                protocol.z(0)
            if index[1] == "1":
                protocol.x(0)
            protocol.barrier()

            # Bob's actions
            protocol.cx(0, 1)
            protocol.h(0)
            protocol.measure_all()

            backend = Aer.get_backend('qasm_simulator')
            result = execute(protocol, backend, shots=1024).result()
            counts = result.get_counts(protocol)
            # result = Sampler().run(protocol).result()
            statistics = result.quasi_dists[0].binary_probabilities()

            final_outcome = statistics[0][0]
            final_outcome_frequency = statistics[0][1]
            for outcome, frequency in statistics.items():
                if final_outcome_frequency < frequency:
                    final_outcome_frequency = frequency
                    final_outcome = outcome

            return final_outcome

        ###################################################

        k = 0
        for i in range(4):
            self.player_list[i].player_id = k
            k = k + 1

        # print(self.player_list)
        self.player_list = rearrange_player_list(self.player_list, first_player)
        # print(self.player_list)
        self.player_list[0].ask_for_swapping = True

        self.selected_card = []

        self.deck = generate_deck()
        distribute_cards(self.player_list, self.deck)
        self.trump_suit = get_trump_suit()
        suit_dic = {"C": "clubs", "D": "diamonds", "H": "hearts", "S": "spades"}
        self.final_marks_by_player = {0: 0, 2: 0, 3: 0, 4: 0}
        self.trump_suit_name = suit_dic.get(self.trump_suit)

        for i, player in enumerate(self.player_list):
            for j, card in enumerate(player.cards):
                card.start_position = (100 + i * 300, 100 + j * 50)

    def render_cards(self):
        card_spacing = 10

        for i, player in enumerate(self.player_list):
            self.display_surfaces[i].fill((33, 124, 60))
            if self.player_list[i].ask_for_swapping:
                swap_text = f"Do you want to swap cards with your teammate? (Click 'Y' to Swap)"
                swap_font = pygame.font.Font(GAME_FONT, 50)
                swap_text_surface = swap_font.render(swap_text, True, (255, 0, 0))
                swap_text_rect = swap_text_surface.get_rect(
                    midtop=(self.screen_width // 2, self.screen_height // 2 - 100))
                self.display_surfaces[i].blit(swap_text_surface, swap_text_rect)
                self.player_list[i].ask_for_swapping = False

            player_number_text = f"Player {self.player_list[i].player_id + 1}"
            select_card_text = f"Current Round Selected Cards (Trump suit is {self.trump_suit_name})"

            player_number_font = pygame.font.Font(GAME_FONT, 150)
            player_number_text_surface = player_number_font.render(player_number_text, True, (255, 255, 255))
            player_number_text_rect = player_number_text_surface.get_rect(center=(self.screen_width // 2, 100))
            self.display_surfaces[i].blit(player_number_text_surface, player_number_text_rect)

            select_card_font = pygame.font.Font(GAME_FONT, 50)
            select_card_text_surface = select_card_font.render(select_card_text, True, (255, 255, 255))
            select_card_text_rect = select_card_text_surface.get_rect(topleft=(self.screen_width // 20, 200))
            self.display_surfaces[i].blit(select_card_text_surface, select_card_text_rect)

            for j, card in enumerate(player.cards):
                card_position_0 = (
                    j * (self.screen_width // len(player.cards) + card_spacing), self.screen_height - 400)
                self.display_surfaces[i].blit(card.card_surf, card_position_0)

            player_name_font = pygame.font.Font(GAME_FONT, 40)
            player_name_text = f"Current Hand: {self.current_player_index + 1}    (Note: Select card by pressing 1-8)"
            player_name_text_surface = player_name_font.render(player_name_text, True, (255, 255, 255))
            player_name_text_rect = player_name_text_surface.get_rect(
                midtop=(self.screen_width // 2, self.screen_height // 2 + 10))
            self.display_surfaces[i].blit(player_name_text_surface, player_name_text_rect)

            for j, card in enumerate(self.selected_cards):
                card_position_1 = (j * (self.screen_width // len(self.selected_cards) + card_spacing),
                                   self.screen_height // 3)
                self.display_surfaces[i].blit(card.card_surf_1, card_position_1)

    def render_points(self):
        pass

    def update(self):
        self.render_cards()

    def handle_events(self):
        keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                pygame.K_8]
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:

                if event.key in keys:
                    self.k += 1
                    selected_card_index = event.key - pygame.K_1

                    self.selected_card = self.player_list[self.current_player_index].cards[selected_card_index]
                    self.player_list[self.current_player_index].remove_card(self.selected_card)
                    self.selected_cards.append(self.selected_card)

                    print(f"Player {self.current_player_index + 1} selected card: {self.selected_card.data}")

                    if self.current_player_index == len(self.player_list) - 1:
                        self.winner = get_winner(self.selected_cards, self.trump_suit)
                        self.winner_index = self.selected_cards.index(self.winner)

                        winning_player = self.player_list[self.winner_index]
                        winning_player.player_mark += 1
                        self.final_marks_by_player = {1: self.player_list[0].player_mark,
                                                      2: self.player_list[1].player_mark,
                                                      3: self.player_list[2].player_mark,
                                                      4: self.player_list[3].player_mark}
                        print(
                            f"Scores: Player 1: {self.player_list[0].player_mark}, Player 2: {self.player_list[1].player_mark}, " f"Player 3: {self.player_list[2].player_mark}, Player 4: {self.player_list[3].player_mark}")
                        if self.winner_index % 2 == 0:
                            self.team_1_mark += 1
                        else:
                            self.team_2_mark += 1
                        print(f"Player {self.winner_index + 1} wins the trick!")
                        print(f"Scores: Team 1: {self.team_1_mark}, Team 2: {self.team_2_mark}")
                        self.copy_selected_cards = self.selected_cards.copy()
                        self.selected_cards = []
                    self.current_player_index = (self.current_player_index + 1) % len(self.player_list)

                else:
                    print("Invalid key. Please try again.")


if __name__ == "__main__":
    pygame.init()
    game = Hand(0)

    card_spacing = 10
    score_display = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        game.handle_events()
        game.update()
        x = len(game.player_list[0].cards) + len(game.player_list[1].cards) + len(game.player_list[2].cards) + len(
            game.player_list[3].cards)

        game_display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        game_display_surface.blit(game.display_surfaces[game.current_player_index], (0, 0))

        pygame.display.flip()

        if game.k == 4:
            score_display.fill((33, 66, 66))
            game.player_list[0].ask_for_swapping = False
            score_display_font = pygame.font.Font(GAME_FONT, 40)
            score_display_text_surface = score_display_font.render("Current Score", True, (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            for j, card in enumerate(game.copy_selected_cards):
                card_position_1 = (j * (WIDTH // len(game.copy_selected_cards) + card_spacing),
                                   HEIGHT // 3 + score_display_text_rect.height + 10)
                score_display.blit(card.card_surf_1, card_position_1)

            score_display_text_surface = score_display_font.render(f"Team 1 Score: {game.team_1_mark}", True,
                                                                   (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 300))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            score_display_text_surface = score_display_font.render(f"Team 2 Score: {game.team_2_mark}", True,
                                                                   (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 250))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            pygame.display.flip()
            pygame.time.wait(800)
            game.selected_cards = []
            game.k = 0

        if x == 0:
            # Clear the display
            score_display.fill((33, 66, 66))
            key_pressed = False  # Flag to check if any key is pressed
            max_player_index = max(game.final_marks_by_player, key=game.final_marks_by_player.get)

            # Render the final score screen
            score_display_font = pygame.font.Font(GAME_FONT, 40)
            score_display_text_surface = score_display_font.render("Final Score (Press Enter to Restart)", True,
                                                                   (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            score_display_text_surface = score_display_font.render(f"Team 1 Score: {game.team_1_mark}", True,
                                                                   (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 300))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            score_display_text_surface = score_display_font.render(f"Team 2 Score: {game.team_2_mark}", True,
                                                                   (255, 255, 255))
            score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 250))
            score_display.blit(score_display_text_surface, score_display_text_rect)

            if game.team_1_mark > game.team_2_mark:
                score_display_text_surface = score_display_font.render(f"Team 1 wins! Next game start with {max_player_index}", True, (255, 255, 255))
                score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200))
                score_display.blit(score_display_text_surface, score_display_text_rect)

            elif game.team_1_mark < game.team_2_mark:
                score_display_text_surface = score_display_font.render(f"Team 2 wins! Next game start with {max_player_index}", True, (255, 255, 255))
                score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200))
                score_display.blit(score_display_text_surface, score_display_text_rect)

            else:
                score_display_text_surface = score_display_font.render(f"Draw Next game start with {max_player_index}", True, (255, 255, 255))
                score_display_text_rect = score_display_text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200))
                score_display.blit(score_display_text_surface, score_display_text_rect)

            # max_player_index = max(game.final_marks_by_player, key=game.final_marks_by_player.get)
            pygame.display.flip()

            wait_start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - wait_start_time < 10000 and not key_pressed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        key_pressed = True

            if key_pressed:
                print(f"Final Mark: {game.final_marks_by_player}")
                print(f"Next game start with {max_player_index}")

                game = Hand(max_player_index)
                game.player_list[max_player_index].ask_for_swapping = True

        pygame.time.wait(1000)
