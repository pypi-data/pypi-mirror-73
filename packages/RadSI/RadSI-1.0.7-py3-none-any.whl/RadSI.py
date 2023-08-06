# -*- coding: utf-8 -*-
"""
Simple command-line interface for a radiactove source inventory
Author: Matthew Durbin
Date: Tue July 07 2020
"""
import fire
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class RadSI(object):
    """
    RadSI interacts with a saved inventory (inventory.csv) to keep track of 
    source activities via a pandas dataframe. Entries to the inventory can be
    made, and the activity can be predicted now, or at a specified time. 
    halflife.csv acts as a libraty for isotopic half lifes
    """

    def load_inventory():
        """
        Loads "inventory.csv" with the source name as the index, and R_Date
        Column read in as a datetime 
        """
        return pd.read_csv("inventory.csv", index_col=0, parse_dates=["R_Date"])

    def load_halflife():
        """
        Loads "halflife.csv" with the isotope as the index.
        half life values are in seconds
        """
        return pd.read_csv("halflife.csv", index_col=0)

    def elapsed_time(time1, time2):
        """
        Returns the absolute value of the time elapsed between two datetimes
        in units of seconds
        time1 - first datetime
        time2 - second datetime
        """
        elapsed = np.abs(timedelta.total_seconds(time1 - time2))
        return elapsed

    def convert(quantity, unit1, unit2):
        """
        Converts from unit1 to Bq,then Bq to unit 2
        quantity - quantity to be converted 
        unit1 - unit to be converted
        unit2 - unit converted to
        """
        con = {"cf": [37e12, 37e9, 37e6, 37e3, 37, 1e12, 1e9, 1e6, 1e3, 1]}
        con_df = pd.DataFrame(
            con,
            index=["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"],
        )
        mid = quantity * con_df.at[unit1, "cf"]
        converted = mid / con_df.at[unit2, "cf"]
        return converted

    def INITIALIZE(self):
        """
        Initializes two CSV files in the current directory:
        inventory.csv - this will be blank until a source is added and acts as
        the main radiation source inventory through out
        halflife.csv - this will contain several included isotopes and thier
        halflifes (in seconds)
        Both fils can be manipulated mannually, or thourgh the CLI
        caution: CLI manipulation ensures correct format, manual manipulation
        does not
        """
        t = open("inventory.csv", "w")
        t.write(",Isotope,R_Date,R_Activity,Unit")
        t.close()
        hl = {
            "Half-Life": [
                6378998.4,
                165879360,
                838080,
                951441120,
                11955686.4,
                426902832,
                83475792,
                1468800,
                5149440,
                32166720,
                49164624000,
                21624.12,
                237513.6,
            ]
        }
        hl_df = pd.DataFrame(
            hl,
            index=[
                "Ir-192",
                "Co-60",
                "Cs-131",
                "Cs-137",
                "Po-210",
                "Eu-152",
                "Cf-252",
                "Pd-103",
                "I-125",
                "Ru-106",
                "Ra-226",
                "T-99m",
                "Mo-99",
            ],
        )
        hl_df.to_csv("halflife.csv")
        print(
            """
               _/_/_/_/                           _/_/_/_/    _/_/_/_/_/
              _/      _/                   _/    _/      _/      _/
             _/      _/                   _/      _/    _/      _/
            _/_/_/_/      _/_/_/     _/_/_/   _/    _/         _/
           _/      _/    _/  _/     _/  _/   _/      _/       _/
          _/        _/  _/_/_/_/   _/_/_/    _/_/_/_/    _/_/_/_/_/
         ___________________________________________________________
             
              Welcome to RadSI: The Radiation Source Inventory
         ___________________________________________________________
              
              Authored by Matthew Durbin - 2020
              
              Github repo: https://github.com/matthewdurbin/RadSI.git
              
              Add your first source with ADD
              
              For help: HELP
              """
        )

    def CONVERT(self, quantity, unit1, unit2, round_to=3):
        """
        Converts from unit1 to Bq,then Bq to unit 2
        quantity - quantity to be converted 
        unit1 - unit to be converted
        unit2 - unit converted to
        round_to - number of digits to round()
        """
        con = {"cf": [37e12, 37e9, 37e6, 37e3, 37, 1e12, 1e9, 1e6, 1e3, 1]}
        con_df = pd.DataFrame(
            con,
            index=["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"],
        )
        if unit1 in con_df.index:
            if unit2 in con_df.index:
                mid = quantity * con_df.at[unit1, "cf"]
                converted = round(mid / con_df.at[unit2, "cf"], round_to)
                print(quantity, unit1, "equals", converted, unit2)
            else:
                print(
                    unit2
                    + " is not an allowed unit. Use HELP for a list of allowed units"
                )
        else:
            print(
                unit1 + " is not an allowed unit. Use HELP for a list of allowed units"
            )

    def INVENTORY(self):
        """
        Prints the current invnetory (invetory.csv)
        """
        try:
            inventory = RadSI.load_inventory()
            print(inventory)
        except:
            print("No inventory to be found. Try INITIALIZE")

    def LIBRARY(self):
        """
        Prints the current halflife library (halflife.csv)
        """
        halflife = RadSI.load_halflife()
        print(halflife)

    def ADD(self, name, isotope, date, activity, unit):
        """
        Adds a new source to the inventory and updates invetory.csv
        name - reference name of a specific source
        isotope - isotope of the source. Format: El-## (element-isotope no)
        date - datetime of referenced activity
        activity - activity of the source at the referenced datetime
        unit - units used for referenced activity
        """
        new = pd.DataFrame(
            [[isotope, date, activity, unit]],
            index=[name],
            columns=["Isotope", "R_Date", "R_Activity", "Unit"],
        )
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        units = ["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"]
        if new.at[name, "Isotope"] in halflife.index:
            if name in inventory.index:
                print(
                    name
                    + " is already is use. Try a new name, or use DELETE to free the name"
                )
            else:
                if unit in units:
                    inventory = inventory.append(new)
                    inventory.to_csv("inventory.csv")
                else:
                    print(
                        unit
                        + " is not an allowed unit. Use HELP for a list of allowed units"
                    )
        else:
            print(
                isotope
                + " is not an isotope in the Halflife Library. Use LIBRARY_ADD to ADD"
            )

    def LIBRARY_ADD(self, isotope, halflife):
        """
        Adds a new isotope to the halflife library and updates halflife.csv
        isotope - isotope to be added. Format: El-## (element-isotope no)
        halflife - halflife of that isotope in seconds
        """
        new = pd.DataFrame([[halflife]], index=[isotope], columns=["Half-Life"],)
        halflife = RadSI.load_halflife()
        halflife = halflife.append(new)
        halflife.to_csv("halflife.csv")

    def DELETE(self, name):
        """
        Deletes a source from the inventory and updates invetory.csv
        name - reference name of a specific source
        """
        inventory = RadSI.load_inventory()
        inventory = inventory.drop([name])
        inventory.to_csv("inventory.csv")

    def NOW(self, name, round_to=3):
        """
        Calculates the current source activity based on the halflife and
        time elapsed since calibrated/fererenced activity, in the unites
        of the reference activity
        name - reference name of a specific source in the inventory
        round_to - number of digits to round()
        """
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        isotope = inventory.at[name, "Isotope"]
        unit = inventory.at[name, "Unit"]
        time1 = inventory.at[name, "R_Date"]
        time2 = datetime.now()
        delta_t = RadSI.elapsed_time(time1, time2)
        t_hl = halflife.at[isotope, "Half-Life"]
        A_0 = inventory.at[name, "R_Activity"]
        A = A_0 * np.e ** (-delta_t * np.log(2) / t_hl)
        units = ["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"]
        if unit in units[:4] and 0.00001 <= A < 0.01:
            unit2 = units[units.index(unit) + 1]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:3] and 1e-8 <= A < 1e-5:
            unit2 = units[units.index(unit) + 2]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:2] and 1e-11 <= A < 1e-8:
            unit2 = units[units.index(unit) + 3]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:1] and A < 1e-11:
            unit2 = units[units.index(unit) + 4]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:8] and 1e-5 <= A < 0.01:
            unit2 = units[units.index(unit) + 1]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:7] and 1e-8 <= A < 1e-5:
            unit2 = units[units.index(unit) + 2]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:6] and A < 1e-8:
            unit2 = units[units.index(unit) + 3]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:5] and A < 1e-11:
            unit2 = units[units.index(unit) + 4]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        print("The activity of " + name + " is currently:")
        print(round(A, round_to), unit)

    def ON(self, name, date, round_to=3):
        """
        Calculates the source activity at a specified datetime based on the
        half life and time elapsed between the calibrated/referenced activity
        and the specified datetime, in the units of the refernce activity
        name - reference name of a specific source in the inventory
        date - datetime to calculate the activity
        round_to - number of digits to round()
        """
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        isotope = inventory.at[name, "Isotope"]
        unit = inventory.at[name, "Unit"]
        time1 = inventory.at[name, "R_Date"]
        time2 = pd.to_datetime(date)
        delta_t = RadSI.elapsed_time(time1, time2)
        t_hl = halflife.at[isotope, "Half-Life"]
        A_0 = inventory.at[name, "R_Activity"]
        A = A_0 * np.e ** (-delta_t * np.log(2) / t_hl)
        units = ["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"]
        if unit in units[:4] and 0.00001 <= A < 0.01:
            unit2 = units[units.index(unit) + 1]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:3] and 1e-8 <= A < 1e-5:
            unit2 = units[units.index(unit) + 2]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:2] and 1e-11 <= A < 1e-8:
            unit2 = units[units.index(unit) + 3]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[:1] and A < 1e-11:
            unit2 = units[units.index(unit) + 4]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:8] and 1e-5 <= A < 0.01:
            unit2 = units[units.index(unit) + 1]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:7] and 1e-8 <= A < 1e-5:
            unit2 = units[units.index(unit) + 2]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:6] and A < 1e-8:
            unit2 = units[units.index(unit) + 3]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2
        elif unit in units[4:5] and A < 1e-11:
            unit2 = units[units.index(unit) + 4]
            A = RadSI.convert(A, unit, unit2)
            unit = unit2

        print("The activity of " + name + " on " + date + " will be:")
        print(round(A, round_to), unit)

    def ALL(self, date="now", round_to=3):
        """
        Calculates the activity of each source in the inventory now or
        at a specified datetime based on the half life and time elapsed between
        the referenced activities and the specified datetime 
        date - datetime to calculate the activity
        round_to - number of digits to round()
        """
        now = datetime.now()
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        As = pd.DataFrame(index=inventory.index)
        As["Isotope"] = ""
        As["Activity"] = ""
        As["Unit"] = ""
        for i in range(len(inventory)):
            name = inventory.index[i]
            isotope = inventory.at[name, "Isotope"]
            unit = inventory.at[name, "Unit"]
            time1 = inventory.at[name, "R_Date"]
            time2 = pd.to_datetime(date)
            delta_t = RadSI.elapsed_time(time1, time2)
            t_hl = halflife.at[isotope, "Half-Life"]
            A_0 = inventory.at[name, "R_Activity"]
            A = A_0 * np.e ** (-delta_t * np.log(2) / t_hl)
            units = ["kCi", "Ci", "mCi", "uCi", "nCi", "TBq", "GBq", "MBq", "kBq", "Bq"]
            if unit in units[:4] and 0.00001 <= A < 0.01:
                unit2 = units[units.index(unit) + 1]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[:3] and 1e-8 <= A < 1e-5:
                unit2 = units[units.index(unit) + 2]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[:2] and 1e-11 <= A < 1e-8:
                unit2 = units[units.index(unit) + 3]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[:1] and A < 1e-11:
                unit2 = units[units.index(unit) + 4]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[4:8] and 1e-5 <= A < 0.01:
                unit2 = units[units.index(unit) + 1]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[4:7] and 1e-8 <= A < 1e-5:
                unit2 = units[units.index(unit) + 2]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[4:6] and A < 1e-8:
                unit2 = units[units.index(unit) + 3]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2
            elif unit in units[4:5] and A < 1e-11:
                unit2 = units[units.index(unit) + 4]
                A = RadSI.convert(A, unit, unit2)
                unit = unit2

            As.at[name, "Isotope"] = isotope
            As.at[name, "Activity"] = round(A, round_to)
            As.at[name, "Unit"] = unit

        if date == "now":
            print("The current activities of your inventory are:")
        else:
            print("The activities of your inventory on " + date + " will be:")
        print(As)

    def WHEN(self, name, A, units="R_unit"):
        """
        Calculates the datetime that a source will or was a specified activity 
        in unites specified
        name - name of the source
        A - activity to calculate to solve 'when' for
        units - units of A (does not have to be units of name in the inventory)
        """
        a_units = [
            "kCi",
            "Ci",
            "mCi",
            "uCi",
            "nCi",
            "TBq",
            "GBq",
            "MBq",
            "kBq",
            "Bq",
            "R_unit",
        ]
        if units in a_units:
            inventory = RadSI.load_inventory()
            halflife = RadSI.load_halflife()
            isotope = inventory.at[name, "Isotope"]
            t_hl = halflife.at[isotope, "Half-Life"]
            A_0 = inventory.at[name, "R_Activity"]
            time1 = inventory.at[name, "R_Date"]
            unit = inventory.at[name, "Unit"]
            if units == "R_unit":
                units = unit
            else:
                A_0 = RadSI.convert(A_0, unit, units)
            delta_t = -t_hl * np.log(A / A_0) / np.log(2)
            time2 = time1 + timedelta(0, delta_t)
            if delta_t > 0:
                print(name + " will be", A, units + " on:")
            else:
                print(name + " was", A, units + " on:")
            print(time2.strftime("%m-%d-%Y %H:%M:%S"))
        else:
            print(
                units + " is not an allowed unit. Use HELP for a list of allowed units"
            )

    def PLOT(self, name, date=datetime.now()):
        """
        Makes a plot of the activity of a specified source from the original
        referenced activity, untill the specified datetime.
        name - reference name of a specific source in the inventory
        date - datetime bound to plot the activity. The current datetime is
        usedi if not specified
        """
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        isotope = inventory.at[name, "Isotope"]
        unit = inventory.at[name, "Unit"]
        time_0 = pd.to_datetime(inventory.at[name, "R_Date"])
        time_f = pd.to_datetime(date)
        delta_t = RadSI.elapsed_time(time_0, time_f)
        time = np.linspace(0, delta_t, 100)
        t_hl = halflife.at[isotope, "Half-Life"]
        A_0 = inventory.at[name, "R_Activity"]
        A = A_0 * np.e ** (-time * np.log(2) / t_hl)
        labels = [
            time_0.strftime("%b %d %Y %H:%M"),
            (time_0 + timedelta(0, delta_t / 3)).strftime("%b %d %Y %H:%M"),
            (time_0 + 2 * timedelta(0, delta_t / 3)).strftime("%b %d %Y %H:%M"),
            time_f.strftime("%b %d %Y %H:%M"),
        ]
        plt.plot(time, A, color="black")
        plt.grid()
        plt.ylabel("Activity in " + unit)
        plt.title("Activity of " + name)
        plt.xticks(np.linspace(0, delta_t, 4), labels, rotation=25)
        plt.tight_layout()
        plt.show()

    def LOGPLOT(self, name, date=datetime.now()):
        """
        Makes a log plot of the activity of a specified source from the original
        referenced activity, untill the specified datetime.
        name - reference name of a specific source in the inventory
        date - datetime bound to plot the activity. The current datetime is
        usedi if not specified
        """
        inventory = RadSI.load_inventory()
        halflife = RadSI.load_halflife()
        isotope = inventory.at[name, "Isotope"]
        unit = inventory.at[name, "Unit"]
        time_0 = pd.to_datetime(inventory.at[name, "R_Date"])
        time_f = pd.to_datetime(date)
        delta_t = RadSI.elapsed_time(time_0, time_f)
        time = np.linspace(0, delta_t, 100)
        t_hl = halflife.at[isotope, "Half-Life"]
        A_0 = inventory.at[name, "R_Activity"]
        A = A_0 * np.e ** (-time * np.log(2) / t_hl)
        labels = [
            time_0.strftime("%b %d %Y %H:%M"),
            (time_0 + timedelta(0, delta_t / 3)).strftime("%b %d %Y %H:%M"),
            (time_0 + 2 * timedelta(0, delta_t / 3)).strftime("%b %d %Y %H:%M"),
            time_f.strftime("%b %d %Y %H:%M"),
        ]
        plt.semilogy(time, A, color="black")
        plt.grid()
        plt.ylabel("Activity in " + unit)
        plt.xticks(np.linspace(0, delta_t, 4), labels, rotation=25)
        plt.tight_layout()
        plt.show()

    def HELP(self):
        """
        Quick help guide
        """
        print(
            """
              To view your current inventory:
                  INVENTORY
                  
              To add a source: 
                  ADD name isotope referencedate referenceactivity activity units
                  
              To calculate the current activty of a source:
                  NOW name
                  
             To calculate the activity of a source at a specified date time:
                 ON name datetime
                 
             To calculate when a source will be or was a certain activity:
                 WHEN name activity units
                 
             Example Datetime format:
                 Chrsitmas day in 2009: 12-25-2009 or 12-25-09
                 When the ball will drop in TimeSquare next year: 01-01-2021-00:00 or 1-1-21
                 1 pm on Augsut 31st, 2030: 08-20-2030-13:00 or 8-20-30-13
                 
            Allowed unitits of activity:
                kCi, Ci, mCi, uCi (microcurie), nCi, TBq, GBq, MBq, kBq, Bq
              """
        )


def main():
    fire.Fire(RadSI)


if __name__ == "__main__":
    main()
