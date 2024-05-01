# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 09:41:46 2023

@author: Anton Baranikov

"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from datetime import date
import shutil
import numpy as np
from pandastable import Table
from app.support import DriveHandle

class SpendingTrackerApp:
    
    def __init__(self, root, file_id = None, test = False):
        
        self.file_id = file_id
        
        if self.file_id is not None:
            # download file from GoogleDrive and write to local file
            self.drive = DriveHandle.login()
            DriveHandle.download_file(self.drive, 'spending.csv', self.file_id)
        else:           
            DriveHandle.dummy_csv_local('spending.csv')
                  
        # save a copy of .csv
        shutil.copyfile('spending.csv', 'spending_safe.csv')
        # handle permanent spendings and salary
        # rent + electricity/gas + water + insurance + home_internet + 2*Sport + 2*phone + 2*train
        self.permanent = [1425, 79, 26, 291, 52, 110, 30, 68]
        self.salary = 4300
        
        self.df = pd.read_csv('spending.csv', index_col = 'Date', parse_dates = True)        
        today = date.today() 
             
        # if empty then assign some defaults to the goal part
        if pd.isna(self.df['Goal'][0]):
            
            self.goal = 10000
        else:
            
            self.goal = float(self.df['Goal'][0])
              
        try:    
            self.goal_date = datetime.datetime.strptime(self.df['Goal'][1], '%Y-%m-%d %H:%M:%S')  
            self.df.iloc[1,2] = self.goal_date # reassign to follow datetime format in the dataframe
        except:              
            
            tm = datetime.time(0)
            dt = datetime.date(today.year, today.month, 1)
            self.goal_date = datetime.datetime.combine(dt, tm)  
                        
        if not test:
            # the only thing we change in the dataframe is to write permanent
            if pd.isna(self.df['Category'][0]):
                for mnth in range(today.month):       
                    self.write_permanent(mnth + 1)
            else:
                self.write_permanent(today.month)
            
            self.Categories = ["All", "Food", "Entertain", "Utils", "Cafe", "Car", "Shop", "Sport", "Edu", "Beauty", "Other", "Income", "Balance"]
            self.root = root
            self.root.title("Spending Tracker")
                                    
            self.create_ui()
            self.goal_date_entry.insert(0, self.goal_date.date().strftime('%d-%m-%Y'))
            self.goal_entry.insert(0, self.goal)
            self.plot_all()
        
    def create_ui(self):
        
        """
        Frames 
        
        """
        r = 1
        #spending
        frame_1 = tk.LabelFrame(self.root, text = 'Spending', font=('Helvetica', 12, 'bold'), labelanchor="n")
        frame_1.grid(row = r-1, column = 0)
        
        #goal settings       
        frame_5 = tk.LabelFrame(self.root, text = 'Our goal', font=('Helvetica', 12, 'bold'), labelanchor="n")
        frame_5.grid(row = r-1 , column = 1, columnspan = 2)
        
        #income
        frame_2 = tk.LabelFrame(self.root, text = 'Income', font=('Helvetica', 12, 'bold'), labelanchor="n")
        frame_2.grid(row = r-1, column = 3)
        
        #selection boxes and plots
        frame_3 = tk.Frame(self.root, pady = 5)
        frame_3.grid(row = r + 1, column = 0, columnspan = 2)
        frame_4 = tk.Frame(self.root, pady = 5)
        frame_4.grid(row = r + 1, column = 2, columnspan = 2)
   
        # validation command
        vcmd_number = (self.root.register(self.validate_number), '%P')
        vcmd_date = (self.root.register(self.validate_date), '%P')
    
        """
        Spending frame
        
        """        
        self.date_label = ttk.Label(frame_1, text="Date (DD-MM-YYYY):")
        self.date_label.pack()
        self.date_entry = ttk.Entry(frame_1, validate = "focusout", validatecommand = vcmd_date, invalidcommand = self.on_invalid_date)
        self.date_entry.pack()

        self.category_label = ttk.Label(frame_1, text="Category:")
        self.category_label.pack()
        # Create a Combobox for selecting categories
        Categories_cut = self.Categories.copy()
        
        for to_cut in ["Balance", "Income", "All"]:
            Categories_cut.remove(to_cut)
            
        self.category_combobox = ttk.Combobox(frame_1, values = Categories_cut)
        self.category_combobox.pack()

        self.amount_label = ttk.Label(frame_1, text="Amount Spent:")
        self.amount_label.pack()
        self.amount_entry = ttk.Entry(frame_1, validate = "key", validatecommand = vcmd_number, invalidcommand = self.on_invalid_number)
        self.amount_entry.pack()

        self.capture_button = ttk.Button(frame_1, text="Capture Spending", command=self.capture_spending)
        self.capture_button.pack()
        
        """
        Income frame
        
        """  
        self.date_label_income = ttk.Label(frame_2, text="Date (DD-MM-YYYY):")
        self.date_label_income.pack()
        self.date_entry_income = ttk.Entry(frame_2, validate = "focusout", validatecommand = vcmd_date, invalidcommand = self.on_invalid_date)
        self.date_entry_income.pack()
        
        self.amount_label_income = ttk.Label(frame_2, text="Amount:")
        self.amount_label_income.pack()
        self.amount_entry_income = ttk.Entry(frame_2, validate = "key", validatecommand = vcmd_number, invalidcommand = self.on_invalid_number)
        self.amount_entry_income.pack()

        self.capture_button_income = ttk.Button(frame_2, text="Capture Income", command=self.capture_income)
        self.capture_button_income.pack()
        
        """
        Goal frame
        
        """
        self.goal_label = ttk.Label(frame_5, text="Goal:")
        self.goal_label.grid(row = 0, column = 0)
        self.goal_entry = ttk.Entry(frame_5, validate = "key", validatecommand = vcmd_number, invalidcommand = self.on_invalid_number)       
        self.goal_entry.grid(row = 1, column = 0)
        self.goal_button = ttk.Button(frame_5, text="SET!", command=self.set_goal)
        self.goal_button.grid(row = 2, column = 0)
        
        self.goal_date_label = ttk.Label(frame_5, text="Start (DD-MM-YYYY):")
        self.goal_date_label.grid(row = 0, column = 1)
        self.goal_date_entry = ttk.Entry(frame_5, validate = "focusout", validatecommand = vcmd_date, invalidcommand = self.on_invalid_date)
                
        self.goal_date_entry.grid(row = 1, column = 1)       
        self.goal_date_button = ttk.Button(frame_5, text="SET!", command=self.set_goal_date)
        self.goal_date_button.grid(row = 2, column = 1)
                     
        self.fig_goal = Figure(figsize = (1.5, 1.5))
        self.ax_goal = self.fig_goal.add_subplot(111)
        self.fig_goal.subplots_adjust(left = 0.0, bottom=0.0, right=1, top=1)
        
        self.canvas_goal = FigureCanvasTkAgg(self.fig_goal, master=frame_5)
        self.canvas_goal.get_tk_widget().grid(row = 3, column = 0, columnspan = 2)
                
        self.display_button = ttk.Button(frame_5, text="Display data", command=self.DisplayDF)
        self.display_button.grid(row = 4, column = 0, columnspan = 2)
        
        self.error_label = ttk.Label(frame_5, foreground = 'red')
        self.error_label.grid(row = 5, column = 0)
        
        """
        Plots frames
        
        """
        # Create a combobox for selecting the month
        self.month_combobox = ttk.Combobox(frame_3, values=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        today = date.today()
        month = today.strftime("%b")
        self.month_combobox.set(month)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_selection)
        self.month_combobox.grid(row = 0, column = 0, pady= 20)
        
        # Create a combobox for selecting the category
        self.cat_combobox = ttk.Combobox(frame_4, values=self.Categories)
        self.cat_combobox.set('All')
        self.cat_combobox.bind("<<ComboboxSelected>>", self.on_category_selection)
        self.cat_combobox.grid(row = 0, column = 1, pady= 20)
        
        # plots
        size = (5,4)
        # plot by categories
        self.fig_cat = Figure(figsize = size)
        self.ax_cat = self.fig_cat.add_subplot(1, 1, 1)
        self.fig_cat.subplots_adjust(bottom = 0.15, top = 0.93)
        # plot by months
        self.fig_month = Figure(figsize = size)
        self.ax_month = self.fig_month.add_subplot(1, 1, 1)
        self.fig_month.subplots_adjust(bottom = 0.15, top = 0.93)
        # self.fig_cat.tight_layout()
        # self.fig_month.tight_layout()
        
        self.canvas_cat = FigureCanvasTkAgg(self.fig_cat, master=frame_3)
        self.canvas_cat.get_tk_widget().grid(row = 1, column = 0)
        self.canvas_month = FigureCanvasTkAgg(self.fig_month, master=frame_4)
        self.canvas_month.get_tk_widget().grid(row = 1, column = 1)
       
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def write_permanent(self, month):
                         
        today = date.today() 
        tm = datetime.time(0)
        
        # initialize the first day of the month
        dt = datetime.date(today.year, month, 1)
        # initialize the 25th day of the month
        dt_salary = datetime.date(today.year, month, 25)
        
        date_permament = datetime.datetime.combine(dt, tm)
        date_salary = datetime.datetime.combine(dt_salary, tm)
        
        entry = pd.DataFrame({
            'Date': [date_permament]*len(self.permanent) + [date_salary],
            'Category': ['Utils']*len(self.permanent) + ['Income'],
            'Amount': self.permanent + [self.salary],
            'Goal': [np.nan]*(len(self.permanent) + 1)
            })

        entry = entry.set_index('Date')
        df_permanent = self.df.loc[((self.df.index == date_permament) | (self.df.index == date_salary)) & ((self.df['Category'] == 'Utils') | (self.df['Category'] == 'Income'))]
               
        # only if the entry doesnt exist
        if self.df['Category'].isnull().all():
            
            self.df = entry
            
        else:       
            
            df_merged = pd.merge(entry.reset_index(), df_permanent.reset_index(), how='outer', indicator = 'exist').set_index('Date')
            self.df = pd.concat([self.df, df_merged[df_merged['exist'] == 'left_only']]).drop(['exist'], axis = 1) # only those present only in the entry
        
    def capture_spending(self):
        
        """
        Capture Spending Button
        
        """
        date_spend = self.date_entry.get()
        category = self.category_combobox.get()
        
        try:
            date_spend = datetime.datetime.strptime(date_spend, '%d-%m-%Y')
            amount = float(self.amount_entry.get())
            if len(category) == 0:
                raise ValueError
        except:
            self.show_message('Please fix entries !!!')
            return
                                  
        entry = pd.DataFrame({
            'Date': [date_spend],
            'Category': [category],
            'Amount': [amount]
            })
        entry = entry.set_index('Date')
        
        self.df = pd.concat([self.df, pd.DataFrame(entry)])
        
        # replot
        self.plot_all()
        self.show_message()
        
    def capture_income(self):   
        
        """
        Capture Income Button
        
        """
       
        date_income = self.date_entry_income.get()
        try:
            date_income = datetime.datetime.strptime(date_income, '%d-%m-%Y')
            amount = float(self.amount_entry_income.get())
        except:
            self.show_message('Please fix entries !!!')
            return
                       
        entry = pd.DataFrame({
            'Date': [date_income],
            'Category': 'Income',
            'Amount': [amount]
            })
        entry = entry.set_index('Date')
        
        self.df = pd.concat([self.df, pd.DataFrame(entry)])
        
        self.plot_all()
        self.show_message()
        
    def set_goal(self):
        
        self.goal = float(self.goal_entry.get())
        self.df.iloc[0, 2]= self.goal;
        self.plot_progress()
          
    def set_goal_date(self):
        
        date_goal = self.goal_date_entry.get()
        self.goal_date = datetime.datetime.strptime(date_goal, '%d-%m-%Y')
        
        self.df.iloc[1, 2] = self.goal_date;
        self.plot_progress()
    
    def plot_categories(self):
        
        today = date.today() 
        # filter today's year
        df_toplot = self.df.loc[(self.df.index.year == today.year)]       
        
        # Clear previous plot data
        self.ax_cat.clear()        
        month = self.month_combobox.get()
        
        df_categories = df_toplot.groupby([pd.Grouper(freq = 'M'), 'Category'])['Amount'].sum().reset_index()
        
        per_month = df_categories[df_categories['Date'].dt.strftime("%b") == month]
        
        if per_month.empty:
            self.canvas_cat.draw() # update the figure
            return
        
        # remove income 
        per_month = per_month[per_month['Category'] != 'Income']
        
        per_month.plot.bar(x = 'Category', y = 'Amount', ax = self.ax_cat, rot = 45, legend=False, title = "Category spending", fontsize = 9)    
        self.ax_cat.bar_label(self.ax_cat.containers[0], fontsize = 9)
        self.ax_cat.xaxis.label.set_visible(False)
        # Redraw the canvas       
        self.canvas_cat.draw()
        
    def plot_months(self):
        
        today = date.today() 
        # filter today's year
        df_toplot = self.df.loc[(self.df.index.year == today.year)]           
        # Clear previous plot data
        self.ax_month.clear()        
        cat = self.cat_combobox.get()
        
        if cat == 'All':       
            
            # remove income
            df = df_toplot[df_toplot['Category'] != 'Income'].copy()
            per_cat = df.groupby(pd.Grouper(freq = 'M'))['Amount'].sum().reset_index()
            
        elif cat == 'Balance':
            
            # remove income
            df_spending = df_toplot[df_toplot['Category'] != 'Income'].copy()
            df_spending = df_spending.groupby(pd.Grouper(freq = 'M'))['Amount'].sum()
            # only income         
            df_income = df_toplot[df_toplot['Category'] == 'Income'].copy()
            df_income = df_income.groupby(pd.Grouper(freq = 'M'))['Amount'].sum()
            per_cat = (df_income - df_spending).reset_index()

        else: 
            
            df_categories = df_toplot[df_toplot['Category'] == cat].copy()
            per_cat = df_categories.groupby([pd.Grouper(freq = 'M')])['Amount'].sum().reset_index()   
            # df_categories = self.df.groupby([pd.Grouper(freq = 'M'), 'Category']).sum().reset_index()            
            # per_cat = df_categories[df_categories['Category'] == cat].copy()
            
            if per_cat.empty:
                self.canvas_month.draw() # update the figure
                return
                             
        per_cat['Month'] = per_cat['Date'].apply(lambda x: x.strftime("%b"))
        per_cat.plot.bar(x = 'Month', y = 'Amount', ax = self.ax_month, rot = 45, legend=False, color = "green", title = "Monthly spending", fontsize = 9)    
        self.ax_month.bar_label(self.ax_month.containers[0], fontsize = 9)
        self.ax_month.xaxis.label.set_visible(False)
        # Redraw the canvas       
        self.canvas_month.draw()
    
    def plot_progress(self):
        
        # Clear previous plot data
        self.ax_goal.clear()     
          
        if pd.isnull(self.goal_date) or pd.isnull(self.goal):
            return        
               
        # today date with zeros time
        today = date.today() 
        tm = datetime.time(0)
        date_today = datetime.datetime.combine(today, tm)
        df_period = self.df[(self.df.index >= self.goal_date) & (self.df.index <= date_today)]
        
        df_spending = df_period[df_period['Category'] != 'Income']
        df_income = df_period[df_period['Category'] == 'Income']
        
        if df_income.empty:
            # balance =  - df_spending.groupby([pd.Grouper(freq = 'Y')]).sum().iloc[0, 0] 
            balance =  - df_spending['Amount'].sum()

        else:
            # balance = df_income.groupby([pd.Grouper(freq = 'Y')]).sum().iloc[0, 1] - df_spending.groupby([pd.Grouper(freq = 'Y')]).sum().iloc[0, 1] 
            balance =  df_income['Amount'].sum() - df_spending['Amount'].sum()

        progress_ratio = balance/self.goal       
        
        if progress_ratio >= 0:
            
            self.ax_goal.pie([np.min([progress_ratio, 1]), 1 - np.min([progress_ratio, 1])], wedgeprops={'width':0.3} , startangle = 90, counterclock = False, colors=['#5DADE2', '#515A5A'])
        
        else:
            
            self.ax_goal.pie([np.min([-progress_ratio, 1]), 1 - np.min([-progress_ratio, 1])], wedgeprops={'width':0.3} , startangle = 90, colors=['#ff0000', '#515A5A'])
        
      
        self.ax_goal.annotate(str(round(balance)), (0,0), weight = 'bold', fontsize = 12, ha='center', va='center')
        # self.fig_goal.tight_layout()
        # Redraw the canvas       
        self.canvas_goal.draw()
        
    def plot_all(self):
        
        self.plot_categories()
        self.plot_months()
        self.plot_progress()
        
    def validate_number(self, P):
        
        if P: # if not empty           
            try:
                float(P)
            except:
                return False
            
        self.show_message()    
        return True
        
    def on_invalid_number(self):
       """
       Show the error message if the data is not valid
       
       """
       self.show_message('Please enter a valid number !!!')
       
    def validate_date(self, P):
        
        if P: # if not empty           
            try:
                datetime.datetime.strptime(P, '%d-%m-%Y')
            except:
                return False
            
        self.show_message()    
        return True
        
    def on_invalid_date(self):
       """
       Show the error message if the data is not valid
       
       """
       self.show_message('Please enter a valid date format !!!')
        
    def show_message(self, error=''):
        
        self.error_label['text'] = error
        
    def DisplayDF(self):
        """
        Show and manipulate the data
        
        """
        frame = tk.Toplevel(self.root) #this is the new window
        df = self.df.reset_index()
        # df['Date'] = df['Date'].apply(lambda x: x.date())
        self.table = Table(frame, dataframe = df, showtoolbar=True, showstatusbar=True)
        self.table.bind("<Destroy>", self.on_table_closing) 
        self.table.show()
        
    def on_table_closing(self, event):
        
       msg_box = tk.messagebox.askquestion('Close Table', 'Do you want to save the data to online file?', icon = 'warning')
       
       if msg_box == 'yes':
           # Retrieve the modified DataFrame from the PandasTable widget
           modified_df = event.widget.model.df
           # Update self.data_frame with the modified DataFrame
           self.df = modified_df.set_index('Date')
           self.plot_all()
       
    def append_to_csv(self, entry):
        
        df = pd.DataFrame(entry)
        
        # append data frame to CSV file
        df.to_csv('spending.csv', mode='a', index=False, header=False)
        
        # on event functions
    def on_month_selection(self, event):
                
        self.plot_categories()
        
    def on_category_selection(self, event):
                
        self.plot_months()   
        
    def on_closing(self):
        
        self.df.to_csv('spending.csv')
        # update file if working in online regime
        if self.file_id is not None:
            DriveHandle.update_file(self.drive, 'spending.csv', self.file_id)
        self.root.destroy()
                      


if __name__ == "__main__":
    
    root = tk.Tk()  # Create an instance of the Tk class
    # root.geometry("1200x700")
    # root = ThemedTk(theme = "winxblue", gif_override=True)
    
    app = SpendingTrackerApp(root)  # Create an instance of your application class, passing the root window as an argument
    root.mainloop()  # Start the Tkinter event loop


