Audio Analysis Program
======================

  Created by: Evan Cummings
  Fall '11 - Min Chen
  CSCI 478 - Multimedia Data Processing
  "Program to classify audio as speech or music."


Analysis:
  For this project I have been tasked with extracting audio features 
  from a set of audio files and classifying these features with data 
  mining algorithms.  The GUI program audioGUI.py uses the functions 
  provided by audio.py to extract features, plot the audio file's 
  waveform and FFT graph, and classify the extracted features.

Design:
  The algorithms used for feature extraction were taken from Content 
  Analysis for Audio Classification and Segmentation .  After building 
  the functions and testing them on a single audio file, I made a loop 
  to traverse the directory and create the training set and testing 
  set feature files.  With this completed I added the data mining 
  functions to output the results in a file.  In testing I would plot 
  the waveform and FFT, and decided to leave these functions available 
  to the user.

  The GUI program uses audio.py's methods to conveniently display the 
  information to the screen.

Usage:
  You will need to install the libraries AudioLab and Orange for 
  python.  

    Orange   - http://orange.biolab.si/
    AudioLab - http://www.ar.media.kyoto-u.ac.jp/members/david/
               softwares/audiolab/sphinx/index.html


  Afterwards you may execute the file with "python audioGUI.py" in your
  terminal.  The directory structure is as follows:

    /data - Audio files, feature files, and results.
    /data/test/ - Testing audio files
    /data/train/ - Training audio files
    /data/results - Data mining results file
    /data/audioTest.tab - Testing set features file
    /data/audioTrain.tab - Training set features file
    /images/ - Folder to hold plot images
    /audio.py - Function class for audio tasks
    /audioGUI.py - GUI program to display the data

