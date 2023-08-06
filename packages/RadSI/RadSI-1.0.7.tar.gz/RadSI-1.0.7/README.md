# RadSI - The Radiation Source Inventory

RadSI is a simple command-line interface (CLI) method of tracking the activities in your inventory of radioactive sources.

![RadSI_Demo](RadSI.PNG)

## Motivation 
As is often the case, each source in a lab or hospital setting gets some sort of binder or massive chart that contains pages of look up tables. Thus to get the activity of a specific source, one has to find the binder or the chart and search through untill you find the right cell that gives you the activity of your source at a specific time.

If you add a new source to your inventory, you have to make a new binder. If you don't have the time you need in the look up table, you have to do some manual interpolation or full calculation to get what you need. You could use spreadsheet software, but that comes with it's own inconveniences. 

RadSI provides a more automated approach, in which you simply enter the source in your logged inventory and your activity is calculated - down to second if need be!

## Quick Install/Initialization From Scratch (No Python on your computer)
While there are ultimetly many ways to go from no Python to using RadSI, here is how I would do it. (If you have Anaconda already, skip step 1. If you have Python, and do not want to use the Anaconda Prompt, skip step 1 & 2, use the terminal of your choice making sure your path/activation/etc... conditions are met)

1. Download the latest version of [Anaconda](https://www.anaconda.com/products/individual). This is an open source Python distrubtuion, that comes with many of the packages you need. No need to use a terminal, the webcite has install wizard type options.
2. Find and open the Anaconda Prompt. You can do this through the Anaconda Navigator, start menu, or by searching on your computer. 
3. Type the following into Anaconda Prompt. This downloads an additional package you need, that does not come with Anaconda.

        pip install fire
        
4. Now type (or copy & paste) the follwoing into the Anaconda Prompt. This downloads RadSI.

        pip install -i https://test.pypi.org/simple/ RadSI
        
5. Change your directory to where you want to store your inventory (in other words, navigate to the "folder" you want to use). This can be done by typing "cd" and then the path. 
6. Type the following command to initialize. 

        RadSI INITIALIZE

This should return a welcome message. This will also create two CSV files and place them in your current directory: inventory.csv and halflife.csv. The former acts as your radiation source iventroy, containing your sources names, isotope, reference date, reference activity, and activity units. The latter is a library of isotopes and their corresponding half-lives in seconds to be used for calculations. Both can be manipulated directly, but it is reccomended to manipulate them via the RadSI CLI to insure propper formatting. When using RadSI, make sure you are in the directory that you INITIALIZE'd in so that RadSI can pull the inventory and library. To use multiple inventories (say for different labs or treatment rooms), simply initialize in seperate folders.


### Dependencies
The following pacakges are required, but don't worry about it if you've followed the steps above:
- setuptools
- pandas
- numpy
- matplotlib
- fire

## Documentation 

### Commands:
To use a command, simply type 

        RadSI COMMAND Parameters 
        
into your python terminal. For example:

        RadSI NOW calibration1
        
Will print the current activity of the source named 'calibration1' in your Inventory. Below is a list of available commands. If you are using Anaconda, open up the Anaconda Prompt.

INITIALIZE - this command must be executed first! It initializes two .csv files in your current directory:
1. inventory.csv- this is your radiation source inventory. Though blank at first, it can be maniuplated with ADD and DELETE
2. halflife.csv - this is your halflife library, with units of seconds. It comes prebuild with isotopes, but additional isotopes can be added with LIBARARY_ADD

INVENTORY - this simply prints the current inventory

LIBRARY - this simpy prints out the current halflife library

ADD - This adds a source to the inventory and updates inventory.csv. The paramaters are:  
- name        - this is the "nick name" of your specific source (Ex: medical1)  
- Isotope     - this is the isotope of your source, written as the elements initals dash mass number (Ex: Co-60)  
- R_Date      - this is the datetime at which your referenced activity was determined, written as month-day-year-hour:minute:second though not all timing info is needed. (Ex: 12-7-2019-12:30:00)  
- R_Activity  - this is the activity of your source at the referenced date time (Ex: 30)  
- Unit        - this is the units of activity for your source (Ex: mCi)  

LIBRARY_ADD - This adds a isotope tot he halflife library and updates halflife.csv. The Parameters are:
- Isotope     - this is the isotope to be added, written as the elements initals dash mass number (Ex: Co-60)
- halflife    - this is the halflife in seconds
        
DELETE - This deletes a source from the inventory and updates invetory.csv. The parameter is:
- name       - this is the "nick name" of your specific sourc (Ex: medical1)  
        
NOW - This calculates the current activity of the specified source. The paramter is:
- name       - this is the "nick name" of your specific sourc (Ex: medical1)  
        
ON - This calculates the activity of the specified source on a specified datetime. The parameters are:
- name       - this is the "nick name" of your specific sourc (Ex: medical1) 
- date       - this is the datetime at which you wish to calculate the activity of the specified source, written as month-day-year-hour:minute:second though not all timing info is needed. (Ex: 12-7-2019-12:30:00)  
        
PLOT - This allows the activity of a specified source to be plotted agaisnt time from the referenced datetime of that source
- name       - this is the "nick name" of your specific sourc (Ex: medical1)
- date       - this is the upperbound of the time plotted (Ex: 12-7-2019-12:30:00), written as month-day-year-hour:minute:second though not all timing info is needed. If left blank, the time is taken as now  

HELP- This simply prints a condensed version of this documentation 


#### A note on date and time

To handle time based calculations, dates and times are entered as month-day-year-hour:minute:second, though not all timing info is needed. The time portion is a 24 hour clock, making midnight and noon 00:00:00 and 12:00:00 resepctively. If no time is specified, midnight is assumed. If no day is specified, the first of the month is assumed. The format is somewhat robust, the following would all represent when the ball dropped in NYC on New Year's Day in 1999:

        01-01-1999:00:00:00   01-01-1999:00:00   01-01-1999:00   01-01-1999   01-01-99   1-1-99   1-99
 
The following would all represent the [time President Obama was born](https://obamawhitehouse.archives.gov/blog/2011/04/27/president-obamas-long-form-birth-certificate):

        08-04-1961-19:24:00   08-04-1961-19:24   08-04-61-19:24  8-4-61-19:24
        
For isotopes or calculations in which time on the order of hours are relevant, care should be taken to input the reference date in the timezone your "NOW" or "ON" calculations are being performed. 

## Feedback
If you use RadSI, I'd very much appreciate your feedback. Feel free to do so via github, or by emailing me at mdurbin@psu.edu.

#### Acknowledgements 
Thank you to Josh Gallagher and Josh Flygare for their helpful feedback so far. Additional thanks to Ryan Sheatsley for, with out knowing it, becoming a compsci mentor of sorts!
