#!/usr/bin/env python3

from random import *
import random
import copy
import math
from itertools import combinations, permutations

#Glabal variable

#The answer of the 4A
secret = [0,0,0,0]
#record all the player guessing 
history = []
#record the posible 4B arrange
posible = []
#The step to call this game
step = []
#record the good stuff(the number in secret)
gdStuff = []
#record the bad stuff(the number NOT in secret)
bdStuff = [0,1,2,3,4,5,6,7,8,9]

#first,second,third elements are result of the warm-up guessing,
#the elements after are STEP! 
#it show how to slove that kind of problem
#Example:
# if warm-up guessing result is (0,2,2), it will follow the 
# step below
# [ 0 , 2 , 2 , 8 , 9 , 102 ] 
#               ^   ^
#             This means 8 and 9 should add in gdStuff[]
# [ 0 , 2 , 2 , 8 , 9 , 102 ] 
#                        ^
#            This mean should deal with step No.102
dataBase = [[0,2,2,8,9,102],
 [0,3,1,101,105],
 [1,3,0,101,104],
 [2,0,2,2,3,8,9],
 [2,0,3,8,9,103,104],
 [2,2,0,2,3,102],
 [3,0,2,2,3,103,105],
 [3,0,3,0,1,104,105],
 #with 3B 
 [1,1,3,8,9,103,106],
 [1,3,1,101,103],
 [2,1,3,0,1,105,106],
 [3,1,2,0,1,104,106],
 [3,1,1,2,3,103,106],
 #others
 [1,1,2,8,9,104,106],
 [1,2,1,102,104,105],
 [1,2,2,102,103,105],
 [2,1,1,2,3,105,106],
 [2,2,1,102,103,104],
 [2,2,2,0,1,102],
 #special case (no stuff)
 [2,1,2,107,103,104,105],
 #with 4B
 [4,0,2,0,1,2,3],
 [0,4,0,4,5,6,7],
 [2,0,4,0,1,8,9]]

#kind of dataBase
'''
To find what to do when encounter 101 ,102, 103, 104... etc.
 101 means "4567" has THREE correct number in it.
 102 means "4567" has TWO   correct number in it.
 103 means "01"   has ONE   correct number in it.
 104 means "23"   has ONE   correct number in it.
 105 means "89"   has ONE   correct number in it.
 106 means "4567" has ONE   correct number in it.
 107 means special case (2,1,2) with no stuff confirm at all.

every ans means one guess, the first element of ans is the form 
of the guess, example , "ss45" means two stuff plus '4' and '5'
the elements after are condition of the guessing output. example
 ["ss45", "1B", "2G67 NX201", "2B", "2G45 NX202"]
    ^ 
  guess should be [stuff, stuff, 4, 5]

 ["ss45", "1B", "2G67 NX201", "2B", "2G45 NX202"]
           ^ 
   if the output of guessing is "1B", then execute the indicate 
   after ,which is "2G67 NX201"

 ["ss45", "1B", "2G67 NX201", "2B", "2G45 NX202"]
                 ^
  "2G67" means 2 numbers '6' and '7' should add in gdstuff[]
  "NX201" means should go to next deeper layer to slove the 
   problem, the next layer is NO.201

 ["ss45", "1B", "2G67 NX201", "2B", "2G45 NX202"]
                               ^
   if the out of guessing is "2B", then execute teh indicate
   after, which is "2G45 NX202"

 ["ss45", "1B", "2G67 NX201", "2B", "2G45 NX202"]
                                     ^
  "2G45" means 2 numbers '4' and '5' should add in gdstuff[]
  "NX202" means should go to next deeper layer to slove the 
   problem, the next layer is NO.202
'''

def breakStep (step):
  ans = []
  #first layer
  if step == 101:
    ans = ["ss45","1B", "2G67 NX201", "2B", "2G45 NX202"]
  elif step == 102:
    ans = ["ss45", "0B", "2G67 2B45", "1B", "NX203" , "2B", "2G45 2B67"]
  elif step == 103:
    ans = ["sss0", "0B", "1G1 1B0", "1B", "1G0 1B1"]
  elif step == 104:
    ans = ["sss2", "0B", "1G3 1B2", "1B", "1G2 1B3"]
  elif step == 105:
    ans = ["sss8", "0B", "1G9 1B8", "1B", "1G8 1B9"]
  elif step == 106:
    ans = ["ss45", "0B", "NX205", "1B" , "NX206"]
  #special case (2,1,2)
  elif step == 107:
    ans = ["2345", "1B", "2B45 NX207", "2B" , "2B67 NX208"]
  
  #second layer
  elif step == 201:
    ans = ["sss4", "0B", "1G5 1B4", "1B", "1G4 1B5"]
  elif step == 202:
    ans = ["sss6", "0B", "1G7 1B6", "1B", "1G6 1B7"]
  elif step == 203:
    ans = ["ss56", "0B" ,"2G47 2B56", "1B" ,"NX204", "2B", "2G56 2B47"]
  elif step == 204:
    ans = ["ss46", "0B","2G57 2B46", "2B", "2G46 2B57"]
  elif step == 205:
    ans = ["sss6", "0B","1G7 3B456", "1B", "1G6 3B457"]
  elif step == 206:
    ans = ["sss4", "0B","1G5 3B467", "1B", "1G4 3B567"]
  elif step == 207:
    ans = ["0156", "1B", "1G7 1B6", "2B", "1G6 1B7"]
  elif step == 208:
    ans = ["0156", "1B", "1G4 1B5", "2B", "1G5 1B4"]
  return ans


'''
find stuff to stuff the guess.
stuffNum is how many stuffs you need to find
the return will be a list with stuffs you need 
could be all gdStuff or all bdStuff or both kinds combined
Example:
if stuffNum is 3, then the output will be like 
['good', 0 , 2, 'bad', 9]
element after 'good' are good stuffs, 0 and 2
element after 'bad'  is  bad  stuff , 9
'''
def getStuff(stuffNum):
  ans = []
  #only use good stuff 
  if len(gdStuff) >= stuffNum:
    ans.insert(0,"good")
    for i in range(stuffNum):
      ans.append(gdStuff[i])
  
  #combine both good stuff and bad stuff
  elif len(gdStuff) + len(bdStuff) >= stuffNum and len(gdStuff) > 0:
    ans.insert(0, "good")
    for i in gdStuff:
      ans.append(i)
    ans.append("bad")
    for i in range(stuffNum - len(gdStuff)):
      ans.append(bdStuff[i])

  #only use bdStuff 
  elif len(bdStuff) >= stuffNum:
    ans.insert(0,"bad")
    for i in range(stuffNum):
      ans.append(bdStuff[i])
  
  else: #not enough stuff
    ans.insert(0,-1)
  
  #print ("getStuff: ", ans)
  return ans  


# execute the indicate
def solveLayer(layer):
  
  guess = []
  #get StuffNUm
  stuffNum = 0  
  for i in range(4):
    if layer[0][i] == 's':
      stuffNum += 1
    else :
      guess.append(int(layer[0][i]))
  tmp = getStuff(stuffNum)

  #get numOfGdStuff
  numOfGdStuff = 0
  goodtmp = False
  for i in tmp :
    if i == "good":
      goodtmp = True
    elif i == "bad":
      goodtmp = False
    elif i == -1 : 
      print ("not enough stuff to solve")
      return 
    else:
      guess.append(i)
      if goodtmp == True:
        numOfGdStuff += 1
  
  #get condition
  output = hintGiven(guess)
  output = output%10 + math.floor(output/10)
  condition = str(output - numOfGdStuff) + "B"
  printHis()
  
  #get indicate
  tmp = layer[layer.index(condition) + 1]
  indicate = tmp.split()
  print ("[Test] indicate = ", indicate)
  
  #solve indicate
  for i in indicate:
    if i[0] == "N" and i[1] == "X":
      tmp  = int(i[2:5])
      solveLayer(breakStep(tmp))
    else:
      if i[1] == "G":
        for j in range(int(i[0])):
          gdStuff.insert(0,int(i[j+2]))
      elif i[1] == "B":
        for j in range(int(i[0])):
          bdStuff.insert(0,int(i[j+2]))

def checkSame (secret):
  for i in range(4):
    for j in range(3):
      temp = copy.copy(secret)
      temp.remove(secret[i])
      if secret[i] == temp[j]:
        return True;
  return False;

#Do the guess!!
def hintGiven (guess):
  ans = 0
  for i in range(4):
    for j in range(4):
      if guess[i] == secret[j]:
        if i==j : # _A
          ans += 10
        else:   #_B 
          ans += 1
  
  tmp = copy.copy(guess)
  tmp.insert(len(tmp), ans)
  history.insert(len(history), tmp)
  return ans

#after 4B is found, delete the combinations that's not posible.
def isPosible(pos, his, his_ans):
  ans = 0
  for i in range(4):
    for j in range(4):
      if pos[i] == his[j]:
        if i==j : # _A
          ans += 10
        else:   #_B 
          ans += 1
  
  if ans == his_ans:
    return True
  else: 
    return False

#genarate a random 4 number list. 
def ranGen ():
  try:
    output = [0,0,0,0]
    while checkSame(output):
      output = [0, 0, 0, 0]
      output[0] = randint(0,9)
      output[1] = randint(0,9)
      output[2] = randint(0,9)
      output[3] = randint(0,9)
  except ValueError as err : 
    print (err)
  return output

#help you print the result of guessing "? A ? B"
def printHint (tmp):
  hint = [0,0]
  hint[0] = math.floor(tmp/10)
  tmp = tmp - hint[0]*10
  hint[1] = math.floor(tmp)
  print ( hint[0], "A" , hint[1], "B")
  return 

#help you print history[]
def printHis ():
  print ("****HISTORY**** ")
  for i in history:
    print (i[0:4], "    ", end='')
    printHint(i[4])

#get all the guessing result from the warm-up.
#and return the accordingly step.
def getStep ():
  indice = [-1,-1,-1]
  tmp = history[0][4]
  indice[0] = int(tmp%10 + (tmp - tmp%10)/10)
  tmp = history[1][4]
  indice[1] = int(tmp%10 + (tmp - tmp%10)/10)
  tmp = history[2][4]
  indice[2] = int(tmp%10 + (tmp - tmp%10)/10)
  
  for i in dataBase:
    if i[0:3] == indice:
      step = copy.copy(i)
      break
  print ("step : ", step)
  return step 

#convert four digits number into List with 4 elements.
#return the List
def numToList (num):
  ans = [0,0,0,0]
  ans[0] = math.floor(num/1000)
  num = num - ans[0]*1000
  ans[1] = math.floor(num/100)
  num = num - ans[1]*100
  ans[2] = math.floor(num/10)
  num = num - ans[2]*10
  ans[3] = math.floor(num/1)
  return ans

#compare history and posible, delete the imposible combinations.
def fourA ():
  ans = []
  for i in list(permutations(gdStuff, 4)):
    isGood = True
    for j in history:
      if not isPosible(i, j[0:4], j[4]):
        isGood = False
        break
    if isGood:
      ans.insert(0,i)
  return ans


# main start here
print("Let's play 2A2B !!")
msg = input("Give me a 4 digit secret number!!(or press enter to generate a random number):")
if msg == '':
  secret = ranGen()
else:
  secret = numToList(int(msg))
print("The answer is " , secret)

msg = input("Do I have to guess myself? (y/n)")
if msg == 'y' or msg == '':
  hintGiven([0,1,2,3])
  hintGiven([4,5,6,7])
  hintGiven([0,1,8,9])
  printHis()
  step = getStep()

  #parse the step 
  for i in range(3):
    step.pop(0)
 
  #get good stuff
  while len(step) != 0 and step[0] < 100:
    gdStuff.insert(0,step[0])
    bdStuff.remove(step[0])
    step.pop(0)

  #get bad stuff
  for i in step:
    if i==101 or i==102 or i==106 :
      bdStuff.remove(4)
      bdStuff.remove(5)
      bdStuff.remove(6)
      bdStuff.remove(7)
    elif i==103 :
      bdStuff.remove(0)
      bdStuff.remove(1)
    elif i==104 :
      bdStuff.remove(2)
      bdStuff.remove(3)
    elif i==105 :
      bdStuff.remove(8)
      bdStuff.remove(9)

  print ("Good stuff : " , gdStuff)
  print ("Bad stuff : " , bdStuff)
  
  while step:
    #first layer and second layer
    solveLayer(breakStep(step[0]))
    step.pop(0)
           
  print (" ")
  print ("***************")
  print ("****  4B  *****")
  print ("***************")
  print (" ")
  print ("Good stuff", gdStuff)
  print ("Bad stuff", bdStuff)
  
  while len(posible) != 1:
    posible = fourA()
    print("posible: ", posible)
    hintGiven(list(posible[0]))
  
  if list(posible[0]) == secret :
    print (" ")
    print ("**************************")
    print ("****  4A game over!!  ****")
    print ("**************************")
    print ("the secret answer is ", posible[0])
    print ("I used ", len(history), end='')
    print (" guess to win the game.")
  else :
    print ("Something goes wrong")
  

else:
  while True : 
    msg = input("Give 4 number (enter 'q' to quit) : ");
    if msg == 'q':
      print ("bye bye ~~")
      break
    if msg == 'his':
      printHis()
      continue
    
    guess = numToList(int(msg))
    print ("your guess is ", guess)
    printHint(hintGiven(guess))
    if hintGiven(guess) == 40: 
      print ("CORRENT ANS!!")
      print ("bye bye ~~")
      break 

