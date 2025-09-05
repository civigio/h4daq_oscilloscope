# h4daq_oscilloscope

Script to read LeCroy waverunner 8104 oscilloscope. Currently running on Python3.

IMPORTANT TO DO BEFORE LAUNCHING THE SCRIPT:

  -Use CH2 & CH3 (if you only want to use one channel, use CH2 and comment lines on acquisition.py as explained in the beginnin of that script)

  -Activate CH2 & CH3 (only CH2 for one channel)
  
  -In the scope, go to File->Save Waveform->Auto Save and tick the box next to "Waveform"; select "All Displayed" as source (select C2 if you only want one channel)
  
  -Take note of the number in file name

IN THE SCRIPT:

  -Write the number on a new line of the runs.txt file

PLEASE BEAR IN MIND: in the runs.txt file, the numbers indicate the first "package" of waveforms of each spill (eg. if runs.txt is 0 4 8 this means spill1->files from 0 to 3, spill2->files from 4 to 7...)
