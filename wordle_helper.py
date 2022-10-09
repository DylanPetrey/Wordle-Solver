import re

WORD_LIST_FILE = "data/wordbank.txt"


# This function reads in the file and creates a list of all the words
def get_word_list() -> list:
    result = []
    file = WORD_LIST_FILE
    with open(file) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result


# Prints the menu for character validation
def validate_menu():
    print("Validate characters with the following format: ")
    print("c - Correct Character")
    print("w - Wrong spot")
    print("x - Character is not in answer")
    print("Ex: cwcxx")


# This function obtains an input from the user and validates it
def get_guesses() -> tuple:
    input_word = ""
    input_guess = ""
    word_match = False
    guess_match = False
    word_regex = re.compile("^[a-z]{5}$")
    guess_regex = re.compile("^[cwx]{5}$")

    while not (word_match and guess_match):
        print("\nEnter word: ")
        input_word = input()
        validate_menu()
        input_guess = input()

        input_word = input_word.lower()
        input_guess = input_guess.lower()

        word_match = word_regex.match(input_word)
        guess_match = guess_regex.match(input_guess)

        if not word_match:
            print("Word is not a valid 5 character guess")
        if not guess_match:
            print("Guess validation does not match the format")

    return input_word, input_guess


# This is what processes the input and stores the letters in the correct locations
def assign_letters(input_guess, input_word, correct_letters, maybe_letters, invalid_letters):
    for index, current_character in enumerate(input_word):
        if input_guess[index] == "c":
            if current_character not in correct_letters[0]:
                correct_letters[0] += current_character
            correct_letters[1][index] = current_character
            if current_character in maybe_letters:
                maybe_letters.remove(current_character)
            if current_character in invalid_letters[0]:
                invalid_letters[0].remove(current_character)
        elif input_guess[index] == "w":
            if current_character not in maybe_letters:
                maybe_letters += current_character
            invalid_letters[1][index] += current_character
            if current_character in invalid_letters[0]:
                invalid_letters[0].remove(current_character)
        else:
            if current_character in invalid_letters[1][index]:
                continue
            elif current_character in correct_letters[0]:
                invalid_letters[1][index] += current_character
            elif current_character not in invalid_letters[0] and current_character not in maybe_letters:
                invalid_letters[0] += current_character
                invalid_letters[1][index] += current_character


# This function removes all of the invalid words based on the letters guessed
def remove_invalid_words(list_of_words, correct_letters, maybe_letters, invalid_letters) -> list:
    new_list = []
    for word in list_of_words:
        valid = True
        for index, letter in enumerate(word):
            if letter != correct_letters[1][index] and correct_letters[1][index] != ".":
                valid = False
                break
            elif letter in invalid_letters[0] or letter in invalid_letters[1][index]:
                valid = False
                break
        if not all(letter in word for letter in maybe_letters):
            valid = False
        if valid:
            new_list.append(word)
    return new_list


# This function weights words based off the frequency that the characters appear
# Then it scores the word and returns the 5 words with the highest score
def rank_words(word_list) -> list:
    # Get letter frequency
    char_freq_list = [{} for sub in range(5)]
    for w in word_list:
        for index, ch in enumerate(w):
            char_freq_list[index][ch] = char_freq_list[index].get(ch, 0) + 1

    # Score the word
    new_list = [[]]
    for w_index, w in enumerate(word_list):
        score = 0
        used_characters = ''
        for index, ch in enumerate(w):
            score_modifier = 1 if ch not in used_characters and word_list else 0.75
            used_characters += ch
            score = score + (char_freq_list[index].get(ch) / word_list.__len__() * score_modifier)
        new_list.insert(w_index, [w, score])
    new_list.pop()

    # Return 5 most common
    return [word[0] for word in sorted(new_list, key=lambda x: x[1], reverse=True)[:5]]


# Prints all the words in the input list
def print_words(word_list):
    for index in range(word_list.__len__()):
        print(word_list[index], end=' ')
        if (index + 1) % 20 == 0:
            print("\n", end='')
    print("\n")


# Main driver of the program
def wordle_helper(list_of_words):
    # Data structures for the individual characters
    correct_letters = [[], [".", ".", ".", ".", "."]]
    maybe_letters = []
    invalid_letters = [[], {0: [], 1: [], 2: [], 3: [], 4: []}]

    number_of_guesses = 0
    end = False

    # loop until the max number of guesses or the word is found
    while not end:
        input_word, input_guess = get_guesses()

        assign_letters(input_guess, input_word, correct_letters, maybe_letters, invalid_letters)
        validated_words = remove_invalid_words(list_of_words, correct_letters, maybe_letters, invalid_letters)

        print("\nThere are " + str(validated_words.__len__()) + " possible words:")
        validated_words.sort()
        print_words(validated_words)

        if validated_words.__len__() > 5:
            best_greens = rank_words(validated_words)
            print("\nThese are the 5 best guesses:")
            print_words(best_greens)

        number_of_guesses += 1

        # End cases
        if validated_words.__len__() == 1:
            print("You found it!")
            end = True
        elif validated_words.__len__() == 0:
            print("There is no answer")
            end = True
        elif number_of_guesses == 6:
            print("You have reached your max number of guesses\n")
            end = True


if __name__ == '__main__':
    words = get_word_list()

    wordle_helper(words)
