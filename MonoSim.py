# Module to hold Classes and Methods needed for Monopoly simulations
import random
import json
import csv


class Player:

    def __init__(self, name, ai_type="Player AI Models\Basic.json"):
        self.board_position = 0
        self.laps_completed = 0
        self.doubles_rolled = 0
        self.times_jailed = 0
        self.player_name = name
        self.consecutive_doubles = 0
        self.in_jail = False
        self.wallet = 1500
        self.total_wealth = 0

        self.upgrades_attempted = 0

        self.AI_type = ai_type

        self.properties = []
        self.landed_on = []
        self.monopolies = {}

        self.ai_data = json_loader(ai_type)
        self.calc_wealth()

    # def __str__(self):
    #     return self.player_name

    def move(self, roll_sum, log):
        self.board_position += roll_sum
        if self.board_position >= 40:
            self.laps_completed += 1
            self.board_position -= 40
            self.wallet += 200
            if log.logging is True:
                log.logger("\t" + self.player_name + " passed GO")
        self.landed_on.append(self.board_position)

    def check_doubles(self, rolled, new):
        if rolled[0] == rolled[1]:
            if new is True:
                self.doubles_rolled += 1
                self.consecutive_doubles += 1
            return True
        else:
            return False

    def check_jail(self):
        if self.board_position == 30:
            self.board_position = 10
            self.times_jailed += 1
            self.in_jail = True
            
    def calc_wealth(self):  # TODO create a new worth report
        self.total_wealth = self.wallet
        for i in self.properties:
            self.total_wealth += int(i.prop_cost)
            if i.type == "basic":
                self.total_wealth += (int(i.houses_built) * int(i.house_cost))
                if i.hotel_built is True:
                    self.total_wealth += int(i.house_cost)
                
    def buy_property(self, m_property, bank, log):  # TODO add in some form of strategy when buying properties
        # print(self.player_name + " buying " + m_property.prop_name)
        self.wallet -= int(m_property.prop_cost)
        m_property.owner = self.player_name
        self.properties.append(m_property)
        if m_property.color != "Special":
            check_monopoly(self, m_property, bank, log)

    def pay_rent(self, owner, rent, log):  # TODO add a way for the players to free up funds to pay rent
        if log.logging is True:
            log_data = self.player_name + " paying rent of " + str(rent) + " to " + owner.player_name
            log.logger("\t" + log_data)
        if self.wallet >= rent:
            self.wallet -= rent
            owner.wallet += rent
        else:
            if log.logging is True:
                log.logger("\t" + self.player_name + " does not have enough money to pay rent")
                log.logger("\t" + "Rent due " + str(rent))
                log.logger("\t" + "Funds available " + str(self.wallet))

    def upgrade_property(self, log):  # TODO add a way to prioritize different upgrade paths
        possible_upgrades = []
        for i in self.monopolies:
            # upgrade data = ['prop_name', 'upgrade_cost', 'houses_built', 'nextRent', 'upgrade_difference']
            for j in self.properties:
                if j.color == i and j.hotel_built is False:
                    upgrade_data = list([])
                    upgrade_data.append(j.prop_name)
                    upgrade_data.append(j.house_cost)
                    upgrade_data.append(j.houses_built)
                    next_rent_value = j.next_rent()
                    upgrade_data.append(next_rent_value)
                    upgrade_difference = next_rent_value - int(j.current_rent)
                    upgrade_data.append(upgrade_difference)
                    possible_upgrades.append(upgrade_data)
                else:
                    pass
        if len(possible_upgrades) != 0:
            possible_upgrades.sort(key=upgrade_gain_sorter)
            upgrade_target = possible_upgrades[0]
            # print(upgrade_target[0])
            for i in self.properties:
                if i.prop_name == upgrade_target[0]:
                    if self.evaluate_purchase(log, i.house_cost) is True:
                        self.buy_house(i, log)

    def buy_house(self, m_property, log):
        if log.logging is True:
            log.logger("\t" + self.player_name + " attempting to upgrade " + m_property.prop_name)
        if self.wallet > int(m_property.house_cost):
            self.wallet -= int(m_property.house_cost)
            if m_property.houses_built != 4:
                m_property.houses_built += 1
                # print(m_property.prop_name + " " + str(m_property.houses_built))
                m_property.update_rent()
                if log.logging is True:
                    log.logger("\t" + self.player_name + " successfully built house on " + m_property.prop_name)
                    log.logger("\t" + str(m_property.houses_built) + " houses on " + m_property.prop_name)
            elif m_property.houses_built == 4:
                m_property.hotel_built = True
                m_property.update_rent()
                if log.logging is True:
                    log.logger("\t" + self.player_name + " successfully built hotel on " + m_property.prop_name)
        else:
            if log.logging is True:
                log.logger("\t" + "Upgrade too expensive")
                log.logger("\t" + str(self.wallet))
                self.upgrades_attempted = 5

    def evaluate_purchase(self, log, cost, type="upgrade"):
        confirm = False
        if type == "purchase":
            if self.wallet - int(cost) > int(self.ai_data["Minimum Wallet Balance"]):
                if log.logging is True:
                    log.logger("\t" + self.player_name + " can purchase")
                confirm = True
            else:
                if log.logging is True:
                    log.logger("\t" + self.player_name + " cannot purchase")
        if type == "upgrade":
            if self.wallet - int(cost) > int(self.ai_data["Minimum Wallet Balance"]):
                if log.logging is True:
                    log.logger("\t" + self.player_name + " can upgrade")
                confirm = True
            else:
                if log.logging is True:
                    log.logger("\t" + self.player_name + " cannot upgrade")
        return confirm


class Reporter:

    @staticmethod
    def jail_report(log, player):
        log_data = player.player_name + " " + str(player.times_jailed)
        log.logger(log_data)

    @staticmethod
    def doubles_report(log, player):
        log_data = player.player_name + " " + str(player.doubles_rolled)
        log.logger(log_data)

    @staticmethod
    def laps_report(log, player):
        log_data = player.player_name + " " + str(player.laps_completed)
        log.logger(log_data)

    @staticmethod
    def landing_report(look_up, player_set, log):
        land_count = {}
        for i in player_set:
            for n in i.landed_on:
                if n not in land_count:
                    land_count[n] = 0
                land_count[n] += 1
        for i in land_count:
            log_data = "Space: " + str(i) + " " + look_up[str(i)] + " " + str(land_count[i])
            log.logger(log_data)

    @staticmethod
    def property_report(log, player):
        log_data = player.player_name + " owns the following properties"
        log.logger(log_data)
        for i in player.properties:
            log_data = i.prop_name
            log.logger(log_data)

    # some random comment


class BasicProperty:

    def __init__(self, prop_data):
        self.prop_name = prop_data["Name"]
        self.prop_cost = prop_data["Cost"]
        self.house_cost = prop_data["perHouse"]
        self.current_rent = prop_data["baseRent"]
        self.one_house_rent = prop_data["oneHouseRent"]
        self.two_house_rent = prop_data["twoHouseRent"]
        self.three_house_rent = prop_data["threeHouseRent"]
        self.four_house_rent = prop_data["fourHouseRent"]
        self.hotel_rent = prop_data["hotelRent"]
        self.houses_built = 0
        self.hotel_built = False
        self.owner = "Bank"
        self.monopoly_parts_needed = prop_data["monoParts"]
        self.color = prop_data["color"]
        self.type = "Basic"
        self.mortgaged = False

    def update_rent(self):
        if self.houses_built == 1:
            self.current_rent = self.one_house_rent
        if self.houses_built == 2:
            self.current_rent = self.two_house_rent
        if self.houses_built == 3:
            self.current_rent = self.three_house_rent
        if self.houses_built == 4:
            self.current_rent = self.four_house_rent
        if self.hotel_built is True:
            self.current_rent = self.hotel_rent

    def next_rent(self):
        if self.houses_built == 0:
            return int(self.one_house_rent)
        if self.houses_built == 1:
            return int(self.two_house_rent)
        if self.houses_built == 2:
            return int(self.three_house_rent)
        if self.houses_built == 3:
            return int(self.four_house_rent)
        if self.houses_built == 4:
            return int(self.hotel_rent)


class SpecialProperty:

    def __init__(self, prop_data):
        self.prop_name = prop_data["Name"]
        self.prop_cost = prop_data["Cost"]
        self.owner = "Bank"
        self.type = prop_data["Type"]
        self.color = "Special"
        
    def calc_rent(self, owner, roll_sum):
        if self.type == "Transport":
            owned = 0
            for i in owner.properties:
                if i.type == "Transport":
                    owned += 1
            if owned == 1:
                return 25
            if owned == 2:
                return 50
            if owned == 3:
                return 100
            if owned == 4:
                return 200
        
        if self.type == "Utility":
            owned = 0
            rent = 0
            for i in owner.properties:
                if i.type == "Utility":
                    owned += 1
            if owned == 1:
                rent = roll_sum * 4
            if owned == 2:
                rent = roll_sum * 10
            return rent


class Card:  # TODO use these, maybe finish at some point

    def __init__(self, card_data):
        self.text = card_data["Text"]
        self.type = card_data["Type"]
        if self.type == "getOutFree":
            self.inDeck = True
            self.owner = "none"
        if self.type == "Move":
            self.target = card_data["moveTarget"]
        if self.type == "Income":
            self.amount = card_data["Amount"]
        if self.type == "Tax":
            self.amount = card_data["Amount"]
        if self.type == "payAll":
            self.amount = card_data["Amount"]
        if self.type == "collectAll":
            self.amount = card_data["Amount"]
        
        
class Bank:

    def __init__(self):
        self.houses = 32
        self.hotels = 12
            
        self.properties = []
            
        file = "Program Resources\monopolies.json"
        raw = open(file)
        self.monopolies = json.load(raw)
        raw.close()


class Logger:
    def __init__(self, logging):
        self.log = open("log.txt", "w")
        self.tracker = open("tracker.csv", mode="w")
        self.tracker_worker = csv.writer(self.tracker)
        if logging is True:
            self.logging = True
        if logging is False:
            self.logging = False

    def logger(self, report):
        self.log.write(str(report) + "\n")

    def tracker(self, data):
        self.tracker_worker.writerow(data)


class Simulation:
    def __init__(self, num_players=random.randint(2, 8), logging=False):
        self.game_over = False
        self.log = Logger(logging)
        self.turn_counter = 0
        self.chance_index = 0
        self.comm_chest_index = 0
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.Reporter = Reporter()
        if num_players >= 2:
            self.players = [self.player1, self.player2]
        if num_players >= 3:
            self.player3 = Player("Player 3")
            self.players.append(self.player3)
        if num_players >= 4:
            self.player4 = Player("Player 4")
            self.players.append(self.player4)
        if num_players >= 5:
            self.player5 = Player("Player 5")
            self.players.append(self.player5)
        if num_players >= 6:
            self.player6 = Player("Player 6")
            self.players.append(self.player6)
        if num_players >= 7:
            self.player7 = Player("Player 7")
            self.players.append(self.player7)
        if num_players == 8:
            self.player8 = Player("Player 8")
            self.players.append(self.player8)
                
        self.Bank = Bank()
        # print(list(self.Bank.monopolies.keys()))
        property_setup(self.log, self.Bank)
        self.chance_deck = []
        self.comm_chest_deck = []
        deck_setup(self.chance_deck, self.comm_chest_deck, self.log)
        random.shuffle(self.chance_deck)
        random.shuffle(self.comm_chest_deck)
            
        self.look_up = json_loader("Program Resources\Board Reference.json")
        self.special_tiles = ("0", "2", "4", "7", "10", "17", "20", "22", "30", "32", "36", "38")
            
        random.shuffle(self.players)
        
    def turn(self, player):
        self.turn_counter += 1
        if self.log.logging is True:
            self.log.logger("Turn " + str(self.turn_counter))
            self.log.logger(player.player_name + 's turn')
        your_turn = True
        player.consecutive_doubles = 0
        player.upgrades_attempted = 0
        while your_turn is True:
            if player.in_jail is True:  # if in jail try to get out
                escape_jail(player)
            rolled = roll()  # roll the dice
            player.check_doubles(rolled, True)
            player.move(rolled[0] + rolled[1], self.log)  # move player through total rolled
            if self.log.logging is True:
                self.log.logger("\tRolled " + str(rolled[0] + rolled[1]))
                self.log.logger("\tLanded on " + self.look_up[str(player.board_position)])
            player.check_jail()     # check to see if landed on go to jail tile
            if player.consecutive_doubles == 3:
                if self.log.logging is True:
                    self.log.logger("\t" + player.player_name + "  rolled triple doubles, going to jail")
                player.board_position = 10
                player.in_jail = True
                # your_turn = False
                break
            if str(player.board_position) not in self.special_tiles:
                self.landed_on_property(player, rolled)

            while player.upgrades_attempted < int(player.ai_data["Upgrades Per Turn"]):
                player.upgrades_attempted += 1
                player.upgrade_property(self.log)
            your_turn = player.check_doubles(rolled, False)  # check if turn ended

        player.calc_wealth()
        if self.log.logging is True:
            self.log.logger("\t" + "Player is worth: " + str(player.total_wealth))
            data = [self.turn_counter]
            for i in self.players:
                data.append(i.player_name)
                data.append(i.wallet)
                data.append(i.total_wealth)
            self.log.tracker_worker.writerow(data)

    def landed_on_property(self, player, rolled):
        for n in self.Bank.properties:
            # Check to see who owns the property the player is currently on
            if n.prop_name == self.look_up[str(player.board_position)]:
                if n.owner == "Bank":  # bank owned property
                    if player.evaluate_purchase(self.log, n.prop_cost, type="purchase"):  # think about buying
                        if self.log.logging is True:
                            log_data = player.player_name + " is buying " + n.prop_name
                            self.log.logger("\t" + log_data)
                        player.buy_property(n, self.Bank, self.log)  # buy property
                elif n.owner != player.player_name:  # owned by another player
                    if self.log.logging is True:
                        self.log.logger("\t" + "Property " + n.prop_name + " not owned by bank")
                    for i in self.players:
                        if n.owner == i.player_name:  # find owner so we can pay them
                            if self.log.logging is True:
                                self.log.logger("\t" + "Owned by " + i.player_name)
                            if n.type == "Basic":
                                player.pay_rent(i, int(n.current_rent), self.log)
                            else:
                                rent = n.calc_rent(i, rolled[0] + rolled[1])
                                player.pay_rent(i, rent, self.log)

    def check_game_over(self):
        if self.players[0].laps_completed == 40:
            self.game_over = True
            if self.log.logging is True:
                self.log.logger("Lap count reached")
        for i in self.players:
            if i.total_wealth <= 0:
                self.game_over = True
                if self.log.logging is True:
                    self.log.logger(i.player_name + " has a net worth of " + i.total_wealth)

    def run_sim(self):
        while self.game_over is False:
            for i in self.players:
                self.turn(i)
            self.check_game_over()
        if self.log.logging is True:
            self.players.sort(key=player_sorter)

            self.log.logger("Properties owned by each player")      # Log the properties owned by each player
            for i in self.players:
                self.Reporter.property_report(self.log, i)

            self.log.logger("Double Rolled")    # Log number of doubles rolled by each player
            for i in self.players:
                self.Reporter.doubles_report(self.log, i)

            self.log.logger("Times Jailed")     # Log number of time each player was jailed
            for i in self.players:
                self.Reporter.jail_report(self.log, i)

            self.log.logger("Laps Completed")   # Log laps completed by each player
            for i in self.players:
                self.Reporter.laps_report(self.log, i)

            self.log.logger("Times Landed on Each Space")   # Log number of times each board space was landed on
            self.Reporter.landing_report(self.look_up, self.players, self.log)

    def step_sim(self, current_state):
        # Steps the simulation forward by giving one player a turn
        # Returns the integer value of the next player
        if self.game_over is True:
            print("Game over")
            return current_state
        self.turn(self.players[current_state["next player"]])
        prev_player = current_state["next player"]
        if prev_player < len(self.players)-1:
            next_player = prev_player + 1
        else:
            next_player = 0
        return {"previous player": prev_player, "next player": next_player}


# End of Class definitions

# Beginning of Function definitions


def property_setup(log, bank):
    data = json_loader("Program Resources\properties.json")
    for n in range(1, 23):
        if log.logging is True:
            log.logger("Creating property " + str(n))
        bank.properties.append(BasicProperty(data.get(str(n))))
        if log.logging is True:
            log.logger("Created " + bank.properties[n-1].prop_name)
        
    file = "Program Resources\specialProperties.json"
    raw = open(file)
    read = json.load(raw)
    raw.close()
    for n in range(1, 7):
        # print (read.get(str(n)))
        if log.logging is True:
            log.logger("Creating special property " + str(n))
        bank.properties.append(SpecialProperty(read.get(str(n))))
        if log.logging is True:
            log.logger("Created " + bank.properties[len(bank.properties) - 1].prop_name)


def deck_setup(chance, comm_chest, log):
    data = json_loader("Program Resources\chance.json")
    for i in range(1, 17):
        if log.logging is True:
            log.logger("Creating chance card " + str(i))
        chance.append(Card(data[str(i)]))

    data = json_loader("Program Resources\commchest.json")
    for i in range(1, 17):
        if log.logging is True:
            log.logger("Creating community chest card " + str(i))
        comm_chest.append(Card(data[str(i)]))
        

def check_monopoly(player, m_property, bank, log):
    monopoly_parts_owned = 0
    if m_property.color in list(bank.monopolies.keys()):
        for i in player.properties:
            if i.color == m_property.color:
                monopoly_parts_owned += 1
    if monopoly_parts_owned == int(m_property.monopoly_parts_needed):
        if log.logging is True:
            log.logger("\t" + player.player_name + " owns the monopoly of color " + m_property.color)
        player.monopolies[m_property.color] = bank.monopolies[m_property.color]
        del bank.monopolies[m_property.color]
        return True
    # print(player.player_name + " owns " + str(monopoly_parts_owned) + " properties of the color " + m_property.color)


def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2


def escape_jail(player):  # TODO implement turn counter that can be used when player has less than $50
    if player.AI_type == "Basic":
        player.wallet -= 50
        player.in_jail = False


def get_current_property(sim, player):
    for n in sim.Bank.properties:
        if n.prop_name == sim.look_up[str(player.board_position)]:
            return sim.Bank.properties.n


def player_sorter(player):
    return player.player_name


def upgrade_cost_sorter(upgrade_data):
    return upgrade_data[1]


def upgrade_gain_sorter(upgrade_data):
    return upgrade_data[4]


def json_loader(file):
    raw = open(file)
    read = json.load(raw)
    raw.close()
    return read


def read_card(player, card, sim):
    if card.type == "Income":
        player.wallet += int(card.amount)
        if sim.log.logging is True:
            sim.log.logger("\t" + card.text + " receive " + card.amount)
    if card.type == "Tax":
        player.wallet -= int(card.amount)
        if sim.log.logging is True:
            sim.log.logger("\t" + card.text + " pay " + card.amount)
    if card.type == "Move":
        player.board_position = int(card.target)
        if sim.log.logging is True:
            sim.log.logger("\t" + card.text)


"""end"""
