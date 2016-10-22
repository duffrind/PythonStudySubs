# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:56:46 2016

Stand-alone Japanese SRS creator

@author: duffrind
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tinysegmenter
import csv
import re
import json

segmenter = tinysegmenter.TinySegmenter()

class App:
    def __init__(self):
        self.root = tk.Tk()
        button = tk.Button(self.root, text="Quit", fg="red", command=self.quit)
        button.pack(side=tk.LEFT)
        srs = tk.Button(self.root, text="Create SRS", command=self.openfile)
        srs.pack(side=tk.LEFT)
        self.root.mainloop()
    def quit(self):
        self.root.destroy()
        return
    def openfile(self):
        file = filedialog.askopenfilename()
        f = open(file,'r')
        filename, _ = os.path.splitext(file)
        csvf = open(filename + '.csv','w+')
        writer = csv.writer(csvf,delimiter='\t')
        word_set = set()
        foo = f.read()
        try:
            f = open(file,'r',encoding='UTF8')
            ftext = f.read()
            m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , ftext)
        except:
            f = open(file,'r',encoding='UTF16')
            ftext = f.read()
            m = re.findall("""[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uff62-\uff9f].*\n?""" , ftext)
        for line in m:
            word_set = word_set | set(segmenter.tokenize(line))
        with open('word_dictionary.json', 'r') as f1:
            try:
                word_dict = json.load(f1)
            except ValueError:
                word_dict = {}
        word_set = word_set & set(word_dict.keys())
        writer.writerow(['vocab','pronunciation','part of speech','meaning'])
        for word in word_set:
            writer.writerow([word] + word_dict[word].split('\t'))
        messagebox.showinfo('StudySubs','Successfully created ' + filename + '.csv')
        return


app = App()
