import constants

class Driver:
    def __init__(self, processors, memory):
        self.processors = processors
        self.memory = memory

        # Buffer for return values to be sent back to the front end
        self.buffer = []

        # Representation of what is on the bus
        self.bus = []

    def setInitialState(self):
        for i in range (len(self.processors)):
            instruction = {
                "processor" : i,
                "value" : constants.NULL_VALUE,
                "state" : constants.STATE_I
            }

            self.buffer.append(instruction)

        instruction = {
            "processor" : constants.MEMORY_ID,
            "value" : constants.DEFAUT_VALUE
        }

        self.buffer.append(instruction)

    # Load all possible actions into the buffer
    def loadValidActions(self):
        for i in range (len(self.processors)):
            self.processors[i].loadValidActions(self.buffer)

    def getBuffer(self):
        return self.buffer

    def clearBuffer(self):
        self.buffer = []

    def getBus(self):
        return self.bus

    def clearBus(self):
        self.bus = []

    def reset(self):
        for i in range (len(self.processors)):
            self.processors[i].setState(constants.STATE_I)
            self.processors[i].setValue(constants.DEFAUT_VALUE)

        self.memory.reset()
        self.clearBus()
        self.clearBuffer()

    def processProcessorAction(self, message):
        processorID = message["processor"]
        self.processors[processorID].updateState(message, self.buffer, self.bus)

    def processBusEvent(self, busIndex):
        # Empty bus so don't do anything
        if len(self.bus) == 0:
            return

        message = self.bus[busIndex] 
        for i in range(len(self.processors)):
            self.processors[i].updateState(message, self.buffer, self.bus)

        self.memory.updateState(message, self.buffer, self.bus)

        self.bus.pop(busIndex) # Finished processing bus message so remove from bus
            
            
                

