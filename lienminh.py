import random
import time
 
class Champion:
    def __init__(self, name, max_hp, attack_power, max_mana, ability_cost, ability_dmg, ability_cd):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power
        self.max_mana = max_mana
        self.mana = max_mana
        self.ability_cost = ability_cost
        self.ability_dmg = ability_dmg
        self.ability_cd = ability_cd
        self.cd_left = 0
        self.potions = 2
 
    def alive(self):
        return self.hp > 0
 
    def auto_attack(self, target):
        # damage with small random variance
        variance = random.uniform(0.9, 1.1)
        dmg = max(0, int(self.attack_power * variance))
        target.hp -= dmg
        return dmg
 
    def use_ability(self, target):
        if self.cd_left > 0:
            return ("cooldown", 0)
import random
import time
 
class Champion:
    def __init__(self, name, max_hp, attack_power, max_mana, ability_cost, ability_dmg, ability_cd):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power
        self.max_mana = max_mana
        self.mana = max_mana
        self.ability_cost = ability_cost
        self.ability_dmg = ability_dmg
        self.ability_cd = ability_cd
        self.cd_left = 0
        self.potions = 2
 
    def alive(self):
        return self.hp > 0
 
    def auto_attack(self, target):
        # damage with small random variance
        variance = random.uniform(0.9, 1.1)
        dmg = max(0, int(self.attack_power * variance))
        target.hp -= dmg
        return dmg
 
    def use_ability(self, target):
        if self.cd_left > 0:
            return ("cooldown", 0)
        if self.mana < self.ability_cost:
            return ("no_mana", 0)
        # ability hits harder and has crit chance
        self.mana -= self.ability_cost
        self.cd_left = self.ability_cd
        crit = random.random() < 0.15
        base = self.ability_dmg
        dmg = base * (2 if crit else 1)
        # small variance
        dmg = int(dmg * random.uniform(0.95, 1.08))
        target.hp -= dmg
        return ("hit", dmg, crit)
 
    def drink_potion(self):
        if self.potions <= 0:
            return 0
        self.potions -= 1
        heal = int(self.max_hp * 0.30)  # potion heals 30% max HP
        self.hp = min(self.max_hp, self.hp + heal)
        return heal
 
    def end_turn(self):
        # mana regen and cooldown tick
        self.mana = min(self.max_mana, self.mana + int(self.max_mana * 0.10))  # regen 10% max mana
        if self.cd_left > 0:
            self.cd_left -= 1
 
    def status(self):
        return f"{self.name}: HP {self.hp}/{self.max_hp}, Mana {self.mana}/{self.max_mana}, CD {self.cd_left}, Potions {self.potions}"
 
def player_turn(player, enemy):
    print("\n-- Your turn --")
    print(player.status())
    print(enemy.status())
    print("Chọn hành động: 1) Đánh thường  2) Kỹ năng  3) Potion  4) Thoát")
    choice = input("=> ").strip()
    if choice == "1":
        dmg = player.auto_attack(enemy)
        print(f"> Bạn đánh thường gây {dmg} sát thương lên {enemy.name}.")
    elif choice == "2":
        res = player.use_ability(enemy)
        if res[0] == "cooldown":
            print("> Kỹ năng đang hồi chiêu.")
        elif res[0] == "no_mana":
            print("> Không đủ mana để dùng kỹ năng.")
        else:
            _, dmg, crit = res
            s = " (CRIT!)" if crit else ""
            print(f"> Bạn dùng kỹ năng gây {dmg} sát thương{s} lên {enemy.name}.")
    elif choice == "3":
        healed = player.drink_potion()
        if healed:
            print(f"> Bạn uống potion và hồi {healed} HP.")
        else:
            print("> Bạn không còn potion.")
    elif choice == "4":
        print("Thoát game. Bye!")
        exit()
    else:
        print("> Lựa chọn không hợp lệ — bạn lỡ mất lượt.")
    player.end_turn()
    time.sleep(0.6)
 
def ai_turn(ai, player):
    print("\n-- Đến lượt đối phương --")
    # simple AI logic: use ability if available & has mana and low enemy HP or random chance
    use_ability = False
    if ai.cd_left == 0 and ai.mana >= ai.ability_cost:
        # prefer ability if it can kill or 40% chance
        if ai.ability_dmg >= player.hp or random.random() < 0.4:
            use_ability = True
 
    if use_ability:
        res = ai.use_ability(player)
        if res[0] == "hit":
            _, dmg, crit = res
            s = " (CRIT!)" if crit else ""
            print(f"> {ai.name} dùng kỹ năng và gây {dmg} sát thương{s} lên bạn.")
        else:
            print(f"> {ai.name} cố dùng kỹ năng nhưng thất bại.")
    else:
        # if low hp and has potion, 40% chance to drink
        if ai.hp < ai.max_hp * 0.35 and ai.potions > 0 and random.random() < 0.4:
            healed = ai.drink_potion()
            print(f"> {ai.name} uống potion và hồi {healed} HP.")
        else:
            dmg = ai.auto_attack(player)
            print(f"> {ai.name} đánh thường và gây {dmg} sát thương lên bạn.")
    ai.end_turn()
    time.sleep(0.6)
 
def main():
    print("=== Mini League-like (console) ===")
    # choose champion presets
    champs = {
        "1": ("Marksman", 90, 18, 50, 20, 45, 2),   # name, hp, atk, mana, cost, ability_dmg, cd
        "2": ("Bruiser", 120, 14, 40, 15, 35, 3),
        "3": ("Mage", 75, 10, 80, 25, 60, 3)
    }
    print("Chọn tướng: 1) Marksman  2) Bruiser  3) Mage")
    pick = input("=> ").strip()
    if pick not in champs:
        pick = "1"
    pconf = champs[pick]
    player = Champion(pconf[0], pconf[1], pconf[2], pconf[3], pconf[4], pconf[5], pconf[6])
 
    # enemy random pick
    epick = random.choice(list(champs.keys()))
    econf = champs[epick]
    enemy = Champion(econf[0]+"-Bot", econf[1], econf[2], econf[3], econf[4], econf[5], econf[6])
 
    print(f"\nBạn chọn {player.name}. Đối thủ: {enemy.name}. Bắt đầu trận!")
    time.sleep(1)
    # battle loop
    while player.alive() and enemy.alive():
        player_turn(player, enemy)
        if not enemy.alive():
            print(f"\n>>> Bạn thắng! {enemy.name} bị hạ.")
            break
        ai_turn(enemy, player)
        if not player.alive():
            print(f"\n>>> Bạn thua... {player.name} bị hạ.")
            break
 
    print("\nTrận đấu kết thúc.")
    print(player.status())
    print(enemy.status())
 
if __name__ == "__main__":
    main()
