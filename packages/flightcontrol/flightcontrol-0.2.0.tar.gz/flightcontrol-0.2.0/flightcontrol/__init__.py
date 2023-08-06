import time
import datetime
import random
import csv

class AltitudeLogger:
    AltitudeLogs = []

    def LogAltitude(self, altitude_cm):
        adtp = AltitudeDateTimePair()
        adtp.altitude_cm = altitude_cm
        adtp.timestamp = datetime.datetime.now()

        #add to altitude log
        self.AltitudeLogs.append(adtp)

    def RateOfChange_cm_per_second(self):
        if self.AltitudeLogs.__len__() < 2:
            raise Exception("There was not a sufficient number of Altitude logs available to complete the request.")
        else:
            last_alt = self.AltitudeLogs[self.AltitudeLogs.__len__()-1]
            penultimate_alt = self.AltitudeLogs[self.AltitudeLogs.__len__()-2]

            #get altitude change
            alt_change = last_alt.altitude_cm - penultimate_alt.altitude_cm

            #Get Elapsed time (in seconds)
            td = last_alt.timestamp - penultimate_alt.timestamp
            elapsed_seconds = td.total_seconds()

            rate = alt_change / elapsed_seconds
            return rate

    def SecondsUntilImpact(self):
        if self.AltitudeLogs.__len__() < 2:
            raise Exception("There was not a sufficient number of Altitude logs available to complete the request.")

        # If we are going up, we will never make an impact!
        if self.RateOfChange_cm_per_second() > 0:
            return float("NaN")
        else:
            last_known_alt = self.AltitudeLogs[self.AltitudeLogs.__len__()-1]
            seconds_til_impact = last_known_alt.altitude_cm / self.RateOfChange_cm_per_second()
            seconds_til_impact = seconds_til_impact * -1
            return seconds_til_impact
    
    def ExportAltitudeLogsToCsv(self, export_to: str):
        file = open(export_to, "w", newline="")
        writer = csv.writer(file)

        RowsToWrite = []

        # Get the header
        x = []
        x.append("Time Stamp")
        x.append("Altitude (cm)")
        RowsToWrite.append(x)

        # Get the altitude logs
        for al in self.AltitudeLogs:
            x = []
            x.append(str(al.timestamp))
            x.append(str(al.altitude_cm))
            RowsToWrite.append(x)

        writer.writerows(RowsToWrite)
            

class AltitudeDateTimePair:
    altitude_cm = 0.0
    timestamp = datetime.datetime.now()

    