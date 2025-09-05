###the script acquires waveforms from CH2 and CH3
###if you only want to use one channel (CH2) please comment lines 27, 28, 29, 30, 31, 49, 50


import pyvisa
import time

IPADDRESS = "169.254.16.17"                                                 # IP address of the oscilloscope

def transfer(lecroy, spill_number, run_number):
    device = 'HDD'                                                          # to save from the HDD of the oscilloscope
    packets_database = "packets.txt"                                              # file to keep track of packages of runs

    with open(packets_database, "r") as file:
        packet_number = int(file.readlines()[-1].strip())                      # first file of new run

    for i in range(100):
        # if packet_number < 10000, use 5 digit zfill, if not use the number as it is
        pack_str = f"{packet_number:05d}" if packet_number < 10000 else str(packet_number)

        filepath = f"D:\\BTL_testbeam\\C2--runx--{pack_str}.trc"             # path on the oscilloscope
        lecroy.write(f"TRFL? DISK,{device},FILE,{filepath}")                # retrieve the file in raw format
        raw_data = lecroy.read_raw()
        if len(raw_data) > 1:                                               # check if the file exists
            with open(f'raws/raw_C2_{run_number:07d}_{spill_number:07d}_{i}.trc', 'wb') as f:      # save the file locally
                f.write(bytearray(raw_data))                                
            with open(f'raws/raw_C3_{run_number:07d}_{spill_number:07d}_{i}.trc', 'wb') as g:
                filepath2 = f"D:\\BTL_testbeam\\C3--runx--{pack_str}.trc"
                lecroy.write(f"TRFL? DISK,{device},FILE,{filepath2}")
                raw_data2 = lecroy.read_raw()
                g.write(bytearray(raw_data2))
            packet_number += 1
    with open(packets_database, "a") as file:
        file.write('\n' + str(packet_number))                                  # writes first package of next run

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

    run_number = input("Enter run number...")
    input("Press to start acquisition...")
    while True:
        spill_number = input("Spill number...")
        start_time = time.time()
        lecroy.write("TRIG_MODE NORM")
        time.sleep(5.2)
        lecroy.write("TRIG_MODE STOP")
        transfer(lecroy, spill_number)
        stop_time = time.time()
        print("Total transfer time: ", stop_time - start_time)



