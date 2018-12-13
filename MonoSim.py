# Module to hold Classes and Methods needed for Monoploy simulations
import random
import json


class Player:

    def __init__(self, name):
        self.boardPosition = 0
        self.lapsCompleted = 0
        self.doublesRolled = 0
        self.timesJailed = 0
        self.playerName = name
        self.consecutiveDoubles = 0
        self.inJail = False
        self.wallet = 1500
        self.totalWealth = 0
        
        self.AItype = "Basic"
        
        self.properties = []
        self.landedOn = []
        
    def __str__(self):
        return self.playerName

    def move(self, rollsum):
        self.boardPosition += rollsum
        if self.boardPosition >= 40:
            self.lapsCompleted += 1
            self.boardPosition -= 40
            self.wallet += 200
        self.landedOn.append(self.boardPosition)

    def check_doubles(self, rolled):
        if rolled[0] == rolled[1]:
            self.doublesRolled += 1
            self.consecutiveDoubles += 1
            return True
        else:
            return False

    def check_jail(self):
        if self.boardPosition == 30:
            self.boardPosition = 10
            self.timesJailed += 1  
            self.inJail = True
            
    def calc_wealth(self):
        self.totalWealth = self.wallet
        for i in self.properties:
            self.totalWealth += i.propCost
            self.totalWealth += (i.housesBuilt * i.houseCost)
            if i.hotelBuilt is True:
                self.totalWealth += i.houseCost
                
    def buy_property(self, mproperty, bank):
        self.wallet -= int(mproperty.propCost)
        mproperty.owner = self.playerName
        self.properties.append(mproperty)
        if mproperty.color != "Special":
            check_monopoly(self, mproperty, bank)
        

class Reporter:

    @staticmethod
    def jail_report(sim, player):

        Simulation.logger(sim, player.playerName + " " + str(player.timesJailed))

    @staticmethod
    def doubles_report(sim, player):
        Simulation.logger(sim, player.playerName + " " + str(player.doublesRolled))

    @staticmethod
    def laps_report(sim, player):
        Simulation.logger(sim, player.playerName + " " + str(player.lapsCompleted))

    @staticmethod
    def landing_report(sim, player_set):
        land_count = {}
        for i in player_set:
            for n in i.landedOn:
                if n not in land_count:
                    land_count[n] = 0
                land_count[n] += 1
        for i in land_count:
            Simulation.logger(sim, "Space " + str(i) + " " + str(land_count[i]))


class BasicProperty:

    def __init__(self, prop_data):
        self.propName = prop_data["Name"]
        self.propCost = prop_data["Cost"]
        self.houseCost = prop_data["perHouse"]
        self.currentRent = prop_data["baseRent"]
        self.housesBuilt = 0
        self.hotelBuilt = False
        self.owner = "Bank"
        self.MonopolyPartsNeeded = prop_data["monoParts"]
        self.color = prop_data["color"]
        self.type = "Basic"


class SpecialProperty:

    def __init__(self, prop_data):
        self.propName = prop_data["Name"]
        self.propCost = prop_data["Cost"]
        self.owner = "Bank"
        self.type = prop_data["Type"]
        self.color = "Special"
        
    def calc_rent(self, owner, roll_sum):
        # TODO Make roll_sum optional?
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


class Card:

    def __init__(self, card_data, deck):
        self.text = card_data["Text"]
        self.type = card_data["Type"]
        self.deck = deck
        if self.type == "getOutFree":
            self.inDeck = True
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
            
        file = "monopolies.json"
        raw = open(file)
        self.monopolies = json.load(raw)
        raw.close()
    

class Simulation:

    def __init__(self, num_players=random.randint(2, 8), logging=False):
        self.logging = logging

        if self.logging is True:
            self.log = open("log.txt", "w")

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
        property_setup(self, self.Bank, self.logging)
            
        self.look_up = json.load(open("boardReference.json"))
            
        random.shuffle(self.players)

        self.run_sim()
        
    def turn(self, player):
        your_turn = True
        player.consecutiveDoubles = 0
        while your_turn is True:
            if player.inJail is True:
                escape_jail(player)
            rolled = roll()  # roll the dice
            player.move(rolled[0] + rolled[1])  # move player through total rolled
            player.check_jail()
            for n in self.Bank.properties:
                if n.propName == self.look_up[str(player.boardPosition)]:
                    if n.owner == "Bank":
                        player.buy_property(n, self.Bank)
            your_turn = player.check_doubles(rolled)  # check if turn ended
            if player.consecutiveDoubles == 3:
                if self.logging is True:
                    print(player.playerName + "Triple doubles going to jail")
                player.boardPosition = 10
                player.inJail = True
                your_turn = False
            
    # def board_reference_setup(self):
    #     file = "boardReference.json"
    #     raw = open(file)
    #     self.look_up = json.load(raw)
    #     raw.close()
    # TODO test new implementation and delete legacy code

    def run_sim(self):
        while self.players[0].lapsCompleted <= 9:
            for i in self.players:
                self.turn(i)
        if self.logging is True:

            self.logger("Double Rolled")    # Log number of doubles rolled by each player
            for i in self.players:
                self.Reporter.doubles_report(self, i)

            self.logger("Times Jailed")     # Log number of time each player was jailed
            for i in self.players:
                self.Reporter.jail_report(self, i)

            self.logger("Laps Completed")   # Log laps completed by each player
            for i in self.players:
                self.Reporter.laps_report(self, i)

            self.logger("Times Landed on Each Space")   # Log number of times each board space was landed on by a player
            self.Reporter.landing_report(self, self.players)

    def logger(self, report):
        self.log.write(str(report) + "\n")

# End of Class definitions

# Beginning of Method definitions


def property_setup(sim, bank, logging):
    file = "properties.json"
    raw = open(file)
    read = json.load(raw)
    raw.close()
    for n in range(1, 23):
        if logging is True:
            Simulation.logger(sim, "Creating property " + str(n))
        bank.properties.append(BasicProperty(read.get(str(n))))
        if logging is True:
            Simulation.logger(sim, "Created " + bank.properties[n-1].propName)
        
    file = "specialproperties.json"
    raw = open(file)
    read = json.load(raw)
    raw.close()
    for n in range(1, 7):
        # print (read.get(str(n)))
        if logging is True:
            Simulation.logger(sim, "Creating special property " + str(n))
        bank.properties.append(SpecialProperty(read.get(str(n))))
        if logging is True:
            Simulation.logger(sim, "Created " + bank.properties[len(bank.properties) - 1].propName)
        

def check_monopoly(player, mproperty, bank):
    monopoly_parts_owned = 0
    if mproperty.color in list(bank.monopolies.keys()):
        for i in bank.monopolies[mproperty.color]:
            if i in player.properties:
                monopoly_parts_owned += 1
    if monopoly_parts_owned == mproperty.MonopolyPartsNeeded:
        player.monopolies[mproperty.color] = bank.monopolies[player.color]
        del bank.properties[mproperty.color]


def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2


def escape_jail(player):
    if player.AItype == "Basic":
        player.wallet -= 50
        player.inJail = False


def get_current_property(sim, player):
    for n in sim.Bank.properties:
        if n.propName == sim.look_up[str(player.boardPosition)]:
            return sim.Bank.properties.n


"""end"""
