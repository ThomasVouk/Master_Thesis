"""
Example script for testing the Azure ttk theme
source_Author: rdbende
License: MIT license
Basis: https://github.com/rdbende/ttk-widget-factory


Created on Wed Jan  3 11:04:30 2024
@author: Thomas Vouk
"""


import tkinter as tk
from tkinter import ttk
from login import login_process


class GUI_Spatial(ttk.Frame):
    def __init__(self, parent, master=None, **kwargs):
        ttk.Frame.__init__(self)
        
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        """
        This value List must be generatete from the database --> via spezific querry for every menu!! 
        """
        # Create value lists
        self.energy_carrier_list = ["Energy carrier","Electricity", "CH4","Hydrogen","District heat"]
        self.user_list = ["User", "TV", "SW", "LK","TK"]
        self.referenz_year_list = ["Referenz Year","2017", "2019", "2020"]
        self.scenario_menu_list = ["Scenario","NIP","InfraTrans_WAM", "InfraTrans_EEF","EAG_ISB","NEFI_POI","NEFI_ZEM"]
        self.calculation_year_list = ["Calculation Year","2020","2025","2030","2035","2040","2045","2050"]
        self.resolution_list = ["Resolution","1H","15MIN"]
        self.target_list = ["Target","USW-district","District"]
        self.intial_data = ["country","state","district"]
        
        #This is a list of dictornaries, where every dictornary saves a Case for a calculation
        self.scenario_cases =[]


        # Create control variables
        self.var_1 = tk.StringVar(value=self.user_list[1])
        self.var_2 = tk.BooleanVar(value=True)
        self.var_3 = tk.BooleanVar(value=True)
        self.var_4 = tk.StringVar(value=self.energy_carrier_list[1])
        self.var_6 = tk.StringVar(value=self.scenario_menu_list[1])
        self.var_7 = tk.StringVar(value=self.referenz_year_list[1])
        self.var_8 = tk.StringVar(value=self.calculation_year_list[1])
        self.var_9 = tk.StringVar(value=self.resolution_list[1])
        self.var_10 = tk.StringVar(value=self.target_list[1])
        self.var_11 = tk.StringVar(value=self.scenario_menu_list[1])
        self.var_12 = tk.StringVar(value=self.energy_carrier_list[1])

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):

        self.radio_frame = ttk.LabelFrame(self, text="Initial data", padding=(20, 10))
        self.radio_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Radiobuttons
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame, text="Country", variable=self.var_2, value=True
        )
        self.radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame, text="State", variable=self.var_2, value=False
        )
        """
        self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_4 = ttk.Radiobutton(
            self.radio_frame, text="District", state="disabled"
        )
        self.radio_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        """
        
        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Create a Frame for the Radiobuttons for Backup
        self.radio_frame = ttk.LabelFrame(self, text="CSV-Backup", padding=(20, 10))
        self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # Radiobuttons_1
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame, text="Unselected", variable=self.var_3, value=False
        )
        self.radio_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame, text="Selected", variable=self.var_3, value=True
        )
        self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.radio_4 = ttk.Radiobutton(
            self.radio_frame, text="Disabled", state="disabled"
        )
        self.radio_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        # Create a Frame for input widgets

        self.widgets_frame = ttk.LabelFrame(self, text="Reference", padding=(20, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")


        # OptionMenu_Referenz year
        self.referenz_year = ttk.OptionMenu(
            self.widgets_frame, self.var_7, *self.referenz_year_list
        )
        self.referenz_year.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # OptionMenu_Energy_carrier
        self.energy_carrier = ttk.OptionMenu(
            self.widgets_frame, self.var_4, *self.energy_carrier_list
        )
        self.energy_carrier.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        # ScenarioMenu
        self.scenario_menu = ttk.OptionMenu(
            self.widgets_frame, self.var_6, *self.scenario_menu_list
        )
        self.scenario_menu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=1, padx=(20, 10), pady=10, sticky="ew")
       
        # Create a Frame for general input data
        self.general_frame = ttk.LabelFrame(self, text="General Data", padding=(20, 10))
        self.general_frame.grid(row=2, column=1, padx=(20, 10), pady=10, sticky="nsew")
        

        # OptionMenu_Energy_carrier
        self.user = ttk.OptionMenu(
            self.general_frame, self.var_1, *self.user_list
        )
        self.user.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Entry
        self.entry = ttk.Entry(self.general_frame)
        self.entry.insert(0, "Comment")
        self.entry.grid(row=1, column=0, padx=5, pady= 10, sticky="nsew")

        # Button
        self.button = ttk.Button(self.general_frame,style="Accent.TButton", text="Set Scenario",command=self.on_apply)
        self.button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")




        # Create a Frame for input widgets
        self.widgets_frame_2 = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame_2 = ttk.LabelFrame(self, text="Calculation", padding=(20, 10))
        self.widgets_frame_2.grid(
            row=0, column=2, padx=10, pady=(20, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame_2.columnconfigure(index=0, weight=1)



        # OptionMenu_Calculation year
        self.calculation_year = ttk.OptionMenu(
            self.widgets_frame_2, self.var_8, *self.calculation_year_list
        )
        self.calculation_year.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # OptionMenu_Energy Carrier
        self.energy_carrier = ttk.OptionMenu(
            self.widgets_frame_2, self.var_12, *self.energy_carrier_list
        )
        self.energy_carrier.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        # ScenarioMenu
        self.scenario_menu = ttk.OptionMenu(
            self.widgets_frame_2, self.var_11, *self.scenario_menu_list
        )
        self.scenario_menu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        
        # ResolutionMenu
        self.resolution_menu = ttk.OptionMenu(
            self.widgets_frame_2, self.var_9, *self.resolution_list
        )
        self.resolution_menu.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        
        # TargetMenu
        self.target_menu = ttk.OptionMenu(
            self.widgets_frame_2, self.var_10, *self.target_list
        )
        self.target_menu.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")


        # Accentbutton
        self.accentbutton = ttk.Button(
            self.widgets_frame_2, text="Finish scenario configuration", style="Accent.TButton",command=self.on_destruction
        )
        self.accentbutton.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")


    def on_apply(self):
        
        self.scenario_configuration ={}

        if self.var_1.get()==self.user_list[0]:
            self.scenario_configuration.__setitem__(self.user_list[0], "Unknown_"+self.var_1.get())
        else:
            self.scenario_configuration.__setitem__(self.user_list[0],self.var_1.get())
        
        if self.var_2.get()== True:
            self.scenario_configuration.__setitem__("initial_data","country")
        else:
            self.scenario_configuration.__setitem__("initial_data","state")

        if self.var_4.get()==self.energy_carrier_list[0]:
            self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.energy_carrier_list[1])
        else:
            self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.var_4.get())
        
        if self.var_6.get()==self.scenario_menu_list[0]:
            self.scenario_configuration.__setitem__(self.scenario_menu_list[0],self.scenario_menu_list[1])
        else:
            self.scenario_configuration.__setitem__(self.scenario_menu_list[0],self.var_6.get())
        
        if self.var_7.get()==self.referenz_year_list[0]:
            self.scenario_configuration.__setitem__(self.referenz_year_list[0],self.referenz_year_list[3])
        else:
            self.scenario_configuration.__setitem__(self.referenz_year_list[0],self.var_7.get())
        
        if self.var_8.get()==self.calculation_year_list[0]:
            self.scenario_configuration.__setitem__(self.calculation_year_list[0],self.calculation_year_list[3])
        else:
            self.scenario_configuration.__setitem__(self.calculation_year_list[0],self.var_8.get())

        if self.var_9.get()==self.resolution_list[0]:
            self.scenario_configuration.__setitem__(self.resolution_list[0],self.resolution_list[1])
        else:
            self.scenario_configuration.__setitem__(self.resolution_list[0],self.var_9.get())

        if self.var_10.get()==self.target_list[0]:
            self.scenario_configuration.__setitem__(self.target_list[0],self.target_list[1])
        else:
            self.scenario_configuration.__setitem__(self.target_list[0],self.var_10.get())

        if self.var_11.get()==self.scenario_menu_list[0]:
            self.scenario_configuration.__setitem__(self.scenario_menu_list[0],self.scenario_menu_list[1])
        else:
            self.scenario_configuration.__setitem__(self.scenario_menu_list[0],self.var_11.get())

        if self.var_12.get()==self.energy_carrier_list[0]:
            self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.energy_carrier_list[1])
        else:
            self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.var_12.get())

        self.scenario_configuration.__setitem__("CSV-Backup",self.var_3.get())
        
        if self.entry.get()=="Comment":
            self.scenario_configuration.__setitem__("Comment","")
        else:
            self.scenario_configuration.__setitem__("Comment",self.entry.get())        
        
        
        self.scenario_cases.append(self.scenario_configuration)
        
        print(self.scenario_cases)
        
    def on_destruction(self):
        
        root.destroy()

if __name__ == "__main__":
    
    #login_process()
    
    root = tk.Tk()
    root.title("Spatial Resolution")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    app = GUI_Spatial(root)
    app.pack(fill="both", expand=True)
    
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
