import logging
import sys
import csv
import os
import gc
import pytz
from   logging.handlers import RotatingFileHandler
from   datetime import datetime
import time


############################################################
#
# Author: Michael Robinson ( michael.robinson1@kochind.com )
# Desc: This class is a set of help functions. Most of this
# class is used for application logging, but there are
# methods in here for doing the same requests in the same
# manner throughout the variouse application ( e.g. Timestamps ).
# You will see many references to the logging methods
# through the various applications that use this class.
# The parameters for logging are in the config file.
# You will see print statements in here because until
# the log file is properly set up logging cannot be used.
#
############################################################

from AppConfiguration import AppParametersHandler


class mcr_mclib():

    logger                = logging.getLogger(__name__)
    ApplicationName       = ""
    ApplicationConfigFile = ""
    LogToConsole          = "False"
    setupOk               = False
    defaultLogSize        = 5000
    defaultBackupCount    = 3

    ################################
    ################################
    @staticmethod
    def AppConfig():
        return(AppParametersHandler.getInstance())

    ################################
    ################################
    @staticmethod
    def Log():
        return(mcr_mclib.logger)

    ################################
    ################################
    @staticmethod
    def getApplicationName():
        return(mcr_mclib.ApplicationName)

    ################################
    ################################
    @staticmethod
    def getConfileFile():
        return(mcr_mclib.ApplicationConfigFile)

    ################################
    ################################
    @staticmethod
    def setConfileFile(pConfigFile):
        mcr_mclib.ApplicationConfigFile = pConfigFile

    ################################
    ################################

    @staticmethod
    def isInitializationOK():
        return(mcr_mclib.setupOk)

    ################################
    ################################

    @staticmethod
    def onStartServiceUp(pApplicationName):

        mcr_mclib.ApplicationName = pApplicationName
        mcr_mclib.setupOk = mcr_mclib.checkServiceArgs()
        if (mcr_mclib.setupOk == True):
            mcr_mclib.setupLogging()

    ################################
    ################################

    @staticmethod
    def onStartUp(pApplicationName, pCommandLine, pLogToConsole="False"):
        mcr_mclib.LogToConsole = pLogToConsole
        mcr_mclib.ApplicationName = pApplicationName

        mcr_mclib.setupOk = mcr_mclib.checkArgs(pCommandLine)

        if (mcr_mclib.setupOk == True):
            mcr_mclib.setupLogging()

    ################################
    ################################
    @staticmethod
    def onShutdown():
        logging.shutdown()

    ################################
    # This is just to setup the Logging
    # configuration.
    # Here are the parameters supported for logging
    #  "AppLogging":
    #   {
    #    "LoggingDirectory"      : "C:\\Temp\\LogFiles\\",
    #    "LogFilePrefix"         : "DefaultLog",
    #    "LoggingLevel"          : "INFO",
    #    "LogToConsole"          : "False",
    #    "LogSizeInBytes"        : "500000",
    #    "LogSizeInBytes"        : "2"
    #   }
    ################################

    @staticmethod
    def setupLogging():

        try:

            FullLogFileName = mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LoggingDirectory" ) + \
                mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LogFilePrefix" ) + '.log'

            # Checking to see if this parameter is in the config file and overrides.
            tLogSize = mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LogSizeInBytes" )

            if int(mcr_mclib.defaultLogSize) > (int(tLogSize)):
                tLogSize = mcr_mclib.defaultLogSize

            #print ("LogFileSize: ", tLogSize)

            # Checking to see if this parameter is in the config file and overrides.
            tBackupCount = mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LogBackupCount" )
            if len(tBackupCount) == 0:
                tBackupCount = mcr_mclib.defaultBackupCount
            #print ("LogFile Backup Depth: ", tBackupCount)

            mcr_mclib.logger = logging.getLogger(
                mcr_mclib.ApplicationName)  # (__name__)
            mcr_mclib.logger.setLevel(mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LoggingLevel" ).upper() )

            # Check that the logfile directory is present or is created if not
            if not os.path.exists(mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LoggingDirectory" )):
                os.makedirs(mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LoggingDirectory" ) )

            handler = RotatingFileHandler(FullLogFileName, maxBytes=int(
                tLogSize), backupCount=int(tBackupCount))
            # handler=RotatingFileHandler(FullLogFileName, maxBytes = 200000, backupCount=5)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            handler.setFormatter(formatter)
            mcr_mclib.logger.addHandler(handler)

            # Checking to see if this parameter is in the config file and overrides.
            tLogToConsole = mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LogToConsole" )
            if len(tLogToConsole) == 0:
                tLogToConsole = mcr_mclib.LogToConsole

            if tLogToConsole.upper() == "True".upper():
                consoleHandler = logging.StreamHandler()
                consoleHandler.setLevel(mcr_mclib.AppConfig().getPropertyValue( "AppLogging", "LoggingLevel" ).upper() )
                consoleHandler.setFormatter(formatter)
                mcr_mclib.logger.addHandler(consoleHandler)

        except ValueError as ke:
            print("Is there a config parameter missing from the config file?", repr(ke))
            mcr_mclib.onShutdown()
            sys.exit()

        except KeyError as ke:
            print("Is there a config parameter missing from the config file?", repr(ke))
            mcr_mclib.onShutdown()
            sys.exit()
            
        except AttributeError as ke:
            print("Is there a section missing for this application [%s] in the config file?" % (
                mcr_mclib.ApplicationName))
            print(repr(ke))
            mcr_mclib.onShutdown()
            sys.exit()

    ################################
    ################################

    @staticmethod
    def checkServiceArgs():
        # global ApplicationConfigFile
        okToExecute = False

        if len(mcr_mclib.ApplicationConfigFile) > 1:
            if os.path.exists(mcr_mclib.ApplicationConfigFile):
                #print ( "I found a %s so I will use that as the config" % mcr_mclib.ApplicationConfigFile)

                okToExecute = True
            else:
                print("Config file [%s] not found" %
                      mcr_mclib.ApplicationConfigFile)

        return okToExecute

    ################################
    ################################

    @staticmethod
    def checkArgs(sysArguments):
        # global ApplicationConfigFile
        okToExecute = False

        if len(sys.argv) < 2:
            # print ( "usage %s [Full Path to Config File]" % sys.argv[0] )
            _ConfigFileName = mcr_mclib.ApplicationName + ".json"
            defaultConfigFile = os.path.join("Config", _ConfigFileName)

            try:
                if os.path.exists(defaultConfigFile):
                    print("I found a %s so I will use that as the config" %
                          defaultConfigFile)
                    okToExecute = True
                    mcr_mclib.ApplicationConfigFile = defaultConfigFile
                else:
                    print("There is not a default config here %s" %
                          defaultConfigFile)
                    print("ALL STOP")
            except Exception as e:
                print("File error ... make sure the file can be read", repr(e))
                print(
                    "if you want to use a specific config file please provide with the full path")
                sys.exit()


        elif len(sys.argv) == 2:
            _cmd_line_param = sys.argv[1]

            if "use_environment_vars" in _cmd_line_param.lower():
                print("Using Environment Vars")
                mcr_mclib.ApplicationConfigFile = _cmd_line_param
                okToExecute = True

            elif os.path.exists(_cmd_line_param):
                print("I found a %s so I will use that as the config" %
                      _cmd_line_param)
                okToExecute = True
                mcr_mclib.ApplicationConfigFile = _cmd_line_param
            else:
                print("Config file [%s] not found" % _cmd_line_param)

        if okToExecute is True:
            mcr_mclib.AppConfig().set_config_file(mcr_mclib.ApplicationConfigFile)
            mcr_mclib.AppConfig().set_application_name(mcr_mclib.ApplicationName)
 
            if "use_environment_vars" not in mcr_mclib.ApplicationConfigFile.lower():
                mcr_mclib.AppConfig().load_config()

        return okToExecute

    ################################
    ################################

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    ##############################################
    #
    #
    ##############################################
    @staticmethod
    def getCurrentDateStringAndEpoch():
        reFormatted = datetime.now()

        timezone = pytz.timezone("America/Chicago")
        tz_awareVersion = timezone.localize(reFormatted)

        epochTimeValue = int(tz_awareVersion.timestamp())
        t_cts = tz_awareVersion.isoformat()

        return t_cts, epochTimeValue

    ###############################
    #
    ###############################
    @staticmethod
    def getEpochStampMilliseconds():
        _t1 = int(round(time.time() * 1000))

        return str(_t1)


# if __name__== "__main__":
##
## mcr_mclib.onStartUp("Default", sys.argv, "True")
##
## mcr_mclib.Log().info("Yaa Yaa")
## mcr_mclib.Log().info("Yaa Yaa2")
## mcr_mclib.Log().critical("33Yaa Yaa2")
##
##
# mcr_mclib.onShutdown()
