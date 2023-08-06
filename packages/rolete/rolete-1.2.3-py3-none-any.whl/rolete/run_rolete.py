import time
from time import sleep
from rolete.class_rolete import ClassRolete
import csv,  sys
from packages.logger.logger_class import Logger
logger_object = Logger()

class RunRolete(object):
    def __init__(self, file_name = None):
        self.file_name = file_name
        if self.file_name != None:
            print("Zagon delovanja rolet ...")
            self.rolete = ClassRolete(self.file_name)
            logger_object.info("{}".format(self.__class__.__name__))
        self.loop(self)
        
    @staticmethod
    def loop(self):
        try:
            while True:
                sleep(0.5)
                for roleta in self.rolete.get_array_rolete():
                    #print(roleta.get_value_tipka_gor())
                    if roleta.get_value_tipka_gor() == False:
                        roleta.set_value_rele_gor(False)
                        print("roleta.set_value_rele_gor(False)")
                #roleta.tipka_gor.set_pin_tipka_value = False
        except KeyboardInterrupt:
            print('interrupted!')
