# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 12:21:58 2023

@author: Anton Baranikov
"""
import tkinter as tk
from app import SpendingTrackerApp


# Create an instance of the Tk class
root = tk.Tk()  
# Create an instance of your application class, passing the root window as an argument
# SpendingTrackerApp(root, file_id = '............')  
SpendingTrackerApp(root)  
root.mainloop()  # Start the Tkinter event loop
