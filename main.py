from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 25, 110, "black")
blizzard = Spell("Blizzard", 25, 115, "black")
meteor = Spell("Meteor", 40, 190, "black")
quake = Spell("Quake", 25, 210, "black")

# create white magic

cure = Spell("Cure", 50, 120, "white")
cura = Spell("Cura", 55, 200, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50, 1)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100, 10)
superpotion = Item("Superpotion", "potion", "Heals 500 HP", 500, 10)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999, 10)
hielixir = Item("Mega-Elixir", "elixir", "Fully restores party's HP/MP.", 9999, 10)

grenade = Item("Grenade", "attack", "Deals 500 damage.", 500, 10)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [potion, hipotion, superpotion, elixir, hielixir, grenade]

enemy_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_items = [potion, hipotion, superpotion, elixir, hielixir, grenade]

# instatiate people
player1 = Person("Shuin", 3260, 132, 180, 34, player_spells, player_items)
player2 = Person("Shera", 4160, 188, 125, 34, player_spells, player_items)
player3 = Person("Aria ", 3089, 174, 110, 34, player_spells, player_items)

players = [player1, player2, player3]


enemy1 = Person("Imp", 1000, 130, 560, 325, enemy_spells, enemy_items)
enemy2 = Person("Omega", 1300, 221, 420, 30, enemy_spells, enemy_items)
enemy3 = Person("Imp", 1000, 130, 560, 325, enemy_spells, enemy_items)

enemies = [enemy1, enemy2, enemy3]



running = True
i = 0

# zero the counters
defeated_enemies = 0
defeated_players = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:

    # ------------- Check Battle Status


    print("========================")
    print("\n\n")
    print("NAME                 -=========HEALTH==========-              -===MP===- ")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()


    for player in players:

        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print("You attacked"+ enemies[enemy].name + "for", dmg, "points of damage. Enemy HP :")

            if enemies[enemy].get_hp() == 0:
                defeated_enemies += 1
                print("\n" + enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough MP" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), " points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    defeated_enemies += 1
                    print("\n" + enemies[enemy].name + " has died. Enemies defeated :" + defeated_enemies)
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item :")) - 1

            item = player.items[item_choice]

            if item_choice == -1:
                continue

            if item.quantity == 0:
                print(bcolors.FAIL + "YOU DO NOT HAVE ANY " + item.name + "s LEFT" + bcolors.ENDC)
                continue

            if item.type == "potion":
                player.heal(item.prop)
                item.quantity -= 1
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega-Elixir":
                    for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp

                    item.quantity -= 1
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                item.quantity -= 1
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " causes " + str(item.prop), " damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    defeated_enemies += 1
                    print("\n" + enemies[enemy].name + " has died. Enemies defeated :" + str(defeated_enemies))
                    del enemies[enemy]




    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1


    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # check if player won
    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "You Win !" + bcolors.ENDC)
        running = False

    # check if enemy won
    elif defeated_players == 3:
        print(bcolors.FAIL + "You Lose" + bcolors.ENDC)
        running = False

#-------------- Enter attack phase

    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ","") + " attacks  " + players[target].name.replace(" ","") + " for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s "+ spell.name + " deals", str(magic_dmg), " points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    defeated_players += 1
                    print("\n" + players[target].name + " has died. Enemies defeated :" + defeated_enemies)
                    del players[target]

            #print("Enemy chose" , spell, "damage is", magic_dmg)