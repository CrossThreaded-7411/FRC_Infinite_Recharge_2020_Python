from datetime import datetime
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import tkinter as tk
from tkinter import filedialog

# Needed for tkinter
root = tk.Tk()
root.withdraw()

# Opens up a tkinter file dialog box
file_path = filedialog.askopenfilename(title='Select Log File',
                                       filetypes=(('log files', '*.log'),
                                                  ('all files', '*.*')))

# Tkinter file dialog box by default give you the whole path.
# Wanted to put the file name in the plot window title so this extracts it.
file_name = file_path.split('/').pop()

# Only keep data from the log file that has a specific level
# Specify the level here
# Option: [SEVERE], [WARNING], [INFO], [FINE], [FINER], [FINEST]
dataFlag = '[INFO]'

# Loop through the log file and parse it line by line
with open(file_path) as LogFile:
    data_list = []

    #Go through each line in the file and run ParseLine() on it
    for index, line in enumerate(LogFile):
        if dataFlag in line:
            # line = line.replace('\n', '')
            # line = line.replace(':', '')
            data_list.append(line.split(' '))
    
    # Massage the data coming in from ascii file into a pandas dataframe
    df = pd.DataFrame(data_list, columns=['Time', 'Level', 'Name', 'Value'], dtype='string')
    df['Time'] = pd.to_timedelta(df['Time'], unit='sec').dt.total_seconds()
    df['Time'] = df['Time'] - df['Time'].iloc[0]
    df['Level'] = df['Level'].str.replace('\[|\]:', '', regex=True)
    df['Name'] = df['Name'].str.replace(':', '', regex=True)
    df['Value'] = df['Value'].str.replace('\n', '', regex=True)
    df['Value'] = pd.to_numeric(df['Value'])

    # Pull data by channel from dataframe
    battery_voltage = df.loc[df['Name'] == 'Battery_Voltage']
    lift_raise_current = df.loc[df['Name'] == 'Raise_Current']
    lift_slide_current = df.loc[df['Name'] == 'Lift_Slide']
    shooter_top_current = df.loc[df['Name'] == 'Top_Shooter']
    shooter_bottom_current = df.loc[df['Name'] == 'Bottom_Shooter']
    shooter_turret_current = df.loc[df['Name'] == 'Turret']
    collector_current = df.loc[df['Name'] == 'Collector']
    drivetrain_RR_current = df.loc[df['Name'] == 'Drivetrain_RR']
    drivetrain_RF_current = df.loc[df['Name'] == 'Drivetrain_RF']
    drivettrain_LF_current = df.loc[df['Name'] == 'Drivettrain_LF']
    drivetrain_LR_current = df.loc[df['Name'] == 'Drivetrain_LR']
    drivetrain_RR_current = df.loc[df['Name'] == 'Drivetrain_RR']
    drivetrain_RF_current = df.loc[df['Name'] == 'Drivetrain_RF']
    drivetrain_LF_current = df.loc[df['Name'] == 'Drivettrain_LF']
    drivetrain_LR_current = df.loc[df['Name'] == 'Drivetrain_LR']
    dunno1 = df.loc[df['Name'] == 'Lift_Slide']
    dunno2 = df.loc[df['Name'] == 'Lift_Raise']

    # Plot data
    plt.figure('Log File Plots')
    plt.suptitle(file_name)
    ax1 = plt.subplot(221)
    ax1.plot(battery_voltage['Time'], battery_voltage['Value'], 'b', label='Battery')
    ax1.set(ylabel='Battery (volts)', ylim=(0, 14))
    ax1.legend(loc='upper right').set_draggable(True)
    ax1.grid(True)

    ax2 = plt.subplot(222, sharex=ax1)
    ax2.plot(lift_slide_current['Time'], lift_slide_current['Value'], 'r', label='Lift Slide')
    ax2.plot(lift_raise_current['Time'], lift_raise_current['Value'], 'b', label='Lift Raise')
    ax2.set(xlabel='Time', ylabel='Current (amps)', ylim=(0, 80))
    ax2.legend(loc='upper right').set_draggable(True)
    ax2.grid(True)

    ax3 = plt.subplot(223, sharex=ax1)
    ax3.plot(shooter_top_current['Time'], shooter_top_current['Value'], 'g', label='Top Motor')
    ax3.plot(shooter_bottom_current['Time'], shooter_bottom_current['Value'], 'm', label='Bottom Motor')
    ax3.plot(shooter_turret_current['Time'], shooter_turret_current['Value'], 'r', label='Turret Motor')
    ax3.plot(collector_current['Time'], collector_current['Value'], 'b', label='Collector Motor')
    ax3.set(xlabel='Time', ylabel='Current (amps)', ylim=(0, 80))
    ax3.legend(loc='upper right').set_draggable(True)
    ax3.grid(True)

    ax4 = plt.subplot(224, sharex=ax1)
    ax4.plot(drivetrain_RR_current['Time'], drivetrain_RR_current['Value'], 'g', label='Drivetrain RR Motor')
    ax4.plot(drivetrain_RF_current['Time'], drivetrain_RF_current['Value'], 'm', label='Drivetrain RF  Motor')
    ax4.plot(drivetrain_LF_current['Time'], drivetrain_LF_current['Value'], 'r', label='Drivetrain LF  Motor')
    ax4.plot(drivetrain_LR_current['Time'], drivetrain_LR_current['Value'], 'b', label='Drivetrain LR  Motor')
    ax4.set(xlabel='Time', ylabel='Current (amps)', ylim=(0, 80))
    ax4.legend(loc='upper right').set_draggable(True)
    ax4.grid(True)

    mplcursors.cursor()
    plt.show()