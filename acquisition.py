###the script acquires waveforms from CH2 and CH3
###if you only want to use one channel (CH2) please comment lines 24, 25, 26, 27, 28, 46, 47


import pyvisa
import time

IPADDRESS = "169.254.16.17"                                                 # IP address of the oscilloscope

def transfer(lecroy, starting_time):
    device = 'HDD'                                                          # to save from the HDD of the oscilloscope
    runs_database = "runs.txt"                                              # file to keep track of packages of runs

    with open(runs_database, "r") as file:
        run_number = int(file.readlines()[-1].strip())                      # first file of new run

    for _ in range(100):
        filepath = f"D:\\BTL_testbeam\\C2--runx--{run_number:05d}.trc"      # path on the oscilloscope
        lecroy.write(f"TRFL? DISK,{device},FILE,{filepath}")                # retrieve the file in raw format
        raw_data = lecroy.read_raw()
        if len(raw_data) > 1:                                               # check if the file exists
            with open(f'raws/raw_C2_{run_number:05d}.trc', 'wb') as f:      # save the file locally
                f.write(bytearray(raw_data))                                
            with open(f'raws/raw_C3_{run_number:05d}.trc', 'wb') as g:
                filepath2 = f"D:\\BTL_testbeam\\C3--runx--{run_number:05d}.trc"
                lecroy.write(f"TRFL? DISK,{device},FILE,{filepath2}")
                raw_data2 = lecroy.read_raw()
                g.write(bytearray(raw_data2))
            run_number += 1
    with open(runs_database, "a") as file:
        file.write('\n' + str(run_number))                                  # writes first package of next run

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()                                           # set VISA communication
    lecroy = rm.open_resource(f"TCPIP0::{IPADDRESS}::INSTR")                # open connection to the oscilloscope
    lecroy.write("COMM_HEADER OFF")                                         # no header in files
    lecroy.timeout=60000                                                    # set timeout to 60s
    lecroy.write("STOP")                                                    # freeze scope to configure it

    #set active channels
    lecroy.write("vbs app.Acquisition.Horizontal.ActiveChannels = false")

    #set vertical and horizontal scale
    lecroy.write("C2:VOLT_DIV 0.5V")
    lecroy.write("C2:OFFSET 0V")
    lecroy.write("C3:VOLT_DIV 0.5V")
    lecroy.write("C3:OFFSET 0V")
    lecroy.write("TIME_DIV 10NS")

    #set trigger options
    lecroy.write("TRIG_SELECT C2")
    lecroy.write("TRIG_DELAY 20NS")
    lecroy.write("C2:TRIG_SLOPE NEG")
    lecroy.write("C2:TRIG_LEVEL -0.1V")

    #set sequence mode options
    lecroy.write("MEMORY_SIZE 500")
    lecroy.write("SEQ ON")
    lecroy.write("vbs app.Acquisition.Horizontal.NumSegments = 2500")

    #set autosave options
    lecroy.write("vbs app.SaveRecall.AutoSave = \"Wrap\"")


    while True:
        input("Press Enter to acquire...")
        start_time = time.time()
        lecroy.write("TRIG_MODE NORM")
        time.sleep(5.2)
        lecroy.write("TRIG_MODE STOP")
        transfer(lecroy)
        stop_time = time.time()
        print("Total transfer time: ", stop_time - start_time)


