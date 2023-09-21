from random import choice
from xkcdpass import xkcd_password


class XKCD:
    delimiters_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    delimiters_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    delimiters_full = ["!", "$", "%", "^", "&", "*", "-", "_", "+", "=",
                       ":", "|", "~", "?", "/", ".", ";"] + delimiters_numbers
    delimiters_ultra = delimiters_alphabet + delimiters_full
    
    def __init__(self, filename: str):
        self.wordlist = xkcd_password.generate_wordlist(
            wordfile=filename, valid_chars="[a-z]", min_length=4, max_length=10,
        )

    def weak(self):
        # 2 words, random CAPITALIZATION, random number as separator between words
        return xkcd_password.generate_xkcdpassword(
            self.wordlist, numwords=2, case="random", random_delimiters=True, valid_delimiters=self.delimiters_numbers )

    def medium(self):
        # 3 words, random CAPITALIZATION, random number as separator between words
        return xkcd_password.generate_xkcdpassword(
            self.wordlist, numwords=3, case="random", random_delimiters=True, valid_delimiters=self.delimiters_numbers
        )

    def strong(self):
        # 4 words, random CAPITALIZATION, random number and symbols as separator between words
        return xkcd_password.generate_xkcdpassword(
            self.wordlist, numwords=4, case="random", random_delimiters=True, valid_delimiters=self.delimiters_full
        )

    def low(self):
        # 8 characters, random CAPITALIZATION, random characters, number, symbols as separator between characters
        return xkcd_password.generate_xkcdpassword(
            self.delimiters_alphabet, numwords=8, case="random", random_delimiters=True, valid_delimiters=self.delimiters_ultra
        )[:-1]

    def normal(self):
        # 12 characters, random CAPITALIZATION, random characters, number, symbols as separator between characters
        return xkcd_password.generate_xkcdpassword(
            self.delimiters_alphabet, numwords=12, case="random", random_delimiters=True, valid_delimiters=self.delimiters_ultra
        )[:-1]

    def hard(self):
        # 16 characters, random CAPITALIZATION, random characters, number, symbols as separator between characters
        return xkcd_password.generate_xkcdpassword(
            self.delimiters_alphabet, numwords=16, case="random", random_delimiters=True, valid_delimiters=self.delimiters_ultra
        )[:-1]

    def custom(self, count: int, separators: bool, prefixes: bool):
        """
        Custom password generation

        :param count: number of characters in password
        :param separators: bool, whether characters must be separated with delimiters
        :param prefixes: bool, whether there must be chars from delimiters list in front and in back
        :return: generated custom password
        """
        pwd = xkcd_password.generate_xkcdpassword(
            self.delimiters_alphabet, numwords=count, case="random", delimiter="",
            random_delimiters=separators, valid_delimiters=self.delimiters_ultra
        )
        if not prefixes and not separators:
            return pwd
        elif prefixes == separators:
            return f"{choice(self.delimiters_ultra)}{pwd[:-1]}{choice(self.delimiters_ultra)}"
        elif separators and not prefixes:
            return pwd[:-1]
        elif prefixes and not separators:
            return f"{choice(self.delimiters_ultra)}{pwd}{choice(self.delimiters_ultra)}"
