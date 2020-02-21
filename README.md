# 2A2B
A program can paly 2A2B itself.

## Usage 
```
$ python3 2a2b.py
```
After execute the program, you will see following question.
```
Let's play 2A2B !!
Give me a 4 digit secret number!!(or press enter to generate a random number)
``` 
Now you can enter 4 digit numbers(e.g. '1357' , '0751') to let computer guess, or press enter key to generate a random number instead.

```
Do I have to guess myself? (y/n)
```
Enter 'y' if you want computer guess automatically.

Enter 'n' to guess secret number yourself, and let computer verify it.

If you choose guess yourself, following message will show up and you have to recussively guess 4 digit number until you get 4A0B. 
```
Give 4 number (enter 'q' to quit) : 1366  
your guess is  [1, 3, 6, 6]
1 A 1 B
```

If you choose computer guessing , it will start palying instantly , and print out the guess process. Something like that.

```
****HISTORY**** 
[0, 1, 2, 3]     0 A 1 B
[4, 5, 6, 7]     0 A 1 B
[0, 1, 8, 9]     0 A 2 B
step :  [1, 1, 2, 8, 9, 104, 106]
Good stuff :  [9, 8]
Bad stuff :  [0, 1]
****HISTORY**** 
[0, 1, 2, 3]     0 A 1 B
[4, 5, 6, 7]     0 A 1 B
[0, 1, 8, 9]     0 A 2 B
[2, 9, 8, 0]     1 A 2 B
[Test] indicate =  ['1G2', '1B3']
****HISTORY**** 
[0, 1, 2, 3]     0 A 1 B
[4, 5, 6, 7]     0 A 1 B
[0, 1, 8, 9]     0 A 2 B
[2, 9, 8, 0]     1 A 2 B
[4, 5, 2, 9]     0 A 3 B
[Test] indicate =  ['NX206']
****HISTORY**** 
[0, 1, 2, 3]     0 A 1 B
[4, 5, 6, 7]     0 A 1 B
[0, 1, 8, 9]     0 A 2 B
[2, 9, 8, 0]     1 A 2 B
[4, 5, 2, 9]     0 A 3 B
[4, 2, 9, 8]     0 A 4 B
[Test] indicate =  ['1G4', '3B567']
 
***************
****  4B  *****
***************
 
Good stuff [4, 2, 9, 8]
Bad stuff [7, 6, 5, 3, 0, 1]
posible:  [(8, 9, 4, 2)]
 
**************************
****  4A game over!!  ****
**************************
the secret answer is  (8, 9, 4, 2)
I used  7 guess to win the game.
```
In this example, computer finally got the ans : (8,9,4,2), and it take 7 guesses to complete this game. Theoretically, it won't take more than 9 steps to win.

Previous messages show the guessing process that computer did. 
HISTORY means numbers computer has guessed.

Good stuff means numbers that definitely in secret number.

Bad stuff means numbers that definitely NOT in secret number.
