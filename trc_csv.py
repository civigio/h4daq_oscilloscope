import csv
from readTrc import Trc
import os

raws_path = 'raws/'
filenames_raws = [f.split('.')[0].split('_')[1] for f in os.listdir(raws_path) if os.path.isfile(os.path.join(raws_path, f))]

csvs_path = 'csvs/'
filenames_csvs = [f.split('.')[0].split('_')[1] for f in os.listdir(csvs_path) if os.path.isfile(os.path.join(csvs_path, f))]

raws_to_be_converted = [item for item in filenames_raws if item not in filenames_csvs]


for fName in raws_to_be_converted:

    trc = Trc()
    fullfName = raws_path+'raw_'+fName+".trc"
    datX, datY, d = trc.open(fullfName)

    with open(csvs_path+'csv_'+fName+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', 'Voltage (V)'])
        for t, v in zip(datX, datY):
            writer.writerow([t, v])

    print(f"Converted {fName} to CSV format.")
