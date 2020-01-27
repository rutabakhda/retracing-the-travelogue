#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2, ax3)= plt.subplots(1, 3, sharex='col', sharey='row')
ax1.set_title("F1 for Chapter1")
ax1.set_ylabel('F1 score')
ax1.set_xlabel('NER tools')

#score = [0.45,0.50,0.37,0.68]
score = [0.40,0.35,0.40,0.54]
libraries = ['NLTK','spaCy','stanford','allenNLP']
index = np.arange(len(libraries))

ax1.bar(libraries,score,align='center',color='blue')


ax2.set_title("F1 for Chapter2")
ax2.set_ylabel('F1 score')
ax2.set_xlabel('NER tools')

#score = [0.58,0.52,0.51,0.69]
score = [0.39,0.50,0.43,0.66]
libraries = ['NLTK','spaCy','stanford','allenNLP']
index = np.arange(len(libraries))

ax2.bar(libraries,score,align='center',color='blue')

ax3.set_title("F1 for Chapter3")
ax3.set_ylabel('F1 score')
ax3.set_xlabel('NER tools')

#score = [0.56,0.54,0.62,0.76]
score = [0.51,0.42,0.52,0.74]

libraries = ['NLTK','spaCy','stanford','allenNLP']
index = np.arange(len(libraries))

ax3.bar(libraries,score,align='center',color='blue')

#plt.xticks(index, libraries, fontsize=5, rotation=30)
#ax.invert_yaxis()

plt.show()