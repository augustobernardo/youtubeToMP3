from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from pathlib import Path
import os

# Create a window
root = Tk()

class youtubeToMp3:
    def __init__(self, arrUrls, outdir):
        self.arrUrls = arrUrls
        self.outdir = outdir
    
    def _popupDownloadError(self):
        popup = Tk()
        popup.wm_title("ERRO")
        label = Label(popup, text="Por favor, insira pelo menos uma URL!")
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="OK", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def _popupInvalidUrls(self, invalidUrls):
        popup = Tk()
        popup.wm_title("ERRO")
        popup.geometry("535x390")

        if len(invalidUrls) == 1:
            label = Label(popup, text="A seguinte URL não é válida: ")
        else:
            label = Label(popup, text="As seguintes URLs não são válidas: ")

        label.pack(side="top", fill="x", pady=10)
        for url in invalidUrls:
            youtube = YouTube(url)
            label = Label(popup, text=youtube.title)
            label.pack(side="top", fill="x", pady=10)

        B1 = Button(popup, text="OK", command = popup.destroy)
        B1.pack()
        popup.mainloop()
        
    def _popupValidUrls(self, validUrls):
        popup = Tk()
        popup.wm_title("Sucesso")
        popup.geometry("535x390")

        if len(validUrls) == 1:
            label = Label(popup, text="O seguinte vídeo foi instalado com sucesso: ")
        else:
            label = Label(popup, text="Os seguintes vídeos foram instalados com sucesso: ")

        label.pack(side="top", fill="x", pady=10)
        for url in validUrls:
            youtube = YouTube(url)
            label = Label(popup, text=youtube.title)
            label.pack(side="top", fill="x", pady=10)

        B1 = Button(popup, text="OK", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def _popupDuplicateUrls(self, duplicateUrls):
        popup = Tk()
        popup.wm_title("ERRO")
        popup.geometry("535x390")

        if len(duplicateUrls) == 1:
            label = Label(popup, text="O seguinte vídeo já foi instalado: ")
        else:
            label = Label(popup, text="Os seguintes vídeos já foram instalados: ")

        label.pack(side="top", fill="x", pady=10)
        for url in duplicateUrls:
            youtube = YouTube(url)
            label = Label(popup, text=youtube.title)
            label.pack(side="top", fill="x", pady=10)

        B1 = Button(popup, text="OK", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def _outDirSelect(self):
        folderSelected = filedialog.askdirectory()
        # Frame to label Out Directory
        frameOutDirLabelBelow = Frame(root)
        frameOutDirLabelBelow.grid(row=3, column=0, padx=10, pady=10)
        # Label to Out Directory
        labelOutDir = Label(frameOutDirLabelBelow, text=f"Diretório selecionado: {folderSelected}")
        labelOutDir.grid(row=0, column=2)

        self.outdir = folderSelected

    def download(self):
        if self.arrUrls == ['']:
            self._popupDownloadError()
            return
        else: 
            self.convertToMp3()

    def convertToMp3(self):
        invalidUrls = []
        validUrls = []
        duplicateUrls = []

        for url in self.arrUrls:
            try:
                youtube = YouTube(url)
                validUrls.append(url)
            except:
                invalidUrls.append(url)
                continue
            video = youtube.streams.filter(abr='160kbps').last()
            out_file = video.download(output_path=self.outdir)
            base, ext = os.path.splitext(out_file)
            new_file = Path(f'{base}.mp3')

            if new_file.exists():
                duplicateUrls.append(url)
                continue
            os.rename(out_file, new_file)

            if new_file.exists() and url == self.arrUrls[-1]:
                self._popupValidUrls(validUrls)
                return
        if invalidUrls != []:
            self._popupInvalidUrls(invalidUrls)
            return
        elif duplicateUrls != []:
            self._popupDuplicateUrls(duplicateUrls)
            return

    def getOutDir(self):
        return self.outdir

    def getUrls(self):
        return txt.get("1.0", END).splitlines()

# ========= #
# Functions #
# ========= #
def selectOutdir():
    youtubeToMp3._outDirSelect(youtubeToMp3)

def getData():
    arrUrls = youtubeToMp3.getUrls(youtubeToMp3)
    outDir = youtubeToMp3.getOutDir(youtubeToMp3)
    ytClass = youtubeToMp3(arrUrls, outDir)
    ytClass.download()

# Create a initial frame to put all the widgets in it
app = Frame(root)
app.grid()
root.title("YouTube to MP3 Converter")
root.geometry("450x390") # Define a size for the window

# Frame to label urls
frameUrlsLabel = Frame(root)
frameUrlsLabel.grid(row=0, column=0, padx=10, pady=10)
# Label to urls
labelUrls = Label(frameUrlsLabel, text="Insira as URLs que você deseja converter: ")
labelUrls.grid(row=0, column=0)

# Frame to TextBox and Scrollbar
frameUrls = Frame(root)
frameUrls.grid(row=1, column=0, padx=10, pady=10)
# TextBox to urls
txt = Text(frameUrls, height=10 , width=50)
txt.grid(row=0, column=2)
# Add a scroll bar to the text box
scroll = Scrollbar(frameUrls, command=txt.yview)
scroll.grid(row=0, column=3, sticky='nsew')
txt['yscrollcommand'] = scroll.set

# Frame and label Out Directory
frameOutdirLabel = Frame(root)
frameOutdirLabel.grid(row=2, column=0, padx=10, pady=10)
labelOutDir = Label(frameOutdirLabel, text="Insira o diretório de saída: ")
labelOutDir.grid(row=0, column=0)
# Button select Out Directory 
buttonOutdir = Button(frameOutdirLabel, text="Selecionar diretório", command=selectOutdir)
buttonOutdir.grid(row=0, column=1)

# Frame to button download and convert
frameDownloadConvert = Frame(root)
frameDownloadConvert.grid(row=4, column=0, padx=10, pady=10)
# Button to download and convert
btnConvert = Button(frameDownloadConvert, text="Converter", command=getData)
btnConvert.grid(row=0, column=0)

root.mainloop()