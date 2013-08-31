# audioGUI.py
# Evan Cummings
# Fall '11 - Min Chen
# CSCI 478 - Multimedia Data Processing
# Program to classify audio as speech or music.


from Tkinter import *
import audio


# Main app.
class Viewer(Frame):
    
    # Constructor.
    def __init__(self, master, resultWin):
                
        Frame.__init__(self, master)
        self.master    = master
        self.resultWin = resultWin
                
        
        # Create Main frame.
        mainFrame = Frame(master)
        mainFrame.pack()
        
        
        # Create Picture chooser frame.
        listFrame = Frame(mainFrame)
        listFrame.pack(side=LEFT)
        
        
        # Create Control frame.
        controlFrame = Frame(mainFrame)
        controlFrame.pack(side=RIGHT)
        
        
        # Create Preview frame.
        previewFrame = Frame(mainFrame, 
            width=200, height=100)
        previewFrame.pack_propagate(0)
        previewFrame.pack(side=RIGHT)
        
        
        # Create Results frame.
        resultsFrame = Frame(self.resultWin)
        resultsFrame.pack(side=BOTTOM)
        resultsScrollbar = Scrollbar(resultsFrame)
        text = Text(resultsFrame, relief=SUNKEN)
        resultsScrollbar.config(command=text.yview)
        text.config(yscrollcommand=resultsScrollbar.set)
        resultsScrollbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
        
        
        # Layout audio file listbox.
        self.listScrollbar = Scrollbar(listFrame)
        self.listScrollbar.pack(side=RIGHT, fill=Y)
        self.list = Listbox(listFrame, 
            yscrollcommand=self.listScrollbar.set, 
            selectmode=BROWSE, 
            height=10)
        for i in range(len(audio.data)):
            self.list.insert(i, audio.data[i][1])
        self.list.pack(side=LEFT, fill=BOTH)
        self.list.activate(1)
        self.list.bind('<<ListboxSelect>>', self.update_preview)
        self.listScrollbar.config(command=self.list.yview)
        
        
        # Layout Controls.
        button = Button(controlFrame, text="Evaluate", 
            fg="red", padx = 10, width=10, 
            command=lambda: self.evaluate())
        button.grid(row=0, column=0, sticky=E)
        
        self.b1 = Button(controlFrame, text="Classify", 
            padx = 10, width=10, 
            command=lambda: self.update_results())
        self.b1.grid(row=1, column=0, sticky=E)
        
        b2 = Button(controlFrame, text="Plot Waveform", 
            padx = 10, width=10, 
            command=lambda: self.plot_waveform())
        b2.grid(row=2, column=0, sticky=E)

        b3 = Button(controlFrame, text="Plot FFT", 
            padx = 10, width=10, 
            command=lambda: self.plot_fft())
        b3.grid(row=3, column=0, sticky=E)
        
                
        # Layout Preview.
        self.fs = Label(previewFrame, text='Samplerate: ')
        self.fs.pack()
        self.chan = Label(previewFrame, text='Channels: ')
        self.chan.pack()
        self.nFrames = Label(previewFrame, text='Number of Frames: ')
        self.nFrames.pack()


    # Event "listener" for listbox change updates the audio properties:
    def update_preview(self, event):
    
        i = self.list.curselection()[0]
        self.fs.configure(text='Samplerate: ' + 
                                str(audio.data[int(i)][0].samplerate) +
                                ' Hz')
        self.chan.configure(text='Channels: ' +
                                  str(audio.data[int(i)][0].channels))
        self.nFrames.configure(text='Number of Frames: ' +
                                     str(audio.data[int(i)][0].nframes))


    # Update the results window with the sorted results.
    def update_results(self):
        
        classifiers, trainData, testData = audio.classify()
        audio.create_results(classifiers, testData)
        results = open('data/results', 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', results)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()
    
    
    # Evaluate the audio files and write them to the .tab files:
    def evaluate(self):
    
        audio.main()
        for i in range(len(audio.data)):
            self.list.insert(i, audio.data[i][1])
        
    
    # Plot the waveform.
    def plot_waveform(self):
    
        i = self.list.curselection()[0]
        audio.plot_waveform(audio.data[int(i)])
    
    
    # Plot the fft.
    def plot_fft(self):
    
        i = self.list.curselection()[0]
        audio.plot_fft(audio.data[int(i)])


# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('Audio Classification')

    resultWin = Toplevel(root)
    resultWin.title('Results')
    resultWin.protocol('WM_DELETE_WINDOW', lambda: None)

    viewer = Viewer(root, resultWin)

    root.mainloop()

