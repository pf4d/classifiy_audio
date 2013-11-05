#
#    Copyright (C) <2012>  <cummings.evan@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# audioGUI.py
# Evan Cummings
# Fall '11 - Min Chen
# CSCI 478 - Multimedia Data Processing
# Set of functions used for audio analysis and classification.

from pylab import *
import scikits.audiolab as al
import glob, os


data = []   # Audio tuple list


# Calculate high-zero-crossing rate ratio:
def hzcrr(frames, numFrames, fs):

  ZCR = 0
  HZCRR = 0.0
  fmCnt = 0
  avgZCR = 0
  # For each frame,
  for i in range(numFrames-1):
    fmCnt += 1
    
    # if it crosses 0, increment the average count.
    if (frames[i] >= 0 and frames[i+1] < 0) or \
       (frames[i] <= 0 and frames[i+1] > 0):
      avgZCR += 1
    # If we've counted 1 second's worth of frames,
    if (fmCnt % fs == 0):
      # Calculate the average,
      avgZCR = avgZCR / fs
      # Iterate through the previous second and compare to average:
      for j in range(fmCnt)[i-fs:]:
        if (frames[j] >= 0 and frames[j+1] < 0) or \
           (frames[j] <= 0 and frames[j+1] > 0):
          ZCR += 1
        HZCRR += np.sign(ZCR - 1.5*avgZCR) + 1
      ZCR = 0
      avgZCR = 0

  HZCRR = HZCRR / (2 * numFrames)
  
  return HZCRR

  
# Calculate low short-time energy ratio:
def lster(frames, numFrames, fs):

  LSTER = 0.0
  fmCnt = 0
  avgSTE = 0
  # For each frame,
  for i in range(numFrames-1):
    fmCnt += 1
    avgSTE += frames[i]**2 # Find average energe
    # if one second has elapsed,
    if (fmCnt % fs == 0):
      # Calculate average:
      avgSTE = avgSTE / fs
      # Iterate through the last second's frames and compare to average:
      for j in range(fmCnt)[i-fs:]:
        STE = frames[j]**2
        LSTER += np.sign(0.5*avgSTE - STE) + 1
      avgSTE = 0
  
  LSTER = LSTER / (2* numFrames)
  
  return LSTER


# Calculate spectrum flux:
def sf(frames, numFrames, fs):

  SF = 0
  d = 0.000000001
  fmCnt = 0
  bins = 1024
  # While there are still frames left,
  while fmCnt+fs < numFrames:
    # determine if there is a full second left,
    if (fmCnt + 2*fs) > numFrames:
      winLen = numFrames - fmCnt - fs
    else:
      winLen = fs
    
    # Apply windowing function to current and previous 1-second window,
    # and calculate the FFT of the frequencies up to Nyquist frequency
    # of windows.
    hann = np.hanning(winLen)
    window1 = hann*frames[fmCnt + fs - winLen: fmCnt + fs]
    window1 = np.abs(np.fft.fft(window1, bins))
    window1 = window1[:len(window1)/2]
    
    fmCnt += fs
    window2 = hann*frames[fmCnt : fmCnt + winLen]
    window2 = np.abs(np.fft.fft(window2, bins))
    window2 = window2[:len(window2)/2]
    
    # Compare each frequency change and add change to counter:
    for k in range(len(window1)):
      q = ( np.log(window2[k] + d) - np.log(window1[k] + d) )
      SF += q**2
    
    window1 = window2

  SF = SF / ((numFrames-1)*(fs-1))
  
  return SF


# FFT Plotting function:
def plot_fft(fileTup, bins=1024):

  # Retrieve file information
  f = fileTup[0]
  name = fileTup[1]
  fs = f.samplerate
  chan = f.channels
  numFrames = f.nframes
  format = f.format
  frames = f.read_frames(numFrames)
  al.Sndfile.seek(f, 0, 0, 'r')  # rewind 
  
  hann = np.hanning(numFrames)
  window = hann*frames                        # Apply windowing function
  window = np.abs(np.fft.fft(frames, bins))   # Give FFT of all frames
  window = window[:len(window)/2]             # Remove above Nyquist
  freqArray = arange(0, fs/2, float(fs)/bins) # Create frequency array
  
  # Plotting
  plot(freqArray, window, color='k', drawstyle='steps')
  title('FFT for ' + name + ' with ' + str(bins) + ' Bins')
  ylabel('Amplitude')
  xlabel('Frequency (Hz)')
  savefig('images/' + name[:-4] + 'FFT')
  show()


# Waveform plotting:
def plot_waveform(fileTup):

  # Retrieve file information
  f = fileTup[0]
  name = fileTup[1]
  fs = f.samplerate
  chan = f.channels
  numFrames = f.nframes
  format = f.format
  frames = f.read_frames(numFrames)
  al.Sndfile.seek(f, 0, 0, 'r')  # rewind 
  
  # Create x-axis array
  timeArray = arange(0, float(numFrames), 1)
  timeArray = timeArray / fs
  timeArray = timeArray * 1000  #scale to milliseconds
  
  # Plotting
  plot(timeArray, frames, color='k', drawstyle='steps')
  title(name + ' Waveform')
  ylabel('Amplitude')
  xlabel('Time (ms)')
  savefig('images/' + name[:-4] + 'Waveform')
  show()


# Evaluate audio file function returns a feature tuple:
def evaluate(fileTup):
  
  # Retrieve file information
  f = fileTup[0]
  name = fileTup[1]
  fs = f.samplerate
  chan = f.channels
  numFrames = f.nframes
  format = f.format
  frames = f.read_frames(numFrames)
  al.Sndfile.seek(f, 0, 0, 'r')  # rewind 
  
  # Extract features:
  f1 = hzcrr(frames, numFrames, fs)
  f2 = lster(frames, numFrames, fs)
  f3 = sf(frames, numFrames, fs)
  
  return (name, f1, f2, f3)


# Make orange tab-delimited data file method:
def create_data(f, s):
  
  # Write orange tab file statistical information:
  f.write('filename\tHZCRR\tLSTER\tSF\tspeech-music\n')
  f.write('discrete\tcontinuous\tcontinuous\tcontinuous\tspeech music\n')
  f.write('ignore\t\t\t\tclass\n') 

  # for each file in the directory specified with s,
  for infile in glob.glob('data/'+ s +'/*.wav'):      
    file, ext = os.path.splitext(infile)
    aud = al.Sndfile(infile, 'r')
    aud = (aud, file[-4:] + ext)
    if aud[1][:2] == 'sp':
      audioClass = 'speech'
    else:
      audioClass = 'music'
    data.append(aud)        # Add the audio file and name tupple to list
    featTup = evaluate(aud) # Give the feature tupple of the file
    # Write the results to the appropriate .tab file
    f.write(featTup[0] + '\t' + 
            str(featTup[1]) + '\t' +
            str(featTup[2]) + '\t' + 
            str(featTup[3]) + '\t' +
            audioClass + '\n')


# Compute classifier accuracy function:
def accuracy(test_data, classifiers):

    correct = [0.0]*len(classifiers)
    for ex in test_data:
      for i in range(len(classifiers)):
        if classifiers[i](ex) == ex.getclass():
          correct[i] += 1
    for i in range(len(correct)):
      correct[i] = correct[i] / len(test_data)
    
    return correct


# Machine learning function:
def classify():

  import orange, orngTree
  
  testData = orange.ExampleTable('data/audioTest.tab')
  trainData = orange.ExampleTable('data/audioTrain.tab')
  bayes = orange.BayesLearner(trainData)
  bayes.name = "bayes"
  tree = orngTree.TreeLearner(trainData)
  tree.name = "tree"
  classifiers = [bayes, tree]
  
  return classifiers, trainData, testData
  
  
# Function to write all the results to the results file:
def create_results(classifiers, testData):
  
  results = open('data/results', 'w')
  
  results.write("\n\n\tBayes Classifier:\n\n")
  for i in range(len(testData)):
    c = classifiers[0](testData[i])
    results.write("%d: %s (originally %s)\n" % 
                  (i+1, c, testData[i].getclass()))
  
  results.write("\n\n\tTree Classifier:\n\n")
  for i in range(len(testData)):
    c = classifiers[1](testData[i])
    results.write("%d: %s (originally %s)\n" % 
                  (i+1, c, testData[i].getclass()))
  results.write("\n")
    
  # compute accuracies
  acc = accuracy(testData, classifiers)
  results.write("Classification accuracies:\n")
  for i in range(len(classifiers)):
    results.write("\t%s: ~%d%%\n" % (classifiers[i].name, int(acc[i]*100)))
  
  results.close()


# 'main' function:
def main():
  
  # initialize the data list:
  del data[:]

  # Training set evaluations:
  features = open('data/audioTrain.tab', 'w')
  create_data(features, 'train')
  features.close()
  
  
  # Testing set evlauations:
  features = open('data/audioTest.tab', 'w')
  create_data(features, 'test')
  features.close()

  return data


