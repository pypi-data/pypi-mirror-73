Flight Control
==============
Flight Control is a python package for storing, tracking, and analyzing flight data.
Example:

    import flightcontrol
    import time

    #Create a new instance of the AltitudeLogger class
    al = flightcontrol.AltitudeLogger()

    #Simulate altitude changing
    al.LogAltitude(50)
    time.sleep(0.5)
    al.LogAltitude(45)
    time.sleep(0.5)
    al.LogAltitude(40)
    time.sleep(0.5)
    al.LogAltitude(35)

    #Get rate of change
    roc = al.RateOfChange_cm_per_second()
    print(roc)

    #Get seconds until impact
    #This will only return a value if the altitude is dropping
    sui = al.SecondsUntilImpact()
    print(sui)