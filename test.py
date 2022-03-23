from fsm.msi_transient_fsm import MSI_Transient_FSM

def main():
    print("Hi")
    msiFSM = MSI_Transient_FSM("5", "Invalid", "0")
    msiFSM.updateState("GET_S")

if __name__ == "__main__":
    main()