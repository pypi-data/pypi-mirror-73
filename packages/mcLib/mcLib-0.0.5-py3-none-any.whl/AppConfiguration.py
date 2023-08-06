import json
import sys
import os
from json_minify import json_minify

"""
This class is intented to work with a central config file that has a heirarchy to it.

So, instead of having multiple config files ( which you could still do with this class )
there is a central one with sections for each application.

The name space is basically the name of the application that has the associated parameters that will be
used for a given application.

example:
  name spaces
        App1
        App2
        App3

Within a name space there can be paragraphs for parameters to be associated ( property section ). For example there could be a section
for database login, servername, db, etc. in addition there could be another paragraph for external api URLs.
  name spaces
        App1
           databaseParams
              dbname
              dbuserid
              dbservername
              ...
           externalAppParams
              url
              secretKey
              ...
        App2
           runtimeEnv
              externalURLForWeather
              logDirectory
              ...
        App3

usage:
  create a new class for each nameSpace, property section, config file name)
  use the getPropertyValue passing in the property name within a section. If the value is not found an
  an empty string of zero length is returned. 
"""


############################################################
#
# Author: Michael Robinson ( michael.robinson1@kochind.com
# Desc: This class abstracts the interaction with the application
# configuration file. At present this is a JSON file, but if
# another configuration option is desired then this class would need to be extended.
#
############################################################
class AppParametersHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AppParametersHandler.__instance is None:
            AppParametersHandler()
        return AppParametersHandler.__instance

    ################
    #
    ################

    def __init__(self):
        if AppParametersHandler.__instance is None:
            AppParametersHandler.__instance = self

    ################
    #
    ################
    def set_config_file(self, _ConfigFileParam):
        self.__DefaultConfigFile = _ConfigFileParam
        # print  ("Default Config File: {}".format (self.__DefaultConfigFile ))

    ################
    #
    ################

    def set_application_name(self, _AppName):
        self.__ApplicationName = _AppName
        # print ("Application Name: {} ".format(self.__ApplicationName ) )

    ################
    #
    ################

    def load_config(self):
        try:
            print("App Config File [{}]".format(self.__DefaultConfigFile))
            self.input_string         = open(self.__DefaultConfigFile, 'r').read()
            self.ParameterFileString  = json.loads(json_minify(self.input_string))
            self._nameSpaceProperties = self.ParameterFileString[self.__ApplicationName]

        except FileNotFoundError as e:
            print("Error message config file not found: ", repr(e))
            print("looking for: %s" % (self.__DefaultConfigFile))
            sys.exit()

    ################
    #
    ################

    def getPropertyValue(self, pPropertySection, pLookupString):
    
        if "use_environment_vars" in self.__DefaultConfigFile.lower():
            try:
                _returnedValue = os.environ[pLookupString]
            except KeyError:
                print("**** ATTENTION: Environment Var Value Not Found", pLookupString)
                _returnedValue = ""

        else:

            try:
                _propertySection = self._nameSpaceProperties[pPropertySection]
                _returnedValue = _propertySection[pLookupString]

            except KeyError:
                print("**** ATTENTION: Key Not found ", pLookupString)
                _returnedValue = ""
                sys.exit()

        return _returnedValue
