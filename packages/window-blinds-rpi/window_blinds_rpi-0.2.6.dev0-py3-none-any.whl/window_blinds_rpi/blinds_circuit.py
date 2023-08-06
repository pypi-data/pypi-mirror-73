import time
import pprint
from .mcp_expander import McpExpander, Blind, BlindControl
import RPi.GPIO as GPIO


class BlindsCircuit():
    mcp = []
    blinds_list = []
    blind_controls_list = []
    
    interrupt_event_state = False
    interrupt_time = 0

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, GPIO.LOW)
        time.sleep(.5)
        GPIO.output(22, GPIO.HIGH)
        GPIO.setup(23, GPIO.IN)

        for value in range(0x20, 0x25):
            self.mcp.append(McpExpander(address=value,))

        for l in self.mcp:
            if(isinstance(l, Blind)):
                self.blinds_list.append(l.get_blinds_list())
            elif(isinstance(l, BlindControl) ):
                self.blind_controls_list.append(l.get_blinds_control_list())

        GPIO.add_event_detect(23, GPIO.BOTH , callback=self.event_detect, bouncetime=200)

        """ function called from GPIO.add_event_detect"""

    def event_detect(self, channel):
        GPIO.remove_event_detect(channel)
        start_time = time.time()
        while(GPIO.input(channel)):
            self.interrupt_event_state = self.get_interrupt_signal()
            time.sleep(0.05)
        stop_time = time.time()
        button_pushed_time = stop_time - start_time
        self.interrupt_event_state = False
        self.interrupt_time  = button_pushed_time
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.event_detect, bouncetime=200)
        print(f"my callback from event detect time : {button_pushed_time}")



    """get unnested list of blinds"""
    def get_blinds_list(self):
        return_list = []
        for x in self.mcp :
            for blind in x.get_blinds_list():
                return_list.append(blind)
        return return_list

    """get unnested list of blind controls (input switches)"""
    def get_blind_controls_list(self):
        return_list = []
        for x in self.blind_controls_list:
            for blind_controls in x:
                return_list.append(blind_controls)
        return return_list

    def set_blinds_up(self, blinds_direction = "up", blinds_controlled = [], *args, **kvargs):
        self.set_blinds(blinds_direction="up", blinds_controlled = blinds_controlled)

    def set_blinds_down(self, blinds_direction = "down", blinds_controlled = [], *args, **kvargs):
        self.set_blinds(blinds_direction="down", blinds_controlled = blinds_controlled)

    def set_blinds(self, blinds_direction = "stop", blinds_controlled = [], *args, **kvargs):
        #print(f"self.get_blinds_list()):{self.get_blinds_list())}, blinds_controlled:{blinds_controlled}")
        for i in blinds_controlled:
            if(i < len(self.get_blinds_list())):
                #blind = self.get_blinds_list()[i]
                #getattr(blind, (f"{(blinds_direction).lower()}"))()
                getattr(self.get_blinds_list()[i],  (f"{(blinds_direction).lower()}"))()
                #exec(f"self.get_blinds_list(){[i]}.{(blinds_direction).lower()}()")


    def apply_changes_to_output(self):
        for m in self.mcp:
            m.apply_changes_to_output()

    def get_interrupt_signal(self):
        self.interrupt_event_state = GPIO.input(23)
        if(self.interrupt_event_state):
            self.mcp[4].read_input_on_interrupt()
            self.interrupt_event_state = GPIO.input(23)
        return self.interrupt_event_state
    
    def get_interrupt_time(self):
        return self.interrupt_time


    def __str__(self):
        return_string = ""
        for s in self.mcp:
            return_string = "#{} {}#\n".format(return_string, str(s) )
        return return_string
