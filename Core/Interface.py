from tkinter import Tk, Frame, Canvas, Label, Entry, Radiobutton, Button, StringVar, IntVar
from Functions import calulate, instructions
from Display_Manager import ThemeManager

class Main_Page(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight = 1)
        Attack_Type = StringVar(value = "ranged")
        Enemy_Type = StringVar(value = "enemy")
        Fire_Mode = StringVar(value = "auto")
        Melee_Mode = StringVar(value = "single")
        self.Rounds = IntVar(value = 0)
        vcmd = (self.register(lambda P: P.isdigit() or P == ""), "%P")
        self.theme = ThemeManager(master)


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


        Title = Label(self, text = "Halo Combat Program", font = self.theme.Title_Font_Size).grid(row = 0, column = 1,pady = self.theme.Title_PadY_Size)

        Left_label = Label(self, text = "Your Stats", font = self.theme.SubTitle_Font_Size).grid(row = 1, column = 0, pady = self.theme.SubTitle_PadY_Size)

        Right_label = Label(self, text = "Enemy Stats", font = self.theme.SubTitle_Font_Size).grid(row = 1, column = 2, pady = self.theme.SubTitle_PadY_Size)



        Left_container = Frame(self)
        Left_container.columnconfigure(0, weight=1)
        Left_container.columnconfigure(1, weight=1)
        Left_container.grid(row = 2, column = 0)


        Ranged_LButton = Radiobutton(Left_container, text = "Ranged", variable = Attack_Type, value = "ranged", command = Swap_Left_Canvas, font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)

        Melee_LButton = Radiobutton(Left_container, text = "Melee", variable = Attack_Type, value = "melee", command = Swap_Left_Canvas, font = self.theme.Text_Font_Size).grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)

        Left_canvas_Frame = Frame(Left_container)
        Left_canvas_Frame.rowconfigure(0, weight=1)
        Left_canvas_Frame.columnconfigure(0, weight=1)
        Left_canvas_Frame.grid(row = 1, column = 0, columnspan = 2)


        Ranged_Canvas = Canvas(Left_canvas_Frame)

        R_Auto_RB = Radiobutton(Ranged_Canvas, text = "Auto Fire", variable = Fire_Mode, value = "auto", font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)

        R_Brust_RB = Radiobutton(Ranged_Canvas, text = "Burst Fire", variable = Fire_Mode, value = "burst", font = self.theme.Text_Font_Size).grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)

        R_SemiAuto_RB = Radiobutton(Ranged_Canvas, text = "Semi Auto Fire", variable = Fire_Mode, value = "semiauto", font = self.theme.Text_Font_Size).grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)


        R_Stat_L = Label(Ranged_Canvas, text = "Ranged Warfare", font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        R_Stat_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Stat_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        R_Stat_E.bind("<FocusIn>", self.on_focus_in)
        R_Stat_E.bind("<FocusOut>", self.on_focus_out)

        R_Shot_L = Label(Ranged_Canvas, text = "Number of Shots", font = self.theme.Text_Font_Size).grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        R_Shot_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Shot_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)
        R_Shot_E.bind("<FocusIn>", self.on_focus_in)
        R_Shot_E.bind("<FocusOut>", self.on_focus_out)

        R_Num_L = Label(Ranged_Canvas, text = "Number of Dice", font = self.theme.Text_Font_Size).grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        R_Num_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Num_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)
        R_Num_E.bind("<FocusIn>", self.on_focus_in)
        R_Num_E.bind("<FocusOut>", self.on_focus_out)

        R_Size_L = Label(Ranged_Canvas, text = "Size of Dice", font = self.theme.Text_Font_Size).grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        R_Size_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Size_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)
        R_Size_E.bind("<FocusIn>", self.on_focus_in)
        R_Size_E.bind("<FocusOut>", self.on_focus_out)

        R_AddD_L = Label(Ranged_Canvas, text = "Added Damage", font = self.theme.Text_Font_Size).grid(row = 7, column = 0, pady = self.theme.Text_PadY_Size)
        R_AddD_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_AddD_E.grid(row = 7, column = 1, pady = self.theme.Text_PadY_Size)
        R_AddD_E.bind("<FocusIn>", self.on_focus_in)
        R_AddD_E.bind("<FocusOut>", self.on_focus_out)

        R_Pierce_L = Label(Ranged_Canvas, text = "Pierce", font = self.theme.Text_Font_Size).grid(row = 8, column = 0, pady = self.theme.Text_PadY_Size)
        R_Pierce_E = Entry(Ranged_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Pierce_E.grid(row = 8, column = 1, pady = self.theme.Text_PadY_Size)
        R_Pierce_E.bind("<FocusIn>", self.on_focus_in)
        R_Pierce_E.bind("<FocusOut>", self.on_focus_out)

        R_Rounds_L = Label(Ranged_Canvas, text = "Rounds in Weapon", font = self.theme.Text_Font_Size).grid(row = 9, column = 0, pady = self.theme.Text_PadY_Size)
        R_Rounds_E = Entry(Ranged_Canvas, textvariable = self.Rounds, validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        R_Rounds_E.grid(row = 9, column = 1, pady = self.theme.Text_PadY_Size)
        R_Rounds_E.bind("<FocusIn>", self.on_focus_in)
        R_Rounds_E.bind("<FocusOut>", self.on_focus_out)


        Melee_Canvas = Frame(Left_canvas_Frame)

        M_Single_RB = Radiobutton(Melee_Canvas, text = "Single Strike", variable = Melee_Mode, value = "single", font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)

        M_Brust_RB = Radiobutton(Melee_Canvas, text = "Burst Strike", variable = Melee_Mode, value = "burst", font = self.theme.Text_Font_Size).grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)


        M_Stat_L = Label(Melee_Canvas, text = "Melee Warfare", font = self.theme.Text_Font_Size).grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        M_Stat_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_Stat_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size)
        M_Stat_E.bind("<FocusIn>", self.on_focus_in)
        M_Stat_E.bind("<FocusOut>", self.on_focus_out)  

        M_Strikes_L = Label(Melee_Canvas, text = "Melee Strikes", font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        M_Strikes_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_Strikes_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        M_Strikes_E.bind("<FocusIn>", self.on_focus_in)
        M_Strikes_E.bind("<FocusOut>", self.on_focus_out)  

        M_Num_L = Label(Melee_Canvas, text = "Number of Dice", font = self.theme.Text_Font_Size).grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        M_Num_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_Num_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)
        M_Num_E.bind("<FocusIn>", self.on_focus_in)
        M_Num_E.bind("<FocusOut>", self.on_focus_out)

        M_Size_L = Label(Melee_Canvas, text = "Size of Dice", font = self.theme.Text_Font_Size).grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        M_Size_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_Size_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)
        M_Size_E.bind("<FocusIn>", self.on_focus_in)
        M_Size_E.bind("<FocusOut>", self.on_focus_out)

        M_AddD_L = Label(Melee_Canvas, text = "Added Damage", font = self.theme.Text_Font_Size).grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        M_AddD_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_AddD_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)
        M_AddD_E.bind("<FocusIn>", self.on_focus_in)
        M_AddD_E.bind("<FocusOut>", self.on_focus_out)

        M_Pierce_L = Label(Melee_Canvas, text = "Pierce", font = self.theme.Text_Font_Size).grid(row = 7, column = 0, pady = self.theme.Text_PadY_Size)
        M_Pierce_E = Entry(Melee_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        M_Pierce_E.grid(row = 7, column = 1, pady = self.theme.Text_PadY_Size)        
        M_Pierce_E.bind("<FocusIn>", self.on_focus_in)
        M_Pierce_E.bind("<FocusOut>", self.on_focus_out)

        L_canvases = {"ranged": Ranged_Canvas,"melee": Melee_Canvas}



        Right_container = Frame(self)
        Right_container.columnconfigure(0, weight=1)
        Right_container.columnconfigure(1, weight=1)
        Right_container.grid(row = 2, column = 2)

        Enemy_RButton = Radiobutton(Right_container, text = "Enemy", variable = Enemy_Type, value = "enemy", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)

        Shield_RButton = Radiobutton(Right_container, text = "Shield", variable = Enemy_Type, value = "shield", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size).grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)

        Vehicle_RButton = Radiobutton(Right_container, text = "Vehicle", variable = Enemy_Type, value = "vehicle", command = Swap_Right_Canvas, font = self.theme.Text_Font_Size).grid(row = 0, column = 2, pady = self.theme.Text_PadY_Size)

        Right_canvas_Frame = Frame(Right_container)
        Right_canvas_Frame.rowconfigure(0, weight=1)
        Right_canvas_Frame.columnconfigure(0, weight=1)
        Right_canvas_Frame.grid(row = 1, column = 0, columnspan = 3)


        Enemy_Canvas = Frame(Right_canvas_Frame)

        E_A_Head_L = Label(Enemy_Canvas, text = "Head Armor", font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        E_A_Head_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_A_Head_E.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        E_A_Head_E.bind("<FocusIn>", self.on_focus_in)
        E_A_Head_E.bind("<FocusOut>", self.on_focus_out)

        E_A_Arm_L = Label(Enemy_Canvas, text = "Arm Armor", font = self.theme.Text_Font_Size).grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        E_A_Arm_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_A_Arm_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)
        E_A_Arm_E.bind("<FocusIn>", self.on_focus_in)
        E_A_Arm_E.bind("<FocusOut>", self.on_focus_out)

        E_A_Chest_L = Label(Enemy_Canvas, text = "Chest Armor", font = self.theme.Text_Font_Size).grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        E_A_Chest_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_A_Chest_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size)
        E_A_Chest_E.bind("<FocusIn>", self.on_focus_in)
        E_A_Chest_E.bind("<FocusOut>", self.on_focus_out)

        E_A_Leg_L = Label(Enemy_Canvas, text = "Leg Armor", font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        E_A_Leg_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_A_Leg_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        E_A_Leg_E.bind("<FocusIn>", self.on_focus_in)
        E_A_Leg_E.bind("<FocusOut>", self.on_focus_out)

        E_Stat_L = Label(Enemy_Canvas, text = "Agility", font = self.theme.Text_Font_Size).grid(row = 4, column = 0, pady = self.theme.Text_PadY_Size)
        E_Agility_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_Agility_E.grid(row = 4, column = 1, pady = self.theme.Text_PadY_Size)
        E_Agility_E.bind("<FocusIn>", self.on_focus_in)
        E_Agility_E.bind("<FocusOut>", self.on_focus_out)

        E_Debuff_L = Label(Enemy_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size).grid(row = 5, column = 0, pady = self.theme.Text_PadY_Size)
        E_A_Debuff_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_A_Debuff_E.grid(row = 5, column = 1, pady = self.theme.Text_PadY_Size)
        E_A_Debuff_E.bind("<FocusIn>", self.on_focus_in)
        E_A_Debuff_E.bind("<FocusOut>", self.on_focus_out)

        E_Toughness_L = Label(Enemy_Canvas, text = "Toughness Modifier", font = self.theme.Text_Font_Size).grid(row = 6, column = 0, pady = self.theme.Text_PadY_Size)
        E_Toughness_E = Entry(Enemy_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        E_Toughness_E.grid(row = 6, column = 1, pady = self.theme.Text_PadY_Size)
        E_Toughness_E.bind("<FocusIn>", self.on_focus_in)
        E_Toughness_E.bind("<FocusOut>", self.on_focus_out)


        Shield_Canvas = Frame(Right_canvas_Frame)

        S_Stat_L = Label(Shield_Canvas, text = "Agility", font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        S_Agility_E = Entry(Shield_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        S_Agility_E.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        S_Agility_E.bind("<FocusIn>", self.on_focus_in)
        S_Agility_E.bind("<FocusOut>", self.on_focus_out)

        S_Debuff_L = Label(Shield_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size).grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        S_A_Debuff_E = Entry(Shield_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        S_A_Debuff_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)
        S_A_Debuff_E.bind("<FocusIn>", self.on_focus_in)
        S_A_Debuff_E.bind("<FocusOut>", self.on_focus_out)


        Vehicle_Canvas = Frame(Right_canvas_Frame)

        V_Armor_L = Label(Vehicle_Canvas, text = "Armor", font = self.theme.Text_Font_Size).grid(row = 0, column = 0, pady = self.theme.Text_PadY_Size)
        V_Armor_E = Entry(Vehicle_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        V_Armor_E.grid(row = 0, column = 1, pady = self.theme.Text_PadY_Size)
        V_Armor_E.bind("<FocusIn>", self.on_focus_in)
        V_Armor_E.bind("<FocusOut>", self.on_focus_out)

        V_Stat_L = Label(Vehicle_Canvas, text = "Manuverability", font = self.theme.Text_Font_Size).grid(row = 1, column = 0, pady = self.theme.Text_PadY_Size)
        V_Agility_E = Entry(Vehicle_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        V_Agility_E.grid(row = 1, column = 1, pady = self.theme.Text_PadY_Size)
        V_Agility_E.bind("<FocusIn>", self.on_focus_in)
        V_Agility_E.bind("<FocusOut>", self.on_focus_out)

        V_Debuff_L = Label(Vehicle_Canvas, text = "Debuff Invulrability Charges", font = self.theme.Text_Font_Size).grid(row = 2, column = 0, pady = self.theme.Text_PadY_Size)
        V_A_Debuff_E = Entry(Vehicle_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        V_A_Debuff_E.grid(row = 2, column = 1, pady = self.theme.Text_PadY_Size)
        V_A_Debuff_E.bind("<FocusIn>", self.on_focus_in)
        V_A_Debuff_E.bind("<FocusOut>", self.on_focus_out)

        V_Toughness_L = Label(Vehicle_Canvas, text = "Toughness Modifier", font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)
        V_Toughness_E = Entry(Vehicle_Canvas, textvariable = IntVar(value = 0), validate = "key", validatecommand = vcmd, font = self.theme.Text_Font_Size)
        V_Toughness_E.grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        V_Toughness_E.bind("<FocusIn>", self.on_focus_in)
        V_Toughness_E.bind("<FocusOut>", self.on_focus_out)

        R_canvases = {"enemy": Enemy_Canvas,"shield": Shield_Canvas,"vehicle": Vehicle_Canvas}


        Swap_Left_Canvas()
        Swap_Right_Canvas()
        self.theme.toggle_dark_mode()
        
        Calculate_B = Button(self, text = "Calculate", command = lambda:[
            calulate(str(Attack_Type.get()), str(Enemy_Type.get()), str(Fire_Mode.get()), str(Melee_Mode.get()),
            int(R_Stat_E.get()), int(M_Stat_E.get()),int(E_Agility_E.get()), int(S_Agility_E.get()), int(V_Agility_E.get()),
            int(R_Shot_E.get()), int(R_Size_E.get()), int(R_Num_E.get()), int(R_AddD_E.get()), int(R_Pierce_E.get()), int(self.Rounds.get()),
            int(M_Strikes_E.get()), int(M_Size_E.get()), int(M_Num_E.get()), int(M_AddD_E.get()), int(M_Pierce_E.get()),
            int(E_A_Head_E.get()), int(E_A_Arm_E.get()), int(E_A_Chest_E.get()), int(E_A_Leg_E.get()), int(V_Armor_E.get()), int(E_A_Debuff_E.get()),
            int(S_A_Debuff_E.get()), 
            int(V_A_Debuff_E.get()), 
            int(E_Toughness_E.get()), int(V_Toughness_E.get()), 
            self.theme.Dark_Mode), self.spend_ronds(int(R_Shot_E.get()))], font = self.theme.Text_Font_Size).grid(row = 3, column = 1, pady = self.theme.Text_PadY_Size)
        
        Dark_Mode_B = Button(self, text = "Dark mode toggle", command = self.theme.toggle_dark_mode, font = self.theme.Text_Font_Size).grid(row = 3, column = 0, pady = self.theme.Text_PadY_Size)

        Instructions_B = Button(self, text = "Instructions", command = lambda: instructions(self.theme.Dark_Mode), font = self.theme.Text_Font_Size).grid(row = 3, column = 2, pady = self.theme.Text_PadY_Size)

    def spend_ronds(self, shots):
        self.Rounds.set(max(0, int(self.Rounds.get()) - shots))

    def on_focus_in(self, event):
        if event.widget.get() == "0":
            event.widget.delete(0, "end")

    def on_focus_out(self, event):
        if event.widget.get().strip() == "":
            event.widget.insert(0, "0")

root = Tk()
root.wm_title("Halo Combat Program")
root.geometry("1000x600")

page_container = Frame(root)
page_container.pack(side = "right", fill = "both", expand = True)
page_container.rowconfigure(0, weight = 1)
page_container.columnconfigure(0, weight = 1)

main_page = Main_Page(page_container)
main_page.grid(row = 0, column = 0, sticky = "nsew")
main_page.tkraise()


root.mainloop()