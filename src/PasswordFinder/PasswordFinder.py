#Dang To          Email: dangto@vt.edu
#Toru Oyama       Email: toyama1@vt.edu

import hashlib
import matplotlib.pyplot as plt
import time
import itertools
from itertools import combinations, permutations

#Function for encrypting to 256
def encrypt256(answer):
    signature = \
        hashlib.sha256(answer.encode()).hexdigest()
    return signature

#Function for encrypting to 512
def encrypt512(answer):
    signature = \
        hashlib.sha512(answer.encode()).hexdigest()
    return signature

#Function for finding the password based on which SHA type
def findPassword(type):
    global found, currentGuess, this_time, guesses, pass256, pass512, test256, test512, min, passwordLength, total_time, elapsed
    
    found = False
    currentGuess = ''
    this_time = time.time()
    guesses = 0
    test256 = ""
    test512 = ""
    
    # Try all combinations
    #Uses floor division to find the max number of minimum length words required 
    #to fill out the password(Helps efficiency)
    for length in range(1, (passwordLength // min) + 1):
        if found == True:
            break
        
        #Uses product from itertools since we don't know if there are repeats in the password.
        #Also converts it to a list so we can use it.
        allCombos = list(itertools.product(word_list, repeat=length))
        for currentGuess in allCombos:
            guesses += 1
            #If length of the currentGuess is length passwordLength, encyrpt and check
            if type == 256:
                test256 = encrypt256(''.join(currentGuess))
            elif type == 512:
                test512 = encrypt512(''.join(currentGuess))
            #The check
            if test256 == pass256 or test512 == pass512:
                elapsed = time.time() - this_time
                
                found = True
                print("SHA" + str(type) + ":Password found in " + str(elapsed) + " seconds with " + str(guesses) + " guesses!")
                
                total_time += elapsed
                break




total_time = 0.0

#Asks for input file as well as password to brute force
inputFile = input('Which dictionary file do you want to test: ')

#Reads the dictionary words into an array
f = open(inputFile, "r")
word_list = []
for word in f:
    word_list.append(word.rstrip())

print('Dictionary file ' + inputFile + ' is of length ' + str(len(word_list)))
answer = input('Type a combination of words from the dictionary to be your password: ')

#Encrypts our password into SHA 256/512  
pass256 = encrypt256(answer)
pass512 = encrypt512(answer)
test256 = ""
test512 = ""

#Gets the length of the password and brute forces combinations{All below}
passwordLength = len(answer)

#Find the minimum length of a word in the dictionary file
min = len(word_list[0])
for dictionaryLength in range(1, len(word_list)):
    if len(word_list[dictionaryLength]) < min:
        min = len(word_list[dictionaryLength])

print('Password is being found...')
#Looked up matPlotLib. Site used was https://matplotlib.org/stable/tutorials/introductory/pyplot.html
names = ['SHA256', 'SHA512']
values = [0, 0]

findPassword(256)
values[0] = elapsed

findPassword(512)
values[1] = elapsed

plt.figure(figsize=(9, 3))
plt.subplot(132)
plt.ylabel('Time')
plt.bar(names, values)
plt.suptitle('SHA256 vs SHA512')
plt.show()
#End of reference

