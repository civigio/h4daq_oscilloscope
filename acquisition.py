import pyvisa
import time

def transfer(lecroy):
    device = 'HDD'  # or whatever device identifier your scope uses
    runs_database = "runs.txt"

    with open(runs_database, "r") as file:
        run_number = int(file.readlines()[-1].strip())

    for _ in range(100):
        filepath = f"D:\\BTL_testbeam\\C2--runx--{run_number:05d}.trc"
        lecroy.write(f"TRFL? DISK,{device},FILE,{filepath}")
        raw_data = lecroy.read_raw()
        if len(raw_data) > 1:
            # Save the data locally
            with open(f'raws/raw_{run_number:05d}.trc', 'wb') as f:
                f.write(bytearray(raw_data))
            run_number += 1
    with open(runs_database, "a") as file:
        file.write('\n' + str(run_number))

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    lecroy = rm.open_resource("TCPIP0::169.254.16.17::INSTR")
    lecroy.write("COMM_HEADER OFF")
    lecroy.timeout=60000
    lecroy.write("STOP")

    lecroy.write("TIME_DIV 10NS")
    lecroy.write("MEMORY_SIZE 500")
    lecroy.write("C2:VOLT_DIV 0.5V")
    lecroy.write("C2:OFFSET 0V")

    lecroy.write("SEQ ON")
    lecroy.write("vbs app.Acquisition.Horizontal.NumSegments = 5000")
    lecroy.write("vbs app.SaveRecall.AutoSave = \"Wrap\"")


    input("Press Enter to acquire...")
    while True:
        start_time = time.time()
        lecroy.write("vbs app.Acquisition.Triggermode = Norm")
        time.sleep(5.5)
        lecroy.write("TRIG_MODE STOP")
        transfer(lecroy)
        stop_time = time.time()
        print("Total transfer time: ", stop_time - start_time)
        input("Press Enter to acquire...")