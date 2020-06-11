from pyagilis.controller import AGP
from sardana import State
from sardana.pool.controller import MotorController, Type, Description, DefaultValue


class AgilisAGPMotorController(MotorController):
    ctrl_properties = {'port': {Type: str, Description: 'The port of the rs232 device', DefaultValue: '/dev/ttyAGILIS1'}}

    axis_attributes = {
        "Homing" : {
                Type         : bool,
                Description  : "(de)activates the motor homing algorithm",
                DefaultValue : False,
            },
    }
    
    MaxDevice = 1
    
    def __init__(self, inst, props, *args, **kwargs):
        super(AgilisCONEXagpController, self).__init__(
            inst, props, *args, **kwargs)
        
        print('AGP Controller Initialization ...'),
        # initialize hardware communication
        self.agilis = AGP(self.port)
        # first query will somehow timeout
        try:
            self.agilis.getStatus()
        except:
            print('initial timeout'),            
        
        if self.agilis.getStatus() == 0: # not referenced
            print('homing ...' % self.port),
            self.agilis.home()
            
        # do some initialization
        print('SUCCESS on port %s' % self.port)
        self._motors = {}

    def AddDevice(self, axis):
        self._motors[axis] = True

    def DeleteDevice(self, axis):
        del self._motors[axis]

    StateMap = {
        1: State.On,
        2: State.Moving,
        3: State.Fault,
    }

    def StateOne(self, axis):
        limit_switches = MotorController.NoLimitSwitch     
        state = self.agilis.getStatus()
                
        return self.StateMap[state], 'some text', limit_switches

    def ReadOne(self, axis):
        return self.agilis.getCurrentPosition()

    def StartOne(self, axis, position):
        self.agilis.moveAbsolute(position)

    def StopOne(self, axis):
        self.agilis.stop()

    def AbortOne(self, axis):
        self.agilis.stop()
        
    def setHoming(self, axis, value):
        """Homing for given axis"""
        if value:       
            self.agilis.home()
    
    def getHoming(self, axis):
        """Homing for given axis"""       
        return False

    
