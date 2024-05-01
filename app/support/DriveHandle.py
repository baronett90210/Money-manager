# -*- coding: utf-8 -*-
"""
Google Drive management

@author: Anton Baranikov

"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import numpy as np
import os

def login():
    
    """
    Authentification using "mycreds.txt". 
    If doesn't exist then "mycreds.txt" will be created after the first manual login in the browser

    """
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    
    if gauth.credentials is None:
        # to avoid the problem of the token refresh       
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:

        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
        
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    # Create GoogleDrive instance
    drive = GoogleDrive(gauth)  
    return drive

def update_file(drive, local_file, file_id):
    """
    updates file on the drive based on the local file

    """
    file_drive = drive.CreateFile({'id': file_id })
    # Set the content of the file to the local CSV file
    file_drive.SetContentFile(local_file)
    # Upload the file to Google Drive
    file_drive.Upload()
    
def download_file(drive, local_file, file_id):    
    """
    downloads file from the drive and writes the content to a local file

    """
    file_drive = drive.CreateFile({'id': file_id })
    file_drive.GetContentFile(local_file) 

def create_file(drive, local_file):
    """
    creates a new local csv if doesn't exist and creates file on the drive

    """
    # create csv locally if it doesnt exist
    dummy_csv_local(local_file)
    # create file on drive
    file_drive = drive.CreateFile({'title': local_file})
    # Set the content of the file to the local CSV file
    file_drive.SetContentFile(local_file)
    # Upload the file to Google Drive
    file_drive.Upload()

def dummy_csv_local(local_file):
    """
    creates a new local dummy csv if doesn't exist 

    """
    # create csv if it doesnt exist
    if not os.path.exists(local_file):
        
        df = pd.DataFrame({
            'Date': [np.nan],
            'Category': [np.nan],
            'Amount': [np.nan],
            'Goal': [np.nan]
            })
        df = df.set_index('Date')
        # data frame to CSV file
        df.to_csv(local_file)
        
