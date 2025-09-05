import csv
from readTrc import Trc
import os
import numpy as np

def timescale_setting(x, y):
    indices = [0]
    for i, item in enumerate(y):
        prev_item = y[i - 1] if i > 0 else None
        if prev_item is not None and item * prev_item < 0 and prev_item > item:
            indices.append(i)

    single_wvfm_voltages = []
    for i, index in enumerate(indices):
        if i == len(indices) - 1:
            break
        subarray = y[index : indices[i + 1]]
        single_wvfm_voltages.append(subarray)

    wvfm_timestamps = []
    for i, index in enumerate(indices):
        if i == len(indices) - 1:
            break
        subarray = x[index : indices[i + 1]]
        wvfm_timestamps.append(subarray)

    time_spans = [subarray[-1]-subarray[0] for subarray in wvfm_timestamps]
    time_intersteps = [wvfm_timestamps[i+1][0]-subarray[-1] for i, subarray in enumerate(wvfm_timestamps[:-1])]

    single_wvfm_timestamps = []
    offset = 0
    for i, s in enumerate(wvfm_timestamps):
        if i == 0: continue
        offset += time_spans[i-1] + time_intersteps[i-1]
        s = s - offset
        single_wvfm_timestamps.append(s)
    
    # concatenate the subarrays into single array
    single_wvfm_timestamps = np.array(single_wvfm_timestamps).flatten().tolist()
    single_wvfm_voltages = np.array(single_wvfm_voltages).flatten().tolist()

    return single_wvfm_timestamps, single_wvfm_voltages




## main ##


timescaling_onoff = False


raws_path = 'raws/'
filenames_raws = ['_'.join(f.split('.')[0].split('_')[1:]) for f in os.listdir(raws_path) if os.path.isfile(os.path.join(raws_path, f))]
print(filenames_raws)

csvs_path = 'csvs/'
filenames_csvs = ['_'.join(f.split('.')[0].split('_')[1:]) for f in os.listdir(csvs_path) if os.path.isfile(os.path.join(csvs_path, f))]
print(filenames_csvs)

raws_to_be_converted = [item for item in filenames_raws if item not in filenames_csvs]
print(raws_to_be_converted)
# check if list is empty
if not raws_to_be_converted:
    print("No new .trc files to convert.")
    exit()


for fName in raws_to_be_converted:

    trc = Trc()
    fullfName = raws_path+'raw_'+fName+".trc"
    datX, datY, d = trc.open(fullfName)

    with open(csvs_path+'csv_'+fName+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', 'Voltage (V)'])
        if timescaling_onoff:
            datX, datY = timescale_setting(datX, datY) 
        for t, v in zip(datX, datY):
            writer.writerow([t, v])

    print(f"Converted {fName} to CSV format.")
