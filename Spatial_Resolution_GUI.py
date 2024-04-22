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
from login import database_connection
from datetime import datetime
import sys



def generate_SpatialGUI():
    
    
    class GUI_Spatial(ttk.Frame):
        def __init__(self, parent, master=None, **kwargs):
            ttk.Frame.__init__(self)
            
            # Make the app responsive
            for index in [0, 1, 2]:
                self.columnconfigure(index=index, weight=1)
                self.rowconfigure(index=index, weight=1)
    
            """
            This value List must be generatete from the database --> via spezific querry for every menu!! 
            This could be an SELECT query or something simmilar 
            """
            # Create value lists
            self.energy_carrier_list = ["Energy carrier","electricity", "CH4","district heat","hydrogen",]
            self.user_list = ["User", "TV", "SW", "LK","TK"]
            self.reference_year_list = ["Reference year","2017", "2019", "2020","2021"]
            self.reference_scenario_menu_list = ["Reference_Scenario","NIP","InfraTrans_WAM", "InfraTrans_EEF","E_AG_ISB","NEFI_POI","NEFI_ZEM","WAM"]
            self.calculation_scenario_menu_list = ["Calculate_Scenario","NIP","InfraTrans_WAM", "InfraTrans_EEF","E_AG_ISB","NEFI_POI","NEFI_ZEM","WAM"]
            self.calculation_year_list = ["Calculation year","2019","2020","2025","2030","2035","2040","2045","2050"]
            self.resolution_list = ["Resolution","1H","15MIN"]
            self.target_list = ["Target","USW-district","Politial district"]
            self.intial_data = ["country","state","district"]
            
            #This is a list of dictornaries, where every dictornary saves a Case for a calculation
            self.scenario_cases =[]
    
    
            # Create control variables
            self.var_1 = tk.StringVar(value=self.user_list[1])
            self.var_2 = tk.BooleanVar(value=True)
            self.var_4 = tk.StringVar(value=self.energy_carrier_list[1])
            self.var_6 = tk.StringVar(value=self.reference_scenario_menu_list[1])
            self.var_7 = tk.StringVar(value=self.reference_year_list[1])
            self.var_8 = tk.StringVar(value=self.calculation_year_list[1])
            self.var_9 = tk.StringVar(value=self.resolution_list[1])
            self.var_10 = tk.StringVar(value=self.target_list[1])
            self.var_11 = tk.StringVar(value=self.calculation_scenario_menu_list[1])
            self.var_12 = tk.StringVar(value=self.energy_carrier_list[1])
            
            self.var_13 = tk.BooleanVar(value=False)
            self.var_14 = tk.BooleanVar(value=False)
            self.var_15 = tk.BooleanVar(value=False)
            self.var_16 = tk.BooleanVar(value=False)
            self.var_17 = tk.BooleanVar(value=False)
            self.var_18 = tk.BooleanVar(value=False)
            self.var_19 = tk.BooleanVar(value=False)
            self.var_20 = tk.BooleanVar(value=False)
            self.var_21 = tk.BooleanVar(value=False)
            self.var_22 = tk.BooleanVar(value=False)
            self.var_23 = tk.BooleanVar(value=False)           
    
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
            self.radio_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
     
            
            # Separator
            self.separator = ttk.Separator(self)
            self.separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
            
            # Separator
            self.separator = ttk.Separator(self)
            self.separator.grid(row=1, column=2, padx=(20, 10), pady=10, sticky="ew")
            # Separator
            
            self.separator = ttk.Separator(self)
            self.separator.grid(row=1, column=3, padx=(20, 10), pady=10, sticky="ew")
    
            
            # Create a Frame for input widgets
    
            self.widgets_frame = ttk.LabelFrame(self, text="Reference scenario", padding=(20, 10))
            self.widgets_frame.grid(
                row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")
    
    
            # OptionMenu_Reference year
            self.reference_year = ttk.OptionMenu(
                self.widgets_frame, self.var_7, *self.reference_year_list
            )
            self.reference_year.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            # OptionMenu_Energy_carrier
            self.energy_carrier = ttk.OptionMenu(
                self.widgets_frame, self.var_4, *self.energy_carrier_list
            )
            self.energy_carrier.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
    
            # ScenarioMenu
            self.scenario_menu = ttk.OptionMenu(
                self.widgets_frame, self.var_6, *self.reference_scenario_menu_list
            )
            self.scenario_menu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    
            # Separator
            self.separator = ttk.Separator(self)
            self.separator.grid(row=1, column=1, padx=(20, 10), pady=10, sticky="ew")
           
            # Create a Frame for general input data
            self.general_frame = ttk.LabelFrame(self, text="General data", padding=(20, 10))
            self.general_frame.grid(row=0, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew")
            
    
            # OptionMenu_Energy_carrier
            self.user = ttk.OptionMenu(
                self.general_frame, self.var_1, *self.user_list
            )
            self.user.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
    
    
            # TargetMenu
            self.target_menu = ttk.OptionMenu(
                self.general_frame, self.var_10, *self.target_list
            )
            self.target_menu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")        
            
            # ResolutionMenu
            self.resolution_menu = ttk.OptionMenu(
                self.general_frame, self.var_9, *self.resolution_list
            )
            self.resolution_menu.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
    
    
            self.widgets_frame_2 = ttk.LabelFrame(self, text="Calculation scenario", padding=(20, 10))
            self.widgets_frame_2.grid(row=0, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")
            
    
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
                self.widgets_frame_2, self.var_11, *self.calculation_scenario_menu_list
            )
            self.scenario_menu.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    
    
            # Create a Frame for the Checkbuttons_Transportation
            self.check_frame = ttk.LabelFrame(self, text="Transportation", padding=(20, 10))
            self.check_frame.grid(
                row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )
    
            # Checkbuttons
            self.check_1 = ttk.Checkbutton(
                self.check_frame, text="Car", variable=self.var_13
            )
            self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_2 = ttk.Checkbutton(
                self.check_frame, text="Heavy duty truck", variable=self.var_14
            )
            self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_3 = ttk.Checkbutton(
                self.check_frame, text="Light duty truck", variable=self.var_15
            )
            self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    
    
            # Create a Frame for the Checkbuttons_Industry
            self.check_frame = ttk.LabelFrame(self, text="Industry", padding=(20, 10))
            self.check_frame.grid(
                row=2, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )
    
            # Checkbuttons
            self.check_4 = ttk.Checkbutton(
                self.check_frame, text="Industry Top-Down", variable=self.var_16
            )
            self.check_4.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_5 = ttk.Checkbutton(
                self.check_frame, text="Company", variable=self.var_17
            )
            self.check_5.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
            
            
            # Create a Frame for the Checkbuttons_Households
            self.check_frame = ttk.LabelFrame(self, text="Households", padding=(20, 10))
            self.check_frame.grid(
                row=2, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )
    
            # Checkbuttons
            self.check_6 = ttk.Checkbutton(
                self.check_frame, text="H0 households", variable=self.var_18
            )
            self.check_6.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_7 = ttk.Checkbutton(
                self.check_frame, text="Households heat demand", variable=self.var_19
            )
            self.check_7.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
    
            # Create a Frame for the Checkbuttons_Services 
            self.check_frame = ttk.LabelFrame(self, text="Services", padding=(20, 10))
            self.check_frame.grid(
                row=2, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )        
            
            self.check_8 = ttk.Checkbutton(
                self.check_frame, text="G0 services", variable=self.var_20
            )
            self.check_8.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_9 = ttk.Checkbutton(
                self.check_frame, text="Services heat demand", variable=self.var_21
            )
            self.check_9.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")        
    
            # Create a Frame for Other Bottom_Up Kathegories 
            self.check_frame_3 = ttk.LabelFrame(self, text="Others", padding=(20, 10))
            self.check_frame_3.grid(
                row=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
            )        
            
            self.check_8 = ttk.Checkbutton(
                self.check_frame_3, text="Locomotiv", variable=self.var_22
            )
            self.check_8.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
            self.check_9 = ttk.Checkbutton(
                self.check_frame_3, text="Compressor station", variable=self.var_23
            )
            self.check_9.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")        
    
    
            self.calculation_frame = ttk.LabelFrame(self, text="Calculate", padding=(20, 10))
            self.calculation_frame.grid(row=3, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew")


            # Button
            self.button = ttk.Button(self.calculation_frame,style="Accent.TButton", text="Set scenario",command=self.on_apply)
            self.button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
    
             # Accentbutton
            self.accentbutton = ttk.Button(self.calculation_frame, text="Go to temporal resolution", style="Accent.TButton",command=self.on_destruction)
            self.accentbutton.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")    
            
            # Delete Button
            self.delete_button = ttk.Button(self.calculation_frame,style="Accent.TButton", text="Delete scenario",command=self.on_delete)
            self.delete_button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
    
    
            self.comment_frame = ttk.LabelFrame(self, text="Comment", padding=(20, 10))
            self.comment_frame.grid(row=3, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew")
    
            # Entry
            self.entry = ttk.Entry(self.comment_frame)
            self.entry.insert(0, "Comment")
            self.entry.grid(row=1, column=0, padx=5, pady= 10, sticky="nsew")
    
        def on_apply(self):
            
            self.scenario_configuration ={}
    
            if self.var_1.get()==self.user_list[0]:
                self.scenario_configuration.__setitem__(self.user_list[0], "Unknown_"+self.var_1.get())
            else:
                self.scenario_configuration.__setitem__(self.user_list[0],self.var_1.get())
            
            if self.var_2.get()== True:
                self.scenario_configuration.__setitem__("Initial_data","country")
            else:
                self.scenario_configuration.__setitem__("Initial_data","state")
    
            if self.var_4.get()==self.energy_carrier_list[0]:
                self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.energy_carrier_list[1])
            else:
                self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.var_4.get())
            
            if self.var_6.get()==self.reference_scenario_menu_list[0]:
                self.scenario_configuration.__setitem__(self.reference_scenario_menu_list[0],self.reference_scenario_menu_list[1])
            else:
                self.scenario_configuration.__setitem__(self.reference_scenario_menu_list[0],self.var_6.get())
            
            if self.var_7.get()==self.reference_year_list[0]:
                self.scenario_configuration.__setitem__(self.reference_year_list[0],self.reference_year_list[3])
            else:
                self.scenario_configuration.__setitem__(self.reference_year_list[0],self.var_7.get())
            
            if self.var_8.get()==self.calculation_year_list[0]:
                self.scenario_configuration.__setitem__(self.calculation_year_list[0],self.calculation_year_list[4])
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
    
            if self.var_11.get()==self.calculation_scenario_menu_list[0]:
                self.scenario_configuration.__setitem__(self.calculation_scenario_menu_list[0],self.calculation_scenario_menu_list[1])
            else:
                self.scenario_configuration.__setitem__(self.calculation_scenario_menu_list[0],self.var_11.get())
    
            if self.var_12.get()==self.energy_carrier_list[0]:
                self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.energy_carrier_list[1])
            else:
                self.scenario_configuration.__setitem__(self.energy_carrier_list[0],self.var_12.get())
    
            self.scenario_configuration.__setitem__("Creation_time",datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            
            if self.entry.get()=="Comment":
                self.scenario_configuration.__setitem__("Comment","")
            else:
                self.scenario_configuration.__setitem__("Comment",self.entry.get())        
            
            if self.var_13.get()==True:
                self.scenario_configuration.__setitem__("Car",True)
            else:
                self.scenario_configuration.__setitem__("Car",False)  

            if self.var_14.get()==True:
                self.scenario_configuration.__setitem__("Heavy duty truck",True)
            else:
                self.scenario_configuration.__setitem__("Heavy duty truck",False)         
 
            if self.var_15.get()==True:
                self.scenario_configuration.__setitem__("Light duty truck",True)
            else:
                self.scenario_configuration.__setitem__("Light duty truck",False) 

            if self.var_16.get()==True:
                self.scenario_configuration.__setitem__("Industry Top-down",True)
            else:
                self.scenario_configuration.__setitem__("Industry Top-down",False)             

            if self.var_17.get()==True:
                self.scenario_configuration.__setitem__("Industrie Bottom-Up",True)
            else:
                self.scenario_configuration.__setitem__("Industrie Bottom-Up",False) 

            if self.var_18.get()==True:
                self.scenario_configuration.__setitem__("Households H0",True)
            else:
                self.scenario_configuration.__setitem__("Households H0",False)

            if self.var_19.get()==True:
                self.scenario_configuration.__setitem__("Households heat demand",True)
            else:
                self.scenario_configuration.__setitem__("Households heat demand",False)

            if self.var_20.get()==True:
                self.scenario_configuration.__setitem__("Services",True)
            else:
                self.scenario_configuration.__setitem__("Services",False)

            if self.var_21.get()==True:
                self.scenario_configuration.__setitem__("Services heat demand",True)
            else:
                self.scenario_configuration.__setitem__("Services heat demand",False)

            if self.var_22.get()==True:
                self.scenario_configuration.__setitem__("Locomotiv",True)
            else:
                self.scenario_configuration.__setitem__("Locomotiv",False)

            if self.var_23.get()==True:
                self.scenario_configuration.__setitem__("Compressor station",True)
            else:
                self.scenario_configuration.__setitem__("Compressor station",False)



            self.scenario_cases.append(self.scenario_configuration)
            
            print(f"Case configurations: {self.scenario_configuration}")
            
        def on_delete(self):
            if len(self.scenario_cases)>0:
                
                self.scenario_cases.pop()           
                print(self.scenario_cases)
            else:
                
                root.destroy()
                #sys.exit()
                
        def on_destruction(self):
            
            root.destroy()
    
    root = tk.Tk()
    root.title("Spatial resolution")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = GUI_Spatial(root)
    app.pack(fill="both", expand=True)
    
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
    
    return app.scenario_cases
        

if __name__ == "__main__":
    
    #database_connection()
    generate_SpatialGUI()

