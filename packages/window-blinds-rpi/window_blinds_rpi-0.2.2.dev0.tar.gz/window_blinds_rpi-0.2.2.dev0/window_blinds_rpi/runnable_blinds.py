#runnable_blinds.py
import time
from .blinds_circuit import BlindsCircuit
import pandas as pd
#import swifter

class RunnableBlinds():

    def __init__(self):
        self.file = "./data/rolete_seznam_.csv"
        self.my_blinds = BlindsCircuit()

        self.blinds_csv = pd.read_csv(self.file)
        self.filter_blinds = (lambda column, value: self.blinds_csv[self.blinds_csv[column] == value]['id'].tolist())     #.tolist()
        #print(f"blinds by smer:{self.filter_blinds('smer', 'zahod')}")
        #self.blind_controls = self.my_blinds.get_blind_controls_list()
        self.blinds = self.my_blinds.get_blinds_list()

    #TODO: add functionality if key is pressed <1s stop/start >1s etc. define functionality ...
    def run(self):
        while 1:
            time.sleep(0.2)
            #self.my_blinds.mcp[4].read_input_on_interrupt()
            interrupted_blind_control = self.my_blinds.get_interrupt_signal()
            interrupt_time = self.my_blinds.get_interrupt_time()
            if(interrupted_blind_control):
                for x in self.my_blinds.mcp[4].blind_controls:
                    #print(f"x.blind_number:{x.get_input()} {self.my_blinds.mcp[4].bits_gpa}")
                    if(x.get_input() != None):
                        interrupted_blind_control = x
                        self.my_blinds.set_blinds(blinds_direction=x.get_input()[1], blinds_controlled = self.filter_blinds("etaza", x.blind_number+1))
                        print(f"x.blind_number:{x.get_input()} gpa:{self.my_blinds.mcp[4].bits_gpa} gpb:{self.my_blinds.mcp[4].bits_gpb}")
                        self.my_blinds.apply_changes_to_output()
                        time.sleep(5)
                        self.my_blinds.set_blinds(blinds_direction="stop", blinds_controlled = self.filter_blinds("etaza", x.blind_number+1))
                        self.my_blinds.apply_changes_to_output()


'''  
                if(interrupted_blind_control == 1):
                    self.my_blinds.set_blinds_down("down", self.filter_blinds('etaza', 1))
                    self.my_blinds.apply_changes_to_output()
                    time.sleep(20)
                    self.my_blinds.set_blinds("stop", self.filter_blinds('etaza', 1))
                    self.my_blinds.apply_changes_to_output()
                    
                if(interrupted_blind_control == 2):
                    self.my_blinds.set_blinds_up("up", self.filter_blinds('etaza', 1))
                    self.my_blinds.apply_changes_to_output()
                    time.sleep(20)
                    self.my_blinds.set_blinds("stop", self.filter_blinds('etaza', 1))
                    self.my_blinds.apply_changes_to_output()

        



   if(self.my_blinds.mcp[4].bits_gpa.any(1) or self.my_blinds.mcp[4].bits_gpb.any(1)):
                start_time = time.clock_gettime
                for x in self.my_blinds.mcp[4].blind_controls:
                    #print(f"x.blind_number:{x.get_input()} {self.my_blinds.mcp[4].bits_gpa}")
                    if(x.get_input() != None):
                        interrupted_blind_control = x
                        self.my_blinds.set_blinds(blinds_direction=x.get_input()[1], blinds_controlled = self.filter_blinds("etaza", x.blind_number+1))
                        print(f"x.blind_number:{x.get_input()} gpa:{self.my_blinds.mcp[4].bits_gpa} gpb:{self.my_blinds.mcp[4].bits_gpb}")
                        self.my_blinds.apply_changes_to_output()
                        time.sleep(40)
                        self.my_blinds.set_blinds(blinds_direction="stop", blinds_controlled = self.filter_blinds("etaza", x.blind_number+1))
                        self.my_blinds.apply_changes_to_output()

'''

#runnable = RunnableBlinds()