"""
Heuristic analysis to determine likely word matches based on grouped syllables.
A tool by Pat Hallbick made to guess the most likely lyrics sung by TTS from songs in SMT III Nocturne.
Originally checked against openbible's corpus: https://openbible.com/texts.htm
Uses a fork of anson vandoren's syllabifier: https://github.com/anson-vandoren/syllabifier
"""

from .syllabifier.syllabifier3 import num_syllables
import re

def syllables(string):
    n = num_syllables(string)
    if not n:
        return best_guess(string)
    return n


vowels = "aeiouy"
def best_guess(s):
    if len(s) <= 0: return 0
    vowel = s[0] in vowels
    changes = 0
    for c in s[:-1]:
        if (c in vowels) != vowel:
            vowel = not vowel
            changes += 1
    return int(round(changes/2 - (0 if vowel else 0.5)))


skip_regex = r"(?:[0-9]+,)?"
def syllable_regex(n):
    if n:
        return f"{n},"
    return ""

def regex(syllables, permissible_skips):
    out = "^(.*?)("
    for s in syllables:
        out += syllable_regex(s) + (skip_regex * permissible_skips)
    return re.compile(f"{out})(.*)")

def match(syllables):
    out = ""
    for s in syllables:
        out += syllable_regex(s)
    return out

def convert(line):
    line = line.strip().split()
    pattern = ""
    for word in line:
        pattern += syllable_regex(syllables(re.sub(r'[^a-z]', '', word.lower())))
    return pattern

def check(file, syllables, permissible_skips=0, verse_filter="Revelation", highlight_excerpt=True):
    pattern_to_match = regex(syllables, permissible_skips)
    print(file)
    with open(file, "r") as f:
        line = f.readline()
        while line:
            split = line.split("\t")
            if len(split) <= 1: 
                line = f.readline()
                continue
            verse, line, *_ = split
            pattern = convert(line)
            if verse and verse.startswith(verse_filter):
                if pattern: 
                    split = line.split()
                    pos = 0
                    i = 0
                    last = ""
                    while m := pattern_to_match.search(pattern[pos:]):
                        before = len(m[1].split(","))-1
                        after = len(m[3].split(","))-1
                        excerpt = ""
                        for word in split[before:-after]:
                            excerpt += f"{word} "
                        if len(excerpt) > 0 and excerpt != last:
                            last = excerpt
                            if highlight_excerpt:
                                print(
                                    " ".join(split[before:]).strip(), 
                                    "\033[31m", 
                                    " ".join([f"{a}[{b}]" for a,b in zip(split[before:-after], m[2].split(","))]).strip(), 
                                    "\033[0m", 
                                    " ".join(split[-after:]).strip(),
                                    "\n"
                                )
                            yield verse, f"...{excerpt.strip()}..."
                        pos += pattern.find(",")+1
                        split = split[1:]
            line = f.readline()
