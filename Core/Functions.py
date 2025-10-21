import random as r
from tkinter import Toplevel, Frame, messagebox, Label, Button, StringVar, IntVar
from Display_Manager import ThemeManager
import Json_Handling as JH



def calulate(Atk_var, Enemy_var, Fire_Mode, Melee_Mode, Range_Dist, Melee_Dist, Range_Stat, Melee_Stat, E_Agility, S_Agility, V_Agility, 
             Shots, R_D_Size, R_D_Num, R_Added_Damage, R_Pierce, R_Rounds, 
             Strikes, M_D_Size, M_D_Num, M_Added_Damage, M_Pierce,
             Head, Arm, Chest, Leg, V_Armor, 
             E_ignores, S_ignores, V_ignores, E_Tough, V_Tough):
    output = Toplevel()
    output.wm_title("Output")
    output.geometry("800x470")
    run_cacl = True

    OP_Frame = Frame(output)
    OP_Frame.grid(row=0, column=0, sticky="nsew")
    output.rowconfigure(0, weight=1)
    output.columnconfigure(0, weight=1)

    Agility = IntVar(value = 0)
    ignores = IntVar(value = 0)
    Total_Damage = IntVar(value = 0)
    dice_min = 0
    outcome = []
    armor = 0
    theme = ThemeManager(OP_Frame)


    if Enemy_var == "enemy":
        toughness = E_Tough
        Agility.set(E_Agility)
        ignores.set(value = E_ignores)

    elif Enemy_var == "shield":
        toughness = 0
        Agility.set(value = S_Agility)
        ignores.set(value = S_ignores)

    elif Enemy_var == "vehicle":
        toughness = V_Tough
        Agility.set(value = V_Agility)
        ignores.set(value = V_ignores)


    if Range_Dist == "Point Blank":
        Range_Stat += 20
    
    elif Range_Dist == "Close":
        Range_Stat += 10

    elif Range_Dist == "Long":
        Range_Stat -= 40
        R_Pierce = int(R_Pierce/2)

    elif Range_Dist == "Extreme":
        Range_Stat -= 80
        R_Pierce = 0

    if Melee_Dist == "Point Blank":
        Melee_Stat += 10

    if JH.read("Preferences.json")["SpecialRules"]["DiceMinimum"]["Active"] and (Atk_var == "ranged"):
        dice_min = JH.read("Preferences.json")["SpecialRules"]["DiceMinimum"]["Value"]
    else:
        dice_min = 0


    if Atk_var == "ranged":
        if R_Rounds > 0:

            if Fire_Mode == "auto":
                for shot in range(0,min(Shots, R_Rounds)):
                    final_stats = attack(0, Range_Stat, Enemy_var, Atk_var, Head, Arm, Leg, Chest, V_Armor, R_Added_Damage, R_D_Num, R_D_Size, toughness, R_Pierce, dice_min)
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
                    loc_tup = location_roll(Enemy_var, roll, Head, Arm, Leg, Chest, V_Armor)
                    armor = loc_tup[0]
                    loc_name = loc_tup[1]
                    debuff = loc_tup[2]

                    for Shot in range(0, min(Shots, R_Rounds)):
                        if JH.read("Preferences.json")["SpecialRules"]["HardLight"]["Active"]:
                            damage += hardlight_dmg_roll(R_Added_Damage, R_D_Num, R_D_Size, dice_min)

                        else:
                            damage += R_Added_Damage
                            if (Enemy_var == "shield") and (JH.read("Preferences.json")["SpecialRules"]["Penetrating"]["Active"]):
                                damage += R_Pierce *3
                            for dice in range(0,R_D_Num):
                                damage += r.randint(dice_min, R_D_Size)

                    armor = max(0, armor - R_Pierce)
                    if ("Head" in loc_name) and JH.read("Preferences.json")["SpecialRules"]["HeadShot"]["Active"]:
                        Final_Damage = max(0, damage - armor)
                    else:
                        Final_Damage = max(0, damage - armor - toughness)

                final_stats = (roll, DegressOfSuccess, Final_Damage, loc_name, debuff)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))

            elif Fire_Mode == "semiauto":
                for shot in range(0, min(Shots, R_Rounds)): 
                    final_stats = attack(10,Range_Stat,Enemy_var, Atk_var, Head, Arm, Leg, Chest, V_Armor, R_Added_Damage, R_D_Num, R_D_Size, toughness, R_Pierce, dice_min)
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
                loc_tup = location_roll(Enemy_var, roll, Head, Arm, Leg, Chest, V_Armor)
                armor = loc_tup[0]
                loc_name = loc_tup[1]
                debuff = loc_tup[2]

                for Strike in range(0,Strikes):
                    damage += M_Added_Damage
                    for dice in range(0,M_D_Num):
                        damage += r.randint(0,M_D_Size)

                armor = max(0, armor - M_Pierce)
                Final_Damage = max(0, damage - armor - toughness)

            final_stats = (roll, DegressOfSuccess, Final_Damage, loc_name, debuff)
            outcome.append(final_stats)
            Total_Damage.set(sum(o[2] for o in outcome))

        elif Melee_Mode == "single":
            if JH.read("Preferences.json")["SpecialRules"]["Assassination"]["Active"]:
                final_stats = attack(0, Melee_Stat, Enemy_var, Atk_var, Head, Arm, Leg, Chest, V_Armor, M_Added_Damage, M_D_Num, M_D_Size, toughness, M_Pierce, dice_min = M_D_Size)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))

            else:
                final_stats = attack(0, Melee_Stat, Enemy_var, Atk_var, Head, Arm, Leg, Chest, V_Armor, M_Added_Damage, M_D_Num, M_D_Size, toughness, M_Pierce, dice_min)
                outcome.append(final_stats)
                Total_Damage.set(sum(o[2] for o in outcome))


    Agility_Var = StringVar(value = f"Agility: {Agility.get()}")
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

        Avoid_button.config(command = lambda s=stat, a= Agility, rv = result_var, ig = ignores, td = Total_Damage, b = Avoid_button:
            (rv.set(avoid_damage(a, s[1], ig, s[2], td)), Agility_Var.set(value = f"Agility: {a.get()}"),
            Total_Damage_Var.set(value = f"Total Damage: {Total_Damage.get()}"), b.config(state = "disabled")))


        result_label = Label(OP_Frame, textvariable=result_var, font = theme.Text_Font_Size, wraplength = theme.Text_WrapLength * 2).grid(row = index, column = 6, pady = theme.Text_PadY_Size)  

    theme.change_theme(output)
    if not run_cacl:
        for widget in output.winfo_children():    
            widget.destroy()
        output.destroy()
        messagebox.showerror(title = "No Ammo", detail = "Reloead required, there are no more rounds in your weapon.")

def avoid_damage(Agility, DegreeOfSuccess, Debuff_Immunity, Damage, Total_Damage):
    roll = percentile_roll()
    response = ""
    DegOF = (Agility.get() - roll) // 10


    if DegOF > DegreeOfSuccess:
        response += f"Success. {DegOF} Degrees. "
        Total_Damage.set(Total_Damage.get() - Damage)
    else:
        response += f"Fail. {DegOF} Degrees. "

    if Debuff_Immunity.get() > 0:
        Debuff_Immunity.set(Debuff_Immunity.get() - 1)
        response += f"Debuff mitigated, {Debuff_Immunity.get()} uses left."
    else:
        new_val = max(0, Agility.get() - 10)
        Agility.set(new_val)
        response += f"Agility is now {Agility.get()}"


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

def location_roll(Enemy_Var,roll, Head, Arm, Leg, Chest, V_Armor):
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


    oness = r.randint(0,9)
    tenss = r.randint(0,9) * 10

    if oness == 0 and tenss == 0:
        d_percent = 100
    elif oness == 0 and tenss != 0:
        d_percent = tenss + 10
    else:
        d_percent = oness + tenss 


    percent = int(str(percent)[::-1])

    if Enemy_Var == "enemy":
        if percent <= 10:
            armor = Head
            loc_name += "Head"
            if (percent <= 2) and roll == 1:
                loc_name += ", Neck"
                if d_percent <= 25:
                    debuff = "Whiplash(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Whiplash(2)"
                elif 41 <= d_percent <= 55:
                    debuff = "Whiplash(3), Bloodloss(1)"
                elif 56 <= d_percent <= 70:
                    debuff = "Whiplash(4), Bloodloss(2), Looming Death(20)"
                else:
                    debuff = f"Whiplast(4), Bloodloss(4), Looming Death({r.randint(1,10)})"

            elif (3 <= percent <= 4) and roll == 1:
                loc_name += ", Mount"
                if d_percent <= 20:
                    debuff = "Lockjaw(1)"
                elif 21 <= d_percent <= 30:
                    debuff = "Lockjaw(5)"
                elif 31 <= d_percent <= 40:
                    debuff = f"Lockjaw(10), Lose {r.randint(1,5)} Teeth"
                elif 41 <= d_percent <= 50:
                    debuff = f"Lockjaw(10), Bloodloss(2), Lose {r.randint(1,5) + r.randint(1,5)} Teeth"
                else:
                    debuff = f"Lockjaw(permanent), Bloodloss(4), Lose {r.randint(1,10) + r.randint(1,10)} Teeth"

            elif (5 <= percent <=6) and roll == 1:
                loc_name += ", Nose"
                if d_percent <= 20:
                    debuff = "Lost(2), Nose Broke"
                elif 21 <= d_percent <= 30:
                    debuff = "Lost(4), Nose Broke"
                elif 31 <= d_percent <= 40:
                    debuff = "Gasping(2), Nose Broke"
                elif 41 <= d_percent <= 50:
                    debuff = "Gasping(3), Nose Broke"
                else:
                    debuff = "Gasping(4), Nose lost"

            elif (percent == 7) and roll == 1:
                loc_name += ", Eye"
                if d_percent <= 20:
                    debuff = "Vision Loss(3)"
                elif 21 <= d_percent <= 30:
                    debuff = "Vision Loss(5)"
                elif 31 <= d_percent <= 40:
                    debuff = "Vision Loss(10), Flinch(1)"
                elif 41 <= d_percent <= 50:
                    debuff = "Vision Loss(10), Flinch(2), Whiplash(1)"
                else:
                    debuff = f"Vision Loss(60), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Eye Lost"

            elif (percent == 8) and roll == 1:
                loc_name += ", Ear"
                if d_percent <= 20:
                    debuff = "Tinnitus(1)"
                elif 21 <= d_percent <= 30:
                    debuff = "Tinnitus(3)"
                elif 31 <= d_percent <= 40:
                    debuff = "Tinnitus(5), Flinch(1)"
                elif 41 <= d_percent <= 50:
                    debuff = "Tinnitus(10), Flinch(2), Whiplast(1)"
                else:
                    debuff = f"Tinnitus(60), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Ear Lost"

            elif (9 <= percent <= 10) and roll == 1:
                loc_name += ", Forehead"
                if d_percent <= 30:
                    debuff = "Lost(2)"
                elif 31 <= d_percent <= 50:
                    debuff = "Lost(4), Shellshock(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Lost(6), Shellshock(2)"
                elif 66 <= d_percent <= 80:
                    debuff = f"Lost(10), Shellshock({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death(10)"
                else:
                    debuff = "Instant Death, Head destroyed"

        elif 11 <= percent <= 20:
            armor = Arm
            loc_name += "Left Arm"

            if (11 <= percent <= 12) and roll == 1:
                loc_name += ", Hand"
                if d_percent <= 25:
                    debuff = "Flinch(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Flinch(1), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Flinch(3), Drop(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Flinch(3), Drop(5), Brone Broken(Shatter)"
                else:
                    debuff = "Flinch(5), Hand Lost"

            elif (13 <= percent <= 15) and roll == 1:
                loc_name += ", Forearm"
                if d_percent <= 30:
                    debuff = "Flinch(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Flinch(2), Paralyzed(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Flinch(5), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Flinch(5), Bone Broken(Shatter)"
                else:
                    debuff = "Looming Death(10), Arm Lost"

            elif (percent == 16) and roll == 1:
                loc_name += ", Elbow"
                if d_percent <= 25:
                    debuff = "Weakend(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Weakend(2), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Weakend(4), Drop(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"
                else:
                    debuff = "Looming Death(9), Arm Lost"

            elif (17 <= percent <= 19) and roll == 1:
                loc_name += ", Bicep"
                if d_percent <= 30:
                    debuff = "Flinch(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Flinch(2), Paralyzed(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Flinch(5), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Flinch(5), Bone Broken(Shatter)"
                else:
                    debuff = "Looming Death(10), Arm Lost"

            elif (percent == 20) and roll == 1:
                loc_name += ", Shoulder"
                if d_percent <= 25:
                    debuff = "Weakend(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Weakend(2), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Weakend(4), Drop(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"
                else:
                    debuff = "Looming Death(9), Arm Lost"

        elif 21 <= percent <= 30:
            armor = Arm
            loc_name += "Right Arm"

            if (21 <= percent <= 22) and roll == 1:
                loc_name += ", Hand"
                if d_percent <= 25:
                    debuff = "Flinch(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Flinch(1), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Flinch(3), Drop(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Flinch(3), Drop(5), Brone Broken(Shatter)"
                else:
                    debuff = "Flinch(5), Hand Lost"

            elif (23 <= percent <= 25) and roll == 1:
                loc_name += ", Forearm"
                if d_percent <= 30:
                    debuff = "Flinch(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Flinch(2), Paralyzed(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Flinch(5), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Flinch(5), Bone Broken(Shatter)"
                else:
                    debuff = "Looming Death(10), Arm Lost"

            elif (percent == 26) and roll == 1:
                loc_name += ", Elbow"
                if d_percent <= 25:
                    debuff = "Weakend(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Weakend(2), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Weakend(4), Drop(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"
                else:
                    debuff = "Looming Death(9), Arm Lost"

            elif (27 <= percent <= 29) and roll == 1:
                loc_name += ", Bicep"
                if d_percent <= 30:
                    debuff = "Flinch(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Flinch(2), Paralyzed(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Flinch(5), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Flinch(5), Bone Broken(Shatter)"
                else:
                    debuff = "Looming Death(10), Arm Lost"

            elif (percent == 30) and roll == 1:
                loc_name += ", Shoulder"
                if d_percent <= 25:
                    debuff = "Weakend(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Weakend(2), Drop"
                elif 41 <= d_percent <= 55:
                    debuff = "Weakend(4), Drop(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Weakend(4), Paralyzed(2), Brone Broken(Shatter)"
                else:
                    debuff = "Looming Death(9), Arm Lost"
                
        elif 31 <= percent <= 45:
            armor = Leg
            loc_name += "Left Leg"

            if (31 <= percent <= 32) and roll == 1:
                loc_name += ", Foot"
                if d_percent <= 25:
                    debuff = "Slowed(2)"
                elif 26 <= d_percent <= 40:
                    debuff = "Slowed(3), Knockdown"
                elif 41 <= d_percent <= 55:
                    debuff = "Slowed(5), Knockdown(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Slowed(6), Knockdown Prone(2), Brone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Knockdown Prone(4), Foot Lost"

            elif (33 <= percent <= 37) and roll == 1:
                loc_name += ", Shin"
                if d_percent <= 30:
                    debuff = "Slowed(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Slowed(3)"
                elif 51 <= d_percent <= 65:
                    debuff = "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost"

            elif (percent == 38) and roll == 1:
                loc_name += ", Knee"
                if d_percent <= 25:
                    debuff = "Knockdown"
                elif 26 <= d_percent <= 40:
                    debuff = "Knockdown(1)"
                elif 41 <= d_percent <= 55:
                    debuff = "Knockdown(2), Slowed(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Knockdown(3), Slowed(5), Brone Broken(Shatter)"
                else:
                    debuff = "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost"

            elif (39 <= percent <= 43) and roll == 1:
                loc_name += ", Thigh"
                if d_percent <= 30:
                    debuff = "Slowed(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Slowed(3)"
                elif 51 <= d_percent <= 65:
                    debuff = "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost"

            elif (44 <= percent <= 45) and roll == 1:
                loc_name += ", Hip"
                if d_percent <= 25:
                    debuff = "Knockdown"
                elif 26 <= d_percent <= 40:
                    debuff = "Knockdown(1)"
                elif 41 <= d_percent <= 55:
                    debuff = "Knockdown(2), Slowed(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Knockdown(3), Slowed(5), Brone Broken(Shatter)"
                else:
                    debuff = "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost"

        elif 46 <= percent <= 60:
            armor = Leg
            loc_name += "Right Leg"

            if (46 <= percent <= 47) and roll == 1:
                loc_name += ", Foot"
                if d_percent <= 25:
                    debuff = "Slowed(2)"
                elif 26 <= d_percent <= 40:
                    debuff = "Slowed(3), Knockdown"
                elif 41 <= d_percent <= 55:
                    debuff = "Slowed(5), Knockdown(2), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Slowed(6), Knockdown Prone(2), Brone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Knockdown Prone(4), Foot Lost"

            elif (48 <= percent <= 53) and roll == 1:
                loc_name += ", Shin"
                if d_percent <= 30:
                    debuff = "Slowed(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Slowed(3)"
                elif 51 <= d_percent <= 65:
                    debuff = "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost"

            elif (percent == 54) and roll == 1:
                loc_name += ", Knee"
                if d_percent <= 25:
                    debuff = "Knockdown"
                elif 26 <= d_percent <= 40:
                    debuff = "Knockdown(1)"
                elif 41 <= d_percent <= 55:
                    debuff = "Knockdown(2), Slowed(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Knockdown(3), Slowed(5), Brone Broken(Shatter)"
                else:
                    debuff = "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost"

            elif (55 <= percent <= 58) and roll == 1:
                loc_name += ", Thigh"
                if d_percent <= 30:
                    debuff = "Slowed(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Slowed(3)"
                elif 51 <= d_percent <= 65:
                    debuff = "Slowed(5), Paralyzed(2), Bone Broken(Fracture)"
                elif 66 <= d_percent <= 80:
                    debuff = "Slowed(6), Paralyzed(3), Bone Broken(Shatter)"
                else:
                    debuff = "Slowed(10), Paralyzed(4), Looming Death(8), Leg Lost"

            elif (59 <= percent <= 60) and roll == 1:
                loc_name += ", Hip"
                if d_percent <= 25:
                    debuff = "Knockdown"
                elif 26 <= d_percent <= 40:
                    debuff = "Knockdown(1)"
                elif 41 <= d_percent <= 55:
                    debuff = "Knockdown(2), Slowed(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Knockdown(3), Slowed(5), Brone Broken(Shatter)"
                else:
                    debuff = "Knockdown(10), Slowed(10),Looming Death(8), Leg Lost"

        else:
            armor = Chest
            loc_name += "Chest"

            if (61 <= percent <= 65) and roll == 1:
                loc_name += ", Pelvis"
                if d_percent <= 25:
                    debuff = "Slowed(2)"
                elif 26 <= d_percent <= 40:
                    debuff = "Slowed(3), Tattered(2)"
                elif 41 <= d_percent <= 55:
                    debuff = "Slowed(4), Tattered(3), Brone Broken(Fracture)"
                elif 56 <= d_percent <= 70:
                    debuff = "Slowed(5), Tattered(4), Brone Broken(Shatter)"
                else:
                    debuff = "Slowed(permanent), Tattered(20), Brone Broken(Shatter)"

            elif (66 <= percent <= 72) and roll == 1:
                loc_name += ", Intestines"
                if d_percent <= 25:
                    debuff = "Tattered(2)"
                elif 26 <= d_percent <= 40:
                    debuff = "Tattered(3), Weakend(2)"
                elif 41 <= d_percent <= 50:
                    debuff = "Tattered(4), Weakend(4)"
                elif 51 <= d_percent <= 60:
                    debuff = "Tattered(5), Weakend(5), Looming Death(15)"
                else:
                    debuff = f"Tattered(6), Weakend(5), Looming Death({r.randint(1,10)})"

            elif (73 <= percent <= 78) and roll == 1:
                loc_name += ", Spine"
                if d_percent <= 25:
                    debuff = "Flinch(1), Drop, Knockdown"
                elif 26 <= d_percent <= 40:
                    debuff = "Flinch(2), Drop(2), Knockdown(1)"
                elif 41 <= d_percent <= 55:
                    debuff = "Paralyzed(2), Knockdown(3), Bone Broken(Fractured)"
                elif 56 <= d_percent <= 70:
                    debuff = "Paralyzed(5), Knockdown Prone(5), Bone Broken(Shattered)"
                else:
                    debuff = "Instant Death, Spine destroyed"

            elif (79 <= percent <= 84) and roll == 1:
                loc_name += ", Stomach, Kidney, or Liver"
                if d_percent <= 25:
                    debuff = "Gasping(1)"
                elif 26 <= d_percent <= 40:
                    debuff = "Gasping(2), Tattered(1)"
                elif 41 <= d_percent <= 50:
                    debuff = "Gasping(3), Tattered(2)"
                elif 51 <= d_percent <= 60:
                    debuff = "Gasping(4), Tattered(5), Looming Death(20)"
                else:
                    debuff = "Gasping(5), Tattered(6), Looming Death(10)"

            elif (85 <= percent <= 89) and roll == 1:
                loc_name += ", Heart"
                if d_percent <= 25:
                    debuff = "Winded(5)"
                elif 26 <= d_percent <= 40:
                    debuff = f"Winded(10), Concussed({r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10) + r.randint(1,10) + r.randint(1,10) + r.randint(1,10) + r.randint(1,10)})"
                elif 41 <= d_percent <= 50:
                    debuff = f"Winded(10), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10) + r.randint(1,10) + r.randint(1,10)})"
                elif 51 <= d_percent <= 60:
                    debuff = f"Winded(Permanent), Concussed({r.randint(1,5) + r.randint(1,5) + r.randint(1,5)}), Looming Death({r.randint(1,10)})"
                else:
                    debuff = "Heart destroyed, Instant Death"

            elif (90 <= percent <= 96) and roll == 1:
                loc_name += ", Lungs"
                if d_percent <= 25:
                    debuff = "Winded(2), Gasping(2)"
                elif 26 <= d_percent <= 40:
                    debuff = "Winded(3), Gasping(3)"
                elif 41 <= d_percent <= 50:
                    debuff = "Winded(4), Gasping(5), Looming Death(20)"
                elif 51 <= d_percent <= 60:
                    debuff = "Winded(5), Gasping(5), Looming Death(15)"
                else:
                    debuff = "Winded(6), Gasping(5), Choking"

            elif (97 <= percent <= 100) and roll == 1:
                loc_name += ", Ribcage, No Organ Struck"
                if d_percent <= 30:
                    debuff = "Winded(1), Gasping(1)"
                elif 31 <= d_percent <= 50:
                    debuff = "Winded(2), Gasping(1)"
                elif 51 <= d_percent <= 65:
                    debuff = "Winded(3), Gasping(2)"
                elif 66 <= d_percent <= 80:
                    debuff = "Winded(4), Gasping(4), Bone Broken(Fractured)"
                else:
                    debuff = "Winded(5), Gasping(4), Bone Broken(Shattered)"


    elif Enemy_Var == "vehicle":
        armor = V_Armor

    else:
        armor = 0

    return (armor, loc_name, debuff)

def attack(Type_Bonus, Range_Stat, Enemy_var, Attack_Var, Head, Arm, Leg, Chest, V_Armor, R_Added_Damage, R_D_Num, R_D_Size, toughness, R_Pierce, dice_min):
    roll = percentile_roll()
    Range_Stat += Type_Bonus
    DegressOfSuccess = 0
    Final_Damage = 0
    loc_name = "missed"
    debuff = ""


    if roll <= Range_Stat:
        DegressOfSuccess = (Range_Stat - roll) // 10
        loc_tup = location_roll(Enemy_var, roll, Head, Arm, Leg, Chest, V_Armor)
        armor = loc_tup[0]
        loc_name = loc_tup[1]
        debuff = loc_tup[2]

        damage = R_Added_Damage
        if (Enemy_var == "shield") and (JH.read("Preferences.json")["SpecialRules"]["Penetrating"]["Active"]):
            damage += R_Pierce * 3

        for dice in range(0,R_D_Num):
            if roll == 1:
                if JH.read("Preferences.json")["SpecialRules"]["HardLight"]["Active"]:
                    damage += R_D_Size + hardlight_dmg_roll(R_Added_Damage, R_D_Size, dice_min)

                else:
                    damage += R_D_Size

            else:
                if JH.read("Preferences.json")["SpecialRules"]["HardLight"]["Active"]:
                    damage += hardlight_dmg_roll(R_Added_Damage, R_D_Size, dice_min)

                else:
                    damage += r.randint(dice_min,R_D_Size)

        armor = max(0, armor - R_Pierce)
        if ("Head" in loc_name) and JH.read("Preferences.json")["SpecialRules"]["HeadShot"]["Active"]:
            Final_Damage = max(0, damage - armor)
        else:
            Final_Damage = max(0, damage - armor - toughness)

        if JH.read("Preferences.json")["SpecialRules"]["Assassination"]["Active"] and (Attack_Var == "melee"):
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
