# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:42:22 2024

@author: Thomas Vouk
"""

import os
from datetime import datetime

def resultDirectory():
    
    date=datetime.today().strftime('%Y-%m-%d')
    script_path = os.path.abspath(__file__)
    script_name = os.path.basename(script_path)
    directory_path = os.path.abspath(__file__)[:-len(script_name)]+"results\\"+date+"\\"
    
    
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # If the directory doesn't exist, create it
        os.makedirs(directory_path)
    
    return directory_path

if __name__ == "__main__":
    
    print(resultDirectory())
