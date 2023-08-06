from rolete.rolete_lib.class_roleta import ClassRoleta
from rolete.rolete_lib import class_i2c_devices
from rolete.rolete_lib.class_i2c_devices import ClassI2cDevices
import csv,  sys
from packages.logger.logger_class import Logger
logger_object = Logger()

class ClassRolete(object):

    def __init__(self, filename = None):
        self.filename = filename
        self.class_i2c_devices = ClassI2cDevices()
        self.array_rolete = self.get_array_rolete()
        self.array_i2c_devices = self.get_array_i2c_devices()
        self.set_inputs_outputs_rolete()
        logger_object.info("{}".format(self.__class__.__name__))
    
    def get_array_rolete(self):
        array_rolete = []
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                array_rolete.append(ClassRoleta(row[0],row[1],row[2],row[3],row[4],row[5], row[6], row[7], row[8]))
        logger_object.info("{}.generiraj_rolete".format(self.__class__.__name__))
        return array_rolete
        
    def get_array_i2c_devices(self):
        return class_i2c_devices.get_array_i2c_devices(self)
    
    #
    def set_inputs_outputs_rolete(self):
        for roleta in self.array_rolete:
            i2c_device = self.array_i2c_devices[int(roleta.get_i2c_device_address(), 16) - int("0x20", 16)]
            roleta.tipka_gor.set_pin_tipka(i2c_device.get_pin_tipka_gor(roleta.get_roleta_number_per_i2c()))
            roleta.tipka_dol.set_pin_tipka(i2c_device.get_pin_tipka_dol(roleta.get_roleta_number_per_i2c()))
            roleta.rele_gor.set_pin_rele( i2c_device.get_pin_rele_gor(roleta.get_roleta_number_per_i2c()))
            roleta.rele_dol.set_pin_rele( i2c_device.get_pin_rele_dol(roleta.get_roleta_number_per_i2c()))
                    
            
        
    def close_all(self):
        pass
    
    def open_all(self):
        pass
        


