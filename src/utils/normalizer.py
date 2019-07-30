"""
Thierry Bertin-Mahieux (2011) Columbia University
tb2332@columbia.edu


This code contains functions to normalize an artist name,
and possibly a song title.
This is intended to do metadata matching.
It is mostly an elaborate hack, I never did an extensive search of
all problematic name matches.
Code developed using Python 2.6 on a Ubuntu machine, using UTF-8

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2011, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import unicodedata
import itertools
import Levenshtein  # http://pypi.python.org/pypi/python-Levenshtein/

# ROTATION SYMBOLS (A and B => B and A)
rotation_symbols = ['\\|', '/', '&', ',', '\\+', ';', '_', 'by']  # , '\-']
rotation_words = ['and', 'y', 'et', 'vs', 'vs.', 'v', 'with', 'feat',
                  'feat.', 'featuring', 'presents', 'ft.', 'pres.']
connection_symbols = ['-', '_', 'by', 'from', '~']
unwanted_symbols = ['\\.', '!!']
# SYMBOLS TO REMOVE AT THE BEGINNING
stub_to_remove = ['dj', 'dj.', 'mc', 'm.c.', 'mc.', 'the', 'los', 'les']

# SYMBOLS TO REMOVE AT THE END
end_to_remove1 = ['big band', 'trio', 'quartet', 'ensemble', 'orchestra']
end_to_remove2 = ['band']

# COMPILED REGULAR EXPRESSION
# white spaces
re_space = re.compile(r'\s')
# non alphanumeric
re_nonalphanum = re.compile(r'\W')
# rotation symbols
re_rotsymbols = re.compile(r'\s*?' + '|'.join(rotation_symbols) + '\\s*?')
# rotation words
re_rotwords = re.compile(r'\s(' + '|'.join(rotation_words) + ')\\s')
# connection symbols
re_connsymbols = re.compile(r'\s*?(' + '|'.join(connection_symbols) + ')\\s*?')
# stub to remove
re_rem_unwanted_symbols = re.compile(r'\s*?(' + '|'.join(unwanted_symbols) + ')\\s*?')
re_remstub = re.compile(r'(' + '|'.join(stub_to_remove) + ')\\s(.*)')
# ending to remove
re_remending1 = re.compile(r'(.*)\s(' + '|'.join(end_to_remove1) + ')')
re_remending2 = re.compile(r'(.*)\s(' + '|'.join(end_to_remove2) + ')')
# quotes to remove
re_remquotes = re.compile(r'(.+)\s(".+?")\s(.+)')
# parenthesis to remove
re_remparenthesis = re.compile(r'(.+)\s(\(.+?\))\s*(.*)')
# brackets to remove
re_rembrackets = re.compile(r'(.+)\s(\[.+?\])\s*(.*)')
re_remextraspaces = re.compile(r'(\s\s)')
re_mentions = re.compile(r'(@.\S*)')
re_hashtags = re.compile(r'(#.\S*)')


def char_is_ascii(c):
    """
    Check if a unicode character, e.g. u'A', u'1' or u'\u0301' is ASCII
    """
    # return ord(c) < 128
    # the following should be faster, according to:
    # http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
    return c < u"\x7F"


def remove_non_ascii(s):
    """
    Normalize characters in unicode string 's' that are not ASCII,
    try to transform accented characters to non accented version.
    Otherwise, remove non-ascii chars
    """
    decomposition = unicodedata.normalize('NFKD', s)
    return "".join([c for c in decomposition if char_is_ascii(c)])


def to_lower_case(s):
    """
    transform a unicode string 's' to lowercase
    ok, this one is trivial, I know
    """
    return s.lower()


def remove_spaces(s):
    """
    Remove all possible spaces in the unicode string s
    """
    return re_space.sub('', s)


def remove_mentions(s):
    """
    Remove all user mentions, like @pwall182
    """
    return re_mentions.sub('', s)


def remove_hashtags(s):
    """
    Remove all hashtags
    """
    return re_hashtags.sub('', s)


def replace_rotation_symbols(s):
    """
    Mostly, replace '&' by 'and'
    """
    return re_rotsymbols.sub(' and ', s)


def replace_connection_symbols(s):
    return re_connsymbols.sub(' - ', s)


def replace_unwanted_symbols(s):
    return re_rem_unwanted_symbols.sub('', s)


def remove_stub(s):
    """
    Remove a questionable beginning, e.g. dj
    otherwise return string at is
    """
    m = re_remstub.match(s)
    if not m:
        return s
    return m.groups()[1]


def remove_long_song(s):
    return s if len(s) <= 50 else ''


def remove_short_song(s):
    return s if len(s) >= 5 else ''


def remove_extra_spaces(s):
    return re_remextraspaces.sub(' ', s)


def remove_endings(s):
    """
    Remove questionable endings, e.g. 'band'
    """
    m = re_remending1.match(s)
    if m:
        s = m.groups()[0]
    m = re_remending2.match(s)
    if m:
        s = m.groups()[0]
    return s


def remove_quotes(s):
    """
    Remove the quote, like Thierry "The Awesomest" BM
    """
    m = re_remquotes.match(s)
    if not m:
        return s
    parts = m.groups()
    assert len(parts) == 3
    return parts[0] + ' ' + parts[2]


def remove_parenthesis(s):
    """
    Remove parenthesis, like Thierry (Coolest guy)
    """
    m = re_remparenthesis.match(s)
    if not m:
        return s
    parts = m.groups()
    assert len(parts) >= 2
    return parts[0] + ' ' + parts[2]


def remove_brackets(s):
    """
    Remove brackets, like Thierry [Coolest guy]
    """
    m = re_rembrackets.match(s)
    if not m:
        return s
    parts = m.groups()
    assert len(parts) >= 2
    return parts[0] + ' ' + parts[2]


def normalize_no_rotation(s):
    """
    We normalize a name that is supposed to contain no
    rotation term ('and', 'y', ...)
    """
    # remove beginning
    s = remove_stub(s)
    # remove ends
    s = remove_endings(s)
    # remove ()
    s = remove_parenthesis(s)
    # remove ""
    s = remove_quotes(s)
    return s


def split_rotation_words(s):
    """
    Split a name using the rotation words: 'and', 'vs', 'y', 'et', ...
    then create all possible permutations
    """
    parts = re_rotwords.split(s)
    parts = [p for p in parts if p not in rotation_words][:5]
    results = set()
    # keep only the individual elems (risky?)
    for p in parts:
        results.add(p)
    # create all permutations
    permutations = itertools.permutations(parts)
    # maxperm = 30
    # count_perm = 0
    for perm in permutations:
        # count_perm += 1
        # if count_perm > maxperm:
        #    break
        results.add(' '.join(perm))
    # redo the same but remove the stub first for all parts
    parts = [normalize_no_rotation(p) for p in parts]
    for p in parts:
        results.add(p)
    permutations = itertools.permutations(parts)
    for perm in permutations:
        results.add(' '.join(perm))
    # done
    return results


def remove_nonalphanumeric(s):
    """
    Remove usual punctuation signs:  ! , ? : ; . '   etc
    Also, we transform long spaces into normal ones
    """
    # split around non-alphanum chars
    parts = re_nonalphanum.split(s)
    # remove empty spots
    parts = filter(lambda p: p, parts)
    # rejoin with regular space ' '
    return ' '.join(parts)


def normalize_title(s):
    """
    Return a set of normalized versions of that artist name
    """
    # normalized versions
    results = set()
    # lower case
    s = to_lower_case(s)
    results.add(s)
    # remove non-ascii chars (try to replace them)
    s = remove_non_ascii(s)
    results.add(s)
    # try removing parenthesis before, in case there's an & in it
    s2 = remove_parenthesis(s)
    results.add(s2)
    # replace rotation symbols
    s = replace_rotation_symbols(s)
    # split and permute according to rotation words
    permutations = split_rotation_words(s)
    results.update(permutations)
    # remove non-alphanumeric and normalize spaces
    results = [remove_nonalphanumeric(s) for s in results]
    # remove all spaces
    results = [remove_spaces(s) for s in results]
    # done (and remove dupes)
    return set(results)


def same_title(name1, name2):
    """
    Compare two artists:
    - edit distance
    - if one name is contained in the other
    - by normalizing the names
    Return True if it's the same artist, False otherwise
    """
    # trivial
    n1 = to_lower_case(name1)
    n2 = to_lower_case(name2)
    if n1 == n2:
        return True
    # edit distance
    if len(n1) >= 10 or len(n2) >= 10:
        if Levenshtein.distance(n1, n2) <= 2:
            return True
    # n1 contains n2? or the other way around
    if len(n1) >= 10 and len(n2) >= 10:
        if len(n1) > len(n2):
            if n1.find(n2) >= 0:
                return True
        else:
            if n2.find(n1) >= 0:
                return True
    # compare by normalizing names
    normalized1 = normalize_title(n1)
    normalized2 = normalize_title(n2)
    if len(normalized1.intersection(normalized2)) > 0:
        return True
    return False


def normalize_string(s: str) -> str:
    s = remove_non_ascii(s)
    s = remove_mentions(s)
    s = remove_hashtags(s)
    s = replace_connection_symbols(s)
    s = remove_extra_spaces(s)
    s = replace_unwanted_symbols(s)
    s = remove_brackets(s)
    s = remove_endings(s)
    s = remove_parenthesis(s)
    s = remove_brackets(s)
    s = remove_quotes(s)
    s = remove_stub(s)
    s = s.strip().strip('-').strip('"').title().strip()
    s = remove_long_song(s)
    s = remove_short_song(s)
    return s
