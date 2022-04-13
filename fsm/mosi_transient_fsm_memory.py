import constants

class MOSI_Transient_FSM_Memory:
	def __init__(self, value, state):
		self.value = value
		self.state = state
		self.id = constants.MEMORY_ID

	def getValue(self):
		return self.value

	def setValue(self, value):
		self.value = value

	def setState(self, state):
		self.state = state

	def getState(self):
		return self.state

	def recordUpdate(self, value, buffer):
		instruction = {
			"action" : "Update",
			"target" : self.id,
			"value" : value,
			"state" : self.state
		}
		buffer.append(instruction)

	def reset(self):
		self.state = constants.STATE_I_OR_S
		self.value = constants.DEFAUT_VALUE

	def updateState(self, message, buffer, bus):  
		event = message["action"]

		if self.state == constants.STATE_I_OR_S:
			if event == constants.EVENT_GET_S:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
					#"exclusive" : 1
				}
				buffer.append(instruction)
				bus.append(instruction)
			elif event == constants.EVENT_GET_M:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
					#"exclusive" : 1
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.state = constants.STATE_M_OR_O
			elif event == constants.EVENT_PUT_M:
				self.state = constants.STATE_I_OR_S_D
			else:
				if message["dst"] == self.id:
					assert False

		elif self.state == constants.STATE_I_OR_S_D:
			if event == constants.EVENT_DATA:
				self.state = constants.STATE_I_OR_S
				self.value = message["value"]
				self.recordUpdate(self.value, buffer)
			elif event == constants.EVENT_NO_DATA:
				self.state = constants.STATE_I_OR_S

		elif self.state == constants.STATE_M_OR_O:
			if event == constants.EVENT_GET_S or event == constants.EVENT_GET_M:
				pass # do nothing
			elif event == constants.EVENT_PUT_M:
				self.state = constants.STATE_M_OR_O_D
			else:
				if message["dst"] == self.id:
					assert False, "Unknown event, MorO"

		elif self.state == constants.STATE_M_OR_O_D:
			if event == constants.EVENT_DATA:
				self.state = constants.STATE_I_OR_S
				self.value = message["value"]
				self.recordUpdate(self.value, buffer)
			elif event == constants.EVENT_NO_DATA:
				self.state = constants.STATE_M_OR_O
			else:
				assert False, "Unknown event, MorO_D"

		else:
			assert False, "Unknown state"
