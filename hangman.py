# Problem Set 2, hangman.py
# Name: Seduhina Alina
# Collaborators:
# Time spent: 4 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string, re

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word_letters = [ ]
    for i in range(len(secret_word)):
        word_letters.append(secret_word[i])
    if (set(word_letters))&(set(letters_guessed)) == set(word_letters):
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_now = []
    word_letters = []
    for i in range(len(secret_word)):
        word_letters.append(secret_word[i])
        word_now.append("_ ")
    for i in range(len(word_letters)):
        if word_letters[i] in letters_guessed:
            word_now.pop(i)
            word_now.insert(i, word_letters[i])
    word_now = "".join(word_now)
    return word_now



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = (set(string.ascii_lowercase)).difference(set(letters_guessed))
    available_letters = "".join(available_letters)
    return available_letters
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!I am thinking of a word that is ", len(secret_word), ' letters long.')
    vowels = ['a', 'e', 'i', 'o', 'u']
    n = 6
    warnings = 3
    letters_guessed = [ ]
    while n > 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print( "-------------")
        print('You have ', n, ' guesses left.')
        print("Available letters: ", get_available_letters(letters_guessed))
        letter = input('Guess a letter ')
        if letter.isalpha() and len(letter) == 1:
            letter = letter.lower()
            if letter not in letters_guessed:
                letters_guessed.append(letter)
                if letter in secret_word:
                    print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
                else:
                    print('Your letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
                    if letter in vowels:
                        n -= 2
                    else:
                        n -= 1
            else:
                print("You already tried this letter")
        else:

            if warnings > 0:
                warnings -= 1
                print(warnings, " warnings left")
            else:
                n -=1
    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        print("Congratulations, you won! Your score: ", (n*(len(secret_word))))
    else:
        print("You failed, my word was ", secret_word)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace("_ ", "\w")
    match = re.findall(my_word, other_word)
    if match!=[ ]:
        if match[0]==other_word:
            my_word = my_word.replace("\w", "")
            for i in range(len(my_word)):
                if re.findall(my_word[i], my_word) != re.findall(my_word[i], other_word):
                    return False
            return True
        else:
            return False
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = [ ]
    for i in range(len(wordlist)):
        if match_with_gaps(my_word, wordlist[i]) == True:
            matches.append(wordlist[i])
    matches = " ".join(matches)
    return matches



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!I am thinking of a word that is ", len(secret_word), ' letters long.')
    vowels = ['a', 'e', 'i', 'o', 'u']
    n = 6
    warnings = 3
    letters_guessed = []
    while n > 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print("-------------")
        print('You have ', n, ' guesses left.')
        print("Available letters: ", get_available_letters(letters_guessed))
        letter = input('Guess a letter ')
        if letter.isalpha() and len(letter) == 1:
            letter = letter.lower()
            if letter not in letters_guessed:
                letters_guessed.append(letter)
                if letter in secret_word:
                    print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
                else:
                    print('Your letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
                    if letter in vowels:
                        n -= 2
                    else:
                        n -= 1
            else:
                print("You already tried this letter")
        elif letter=='*':
            print('Possible word matches are:', show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        else:

            if warnings > 0:
                warnings -= 1
                print(warnings, " warnings left")
            else:
                n -= 1
    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        print("Congratulations, you won! Your score: ", (n * (len(secret_word))))
    else:
        print("You failed, my word was ", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
