import random
import re
import requests
import Color
from collections import defaultdict
from bs4 import BeautifulSoup
from IPython.display import display


url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'


def main():
    while True:
        try:
            word_length = int(input('Choose the word length (3 ≤ x ≤ 45): '))
            print(word_guessr(word_length))
            return
            
        except ValueError:
            print('Invalid word length. Retry...')


def dictionary(url_, length=5):
    if not isinstance(length, int):
        raise ValueError(f'{length} is not an integer.')
    elif length <= 0:
        raise ValueError(f'{length} is less than 1.')
    
    response = requests.get(url_)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        words_text = soup.get_text()

        dictionary = set(word.lower() for word in words_text.split('\n') if re.match(r'^[A-Za-z]+$', word))
        partitioned_dictionary = []

        for word in dictionary:
            if len(word) == length:
                partitioned_dictionary.append(word)

        return partitioned_dictionary
        
    return f'Failed to fetch the URL: {response.status_code}'


def word_guessr(word_length=5):
    if not isinstance(word_length, int):
        raise ValueError(f'{word_length} is not an integer.')
    elif word_length < 3:
        raise ValueError(f'{word_length} is less than 5.')
    
    stripped_dictionary = dictionary(url, word_length)
    random_word = random.choice(stripped_dictionary)
    i = 0

    while i < 5:

        while True:
            guess = input("Guess: ").lower()
            if len(guess) == word_length and re.match(r'^[a-z]+$', guess):
                if guess not in stripped_dictionary:
                    print(f'{guess} is not an English word. Retry...')
                else:
                    break
            else:
                print("Invalid guess. Retry...")
        
        correctness_level = word_correctness(random_word, guess)
        print(correctness_level)

        if guess == random_word:
            return "Excellent! You guessed right!!!"
        else:
            print('Wrong guess! Try again...')
        i += 1

    return f'You lost... the word was {random_word}'


def word_correctness(word_, guess_):
    length = len(word_)
    quantifier = []

    for i in range(length):
        if guess_[i] == word_[i]:
            quantifier.append(Color.GREEN + guess_[i] + Color.END)
        elif guess_[i] in word_:
            quantifier.append(Color.ORANGE + guess_[i] + Color.END)
        else:
            quantifier.append(Color.RED + guess_[i] + Color.END)

    return " ".join(quantifier)


if __name__ == "__main__":
    main()
