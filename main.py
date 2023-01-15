import time
import matplotlib.pyplot as plt
import numpy
import random
import tensorflow

#----------- IMMUTABLE OBJECTS -----------#

EPOCH_SIZE = 1000
BATCH_SIZE = 100
ALPHA_LIST = ["","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","é","è","ç","à","ù","â","ô","ê","î","ë"]
DATA_USED = "DATAS/data_12k.csv"

def NOISE(proportion,word,formation):
    worm = word # abomination of python
    for i in range(len(worm)): #list every letter (float) of the word
        if random.randint(0,100) > proportion: #probability applied
            worm[i] = random.randint(0,formation[0])/formation[1] #new letter, can both do  integrers (0-38) or float (0-1)

    return worm

#----------- LOADING DATA SETS -----------#

# get csv file datas #

arr = numpy.loadtxt(DATA_USED,delimiter=",", dtype=str)

# creating next dataset #

DATA_SETS = []
for k in range(12):
    DATA_SETS.append([])

# filling new dataset with RAW tokenized words #

for i in range(1,len(arr)): 
    DATA_SETS[1].append([int(x)/38 for x in list(filter(("").__ne__, str(arr[i][1][1:-1]).split(" ")))]) # turns numpy array into text, removes brackets from text, splits within spaces, removes them
                                                                                                         # convert into a list of integrers, normalize datas, add it to DATA_SETS first column

# creating a second dataset, copied from first one #

DATA_SETS_2 = DATA_SETS.copy()

# noising both datasets #

for k in range(0,len(DATA_SETS[1])): # listing all the tok-words
    for l in range(0,10): # listing all the columns = noising degree
        DATA_SETS[2+l].append(NOISE(90-l*10,DATA_SETS[1+l][k].copy(),(1000,1000))) #applying NOISE function to datas

for k in range(0,len(DATA_SETS_2[1])):
    for l in range(0,10):
        DATA_SETS_2[2+l].append(NOISE(90-l*10,DATA_SETS_2[1+l][k].copy(),(1000,1000)))




#-------- RANDOMIZE DATA SET --------#

# create new data set #

R_DATA_SETS = []
for k in range(2):
    R_DATA_SETS.append([])

# randomly add values of both DATA_SETS #

for i in range(0,12000): #get 12,000 first words
    column = random.randint(6,9) #get a random column
    R_DATA_SETS[0].append(DATA_SETS[11-column][i]) #fill in Xs
    R_DATA_SETS[1].append(DATA_SETS[11-column-1][i]) #fill in Ys

for i in range(0,12000): #get 12,000 first words
    column = random.randint(6,9) #//
    R_DATA_SETS[0].append(DATA_SETS_2[11-column][i]) #//
    R_DATA_SETS[1].append(DATA_SETS_2[11-column-1][i]) #//


#-------- KERAS AI MODEL --------#

model = tensorflow.keras.models.Sequential()

# add layers #

model.add(tensorflow.keras.layers.Dense(20, input_shape=(20,), activation='relu'))
model.add(tensorflow.keras.layers.Dense(8, activation='relu'))
model.add(tensorflow.keras.layers.Dense(12, activation='relu'))
model.add(tensorflow.keras.layers.Dense(30, activation='relu'))
model.add(tensorflow.keras.layers.Dense(20, activation='relu'))
model.summary()

# loading last weights, can be deleted #

model.load_weights("weights2.h5")

# compile and fit the model #

model.compile(optimizer=tensorflow.keras.optimizers.Adam(learning_rate=1e-3),
              loss="mean_squared_error",
              metrics=[tensorflow.keras.metrics.BinaryAccuracy()])


history = model.fit(R_DATA_SETS[0], R_DATA_SETS[1],
          batch_size=100,
          epochs=1000,
          verbose=2,
          validation_data=(R_DATA_SETS[0], R_DATA_SETS[1]))

# saving new weights as weights2 in main directory #

model.save_weights("weights2.h5")

#-------- PYPLOT GRAPHICS --------#

train_loss = history.history['loss']
val_loss   = history.history['val_loss']
xc         = range(1000)

plt.figure()
plt.plot(xc, train_loss)
plt.plot(xc, val_loss)
plt.show()

##-------- GENERATION TEST --------#

"""
rfile = numpy.append(numpy.random.uniform(low=0.0, high=1.0, size=(5,)),[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
test = rfile #DATA_SETS[2][9]
result = rfile # DATA_SETS[1][9]




e = tensorflow.constant([test])


prediction = model.predict(e)
for i in range(5000):
    prediction = model.predict(e)

word = ""
for s in prediction[0]:
    word += alphabet[int(float(s)*38)]
initial_word = ""

f_word = ""

for s in test:
    f_word += alphabet[int(float(s)*38)]

print("Est parti de "+f_word+" ; devait trouver "+initial_word+" ; a trouvé : "+word)
"""