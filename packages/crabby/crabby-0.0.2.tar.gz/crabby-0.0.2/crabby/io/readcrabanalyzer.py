import pandas as pd
import numpy as np
from glob import glob
import os
import platform
import time
import re

__all__ = ['readtoDataFrame', 'load_experiment_folder']

def readtoDataFrame(path, remove_time_date=False, get_experimental_details=True):
    """Reads a tab deliminated xl output from the Crab Analyzer Spike2 script into a pandas DataFrame

    INPUTS:
    ---------
    path: str, path to file, MUST BE xl NOT log output currently
    remove_time_date: boolean, whether or not to get absolute file time of each burst
    get_experimental_details: boolean, whether or not to get the experimental headers

    OUTPUTS:
    ---------
    dataframe: pd.DataFrame, dataframe of all the relevant full data for all neurons in file analyzed
    """
    start = False
    data = []
    dataframe = []
    
    # Open file and go through line by line it's contents
            
    with open(path) as f:
        lines = f.readlines()
        
        if get_experimental_details:
            details = dict(motor_pattern=lines[9],
                           experimental_manipulation=lines[8].replace('\t', '')) # This is making it still have \t\t\t\\t\t\t\t shit

        for i,line in enumerate(lines):
            
            # TODO: Add in here argument from up there
                
            if '\t' not in line:  # Skip through all the details of the experimental set-up
                continue

            if 'Neuron\tBurst' in line: # Relevant Starting Column Names for Neuron Full Data
                start = True
                itering = 0
                column_names = line[:-1].split('\t')
                continue

            if 'Neuron\t# of Bursts' in line: # Relevant Starting Column Names for Neuron Summary Data
                start = False
                dat = pd.concat(data, axis=1)
                dat = dat.T
                dat = dat.rename(mapper=dict(zip(dat.columns, column_names)),axis=1)
                dataframe.append(dat)
                data = []
            
            if start == False: # Don't care about any of the summary vals for now
                continue

            dat= list(map(string_convert, line[:-1].split('\t')))
            if itering == 0:
                neuron_name = dat[0]

            if itering > 0:
                dat[0] = neuron_name

            data.append(pd.DataFrame(dat))
            itering += 1

    dataframe = pd.concat(dataframe)
    
    # Necessary because on the last period analyzed instant. period and freq are labeled as "N/A" by output
    dataframe.replace("N/A", np.nan, inplace = True)
    dataframe = dataframe.dropna()
    
    # Remove redundant columns
    if remove_time_date:
        dataframe = dataframe.drop(labels=['Real Time of Burst Onset (sec)', 'Real Time of Burst Offset (sec)',],axis=1)
        
    if get_experimental_details:
        dataframe.loc[:,'Motor Pattern'] = pd.Series(details['motor_pattern'].split('  ')[-1][:-1].split('\t')[0], index=dataframe.index)
        dataframe.loc[:,'Experimental Manipulation'] = pd.Series(details['experimental_manipulation'].split('  ')[-1][:-1].split('\t')[0], index=dataframe.index)

    condition = find_condition_regrex(path)
    dataframe['Condition'] = condition
    # Try to add in the date
    try:
        date = np.array(path.split('/'))[np.array(['-' in x or '_' in x for x in path.split('/')])]
        date = date[0].replace('_', '-')

    except Exception as e: # TODO: Fix this kind of bad practice wherever it is
        print(e,'Defaulting to getting date from file metadata....')
        try:
            date = creation_date(path)
        except:
            print('Failed to get date from file metadata....')
            return dataframe

    dataframe['Date'] = date
    return dataframe


def load_experiment_folder(path, remove_time_date=False, get_experimental_details=True):
    """Reads folder of tab deliminated xl outputs from the Crab Analyzer into a pandas DataFrame
    INPUTS:
    --------
    path: str, path to folder containing pre, post, and exp file
    remove_time_date: boolean
    get_experimental_details: boolean,

    OUTPUTS:
    --------
    dataframe: pd.DataFrame, dataframe of all the relevant full data for all neurons analzyed

    """
    # Get all files, sort so it goes pre -> exp -> post; is there a better way?
    
    if path[-1] != '/':
        path = path +'/'

    folder_paths = sorted(glob(path + '*_xl'))
    
    dat = []
    #

    # TODO: Change 'Order' column out of this into readDataFrame...
    for i, path in enumerate(folder_paths):
        df = readtoDataFrame(path,
                             remove_time_date=remove_time_date,
                             get_experimental_details=get_experimental_details)
        print('Successfully load file at {}'.format(path))
        #condition = find_condition_regrex(path)

        #df['Condition'] = condition
        df['Order'] = i
        
        dat.append(df)

    # Make it all one data-table and add in a duty cycle variable
    df = pd.concat(dat)
    
    # Make sure you don't have any stupid string formatting of numbers
    check_numeric=['Burst#', '# of Spikes', 'Spike Frequency (Hz)', 
                   'Instantaneous Frequency (Hz)', 'Burst Duration (sec)', 
                   'Instantaneous Period (sec)']
    for column in check_numeric:
        df[column] = pd.to_numeric(df[column])
        
    try: # Handling in case numbers got interpretted as strings in the loading process
        df['Duty Cycle'] = df['Burst Duration (sec)']/df['Instantaneous Period (sec)']
    
    except Exception as e:
        print(e, 'attempting to resolve....')
        try:
            df['Burst Duration (sec)'] = pd.to_numeric(df['Burst Duration (sec)'])
            df['Instantaneous Period (sec)'] = pd.to_numeric(df['Instantaneous Period (sec)'])
            df['Duty Cycle'] = df['Burst Duration (sec)']/df['Instantaneous Period (sec)']
            print('Error resolved')
        
        except Exception as e: # If unable to resolve
            raise(e)
    #df['Date'] = date
    
    return df

# -------> Utility functions used above
def creation_date(path_to_file):
    """ Try to get the date that a file was created, falling back to when it was
    last modified if creation date isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    
    INPUTS
    --------
    path_to_file: str, the path to the file
    
    OUTPUTS
    --------
    the date of creation
    """
    if platform.system() == 'Windows':
        epoch_time = os.path.getctime(path_to_file)
    
    else:
        stat = os.stat(path_to_file)
        try:
            epoch_time = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux if this happens. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
    return time.strftime('%m-%d-%Y', time.localtime(epoch_time))

def find_condition_regrex(file_path):
    """Finds experimental condition if it is formatted such 'date_fileletter_condition_xl',
    INPUTS:
    --------
    file_path: str, path to folder containing excel experiment file


    OUTPUTS:
    --------
    match: str, corresponding condition of the experiment file

    NOTES:
    ----------
    Currently accepted file conditions are: fed hemo, unfed hemo, ccap, pre, post, saline
    """
    # make it so arbitrary capitalization does not throws off code
    file_path = file_path.lower()
    
    # Check if it's condition is "post"
    if re.search("post", file_path):
        # Check if there's any 0,1,2 etc. labeling for experiments w/ multiple of a thing
        if re.search("post[0-9]",file_path):

            match = re.search("post[0-9]",file_path)[0]
            match = match.replace('post', 'Post ')
            
        else:
            match = "Post"

    # Check if it's pre; saline
    elif re.search("pre", file_path):

        if re.search("pre[0-9]", file_path):
            match = re.search("pre[0-9]", file_path)[0]
            match = match.replace('pre', 'Pre ') # Include the numbering but put a space and capitilize
            
        else:
            match = 'Pre'
            
            
    # Check if it's ccap
    elif re.search('ccap', file_path):
        if re.search('ccap[0-9]', file_path):
            match = re.search('ccap[0-9]', file_path)[0]
            match = match.replace('ccap', 'CCAP ')
            
        else: 
            match='CCAP'
        
    # Need to put in something that tests CCAP + fed and unfed vs just ccap
    elif re.search('fed_hemo', file_path , flags=re.IGNORECASE):
        
        if re.search("unfed_hemo",file_path):
            if re.search('unfed_hemo[0-9]', file_path):
                match = re.search('unfed_hemo[0-9]', file_path)[0]
                match = match.replace('unfed_hemo', 'Unfed Hemo ')
            else:
                match = 'Unfed Hemo'

        elif re.search('fed_hemo[0-9]', file_path):
            match = re.search('fed_hemo[0-9]', file_path)[0]
            match = match.format('fed_hemo', 'Fed Hemo ')
        
        else:
            match = 'Fed Hemo'

    #elif re.search('hemo', file_path , flags=re.IGNORECASE):
        #match = 'Unfed Hemo'
        
    else:
        warning="Could not find a Condition match for path {}, Setting Condition as Unknown"
        print(warning.format(file_path))
        match = 'Unknown Condition'
        
    if re.search("hemo +", file_path):
        UserWarning("Hemolymph plus other things not currently available")

    return match

def get_digits(text):
    """Throw away fuction to get a string back from string of numbers and letters"""
    return ''.join(filter(str.isdigit, text))

def string_convert(string):
    """throw away function to handle type conversion of string to float"""
    try:
        return float(string)
    except ValueError:
        return string