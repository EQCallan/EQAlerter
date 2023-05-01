#    This file is part of EQAlerter.

#    EQAlerter is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    EQAlerter is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with EQAlerter.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import sys
import os
import platform

from os.path import isfile

from config import *

# DepCheck - verifies dependencies are met prior to running
#            also contains a method to validate users
class DepCheck:

    def __init__(self):
        print("DEBUG: Checking dependencies")

# verify that the SAPI TTS engine is installed
    def verifyFlite():
        print("DEBUG: Checking SAPI TTS engine")

        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            print("DEBUG: SAPI TTS engine is installed")
        except ImportError:
            print("")
            print("ERROR: SAPI TTS engine is not installed on your system. Please install it and try again.")
            sys.exit()

# verify that Windows Terminal is installed
    def verifyWindowsTerminal():
        print("DEBUG: Windows Terminal install path:")
        if not isfile("C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_*\\wt.exe"):
            print("")
            print("ERROR: Windows Terminal is either not installed on the system or not in your path. Please install it from the Microsoft Store or from source and add it to your path")
            sys.exit()
        print("")


# verify that LOG=TRUE in eqclient.ini
    def verifyLogging(eqhome):
        # open eqclient.ini for reading
        # search the file for LOG=TRUE
        # if not found error out
        # else proceed on
        if 'Log=1' in open(eqhome+"eqclient.ini").read():
            print("DEBUG: Logging is enabled")
        else:
            print("ERROR: Please enable logging in your 'eqclient.ini' file by setting Log=TRUE")
            sys.exit()

# check for character log file
    def getLogFile(eqhome, character, logpath):
        logfile = DepCheck.pathScan(eqhome, logpath)
        if logfile:
            print("\n\nMonitoring [%s] using the following log file: %s \n" % (character, logfile))
            return logfile
        else:
            print("\n\nERROR: No chat log file exists for the selected character.\n")
            print("Please verify that 'Log=1' in 'eqclient.ini',\n")
            print("then log the character into the game and re-run this utility.\n")
            sys.exit()

    def pathScan(base_folder, filename):
        if os.path.isfile(os.path.join(base_folder, filename)):
            return os.path.join(base_folder, filename)
        if os.path.isfile(os.path.join(base_folder, "Logs", filename)):
            return os.path.join(base_folder, "Logs", filename)
        return None


#End of Class