#!/usr/bin/env python3
import readline
from argparse import ArgumentParser
from typing import List

from pyfzf.pyfzf import FzfPrompt

SEARCH = 0
ADD = 1


class Command:
    """Parsed command with category ID and associated metadata.
    """

    def __init__(self, category, metadata=None):
        self._category = category
        self._metadata = metadata

    @property
    def category(self):
        """The command category.

        Returns:
            int: The category id,
        """
        return self._category

    @property
    def metadata(self):
        """The metadata associated with the command.

        Returns:
            Any | None: The associated metadata.
        """
        return self._metadata


def word_to_char_ids(word: str) -> List[int]:
    """Converts the letters in a word to corresponding alphabet ids.

    Args:
        word (str): The string to be converted. Must be lowercase.

    Returns:
        List[int]: a list of integer between 0 and 25.
    """
    return [ord(c) - ord('a') for c in word]


class Constraint:

    def __init__(self, word, verdict):
        self._word = word
        self._verdict = verdict

    @property
    def word(self):
        return self._word

    @property
    def char_ids(self):
        return word_to_char_ids(self._word)

    @property
    def verdict(self):
        return self._verdict


class WordFilter:

    def __init__(self):
        self._min_count = [0] * 26
        self._max_count = [None] * 26
        self._matrix = [[None] * 26 for _ in range(5)]

    def add_constraint(self, constraint: Constraint):
        """Adds a new constraint to the word filter.

        Args:
            constraint (Constraint): The constraint.
        """
        min_count = [0] * 26
        exclude = []
        for idx, (char, verd) in enumerate(
                zip(constraint.char_ids, constraint.verdict)):
            if verd == 0:
                self._matrix[idx][char] = False
                # handle gray verdicts for other positions later since other
                # positions might contain this letter
                exclude.append(char)
            elif verd == 1:
                self._matrix[idx][char] = False
                min_count[char] += 1
            elif verd == 2:
                for i in range(26):
                    self._matrix[idx][i] = False
                self._matrix[idx][char] = True
                min_count[char] += 1
        for char in exclude:
            if min_count[char] == 0:
                # no other yellow or green verdicts for this letter
                for i in range(5):
                    self._matrix[i][char] = False
            else:
                self._max_count[char] = min_count[char]
        self._min_count = [
            max(a, b) for a, b in zip(self._min_count, min_count)
        ]

    def match(self, word: str) -> bool:
        """Checks if a word matches all the constraints of the word filter.

        Args:
            word (str): The word to be checked.

        Returns:
            bool: True if the word matches all the constraints.
        """
        char_ids = word_to_char_ids(word)
        count = [0] * 26
        for i, char in enumerate(char_ids):
            if self._matrix[i][char] is not None and not self._matrix[i][char]:
                return False
            count[char] += 1
        for i in range(26):
            if self._max_count[i] is not None and count[i] > self._max_count[i]:
                return False
        return all(a >= b for a, b in zip(count, self._min_count))

    def apply(self, words: List[str]) -> List[str]:
        """Filters the possible candidates from a list of candidates.

        Args:
            words (List[str]): The list of candidates.

        Returns:
            List[str]: The list of possible candidates.
        """
        return [word for word in words if self.match(word)]


def parse_command(cmd_str: str) -> Command:
    """Parses the command string.

    Args:
        cmd_str (str): The command string.

    Raises:
        ValueError: Wrong command format.

    Returns:
        Command: Parsed command.
    """
    tokens = cmd_str.split()
    if len(tokens) == 1 and tokens[0] in ("s", "search"):
        cmd = Command(SEARCH)
        return cmd
    if len(tokens) == 3 and tokens[0] in ("a", "add"):
        word, verdict_str = tokens[1], tokens[2]
        if len(word) != 5 or not word.isalpha():
            raise ValueError("Invalid word format")
        if len(verdict_str) != 5 or not verdict_str.isdigit():
            raise ValueError("Invalid verdict format")

        word = word.lower()
        verdict = [int(c) for c in verdict_str]
        if not all(0 <= v <= 2 for v in verdict):
            raise ValueError("Unknown verdict")

        constraint = Constraint(word, verdict)
        cmd = Command(ADD, metadata=constraint)
        return cmd
    raise ValueError("Invalid command format")


def main():
    """Main function.
    """
    parser = ArgumentParser()
    parser.add_argument("wordlist", help="List of possible words")
    args = parser.parse_args()

    # load words
    words = []
    with open(args.wordlist, encoding="ascii") as word_file:
        words = word_file.read().splitlines()

    fzf_prompt = FzfPrompt()
    word_filter = WordFilter()
    try:
        while True:
            cmd_str = input(">> ")
            try:
                cmd = parse_command(cmd_str)
                if cmd.category == SEARCH:
                    fzf_prompt.prompt(words)
                elif cmd.category == ADD:
                    word_filter.add_constraint(cmd.metadata)
                    words = word_filter.apply(words)
                else:
                    raise ValueError("Unknown command category")
            except ValueError as err:
                print(err)
    except EOFError:
        print("\nQuitting...")
    except KeyboardInterrupt:
        print("\nQuitting...")


if __name__ == "__main__":
    main()
