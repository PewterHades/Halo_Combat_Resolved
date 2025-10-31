from tkinter import Tk, Frame, Widget, Toplevel, Label, Entry, Radiobutton, Button, Scale, StringVar, IntVar, END
from tkinter.ttk import Combobox
from tkextrafont import Font
from Functions import calulate
from Display_Manager import ThemeManager, create_tooltip
import Json_Handling as JH
import Json_Maps as JM


class Main_Page(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        Attack_Type = StringVar(value = "ranged")
        Enemy_Type = StringVar(value = "enemy")
        Fire_Mode = StringVar(value = "auto")
        Melee_Mode = StringVar(value = "single")
        self.vcmd = (self.register(lambda P: P.isdigit() or P == ""), "%P")
        self.theme = ThemeManager(master)

        self.enemy_agility = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyagility"))
        self.enemy_debuff = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemydebuff"))
        self.vehicle_agility = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclemanuverability"))
        self.vehicle_debuff = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehicledebuff"))
        self.weapon_rounds = IntVar( value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "roundsinweapon"))

        def Swap_Left_Canvas():
            choice = Attack_Type.get()

            for canvases in L_canvases.values():
                canvases.grid_forget()

            L_canvases[choice].grid(row = 0, column = 0, columnspan = 3)

        def Swap_Right_Canvas():
            choice = Enemy_Type.get()

            for canvases in R_canvases.values():
                canvases.grid_forget()

            R_canvases[choice].grid(row = 0, column = 0, columnspan = 3)


        Title = Label(self, text = "Halo: Combat Resolved", font = self.theme.Title_Font_Size).grid(row = 0, column = 0, columnspan = 3, pady = self.theme.Title_PadY_Size, sticky = "")

        Left_label = Label(self, text = "Your Stats", font = self.theme.SubTitle_Font_Size).grid(row = 1, column = 0, pady = self.theme.SubTitle_PadY_Size)

        Right_label = Label(self, text = "Enemy Stats", font = self.theme.SubTitle_Font_Size).grid(row = 1, column = 2, pady = self.theme.SubTitle_PadY_Size)



        Left_container = Frame(self)
        Left_container.columnconfigure(0, weight=1)
        Left_container.columnconfigure(1, weight=1)
        Left_container.grid(row = 2, column = 0)


        Ranged_LButton = Radiobutton(Left_container, text = "Ranged", variable = Attack_Type, value = "ranged", command = Swap_Left_Canvas, font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        Ranged_LButton.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(Ranged_LButton, "Choose the weapon type")

        Melee_LButton = Radiobutton(Left_container, text = "Melee", variable = Attack_Type, value = "melee", command = Swap_Left_Canvas, font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        Melee_LButton.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        create_tooltip(Melee_LButton, "Choose the weapon type")

        Left_canvas_Frame = Frame(Left_container)
        Left_canvas_Frame.rowconfigure(0, weight=1)
        Left_canvas_Frame.columnconfigure(0, weight=1)
        Left_canvas_Frame.grid(row = 1, column = 0, columnspan = 2)


        Ranged_Canvas = Frame(Left_canvas_Frame)

        R_Auto_RB = Radiobutton(Ranged_Canvas, text = "Auto Fire", variable = Fire_Mode, value = "auto", font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        R_Auto_RB.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Auto_RB, "Requirement: Weapon has the option for Auto Fire\nModifier: No modifier")

        R_Brust_RB = Radiobutton(Ranged_Canvas, text = "Burst Fire", variable = Fire_Mode, value = "burst", font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        R_Brust_RB.grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Brust_RB, "Requirement: Weapon has the option for Burst Fire\nModifier: roll one attack but all shots roll their own damage, +5 to Ranged Warfare")

        R_SemiAuto_RB = Radiobutton(Ranged_Canvas, text = "Semi Auto Fire", variable = Fire_Mode, value = "semiauto", font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        R_SemiAuto_RB.grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_SemiAuto_RB, "Requirement: Weapon has the option for Semi Automatic Fire\nModifier +10 to Ranged Warfare")


        R_Stat_L = Label(Ranged_Canvas, text = "Ranged Warfare", font = self.theme.Text_Font_Size)
        R_Stat_L.grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Stat_L, "Insert your Ranged Warframe stat without the buff from the Fire Type or Distance")
        R_Stat_E = Entry(Ranged_Canvas, name = "rangedwarfare", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedwarfare")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Stat_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)

        R_Shot_L = Label(Ranged_Canvas, text = "Number of Shots", font = self.theme.Text_Font_Size)
        R_Shot_L.grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Shot_L, "Insert the number of shots your weapon will fire for the respective Fire Type")
        R_Shot_E = Entry(Ranged_Canvas, name = "rangednumberofshots", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangednumberofshots")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Shot_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)

        R_Num_L = Label(Ranged_Canvas, text = "Number of Dice", font = self.theme.Text_Font_Size)
        R_Num_L.grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Num_L, "Insert the number of damage dice for one shot")
        R_Num_E = Entry(Ranged_Canvas, name = "rangednumberofdice", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangednumberofdice")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Num_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)

        R_Size_L = Label(Ranged_Canvas, text = "Size of Dice", font = self.theme.Text_Font_Size)
        R_Size_L.grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Size_L, "Insert the number of sides for you damage dice")
        R_Size_E = Entry(Ranged_Canvas, name = "rangedsizeofdice", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedsizeofdice")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Size_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)

        R_AddD_L = Label(Ranged_Canvas, text = "Added Damage", font = self.theme.Text_Font_Size)
        R_AddD_L.grid(row = 7, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_AddD_L, "Insert the flat damage increase for one shot")
        R_AddD_E = Entry(Ranged_Canvas, name = "rangedaddeddamage", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedaddeddamage")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_AddD_E.grid(row = 7, column = 1, pady = self.theme.Text_PadY_Size)

        R_Pierce_L = Label(Ranged_Canvas, text = "Pierce", font = self.theme.Text_Font_Size)
        R_Pierce_L.grid(row = 8, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Pierce_L,"Insert the Pierce value for the gun without Distance modifiers")
        R_Pierce_E = Entry(Ranged_Canvas, name = "rangedpierce", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "rangedpierce")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Pierce_E.grid(row = 8, column = 1, pady = self.theme.Text_PadY_Size)

        R_Rounds_L = Label(Ranged_Canvas, text = "Rounds in Weapon", font = self.theme.Text_Font_Size)
        R_Rounds_L.grid(row = 9, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(R_Rounds_L, "Insert the number of rounds in you gun, this will go down as you shoot and will not let you shoot if it is at zero")
        R_Rounds_E = Entry(Ranged_Canvas, name = "roundsinweapon", textvariable = self.weapon_rounds, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        R_Rounds_E.grid(row = 9, column = 1, pady = self.theme.Text_PadY_Size)

        R_Dist_S = Scale(Ranged_Canvas, from_ = 0, to = 4, orient = "horizontal", label = "Distance", font = self.theme.Text_Font_Size, showvalue = 0, troughcolor = self.theme.green)
        R_Dist_S.grid(row = 10, column = 0, pady = self.theme.Text_PadY_Size, sticky = "nsew")
        create_tooltip(R_Dist_S, "Choose the Distance you are firing from")
        R_Dist_S.set(2)
        R_Dist_Ranges = ["Point Blank", "Close", "Normal", "Long", "Extreme"]
        R_Dist_L = Label(Ranged_Canvas, text = R_Dist_Ranges[2], font = self.theme.Text_Font_Size)
        R_Dist_L.grid(row = 10, column = 1, pady = self.theme.Text_PadY_Size)
        self.slider_vars(R_Dist_L, R_Dist_S, R_Dist_Ranges)
        create_tooltip(R_Dist_L, "Point Blank:\nRequirement: Within 3 meters, Modifier: +20 to Ranged Warfare\nClose:\nRequirement: Between 3 meters and lower range increment, Modifier: +10 to Ranged Warfare\nNormal:\nRequirement: Between min and max values of range increment, Modifier: No modifier\nLong:\nRequirement: Between 1x and 2x your max range increment, Modifier: -40 to Ranged Warfare and Pierce is halved\nExteme:\nRequirement: 2x to 3x your max range increment, Modifier: -80 to Ranged Warfare and no Pierce")



        Melee_Canvas = Frame(Left_canvas_Frame)

        M_Single_RB = Radiobutton(Melee_Canvas, text = "Single Strike", variable = Melee_Mode, value = "single", font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        M_Single_RB.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Single_RB, "Choose what Strike type you intend to use")

        M_Brust_RB = Radiobutton(Melee_Canvas, text = "Burst Strike", variable = Melee_Mode, value = "burst", font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        M_Brust_RB.grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Brust_RB, "Choose what Strike type you intend to use")


        M_Stat_L = Label(Melee_Canvas, text = "Melee Warfare", font = self.theme.Text_Font_Size)
        M_Stat_L.grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Stat_L, "Insert your Melee Warframe stat without the buff from Distance")
        M_Stat_E = Entry(Melee_Canvas, name = "meleewarfare", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleewarfare")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_Stat_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size) 

        M_Strikes_L = Label(Melee_Canvas, text = "Melee Strikes", font = self.theme.Text_Font_Size)
        M_Strikes_L.grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Strikes_L, "Inster number of strikes you will make (Only change if on \"Burst Melee\")")
        M_Strikes_E = Entry(Melee_Canvas, name = "meleestrikes", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleestrikes")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_Strikes_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)

        M_Num_L = Label(Melee_Canvas, text = "Number of Dice", font = self.theme.Text_Font_Size)
        M_Num_L.grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Num_L, "Insert the number of damage dice for one melee strike")
        M_Num_E = Entry(Melee_Canvas, name = "meleenumberofdice", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleenumberofdice")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_Num_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)

        M_Size_L = Label(Melee_Canvas, text = "Size of Dice", font = self.theme.Text_Font_Size)
        M_Size_L.grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Size_L, "Insert the number of sides for you damage dice")
        M_Size_E = Entry(Melee_Canvas, name = "meleesizeofdice", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleesizeofdice")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_Size_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)

        M_AddD_L = Label(Melee_Canvas, text = "Added Damage", font = self.theme.Text_Font_Size)
        M_AddD_L.grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_AddD_L, "Insert the flat damage increase for one melee attack")
        M_AddD_E = Entry(Melee_Canvas, name = "meleeaddeddamage", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleeaddeddamage")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_AddD_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)

        M_Pierce_L = Label(Melee_Canvas, text = "Pierce", font = self.theme.Text_Font_Size)
        M_Pierce_L.grid(row = 7, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(M_Pierce_L, "Insert the Pierce value for the gun")
        M_Pierce_E = Entry(Melee_Canvas, name = "meleepierce", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "meleepierce")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        M_Pierce_E.grid(row = 7, column = 1, pady = self.theme.Text_PadY_Size)

        M_Dist_S = Scale(Melee_Canvas, from_ = 0, to = 1, orient = "horizontal", label = "Distance", font = self.theme.Text_Font_Size, showvalue = 0, troughcolor = self.theme.green)
        M_Dist_S.grid(row = 10, column = 0, pady = self.theme.Text_PadY_Size, sticky = "nsew")
        create_tooltip(M_Dist_S, "Choose the Distance you are striking from")
        M_Dist_S.set(2)
        M_Dist_Ranges = ["Point Blank", "Normal"]
        M_Dist_R_TT = ["Requirment: Within 3 meters\nModifiers: +10 to attack roll","no modifiers"]
        M_Dist_L = Label(Melee_Canvas, text = M_Dist_Ranges[1], font = self.theme.Text_Font_Size)
        M_Dist_L.grid(row = 10, column = 1, pady = self.theme.Text_PadY_Size)
        M_Dist_TT_Current = StringVar(value = M_Dist_R_TT[1])
        self.slider_vars(M_Dist_L, M_Dist_S, M_Dist_Ranges, M_Dist_R_TT, M_Dist_TT_Current)
        create_tooltip(M_Dist_L, "Point Blank:\nRequirment: Within 3 meters, Modifiers: +10 to Melee Warfare\nNormal:\nRequirement: Between 3 meters and melee range, Modifier: No Modifier")


        L_canvases = {"ranged": Ranged_Canvas,"melee": Melee_Canvas}



        Right_container = Frame(self)
        Right_container.columnconfigure(0, weight=1)
        Right_container.columnconfigure(1, weight=1)
        Right_container.grid(row = 2, column = 2)

        Enemy_RButton = Radiobutton(Right_container, text = "Enemy", variable = Enemy_Type, value = "enemy", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        Enemy_RButton.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(Enemy_RButton, "Choose the Enemy Type you are attacking")

        Shield_RButton = Radiobutton(Right_container, text = "Shield", variable = Enemy_Type, value = "shield", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        Shield_RButton.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        create_tooltip(Shield_RButton, "Choose the Enemy Type you are attacking")

        Vehicle_RButton = Radiobutton(Right_container, text = "Vehicle", variable = Enemy_Type, value = "vehicle", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size, indicatoron = 0, selectcolor = self.theme.green)
        Vehicle_RButton.grid(row = 0, column = 2, pady = self.theme.Text_PadY_Size)
        create_tooltip(Vehicle_RButton, "Choose the Enemy Type you are attacking")

        Right_canvas_Frame = Frame(Right_container)
        Right_canvas_Frame.rowconfigure(0, weight=1)
        Right_canvas_Frame.columnconfigure(0, weight=1)
        Right_canvas_Frame.grid(row = 1, column = 0, columnspan = 3)


        Enemy_Canvas = Frame(Right_canvas_Frame)

        E_A_Head_L = Label(Enemy_Canvas, text = "Head Armor", font = self.theme.Text_Font_Size)
        E_A_Head_L.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_A_Head_L, "Input the Armor value for the enemies head")
        E_A_Head_E = Entry(Enemy_Canvas, name = "enemyahead", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyahead")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_A_Head_E.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)

        E_A_Arm_L = Label(Enemy_Canvas, text = "Arm Armor", font = self.theme.Text_Font_Size)
        E_A_Arm_L.grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_A_Arm_L, "Input the Armor value for the enemies arm")
        E_A_Arm_E = Entry(Enemy_Canvas, name = "enemyaarm", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyaarm")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_A_Arm_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)

        E_A_Chest_L = Label(Enemy_Canvas, text = "Chest Armor", font = self.theme.Text_Font_Size)
        E_A_Chest_L.grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_A_Chest_L, "Input the Armor value for the enemies chest")
        E_A_Chest_E = Entry(Enemy_Canvas, name = "enemyachest", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyachest")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_A_Chest_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size)

        E_A_Leg_L = Label(Enemy_Canvas, text = "Leg Armor", font = self.theme.Text_Font_Size)
        E_A_Leg_L.grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_A_Leg_L, "Input the Armor value for the enemies leg")
        E_A_Leg_E = Entry(Enemy_Canvas, name = "enemyaleg", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyaleg")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_A_Leg_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)

        E_Stat_L = Label(Enemy_Canvas, text = "Agility", font = self.theme.Text_Font_Size)
        E_Stat_L.grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_Stat_L, "Input the enemies current Agility value")
        E_Agility_E = Entry(Enemy_Canvas, name = "enemyagility", textvariable = self.enemy_agility, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_Agility_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)

        E_Debuff_L = Label(Enemy_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size)
        E_Debuff_L.grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_Debuff_L, "Input the number of times the enemy can negate the Agility debuff from dodging or parrying")
        E_A_Debuff_E = Entry(Enemy_Canvas, name = "enemydebuff", textvariable = self.enemy_debuff, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_A_Debuff_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)

        E_Toughness_L = Label(Enemy_Canvas, text = "Toughness Modifier", font = self.theme.Text_Font_Size)
        E_Toughness_L.grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(E_Toughness_L, "Input the enemies Toughness modifier")
        E_Toughness_E = Entry(Enemy_Canvas, name = "enemytoughness", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemytoughness")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        E_Toughness_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)


        Shield_Canvas = Frame(Right_canvas_Frame)

        S_Stat_L = Label(Shield_Canvas, text = "Agility", font = self.theme.Text_Font_Size)
        S_Stat_L.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(S_Stat_L, "Input the enemies current Agility value")
        S_Agility_E = Entry(Shield_Canvas, textvariable = self.enemy_agility, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        S_Agility_E.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)

        S_Debuff_L = Label(Shield_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size)
        S_Debuff_L.grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(S_Debuff_L, "Input the number of times the enemy can negate the Agility debuff from dodging or parrying")
        S_A_Debuff_E = Entry(Shield_Canvas, textvariable = self.enemy_debuff, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        S_A_Debuff_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)


        Vehicle_Canvas = Frame(Right_canvas_Frame)

        V_Armor_L = Label(Vehicle_Canvas, text = "Armor", font = self.theme.Text_Font_Size)
        V_Armor_L.grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(V_Armor_L, "Chose the location you are attacking and the armor value of that part")
        V_Armor_Loc_list = ["Front", "Back", "Side", "Top", "Bottom"]
        V_Armor_CB = Combobox(Vehicle_Canvas,name = "vehiclehitlocation", values = V_Armor_Loc_list, font = self.theme.Text_Font_Size)
        V_Armor_CB.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        V_Armor_CB.current(V_Armor_Loc_list.index(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclehitlocation")))
        V_Armor_CB.bind("<Button-1>", lambda event: event.widget.focus_set())
        self.V_Armor_E = Entry(Vehicle_Canvas, name = "vehiclearmor", textvariable = IntVar(value = JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"][JH.read("Saved_Stats.json")["YourStats"]["VehicleHitLocation"]]), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        self.V_Armor_E.grid(row = 0, column = 2, pady = self.theme.Text_PadY_Size)

        V_Stat_L = Label(Vehicle_Canvas, text = "Manuverability", font = self.theme.Text_Font_Size)
        V_Stat_L.grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(V_Stat_L, "Input the vehicles current Manuverability value")
        V_Agility_E = Entry(Vehicle_Canvas, name = "vehiclemanuverability", textvariable = self.vehicle_agility, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        V_Agility_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)

        V_Debuff_L = Label(Vehicle_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size)
        V_Debuff_L.grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(V_Debuff_L, "Input the number of times the vehicle can negate the Agility debuff from dodging or parrying")
        V_A_Debuff_E = Entry(Vehicle_Canvas, name = "vehicledebuff", textvariable = self.vehicle_debuff, validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        V_A_Debuff_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size)

        V_Toughness_L = Label(Vehicle_Canvas, text = "Toughness Modifier", font = self.theme.Text_Font_Size)
        V_Toughness_L.grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        create_tooltip(V_Toughness_L, "Input the vehicles Toughness modifier")
        V_Toughness_E = Entry(Vehicle_Canvas, name = "vehicletoughness", textvariable = IntVar(value = JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehicletoughness")), validate = "key", validatecommand = self.vcmd, font = self.theme.Text_Font_Size)
        V_Toughness_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)

        R_canvases = {"enemy": Enemy_Canvas,"shield": Shield_Canvas,"vehicle": Vehicle_Canvas}



        root = self.winfo_toplevel()
        root.bind("<<ToplevelClosed>>", self.update_entries)
        Swap_Left_Canvas()
        Swap_Right_Canvas()
        self.all_entry_focus(self)
        self.theme.change_theme(self)
        
        Calculate_B = Button(self, text = "Calculate", command = lambda:[
            calulate(str(Attack_Type.get()), str(Enemy_Type.get()), str(Fire_Mode.get()), str(Melee_Mode.get()), str(R_Dist_L.cget("text")), str(M_Dist_L.cget("text")), root),],
            font = self.theme.Text_Font_Size).grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        
        Settings_B = Button(self, text = "Settings", command = self.open_settings, font = self.theme.Text_Font_Size).grid(row = 3, column = 2, pady = self.theme.Text_PadY_Size)

        Special_Rules_B = Button(self, text = "Weapon Special Rules", command = self.open_special_rules, font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)

        self.theme.change_theme(self)


    def on_focus_in(self, event):
        if event.widget.get() == "0":
            event.widget.delete(0, "end")

    def on_focus_out(self, event):
        try:    
            json_val = int(event.widget.get())
        except ValueError:
            json_val = str(event.widget.get())
            
        if str(event.widget).split(".")[-1] == "vehiclehitlocation":
            JH.set_json_val("Saved_Stats.json", JM.Entry_map, json_val, event.widget)
            self.V_Armor_E.delete(0, END)
            self.V_Armor_E.insert(0, JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"][JH.read("Saved_Stats.json")["YourStats"]["VehicleHitLocation"]])
            if self.V_Armor_E.get().strip() == "":
                self.V_Armor_E.insert(0, "0")
            if JH.read("Saved_Stats.json")["EnemyStats"]["Vehicle"]["Armor"][JH.read("Saved_Stats.json")["YourStats"]["VehicleHitLocation"]] == 0:
                if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode"):
                    self.V_Armor_E.config(bg = self.theme.modes["Dark"]["bg"])
                else:
                    self.V_Armor_E.config(bg = self.theme.modes["Light"]["bg"])
            else:
                self.V_Armor_E.config(bg = self.theme.green)
        else:
            JH.set_json_val("Saved_Stats.json", JM.Entry_map, json_val, event.widget)


        if event.widget.get().strip() == "":
            event.widget.insert(0, "0")
        elif event.widget.get().strip() == "0":
            if not isinstance(event.widget, Combobox):
                if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode"):
                    event.widget.config(bg = self.theme.modes["Dark"]["bg"])
                else:
                    event.widget.config(bg = self.theme.modes["Light"]["bg"])
        else:
            if not isinstance(event.widget, Combobox):
                event.widget.config(bg = self.theme.green)
        
    def on_focus(self, entry):
        entry.bind("<FocusIn>", self.on_focus_in)
        entry.bind("<FocusOut>", self.on_focus_out)  

    def all_entry_focus(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, Entry) and not isinstance(child, Combobox):
                self.on_focus(child)
            elif isinstance(child, Combobox):
                self.on_focus(child)

            if child.winfo_children():
                self.all_entry_focus(child)     

    def slider_vars(self, lab, slide, variables, tooltips = None, sel_tt= None):
        def update_label(*args):
            value = int(slide.get())
            lab.configure(text = variables[value])
            if tooltips and sel_tt:
                sel_tt.set(tooltips[value])
        slide.config(command = update_label)
        
    def open_settings(self):
        Settings = Toplevel(self)
        Settings.wm_title("Settings")
        Settings.geometry("400x225")
        Settings.rowconfigure(0, weight=1)
        Settings.columnconfigure(0, weight=1) 

        Set_Frame = Frame(Settings)
        Set_Frame.grid(row=0, column=0, sticky="nsew")
        theme = ThemeManager(Set_Frame)

        DarkMode_B = Button(Set_Frame, text = "Toggle Dark Mode", command = lambda: theme.global_theme_change(self, toggle = True), font = theme.Text_Font_Size)
        DarkMode_B.grid(row = 0, column = 0)
        DarkMode_L = Label(Set_Frame, text = "", font = theme.Text_Font_Size)
        DarkMode_L.grid(row = 0, column = 1)

        ToolTip_B = Button(Set_Frame, text = "Toggle Tooltips", command = lambda: JH.toggle_bool("Preferences.json", "Settings,ToolTips"), font = theme.Text_Font_Size)
        ToolTip_B.grid(row = 1, column = 0)
        ToolTip_L = Label(Set_Frame, text = "", font = theme.Text_Font_Size)
        ToolTip_L.grid(row = 1, column = 1)

        SaveReset_B = Button(Set_Frame, text = "Reset shown stats on program open", command = lambda: JH.toggle_bool("Preferences.json", "Settings,ResetEntriesOnOpen"), font = theme.Text_Font_Size)
        SaveReset_B.grid(row = 2, column = 0)
        SaveReset_L = Label(Set_Frame, text = "", font = theme.Text_Font_Size)
        SaveReset_L.grid(row = 2, column = 1)

        button_List = [DarkMode_B, ToolTip_B, SaveReset_B]
        label_map = {
            "Settings,DarkMode": DarkMode_L,
            "Settings,ToolTips": ToolTip_L,
            "Settings,ResetEntriesOnOpen": SaveReset_L
        }

        for button in button_List:
            button.bind('<ButtonRelease-1>', lambda event: Set_Frame.after(0, theme.bool_update_label, "Preferences.json", label_map), add=True)

        theme.bool_update_label("Preferences.json", label_map)
        theme.change_theme(self)

    def open_special_rules(self):
        SpecialR = Toplevel()
        SpecialR.wm_title("Weapon Special Rules")
        SpecialR.geometry("496x279")
        SpecialR.rowconfigure(0, weight=1)
        SpecialR.columnconfigure(0, weight=1) 

        Spec_Frame = Frame(SpecialR)
        Spec_Frame.pack(side = "right", fill = "both", expand = True)
        Spec_Frame.rowconfigure(0, weight=1)
        Spec_Frame.columnconfigure(0, weight=1) 
        theme = ThemeManager(Spec_Frame)

        def rule_toggle(widget1, widget2 = None):
            var = str(widget1.cget("text"))
            data = JH.read("Preferences.json")
            data["SpecialRules"][var]["Active"] = not data["SpecialRules"][var]["Active"]
            

            if data["SpecialRules"][var]["Active"]:
                widget1.config(bg = theme.green)
            else:
                if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode"):       
                    widget1.config(bg = self.theme.modes["Dark"]["bg"])
                else:
                    widget1.config(bg = self.theme.modes["Light"]["bg"])

            
            if widget2:
                val = 0
                if data["SpecialRules"][var]["Active"]:
                    val = int(widget2.get())
                else:
                    val = 0

                data["SpecialRules"][var]["Value"] = val

            JH.save("Preferences.json", data)

        Ranged_L = Label(Spec_Frame, text = "Ranged Rules", font = theme.Title_Font_Size)
        Ranged_L.grid(row = 0, column = 0, padx = theme.Title_PadX_Size, pady = theme.Title_PadY_Size)

        Melee_L = Label(Spec_Frame, text = "Melee Rules", font = theme.Title_Font_Size)
        Melee_L.grid(row = 0, column = 1, padx = theme.Title_PadX_Size, pady = theme.Title_PadY_Size)


        Ranged_Canvas = Frame(Spec_Frame)
        Ranged_Canvas.grid(row = 1, column = 0)
        Ranged_Canvas.columnconfigure(0, weight = 1)
        Ranged_Canvas.rowconfigure(0, weight = 1)

        Penetrating_B = Button(Ranged_Canvas, text = "Penetrating", font = theme.Text_Font_Size, relief = "raised")
        Penetrating_B.config(command = lambda PB = Penetrating_B: rule_toggle(PB), bg = theme.green if JH.get_json_val("Preferences.json", JM.Prefernce_map, "penetrating") else (self.theme.modes["Dark"]["bg"] if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else self.theme.modes["Light"]["bg"]))
        Penetrating_B.grid(row = 0, column = 0)
        create_tooltip(Penetrating_B, "If target is a shield, 3 times your Pierce will be added to damage per shot")

        DiceMin_B = Button(Ranged_Canvas, text = "DiceMinimum", font = theme.Text_Font_Size, relief = "raised")
        DiceMin_B.grid(row = 1, column = 0)
        DiceMin_E = Entry(Ranged_Canvas, textvariable = IntVar(value = JH.get_json_val("Preferences.json", JM.Prefernce_map, "diceminimumv")), validate = "key", validatecommand = self.vcmd, font = theme.Text_Font_Size)
        DiceMin_E.grid(row = 1, column = 1)
        DiceMin_B.config(command = lambda DMB = DiceMin_B, DME = DiceMin_E: rule_toggle(DMB, DME), bg = theme.green if JH.get_json_val("Preferences.json", JM.Prefernce_map, "diceminimuma") else (self.theme.modes["Dark"]["bg"] if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else self.theme.modes["Light"]["bg"]))
        create_tooltip(DiceMin_B, "Sets the minumum value of your dice roll for damage. (Insert value before pressing button)")

        HardLight_B = Button(Ranged_Canvas, text = "HardLight", font = theme.Text_Font_Size, relief = "raised")
        HardLight_B.config(command = lambda HLB = HardLight_B: rule_toggle(HLB), bg = theme.green if JH.get_json_val("Preferences.json", JM.Prefernce_map, "hardlight") else (self.theme.modes["Dark"]["bg"] if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else self.theme.modes["Light"]["bg"]))
        HardLight_B.grid(row = 2, column = 0)
        create_tooltip(HardLight_B, "Adds extra damage dice for each dice that rolls max damage")

        HeadShot_B = Button(Ranged_Canvas, text = "HeadShot", font = theme.Text_Font_Size, relief = "raised")
        HeadShot_B.config(command = lambda HSB = HeadShot_B: rule_toggle(HSB), bg = theme.green if JH.get_json_val("Preferences.json", JM.Prefernce_map, "headshot") else (self.theme.modes["Dark"]["bg"] if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else self.theme.modes["Light"]["bg"]))
        HeadShot_B.grid(row = 3, column = 0)
        create_tooltip(HeadShot_B, "If you hit the head, the enemies Toughness modifier will be ignored")


        Melee_Canvas = Frame(Spec_Frame)
        Melee_Canvas.grid(row = 1, column = 1, )
        Melee_Canvas.columnconfigure(0, weight = 1)
        Melee_Canvas.rowconfigure(0, weight = 1)

        Assassination_B = Button(Melee_Canvas, text = "Assassination", font = theme.Text_Font_Size, relief = "raised")
        Assassination_B.config(command = lambda AB = Assassination_B: rule_toggle(AB), bg = theme.green if JH.get_json_val("Preferences.json", JM.Prefernce_map, "assassination") else (self.theme.modes["Dark"]["bg"] if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else self.theme.modes["Light"]["bg"]))
        Assassination_B.grid(row = 2, column = 0)
        create_tooltip(Assassination_B, "All dice roll max damage and total damage will be multiplied by 4")

        self.theme.change_theme(SpecialR)

    def update_entries(self, event = None):
        self.enemy_agility.set(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemyagility"))
        self.enemy_debuff.set(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "enemydebuff"))
        self.vehicle_agility.set(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehiclemanuverability"))
        self.vehicle_debuff.set(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "vehicledebuff"))
        self.weapon_rounds.set(JH.get_json_val("Saved_Stats.json", JM.Entry_map, "roundsinweapon"))

root = Tk()
root.wm_title("Halo: Combat Resolved")
root.geometry("1008x567")
root.bind_all("<Button-1>", lambda event: event.widget.focus_set() if isinstance(event.widget, Widget) and event.widget.winfo_class() != 'TCombobox' else None)



halo_font = Font(file = "Fonts/Halo.ttf")
assert halo_font.is_font_available('Halo')
assert 'Halo' in halo_font.loaded_fonts()

if JH.get_json_val("Preferences.json", JM.Prefernce_map, "resetentries"):
    JH.reset_vals("Saved_Stats.json")


page_container = Frame(root)
page_container.pack(side = "right", fill = "both", expand = True)
page_container.rowconfigure(0, weight = 1)
page_container.columnconfigure(0, weight = 1)

main_page = Main_Page(page_container)
main_page.grid(row = 0, column = 0, sticky = "nsew")
main_page.tkraise()


root.mainloop()