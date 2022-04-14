import constants

class MOESI_Transient_FSM_Memory:
	def __init__(self, value, state):
		self.value = value
		self.state = state
		self.id = constants.MEMORY_ID
		self.num_sharers = 0

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
		self.state = constants.STATE_I
		self.value = constants.DEFAUT_VALUE

	def unhandledEvent(self, event):
		assert False, f"Unhandled event {event} in state {self.state}"
	
	def unhandledState(self):
		assert False, f"Unhandled state {self.state}"

	def updateState(self, message, buffer, bus):  
		event = message["action"]

		if message["target"] != self.id:
			return
		
		assert self.num_sharers >= 0 and self.num_sharers <= constants.NUM_PROCESSORS

		if self.state == constants.STATE_I:
			assert self.num_sharers == 0

			if event == constants.EVENT_GET_S:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"exclusive" : 1
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.state = constants.STATE_E
			elif event == constants.EVENT_GET_M:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.state = constants.STATE_M
			else:
				self.unhandledEvent(event)

		elif self.state == constants.STATE_S:
			assert self.num_sharers >= 1

			if event == constants.EVENT_GET_S:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"exclusive" : 0
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.num_sharers += 1
			elif event == constants.EVENT_GET_M:
				instruction = {
					"action" : constants.EVENT_DATA,
					"value" : self.value,
					"target" : message["src"],
					"src" : self.id,
					"dst" : constants.BUS_ID,
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.state = constants.STATE_M
				self.num_sharers = 0
			elif event == constants.EVENT_DATA and message["src"] == self.id:
				pass
			elif event == constants.EVENT_PUT_S:
				self.num_sharers -= 1
				if self.num_sharers == 0:
					self.state = constants.STATE_I
			else:
				self.unhandledEvent(event)

		elif self.state == constants.STATE_E:
			assert self.num_sharers == 0

			if event == constants.EVENT_GET_S:
				self.num_sharers = 1
				self.state = constants.STATE_S_D
			elif event == constants.EVENT_GET_M:
				self.state = constants.STATE_M
			elif event == constants.EVENT_PUT_M:
				self.state = constants.STATE_MI_D
			elif event == constants.EVENT_DATA and message["src"] == self.id:
				pass
			else:
				self.unhandledEvent(event)

		elif self.state == constants.STATE_M:
			assert self.num_sharers == 0

			if event == constants.EVENT_GET_S:
				self.num_sharers = 1
				self.state = constants.STATE_O
			elif event == constants.EVENT_GET_M:
				pass
			elif event == constants.EVENT_PUT_M:
				self.state = constants.STATE_MI_D
			elif event == constants.EVENT_DATA and message["src"] == self.id:
				pass
			else:
				self.unhandledEvent(event)
		
		elif self.state == constants.STATE_O:
			if event == constants.EVENT_GET_S:
				self.num_sharers += 1
			elif event == constants.EVENT_GET_M:
				self.num_sharers = 0
				self.state = constants.STATE_M
			elif event == constants.EVENT_PUT_M:
				self.state = constants.STATE_MI_D
			elif event == constants.EVENT_PUT_S:
				self.num_sharers -= 1
			else:
				self.unhandledEvent(event)
		
		elif self.state == constants.STATE_S_D:
			if event == constants.EVENT_DATA:
				self.state = constants.STATE_O
			elif event == constants.EVENT_NO_DATA_E:
				self.num_sharers += 1
				self.state = constants.STATE_S
			else:
				self.unhandledEvent(event)
		
		elif self.state == constants.STATE_MI_D:
			if event == constants.EVENT_DATA:
				self.value = message["value"]
				self.recordUpdate(self.value, buffer)

				if self.num_sharers == 0:
					self.state = constants.STATE_I
				else:
					self.state = constants.STATE_S
			elif event == constants.EVENT_NO_DATA_E:
				self.state = constants.STATE_I
			else:
				self.unhandledEvent(event)

		else:
			self.unhandledState()
