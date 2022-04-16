import sys

DEFAUT_VALUE = 100
NULL_VALUE = sys.maxsize

# Constants for ID
MEMORY_ID = -1
BUS_ID = -2

NUM_PROCESSORS = 3

# Constants for Events
EVENT_GET_S = "GetS"
EVENT_GET_M = "GetM"
EVENT_DATA = "Data"
EVENT_UPDATE = "Update"
EVENT_PUT_M = "PutM"
EVENT_LOAD = "Load"
EVENT_STORE = "Store"
EVENT_EVICT = "Evict"
EVENT_NO_DATA_E = "NoData_E"
EVENT_NO_DATA = "NoData"
EVENT_HIT = "Hit"
EVENT_PUT_S = "PutS"
EVENT_STALL = "Stall"

# Constants for Cache Controller States
STATE_I = "I"
STATE_IS_D = "IS_D"
STATE_IM_D = "IM_D"
STATE_S = "S"
STATE_SM_D = "SM_D"
STATE_M = "M"
STATE_IS_AD = "IS_AD"
STATE_IM_AD = "IM_AD"
STATE_IS_A = "IS_A"
STATE_IM_A = "IM_A"
STATE_SM_AD = "SM_AD"
STATE_SM_A = "SM_A"
STATE_MI_A = "MI_A"
STATE_II_A = "II_A"
STATE_E = "E"
STATE_EI_A = "EI_A"
STATE_O = "O"
STATE_OM_A = "OM_A"
STATE_OI_A = "OI_A"

# Constants for Memory Controller States
STATE_I_OR_S = "IorS"
STATE_I_OR_S_D = "IorS_D"
STATE_M = "M"
STATE_E_OR_M = "EorM"
STATE_I_D = "I_D"
STATE_S_D = "S_D"
STATE_E_OR_M_D = "EorM_D"
STATE_E_OR_M = "EorM"
STATE_I_OR_S_A = "IorS_A"
STATE_M_OR_O = "MorO"
STATE_M_OR_O_D = "MorO_D"
STATE_I = "I"
STATE_S = "S"
STATE_E = "E"
STATE_O = "O"
STATE_MI_D = "MI_D"
