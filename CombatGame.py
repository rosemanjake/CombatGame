import random
import sys
import re

previousstate = 0
gameover = False
statelist = [True, False, False, False, False, False] #0 = in menu, 1 = in combat, 2 = in inventory, 3 = in store, 4 = in exploremenu, 5 = in attack menu
enemyalive = False

currentdifficulty = 0 # 0 = easy, 1 = medium, 2 = hard 

class Character:
    Name = "name"
    Level = 0

    maxHealth = 0
    maxFatigue = 0
    maxStrength = 0
    
    currentHealth = 0
    currentFatigue = 0
    currentStrength = 0
    currentLevel = 0    

    def __init__(self, aName, aHealth, aFatigue, aAttack, aLevel):
        self.Name = aName
        self.Level = aLevel

        self.maxHealth = aHealth
        self.maxFatigue = aFatigue
        self.maxStrength = aAttack

        self.currentHealth = aHealth
        self.currentFatigue = aFatigue
        self.currentStrength = aAttack

class Player(Character):
    money = 0
    xp = 0
    currentitems = []
    currentweapons = []

    def __init__(self, aName, aHealth, aFatigue, aAttack, aLevel, aInventory, aWeapons):
        Character.__init__(self, aName, aHealth, aFatigue, aAttack, aLevel)
        self.currentitems = aInventory  
        self.currentweapons = aWeapons

#TO DO: Generic item parent class and weapon/item specific child classes
class Item:
    Name = "name"
    PoisonDmg = 0
    RestoreHealth = 0
    Value = 0

    def __init__(self, aName, aPoisonDmg, aRestoreHealth, aValue):
        self.Name = aName
        self.PoisonDmg = aPoisonDmg
        self.RestoreHealth = aRestoreHealth
        self.Value = aValue

class Weapon:
    Name = "name"
    SlashDmg = 0
    StabDmg = 0
    ChopDmg = 0
    BluDmg = 0
    Value = 0

    def __init__(self, aName, aSlashDmg, aStabDmg, aChopDmg, aBluDmg, aValue):
        self.Name = aName
        self.SlashDmg = aSlashDmg
        self.StabDmg = aStabDmg 
        self.ChopDmg = aChopDmg
        self.BluDmg = aBluDmg
        self.Value = aValue

#TO DO: Separate inventory objects for weapons and potions
class Inventory:
    Items = []

    def __init__(self, aInventory):
        self.Items = aInventory

#Check current state of the program
def checkstate():
    counter = 0
    for state in statelist:
        if state == True:
            break
        else:
            counter += 1
    return counter

def attrnamer(attribute):
    names = {
        "RestoreHealth": "Restore Health",
        "PoisonDmg": "Poison Damage",
        "SlashDmg": "Slash Damage", 
        "StabDmg": "Stab Damage",
        "ChopDmg": "Chop Damage",
        "BluDmg": "Bludgeon Damage",
        }
    return names[attribute]

#Function for finding what effects a object has - loop through attributes, find non-zero ones excluding value, apply that effects
def geteffects(item):
    attributes = []
    for a in dir(item):
        if not a.startswith('__'):
            attributes.append(a)
    
    effects = {}
    for at in attributes:
        if not at == "Value" and not at == "Name":
            value = getattr(item, at)
            if not value == 0:
                effects[at] = value

    return(effects)    #Should this dictionary itself become an attribute of the object - called in the constructor?

#Effectively a use item function - I probably need a generic method that will apply effects to current attributes and limit to the max values
def applyeffects(item, character):
    
    effects = geteffects(item)

    for ef in effects:
        if ef == "RestoreHealth":
            character.currentHealth = (character.currentHealth + item.RestoreHealth)
            if character.currentHealth > character.maxHealth:
                character.currentHealth = character.maxHealth
            print(f"{item.Name} raised player's health by {item.RestoreHealth}. Player health now {player.currentHealth}")
        if ef == "PoisonDmg":
            character.currentHealth = (character.currentHealth - item.PoisonDmg)
            print(f"{item.Name} lowered player's health by {item.PoisonDmg}. Player health now {player.currentHealth}")
         
    character.currentitems.remove(item)

#Set the current state of the game and save the previous state
def setstate(newstate):
    i = 0
    global previousstate
    previousstate = checkstate()
    
    for state in statelist:
        statelist[i] = False
        i += 1
    statelist[newstate] = True

#TO DO: Will need to amend to display weapons and potions
def printinventory(inventory):
    print("Current items in your inventory:")
    for item in inventory:
        print(item.Name)

#Input validation function, make sure inputs are legal
def commandverify(input, state):
    menu = ["f", "p", "s", "c", "i"]
    combat = ["a", "r", "b", "p", "i"] 
    inventory = ["use", "equip", "r"]
    store = ["buy", "r"]
    explore = ["d", "m", "e"]
    attack = ["use", "b"]
    listoflists = [menu, combat, inventory, store, explore, attack]
    
    if input in listoflists[state]:
        return True
    else:
        return False

#Another input validation function, check to make sure the object you're interacting with actually exists
def itemvalidation(desireditem, list):
    for item in list:
        if item.Name.lower() == desireditem.lower():
            return True
    
    print("Item not found. Please enter a valid item...")
    commandhandler(input())

#Another input validation function, check to make sure the attack you want exists for the current weapon - different from the above as it takes a list of strings
def attackvalidation(desiredattack, attacks):
    for attack in attacks:
        possattack = attrnamer(attack).lower().split(" ")[0]
        if possattack == desiredattack.lower():
            return True
    
    print("Attack not found. Please enter a valid attack...")
    commandhandler(input())

def equip(weapon):
    global equipped
    equipped = weapon
    print(f"Equipped {weapon.Name}")
  
#TO DO: Break out some of the more complex commands into their own methods that we can call in one or two lines in commandhandler()
def commandhandler(playerinput):
    state = checkstate()
    splitinput = playerinput.split(' ')

    if playerinput == "":
        print("Input invalid. Please enter a valid input...")
        commandhandler(input())
    if not (commandverify(splitinput[0], state)):
        print("Input invalid. Please enter a valid input...")
        commandhandler(input())
    
    if state == 0: # in menu
        if playerinput == "f":
            exploremenu()
        elif playerinput == "p":
            printattributes(player)
            menu()
        elif playerinput == "s":
            storemenu()
        elif playerinput == "c":
            global gameover
            gameover = True
        elif playerinput == "i":
            inventorymenu()
            #returnto()
    if state == 1: # in combat 
        if playerinput == "a":
            attack(player, enemy)
            player.currentStrength = player.maxStrength
            if enemyalive == True:
                enemyturn()
        elif playerinput == "r":
            run(player, enemy)
        elif playerinput == "b":
            enemyturn()
        elif playerinput == "p":
            printattributes(player)
            printattributes(enemy)
            combatmenu()
        elif playerinput == "i":
            inventorymenu()
            combatmenu()
    if state == 2: # in inventory
        if splitinput[0] == "use":
            splitinput.remove(splitinput[0])
            desireditem = ' '.join(splitinput)
            if (itemvalidation(desireditem, player.currentitems)):
                for item in player.currentitems:
                    if item.Name.lower() == desireditem.lower():
                        applyeffects(item, player)
                if previousstate == 1:
                    enemyturn()
        if splitinput[0] == "equip":
            splitinput.remove(splitinput[0])
            desireditem = ' '.join(splitinput)
            if (itemvalidation(desireditem, player.currentweapons)):
                for weapon in player.currentweapons:
                    if weapon.Name.lower() == desireditem.lower():
                        equip(weapon)
                if previousstate == 1:
                    enemyturn()
        elif playerinput == "r":
            returnto()
    if state == 3: # in store
        #TO DO - This should really be separated out as a separate method - make it impossible to buy something if you don't have the money 
        if splitinput[0] == "buy":
            splitinput.remove(splitinput[0])
            desireditem = ' '.join(splitinput)
            if (itemvalidation(desireditem, storestock)):
                i = 0
                for item in storestock:
                    if item.Name.lower() == desireditem.lower():
                        break
                    else:
                        i += 1
                if player.money >= storestock[i].Value:
                    player.currentitems.append(storestock[i])
                    player.money = (player.money - storestock[i].Value)
                    print(f"You buy {storestock[i].Name} for {storestock[i].Value}. You now have {player.money} gold.")
                    storestock.remove(storestock[i])
                    storemenu()
                else: 
                    print(f"You only have {player.money} gold. It's not enough to buy {storestock[i].Name} for {storestock[i].Value}")
                    returnto()
        elif playerinput == "r":
            returnto()
    if state == 4: #exploremenu
        global currentdifficulty
        if playerinput == "d":
            currentdifficulty = 0
            print("You enter a dark swamp.")
            combat(random.uniform(1.2,2.5), 1)
        if playerinput == "m":
            currentdifficulty = 1
            print("You enter a ruin on open ground.")
            combat(1, 1)
        if playerinput == "e":
            currentdifficulty = 2
            print("You enter a flowery meadow.")
            combat(random.uniform(0.1,0.5), 1)
    if state == 5: #attackmenu
        if splitinput[0] == "use":
            splitinput.remove(splitinput[0])
            desiredattack = ' '.join(splitinput)
            if (attackvalidation(desiredattack, geteffects(equipped).keys())):
                print(f"You {desiredattack} the {enemy.Name}!\n")

def returnto():
    global previousstate
    if previousstate == 0:
        menu()
    elif previousstate == 1:
        combatmenu()
    elif previousstate == 2:
        inventorymenu()
    elif previousstate == 3:
        storemenu()

#TO DO: More interesting damage model
def attack(attacker, defender):
    if attacker == player:
        attackmenu()
    
    print(f"{attacker.Name} attacks")
    damage = (round(attacker.currentStrength * random.uniform(0.5,1.0)))
    defender.currentHealth = defender.currentHealth - damage

    print(f"Damage = {damage}")
    print(f"{defender.Name}'s health = {defender.currentHealth}")

    checkhealth(defender)

#track player damage state (poisoned, burning, etc. and apply effect here) 
def enemyturn():
    attack(enemy, player) 
    combatmenu()

def checkhealth(character):
    if character.currentHealth <= 0:
        if not character == player:
            print(f"{character.Name} is dead")
            victory(player, enemy)
            global enemyalive
            enemyalive = False
        else:
            defeat()       

def restoreattributes(character):
    character.currentHealth = character.maxHealth
    character.currentFatigue = character.maxFatigue
    character.currentStrength = character.maxStrength

# Make it scale by level as well
def winnings(player, enemy):
    if currentdifficulty == 0:
        scale = random.uniform(1.5,3)
    if currentdifficulty == 1:
        scale = 1
    if currentdifficulty == 2:
        scale = random.uniform(0.3,0.8)

    return round(random.randint(5,25) * scale)

#Calculate xp required to level up
def xpcalc(level):
    return ((level * 10) ** 1.3)

#TO DO: funcion for calculating xp gained when enemy killed
def xpgain(enemy, win):
    xp = round((player.xp + enemy.maxHealth) /2) # placeholder
    if win:
        print(f"You gain {xp} XP")
    if not win:
        xp = round((xp * -0.2))
        print(f"You lose {abs(xp)} XP.")
    levelup(xp)

#Function called when levelling up
def levelup(xp):
    player.xp = round(player.xp + xp)
    if player.xp < 0:
        player.xp = 0
    xpreq = xpcalc(player.Level)

    if player.xp >= xpreq:
        player.Level += 1
        if player.xp > xpreq:
            player.xp = (player.xp - xpreq)
        else:
            player.xp = 0
        print(f"You have levelled up! You are now level {player.Level}.")
        levelupstats()
    else:
        print(f"Your XP is now: {player.xp}. XP required for level {player.Level + 1} is {round(xpreq - player.xp)}")

#Function that allows user to increment an attribute when levelling up
def levelupstats():
    print("Which attribute would you like to level up?")

#TO DO: Make XP functional
def victory(player, enemy):
    geld = winnings(player,enemy)
    print(f"You win! You receive {geld} gold.")
    restoreattributes(player)
    player.money = player.money + geld
    xpgain(enemy, True)
    restock()
    menu()

def defeat():
    print("You have died! You lose! One level down.")
    if player.Level > 1:
        player.Level -= 1
    restoreattributes(player)
    xpgain(enemy, False)
    restock()
    menu()

def run(player, enemy):
    diceroll = random.randint(0,100)
    if diceroll > 50:
        print("You ran away, combat over")
        restoreattributes(player)
        menu()
    else:
        print("You fail to run away. Enemy is coming at you.")
        enemyturn()

def printattributes(character):
    print(f"{character.Name} health: {character.currentHealth}")
    print(f"{character.Name} fatigue: {character.currentFatigue}")
    print(f"{character.Name} attack: {character.currentStrength}")
    print(f"{character.Name} level: {character.Level}")
    if character == player:
        print(f"{character.Name} XP: {character.xp} / {xpcalc(character.Level)}")        

def dictostring(dict, attack):
    strings = []
    for key in dict.keys():
        if (attack):
            strings.append(f"\n\t- {attrnamer(key).split(' ')[0]}. Damage: {dict[key]}") #Just take the first word when listing possible attacks (eg. "chop", not "chop damage")
            attackmod = (player.currentStrength + 50) / 100
            player.currentStrength = (dict[key] * attackmod) #TO DO: divide by defense attribute if you add that
        else:
            strings.append(f"\n\t- {attrnamer(key)}:{dict[key]}")
    return "".join(strings)

def printitems(list, type):
    if len(list) > 0:
        print(f"Current {type}s in inventory:")
    else:
        print(f"No {type}s in inventory!")
    
    for item in reversed(itemnumbering(list)):
       print(f"- {item.Name}, {dictostring(geteffects(item), False)}")

def inventorymenu():
    setstate(2)

    print(f"Current gold: {player.money}")
    print(f"Currently equipped weapon: {equipped.Name}")
    printitems(player.currentitems, "item")
    printitems(player.currentweapons, "weapon")
        
    print("To use an item type \"use itemname\". To equip a weapon type \"equip weaponname\". Or you can [r]eturn to where you were.")
    commandhandler(input())

def menu():
    setstate(0)
    print("Would you like to [f]ight, [p]rint player attributes, view your [i]nventory, visit the [s]tore, or [c]lose the application")
    commandhandler(input())

def exploremenu():
    setstate(4)
    print("Would you like to explore a [d]ifficult area with high risk and high reward, a [m]edium area with moderate risk and reward, or an [e]asy area with low risk and low reward?")
    commandhandler(input())

def namegen():
    enemynames = ["Goblin", "Skelly", "Goul", "Zombie", "Goose"]
    return enemynames[random.randint(0,4)]

def enemygen(difficulty, sign):

    enemy.maxHealth = round((player.maxHealth * (random.uniform(0.9,1.1)) * (difficulty * sign)))
    enemy.maxFatigue = round((player.maxFatigue * (random.uniform(0.9,1.1)) * (difficulty * sign)))
    enemy.maxStrength = round((player.maxStrength * (random.uniform(0.9,1.1)) * (difficulty * sign)))
    if player.Level > 1:
        enemy.Level = round(player.Level + (difficulty * random.randint(-1,2)))
    else:
        enemy.Level = round(player.Level + (difficulty * random.randint(-2,2)))

    restoreattributes(enemy)

    global enemyalive
    enemyalive = True

def combat(difficulty, sign):
    enemygen(difficulty, sign)

    print("An enemy approaches...")
    printattributes(enemy)
    combatmenu()

def combatmenu():
    setstate(1)
    print("Would you like to [a]ttack, [r]un, be a [b]ack into the fetal position and let the enemy attack, [p]rint both your and the enemy's stats, display your [i]nventory?")
    commandhandler(input())

def attackmenu():
    setstate(5)
    print(f"Which attack would you like to perform with {equipped.Name}:")
    print(f"{dictostring(geteffects(equipped), True)}")
    #attrnamer(attack).lower().split(" ")[0]
    commandhandler(input())

def stocker():
    global storestock
    global initial
    
    if (initial):
        numberofthings = random.randint(5,10)
    else:
        numberofthings = random.randint(0,3)
    
    i = 0
    while i < numberofthings:
        if len(storestock) < 10:
            storestock.append(Item(f"Potion", 0, random.randint(20,40), random.randint(10,20)))
        i += 1
    
    initial = False
    return storestock

def itemnumbering(itemlist):

    for item in itemlist:
        if re.match(".*\s\d$", item.Name):
            item.Name = re.sub("\s\d$", "", item.Name)

    for item in itemlist:
        count = 0
        for dup in itemlist:
            if re.match(dup.Name, item.Name):
                count += 1
        if item == itemlist[len(itemlist) - 1]:
            item.Name = re.sub("\s\d$", "", item.Name)
        if count > 1:
            item.Name = (item.Name + f" {count}")

    return itemlist

def restock():
    if random.randint(0,100) > 50:
        stocker()
        print(f"Store restocked! {len(storestock)} items available.")

def storemenu():
    setstate(3)
    global storestock

    print(f"Welcome to the store. You have {player.money} gold. The current items in stock are:")
    for item in reversed(itemnumbering(storestock)):
        print(f"{item.Name}, price: {item.Value}, {geteffects(item)}")
    print("To buy an item, type \"buy itemname\", or [r]eturn to where you were.")
    commandhandler(input())

healthpotion = Item("Tainted potion", random.randint(20,40), random.randint(0,20), 20)
inventory = list()
inventory.append(healthpotion)

Sword = Weapon("Steel Sword", random.randint(5,20), random.randint(10,30), random.randint(5,15), random.randint(1,5), 20)
Dagger = Weapon("Steel Dagger", random.randint(3,10), random.randint(10,20), random.randint(3,10), random.randint(1,3), 20)
Axe = Weapon("Axe", random.randint(5,15), 0, random.randint(20,30), random.randint(1,3), 20)
Mace = Weapon("Mace", random.randint(2,6), 0, random.randint(2,6), random.randint(15,25), 20)
weapons = []
weapons.append(Sword)
weapons.append(Mace)

equipped = Sword

initial = True
storestock = []
storestock = stocker()

player = Player("Player", 100, 70, 50, 1, inventory, weapons)

enemy = Character(namegen(), 1, 1, 1, 1)

while gameover == False:
    menu()

print("Thanks for playing!")
