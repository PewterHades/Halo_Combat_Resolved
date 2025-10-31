import random as r
from tkinter import Toplevel, Frame, messagebox, Label, Button, StringVar, IntVar
from Display_Manager import ThemeManager
import Json_Handling as JH
import Json_Maps as JM



def calulate(Atk_var, Enemy_var, Fire_Mode, Melee_Mode, Range_Dist, Melee_Dist, root):
    output = Toplevel()
    output.wm_title("Output")
    output.geometry("800x470")
    run_cacl = True

    def on_close():
        root.event_generate("<<ToplevelClosed>>")
        output.destroy()

    output.protocol("WM_DELETE_WINDOW", on_close)

    OP_Frame = Frame(output)
    OP_Frame.grid(row=0, column=0, sticky="nsew")
    output.rowconfigure(0, weight=1)
    output.columnconfigure(0, weight=1)


    Total_Damage = IntVar(value = 0)
    outcome = []
    theme = ThemeManager(OP_Frame)

    Range_Stat = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedwarfare")
    Shots = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangednumberofshots")
    Range_Dice_Number = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangednumberofdice")
    Range_Dice_Size = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedsizeofdice")
    Range_Damage_Added = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedaddeddamage")
    Range_Pierce = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedpierce")
    Rounds = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "roundsinweapon")

    Melee_Stat = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleewarfare")
    Strikes = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleestrikes")
    Melee_Dice_Number = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleenumberofdice")
    Melee_Dice_Size = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleesizeofdice")
    Melee_Damage_Added = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleeaddeddamage")
    Melee_Pierce = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleepierce")

    Armor = {
        "Enemy": {
            "Head": JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyahead"),
            "Arm": JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyaarm"),
            "Chest": JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyachest"),
            "Leg": JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyaleg"),
        },
        "Vehicle": {
            "HitLocation": JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclehitlocation"),
            "Front": JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"]["Front"],
            "Back": JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"]["Back"],
            "Side": JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"]["Side"],
            "Top": JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"]["Top"],
            "Bottom": JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"]["Bottom"]
        }
    }

    if Enemy_var == "enemy":
        toughness = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemytoughness")


    elif Enemy_var == "shield":
        toughness = 0


    elif Enemy_var == "vehicle":
        toughness = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehicletoughness")


    if Range_Dist == "Point Blank":
        Range_Stat += 20 
    
    elif Range_Dist == "Close":
        Range_Stat += 10 

    elif Range_Dist == "Long":
        Range_Stat -= 40
        Range_Pierce = int(Range_Pierce/2)

    elif Range_Dist == "Extreme":
        Range_Stat = max(0, Range_Stat - 80)
        Range_Pierce = 0

    if Melee_Dist == "Point Blank":
        Melee_Stat += 10

    if JH.get_json_val("Preferences.json", JM.Prefernce_map, "diceminimuma") and (Atk_var == "ranged"):
        dice_min = JH.get_json_val("Preferences.json", JM.Prefernce_map, "diceminimumv")
    else:
        dice_min = 0


    if Atk_var == "ranged":
        if Rounds > 0:

            if Fire_Mode == "auto":
                for shot in range(0,min(Shots, Rounds)):
                    final_stats = attack(0, Range_Stat, Enemy_var, Atk_var, Armor, Range_Damage_Added, Range_Dice_Number, Range_Dice_Size, toughness, Range_Pierce, dice_min)
                    outcome.append(final_stats)
                    Total_Damage.set(sum(o[2] for o in outcome))

            elif Fire_Mode == "burst":
                roll = percentile_roll()
                Range_Stat += 5
                DegressOfSuccess = 0
                Final_Damage = 0
                damage = 0
                loc_name = "missed"
                debuff = ""


                if roll <= Range_Stat:
                    DegressOfSuccess = (Range_Stat - roll) // 10
                    loc_tup = location_roll(Enemy_var, roll, Armor)
                    armor = loc_tup[0]
                    loc_name = loc_tup[1]
                    debuff = loc_tup[2]

                    for Shot in range(0, min(Shots, Rounds)):
                        if JH.get_json_val("Preferences.json", JM.Prefernce_map, "hardlight"):
                            damage += hardlight_dmg_roll(Range_Damage_Added, Range_Dice_Number, Range_Dice_Size, dice_min)

                        else:
                            damage += Range_Damage_Added
                            if (Enemy_var == "shield") and (JH.get_json_val("Preferences.json", JM.Prefernce_map, "penetrating")):
                                damage += Range_Pierce *3
                            for dice in range(0,Range_Dice_Number):
                                damage += r.randint(dice_min, Range_Dice_Size)

                    armor = max(0, armor - Range_Pierce)
                    if ("Head" in loc_name) and JH.get_json_val("Preferences.json", JM.Prefernce_map, "headshot"):
                        Final_Damage = max(0, damage - armor)
                    else:
                        Final_Damage = max(0, damage - armor - toughness)

                final_stats = (roll, DegressOfSuccess, Final_Damage, loc_name, debuff)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))

            elif Fire_Mode == "semiauto":
                for shot in range(0, min(Shots, Rounds)): 
                    final_stats = attack(10,Range_Stat,Enemy_var, Atk_var, Armor, Range_Damage_Added, Range_Dice_Number, Range_Dice_Size, toughness, Range_Pierce, dice_min)
                    outcome.append(final_stats)
                    Total_Damage.set(sum(o[2] for o in outcome))

        else:
            run_cacl = False


    elif Atk_var == "melee":
        if Melee_Mode == "burst":
            roll = percentile_roll()
            Range_Stat += 0
            DegressOfSuccess = 0
            Final_Damage = 0
            damage = 0
            loc_name = "missed"
            debuff = ""


            if roll <= Melee_Stat:
                DegressOfSuccess = (Melee_Stat - roll) // 10
                loc_tup = location_roll(Enemy_var, roll, Armor)
                armor = loc_tup[0]
                loc_name = loc_tup[1]
                debuff = loc_tup[2]

                for Strike in range(0,Strikes):
                    damage += Melee_Damage_Added
                    for dice in range(0,Melee_Dice_Number):
                        damage += r.randint(0,Melee_Dice_Size)

                armor = max(0, armor - Melee_Pierce)
                Final_Damage = max(0, damage - armor - toughness)

            final_stats = (roll, DegressOfSuccess, Final_Damage, loc_name, debuff)
            outcome.append(final_stats)
            Total_Damage.set(sum(o[2] for o in outcome))

        elif Melee_Mode == "single":
            if JH.get_json_val("Preferences.json", JM.Prefernce_map, "assassination"):
                final_stats = attack(0, Melee_Stat, Enemy_var, Atk_var, Armor, Melee_Damage_Added, Melee_Dice_Number, Melee_Dice_Size, toughness, Melee_Pierce, dice_min = Melee_Dice_Size)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))

            else:
                final_stats = attack(0, Melee_Stat, Enemy_var, Atk_var, Armor, Melee_Damage_Added, Melee_Dice_Number, Melee_Dice_Size, toughness, Melee_Pierce, dice_min)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))


    Agility_Var = StringVar(value = f"Agility: {JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyagility") if (Enemy_var == "enemy") else JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclemanuverability")}")
    Agility_Label = Label(OP_Frame, textvariable = Agility_Var, font = theme.Text_Font_Size).grid(row=0, column=0, pady = theme.Text_PadY_Size)

    Total_Damage_Var = StringVar(value = f"Total Damage: {Total_Damage.get()}")
    Total_Damage_Label = Label(OP_Frame, textvariable = Total_Damage_Var, font = theme.Text_Font_Size).grid(row = 0, column = 1, pady = theme.Text_PadY_Size)

    for i, stat in enumerate(outcome):
        index = i + 1
        roll_lable = Label(OP_Frame, text = f"You rolled a {stat[0]}", font = theme.Text_Font_Size).grid(row = index, column = 0, pady = theme.Text_PadY_Size)

        DOS_lable = Label(OP_Frame, text = f"You got {stat[1]} DOS", font = theme.Text_Font_Size).grid(row = index, column = 1, pady = theme.Text_PadY_Size)

        Location_lable = Label(OP_Frame, text = f"You {stat[3]}", font = theme.Text_Font_Size).grid(row = index, column = 2, pady = theme.Text_PadY_Size)

        Damage_lable = Label(OP_Frame, text = f"You dealt {stat[2]} damage", font = theme.Text_Font_Size).grid(row = index, column = 3, pady = theme.Text_PadY_Size)

        Debuff_lable = Label(OP_Frame, text = f"Debuffs: {stat[4]}", font = theme.Text_Font_Size, wraplength = theme.Text_WrapLength * 2, justify = "left").grid(row = index, column = 4, pady = theme.Text_PadY_Size, sticky = "w")

        result_var = StringVar(value="")
        Avoid_button = Button(OP_Frame, text = "Evade / Parry", font = theme.Text_Font_Size)
        Avoid_button.grid(row = index, column = 5, pady = theme.Text_PadY_Size)

        Avoid_button.config(command = lambda ev = Enemy_var, s=stat, rv = result_var, td = Total_Damage, b = Avoid_button:
            (rv.set(avoid_damage(ev, s[1], s[2], td)), Agility_Var.set(value = f"Agility: {JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclemanuverability" if (Enemy_var == "vehicle") else "enemyagility")}"),
            Total_Damage_Var.set(value = f"Total Damage: {Total_Damage.get()}"), b.config(state = "disabled")))


        result_label = Label(OP_Frame, textvariable=result_var, font = theme.Text_Font_Size, wraplength = theme.Text_WrapLength * 2).grid(row = index, column = 6, pady = theme.Text_PadY_Size)  

    round_var = Rounds - Shots
    JH.set_json_val("Saved_Stats.json", JM.Entry_map, round_var, "roundsinweapon")


    theme.change_theme(output)
    if not run_cacl:
        for widget in output.winfo_children():    
            widget.destroy()
        output.destroy()
        messagebox.showerror(title = "No Ammo", detail = "Reloead required, there are no more rounds in your weapon.")

def avoid_damage(Enemy_var, DegreeOfSuccess, Damage, Total_Damage):
    roll = percentile_roll()
    response = ""

    if Enemy_var == "enemy" or Enemy_var == "shield":
        agi_str = "enemyagility"
        deb_str = "enemydebuff"
        agility = JH.get_json_val("Saved_Stats.json", JM.Entry_map, agi_str)
        debuff = JH.get_json_val("Saved_Stats.json", JM.Entry_map, deb_str)
    
    elif Enemy_var == "vehicle":
        agi_str = "vehiclemanuverability"
        deb_str = "vehicledebuff"
        agility = JH.get_json_val("Saved_Stats.json", JM.Entry_map, agi_str)
        debuff = JH.get_json_val("Saved_Stats.json", JM.Entry_map, deb_str)   

    DegOF = (agility - roll) // 10

    if DegOF > DegreeOfSuccess:
        response += f"Success. {DegOF} Degrees. "
        Total_Damage.set(Total_Damage.get() - Damage)
    else:
        response += f"Fail. {DegOF} Degrees. "

    if debuff > 0:
        new_val = max(0, debuff - 1)
        JH.set_json_val("Saved_Stats.json", JM.Entry_map, new_val, deb_str)
        response += f"Debuff mitigated, {new_val} uses left."
    else:
        new_val = max(0, agility - 10)
        JH.set_json_val("Saved_Stats.json", JM.Entry_map, new_val, agi_str)
        response += f"Agility is now {new_val}"


    return response

def percentile_roll():
    ones = r.randint(0,9)
    tens = r.randint(0,9) * 10

    if ones == 0 and tens == 0:
        percent = 100
    elif ones == 0 and tens != 0:
        percent = tens + 10
    else:
        percent = ones + tens 

    return percent  

def location_roll(Enemy_Var, roll, Armor):
    loc_name = "hit the "
    debuff = ""
    ones = r.randint(0,9)
    tens = r.randint(0,9) * 10

    if ones == 0 and tens == 0:
        percent = 100
    elif ones == 0 and tens != 0:
        percent = tens + 10
    else:
        percent = ones + tens 
    percent = int(str(percent)[::-1])


    oness = r.randint(0,9)
    tenss = r.randint(0,9) * 10

    if oness == 0 and tenss == 0:
        d_percent = 100
    elif oness == 0 and tenss != 0:
        d_percent = tenss + 10
    else:
        d_percent = oness + tenss 


    Main_Location =[(1, 2, "Head", "Neck"),
                    (3, 4, "Head", "Mouth"),
                    (5, 6, "Head", "Nose"),
                    (7, 7, "Head", "Eye"),
                    (8, 8, "Head", "Ear"),
                    (9, 10, "Head", "Forehead"),
                    (11, 12, "Left Arm", "Hand"),
                    (13, 15, "Left Arm", "Forearm"),
                    (16, 16, "Left Arm", "Elbow"),
                    (17, 19, "Left Arm", "Bicep"),
                    (20, 20, "Left Arm", "Shoulder"),
                    (21, 22, "Right Arm", "Hand"),
                    (23, 25, "Right Arm", "Forearm"),
                    (26, 26, "Right Arm", "Elbow"),
                    (27, 29, "Right Arm", "Bicep"),
                    (30, 30, "Right Arm", "Shoulder"),
                    (31, 32, "Left Leg", "Foot"),
                    (33, 37, "Left Leg", "Shin"),
                    (38, 38, "Left Leg", "Knee"),
                    (39, 43, "Left Leg", "Thigh"),
                    (44, 45, "Left Leg", "Hip"),
                    (46, 47, "Right Leg", "Foot"),
                    (48, 53, "Right Leg", "Shin"),
                    (54, 54, "Right Leg", "Knee"),
                    (55, 58, "Right Leg", "Thigh"),
                    (59, 60, "Right Leg", "Hip"),
                    (61, 65, "Chest", "Pelvis"),
                    (66, 72, "Chest", "Intestines"),
                    (73, 78, "Chest", "Spine"),
                    (79, 84, "Chest", "Stomach, Kidney, or Liver"),
                    (85, 89, "Chest", "Heart"),
                    (90, 96, "Chest", "Lungs"),
                    (97, 100, "Chest", "Ribcage, No Organ Struck")                  
                    ]

    Debuff_Location={
        "Neck":[(1, 25, "Whiplash(1)"),
                (26, 40, "Whiplash(2)"),
                (41, 55, "Whiplash(3), Bloodloss(1)"),
                (56, 70, "Whiplash(4), Bloodloss(2), Looming Death(20)"),
                (71, 100, f"Whiplast(4), Bloodloss(4), Looming Death({r.randint(1,10)})")],
        "Mouth":[(1, 20, "Lockjaw(1)"),
                 (21, 30, "Lockjaw(5)"),
                 (31, 40, f"Lockjaw(10), Lose {r.randint(1,5)} Teeth"),
                 (41, 50, f"Lockjaw(10), Bloodloss(2), Lose {r.randint(1,5) + r.randint(1,5)} Teeth"),
                 (51, 100, f"Lockjaw(permanent), Bloodloss(4), Lose {r.randint(1,10) + r.randint(1,10)} Teeth")],
        "Nose":[(1, 20, "Lost(2), Nose Broke"),
                (21, 30, "Lost(4), Nose Broke"),
                (31, 40, "Gasping(2), Nose Broke"),
                (41, 50, "Gasping(3), Nose Broke"),
                (51, 100, "Gasping(4), Nose lost")],
        "Eye":[(1, 20, "Vision Loss(3)"),
               (21, 30, "Vision Loss(5)"),
               (31, 40, "Vision Loss(10), Flinch(1)"),
               (41, 50, "Vision Loss(10), Flinch(2), Whiplash(1)"),
               (51, 100, f"Vision Loss(60), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Eye Lost")],
        "Ear":[(1, 20, "Tinnitus(1)"),
               (21, 30, "Tinnitus(3)"),
               (31, 40, "Tinnitus(5), Flinch(1)"),
               (41, 50, "Tinnitus(10), Flinch(2), Whiplast(1)"),
               (51, 100, f"Tinnitus(60), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Ear Lost")],
        "Forehead":[(1, 30, "Lost(2)"),
                    (31, 50, "Lost(4), Shellshock(1)"),
                    (51, 65, "Lost(6), Shellshock(2)"),
                    (66, 80, f"Lost(10), Shellshock({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death(10)"),
                    (81, 100, "Instant Death, Head destroyed")],
        "Hand":[(1, 25, "Flinch(1)"),
                (26, 40, "Flinch(1), Drop"),
                (41, 55, "Flinch(3), Drop(3), Brone Broken(Fracture)"),
                (56, 70, "Flinch(3), Drop(5), Brone Broken(Shatter)"),
                (71, 100, "Flinch(5), Hand Lost")],
        "Forearm":[(1, 30, "Flinch(1)"),
                   (31, 50, "Flinch(2), Paralyzed(1)"),
                   (51, 65, "Flinch(5), Bone Broken(Fracture)"),
                   (66, 80, "Flinch(5), Bone Broken(Shatter)"),
                   (81, 100, "Looming Death(10), Arm Lost")],
        "Elbow":[(1, 25, "Weakend(1)"),
                 (26, 40, "Weakend(2), Drop"),
                 (41, 55, "Weakend(4), Drop(2), Brone Broken(Fracture)"),
                 (56, 70, "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"),
                 (71, 100, "Looming Death(9), Arm Lost")],
        "Bicep":[(1, 30, "Flinch(1)"),
                 (31, 50, "Flinch(2), Paralyzed(1)"),
                 (51, 65, "Flinch(5), Bone Broken(Fracture)"),
                 (66, 80, "Flinch(5), Bone Broken(Shatter)"),
                 (81, 100, "Looming Death(10), Arm Lost")],
        "Shoulder":[(1, 25, "Weakend(1)"),
                    (26, 40, "Weakend(2), Drop"),
                    (41, 55, "Weakend(4), Drop(2), Brone Broken(Fracture)"),
                    (56, 70, "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"),
                    (71, 100, "Looming Death(9), Arm Lost")],
        "Foot":[(1, 25, "Slowed(2)"),
                (26, 40, "Slowed(3), Knockdown"),
                (41, 55, "Slowed(5), Knockdown(2), Brone Broken(Fracture)"),
                (56, 70, "Slowed(6), Knockdown Prone(2), Brone Broken(Shatter)"),
                (71, 100, "Slowed(10), Knockdown Prone(4), Foot Lost")],
        "Shin":[(1, 30, "Slowed(1)"),
                (31, 50, "Slowed(3)"),
                (51, 65, "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"),
                (66, 80, "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"),
                (81, 100, "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost")],
        "Knee":[(1, 25, "Knockdown"),
                (26, 40, "Knockdown(1)"),
                (41, 55, "Knockdown(2), Slowed(3), Brone Broken(Fracture)"),
                (56, 70, "Knockdown(3), Slowed(5), Brone Broken(Shatter)"),
                (71, 100, "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost")],
        "Thigh":[(1, 30, "Slowed(1)"),
                 (31, 50, "Slowed(3)"),
                 (51, 65, "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"),
                 (66, 80, "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"),
                 (81, 100, "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost")],
        "Hip":[(1, 25, "Knockdown"),
               (26, 40, "Knockdown(1)"),
               (41, 55, "Knockdown(2), Slowed(3), Brone Broken(Fracture)"),
               (56, 70, "Knockdown(3), Slowed(5), Brone Broken(Shatter)"),
               (71, 100, "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost")],
        "Pelvis":[(1, 25, "Slowed(2)"),
                  (26, 40, "Slowed(3), Tattered(2)"),
                  (41, 55, "Slowed(4), Tattered(3), Brone Broken(Fracture)"),
                  (56, 70, "Slowed(5), Tattered(4), Brone Broken(Shatter)"),
                  (71, 100, "Slowed(permanent), Tattered(20), Brone Broken(Shatter)")],
        "Intestines":[(1, 25, "Tattered(2)"),
                      (26, 40, "Tattered(3), Weakend(2)"),
                      (41, 50, "Tattered(4), Weakend(4)"),
                      (51, 60, "Tattered(5), Weakend(5), Looming Death(15)"),
                      (61, 100, f"Tattered(6), Weakend(5), Looming Death({r.randint(1,10)})")],
        "Spine":[(1, 25, "Flinch(1), Drop, Knockdown"),
               (26, 40, "Flinch(2), Drop(2), Knockdown(1)"),
               (41, 55, "Paralyzed(2), Knockdown(3), Bone Broken(Fractured)"),
               (56, 70, "Paralyzed(5), Knockdown Prone(5), Bone Broken(Shattered)"),
               (71, 100, "Instant Death, Spine destroyed")],
        "Stomach, Kidney, or Liver":[(1, 25, "Gasping(1)"),
                                     (26, 40, "Gasping(2), Tattered(1)"),
                                     (41, 50, "Gasping(3), Tattered(2)"),
                                     (51, 60, "Gasping(4), Tattered(5), Looming Death(20)"),
                                     (61, 100, "Gasping(5), Tattered(6), Looming Death(10)")],
        "Heart":[(1, 25, "Winded(5)"),
                 (26, 40, f"Winded(10), Concussed({r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10) + r.randint(1,10) + r.randint(1,10) + r.randint(1,10) + r.randint(1,10)})"),
                 (41, 50, f"Winded(10), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10) + r.randint(1,10) + r.randint(1,10)})"),
                 (51, 60, f"Winded(Permanent), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10)})"),
                 (61, 100, "Heart destroyed, Instant Death")],
        "Lungs":[(1, 25, "Winded(2), Gasping(2)"),
                 (26, 40, "Winded(3), Gasping(3)"),
                 (41, 50, "Winded(4), Gasping(5), Looming Death(20)"),
                 (51, 60, "Winded(5), Gasping(5), Looming Death(15)"),
                 (61, 100, "Winded(6), Gasping(5), Choking")],
        "Ribcage, No Organ Struck":[(1, 30, "Winded(1), Gasping(1)"),
                                    (31, 50, "Winded(2), Gasping(1)"),
                                    (51, 65, "Winded(3), Gasping(2)"),
                                    (66, 80, "Winded(4), Gasping(4), Bone Broken(Fractured)"),
                                    (81, 100, "Winded(5), Gasping(4), Bone Broken(Shattered)")]}


    def list_locations(ranges, loc = None):
            outputs = [None] * 100
            if not loc:
                for min_val, max_val, outcome1, outcome2 in ranges:
                    for i in range(min_val, max_val + 1):
                        outputs[i - 1] = (outcome1, outcome2)

            elif loc:
                for min_val, max_val, outcome in ranges[loc]:
                    for i in range(min_val, max_val + 1):
                        outputs[i - 1] = outcome
            return outputs
                
    if Enemy_Var == "enemy":
        loc_name += list_locations(Main_Location)[percent][0]
        if "Head" in loc_name:
            armor = Armor["Enemy"]["Head"]
        elif "Chest" in loc_name:
            armor = Armor["Enemy"]["Chest"]
        elif "Arm" in loc_name:
            armor = Armor["Enemy"]["Arm"]
        else:
            armor = Armor["Enemy"]["Leg"]

        if roll == 1:
            loc_name += f", {list_locations(Main_Location)[percent][1]}"
            debuff = {list_locations(Debuff_Location, loc = (list_locations(Main_Location)[percent][1]))[d_percent]}
        
        else:
            loc_name = loc_name

    elif Enemy_Var == "vehicle":
        armor = Armor["Vehicle"][Armor["Vehicle"]["HitLocation"]]

    else:
        armor = 0

    return (armor, loc_name, debuff)

def attack(Type_Bonus, Range_Stat, Enemy_var, Attack_Var, Armor, R_Added_Damage, R_D_Num, R_D_Size, toughness, R_Pierce, dice_min):
    roll = percentile_roll()
    Range_Stat += Type_Bonus
    DegressOfSuccess = 0
    Final_Damage = 0
    loc_name = "missed"
    debuff = ""


    if roll <= Range_Stat:
        DegressOfSuccess = (Range_Stat - roll) // 10
        loc_tup = location_roll(Enemy_var, roll, Armor)
        armor = loc_tup[0]
        loc_name = loc_tup[1]
        debuff = loc_tup[2]

        damage = R_Added_Damage
        if (Enemy_var == "shield") and (JH.get_json_val("Preferences.json", JM.Prefernce_map, "penetrating")):
            damage += R_Pierce * 3

        for dice in range(0,R_D_Num):
            if roll == 1:
                if JH.get_json_val("Preferences.json", JM.Prefernce_map, "hardlight"):
                    damage += R_D_Size + hardlight_dmg_roll(R_Added_Damage, R_D_Size, dice_min)

                else:
                    damage += R_D_Size

            else:
                if JH.get_json_val("Preferences.json", JM.Prefernce_map, "hardlight"):
                    damage += hardlight_dmg_roll(R_Added_Damage, R_D_Size, dice_min)

                else:
                    damage += r.randint(dice_min,R_D_Size)

        armor = max(0, armor - R_Pierce)
        if ("Head" in loc_name) and JH.get_json_val("Preferences.json", JM.Prefernce_map, "headshot"):
            Final_Damage = max(0, damage - armor)
        else:
            Final_Damage = max(0, damage - armor - toughness)

        if JH.get_json_val("Preferences.json", JM.Prefernce_map, "assassination") and (Attack_Var == "melee"):
            Final_Damage = Final_Damage * 4
        else:
            Final_Damage = Final_Damage

    final_stats = (roll, DegressOfSuccess, Final_Damage, loc_name, debuff)
    return final_stats

def hardlight_dmg_roll(R_Added_Damage, R_D_Size, dice_min):
    damage = R_Added_Damage
    index = 0
    while index < 1:
        add_dmg = r.randint(dice_min, R_D_Size)
        index += 1
        if add_dmg == R_D_Size:
            index -= 1
        damage += add_dmg
    return damage
