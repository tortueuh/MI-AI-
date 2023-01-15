#------- IMPORTS AND CO -------#

from io import StringIO #reading lines
import time #test
import numpy #array
import PyPDF4 #reading pdf
import re #text modeling
import random #probability
import pandas as pd

# DATA SET :
words_data_row = numpy.empty(0, dtype=str)
words_data_100 = []
noised_collections = []

noise = numpy.empty(0, dtype=str)

# ALPHABET

DIKT = {" ":0,"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26,"é":27,"è":28,"ç":29,"à":30,"ù":31,"â":32,"ô":33,"ê":34,"î":35,"û":36,"ë":37,"6":0,"(":0,")":0,"[":0,"]":0,":":0,"ï":38}

# FUNCTIONS

def noise(proportion,word,formation):
    for i in range(len(word)):
        if random.randint(0,100) > proportion:
            word[i] = random.randint(0,formation[0])/formation[1]

    return word 


#------- TOKENIZING WORDS AND LINES -------#

def get_words(book,wrow,w100):

    #{- LOAD PDF FILE -}#

    pdfFileObj = open(book, 'rb')
    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)

    pages_text = pageObj.extractText()
    buf = StringIO(pages_text)
    
    #{- READ PDF FILE -}#

    for i in range(pdfReader.getNumPages()):
        buf = StringIO(pdfReader.getPage(i).extractText())

        for line in buf:

            #** removes wrong characters and removes empty lines **#

            line_temp = re.subn('[\n,.,,,?,!,;,0,1,2,3,4,5,6,7,8,9,),(,:,*,ì,ò,",«,»,ü]',"",re.subn("[-,',€]"," ",line)[0])[0].replace("[","").replace("]","").replace("/","").split(" ") 
            while "" in line_temp: line_temp.remove("",)
            
            for word in line_temp:
                
                #** reaches 20 chars per word **#

                while len(word) < 20: word+=" "

                #** converts chars to numbers **#

                tokenized_word = []
                for char in word: tokenized_word.append(DIKT[char.lower()])


                #** appends new int-words to data **#

                wrow = numpy.append(wrow,word.lower())
                w100.append(tokenized_word)
    
    return wrow, w100


# Atrocity #

l1 = get_words("DATAS/école_des_femmes.pdf",numpy.empty(0, dtype=str),[])
l2 = get_words("DATAS/malade_imaginaire.pdf",words_data_row,l1[1])
l3 = get_words("DATAS/avare.pdf",numpy.empty(0, dtype=str),l2[1])
l4 = get_words("DATAS/misanthrope.pdf",numpy.empty(0, dtype=str),l3[1])
l5 = get_words("DATAS/psyche.pdf",numpy.empty(0, dtype=str),l4[1])
l6 = get_words("DATAS/phedre.pdf",numpy.empty(0, dtype=str),l5[1])
l7 = get_words("DATAS/iphigenie.pdf",numpy.empty(0, dtype=str),l6[1])
l8 = get_words("DATAS/celinde.pdf",numpy.empty(0, dtype=str),l7[1])

words_data_row = numpy.unique(numpy.append(numpy.append(numpy.append(numpy.append(numpy.append(numpy.append(numpy.append(l1[0],l2[0]),l3[0]),l4[0]),l5[0]),l6[0]),l7[0]),l8[0]))
words_data_100 = numpy.array(l8[1])


words_data_100 = numpy.unique(words_data_100,axis=0)

print(len(words_data_100),len(words_data_row))

#------- NOISING AND CREATING NOISED COLLECTIONS -------#

for i in range(0,10):
    noised_collections.append([i*10,words_data_100.copy()])
    for tok_word in noised_collections[i][1]:
        tok_word = noise(noised_collections[i][0],tok_word,[38,1])



#-------  RETURN TO STRING -------#

#** creating new lists **#
S_words_data_100 = []
S_noised_collections = []
for i in range(0,10):
    S_noised_collections.append([i*10,[]])

#** turning list to string **#
for i in range(len(words_data_100)):
    S_words_data_100.append(str(words_data_100[i]))
    for j in range(10): S_noised_collections[j][1].append(str(noised_collections[j][1][i]))


#------- SAVING TO CSV FILE -------#

dicker = {"row":words_data_row,"100":S_words_data_100} #headers 

df = pd.DataFrame(data=dicker) # pandatification 
df.to_csv('DATAS/data_12k.csv', index=False) # saving