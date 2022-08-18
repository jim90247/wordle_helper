# Wordle Helper

An interactive CLI tool for playing [Wordle](https://www.nytimes.com/games/wordle/index.html) which can filter the candidate words based on the constraints.

Built with [fzf](https://github.com/junegunn/fzf) and [pyfzf](https://github.com/nk412/pyfzf) to provide fuzzy search on candidates.

## Install

### Dependencies

* fzf
* pyfzf

### Word list

Use the [words.txt](words.txt) provided in this repository (obtained from [tabatkins/wordle-list](https://github.com/tabatkins/wordle-list)), or you may use any other files in which each line contains a five-letter word.

## Usage

Wordle Helper supports two commands: *search* and *add*.

* search: Lists all the candidates that satisfy current constraints.
  * Synposis: `s` or `search`
  * This will show a `fzf` prompt with all the possible candidates.
* add: Adds a constraint (a guess and its result).
  * Synopsis: `a [word] [verdict]` or `add [word] [verdict]`
  * *Verdict* is a 5-char sequence of 0, 1 and 2.
    * 0 for gray verdict (not match)
    * 1 for yellow verdict (partial match)
    * 2 for green verdict (exact match)
    * Example: ⬜️🟨🟩🟩⬜️ -> `01220`.

### Demo

![Demo](demo.gif)
