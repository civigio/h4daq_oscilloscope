# h4daq_oscilloscope

Script to read LeCroy waverunner 8104 oscilloscope. Currently running on Python3.

IMPORTANT TO DO BEFORE LAUNCHING THE SCRIPT:

  -Create two folders in the directory, called "runs" and "csvs"

  -Use CH2 & CH3 (if you only want to use one channel, use CH2 and comment lines on acquisition.py as explained in the beginnin of that script)

  -Activate CH2 & CH3 (only CH2 for one channel)
  
  -In the scope, go to File->Save Waveform->Auto Save and tick the box next to "Waveform"; select "All Displayed" as source (select C2 if you only want one channel)
  
  -Take note of the number in file name

IN THE SCRIPT:

  -Write the number on a new line of the packets.txt file

PLEASE BEAR IN MIND: in the packets.txt file, the numbers indicate the first "package" of waveforms for each spill (eg. if runs.txt is 0 4 8 this means spill1->files from 0 to 3, spill2->files from 4 to 7...). Spills are continuous and not resetted as run changes (at least in this file).

TO SEND OUT TRIGGER SIGNAL FROM OSCILLOSCOPE FROM THE AUX PORT: go to Utilities->Utilities setup->Aux output and press "Trigger Out" in the "Use Auxiliary Output For" window
