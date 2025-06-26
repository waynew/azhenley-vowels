import csv
import re
import timeit
import random
import string
from functools import reduce
from math import factorial, gcd
import collections

# --- Generate test strings: Half with vowels, half without vowels ---

NUM_STRINGS = 2000
half = NUM_STRINGS // 2
REPEATS = 5
STRING_LENGTH = 100
VOWELS = "aeiouAEIOU"
SET_VOWELS = set(VOWELS)
VOWELS_AT_END = False

# Generate half strings with a vowel inserted
with_vowel = []
for _ in range(half):
    base = [random.choice(string.ascii_letters.translate(str.maketrans('', '', VOWELS)))
            for _ in range(STRING_LENGTH - 1)]
    start_index = 0 if not VOWELS_AT_END else int(len(base) * 0.9) 
    insert_index = random.randint(start_index, len(base)) # Randomly place vowel, either anywhere or in the last 10%
    base.insert(insert_index, random.choice(VOWELS))
    with_vowel.append(''.join(base))

# Generate strings without vowels
non_vowel_letters = ''.join(set(string.ascii_letters) - set(VOWELS))
without_vowel = [''.join(random.choices(non_vowel_letters, k=STRING_LENGTH)) for _ in range(half)]

# Combine and shuffle
test_strings = with_vowel + without_vowel
random.shuffle(test_strings)

# --- Prime cache for method_prime ---
primes = [i for i in range(2, 1000) if factorial(i - 1) % i == (i - 1)]
pattern = re.compile(r'[aeiouAEIOU]')

# --- Function definitions ---

def method_loop_or(s: str) -> bool:
    for c in s:
        if c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u' or \
           c == 'A' or c == 'E' or c == 'I' or c == 'O' or c == 'U':
            return True
    return False

def method_loop_in(s: str) -> bool:
    vowels = "aeiouAEIOU"
    for c in s:
        if c in vowels:
            return True
    return False

def method_any_gen(s: str) -> bool:
    vowels = "aeiouAEIOU"
    return any(c in vowels for c in s)

def method_set_intersection(s: str) -> bool:
    vowels = "aeiouAEIOU"
    return bool(set(s) & set(vowels))

def method_regex(s: str) -> bool:
    return bool(re.search(r'[aeiouAEIOU]', s))

def method_regex_compiled(s: str) -> bool:
    return bool(pattern.search(s))

def method_regex_replace(s: str) -> bool:
    return len(re.sub(r'[aeiouAEIOU]', '', s)) != len(s)

def method_filter(s: str) -> bool:
    vowels = "aeiouAEIOU"
    return bool(list(filter(lambda x: x in vowels, s)))

def method_map(s: str) -> bool:
    vowels = "aeiouAEIOU"
    return any(map(lambda x: x in vowels, s))

def method_recursion(s: str) -> bool:
    vowels = "aeiouAEIOU"
    if not s:
        return False
    return s[0] in vowels or method_recursion(s[1:])

def method_nested_loop(s: str) -> bool:
    vowels = "aeiouAEIOU"
    for c in s:
        for v in vowels:
            if c == v:
                return True
    return False

def method_prime(s: str) -> bool:
    vowels = "aeiouAEIOU"
    vowel_primes_dict = {c: primes[ord(c)] for c in vowels}
    try:
        s_num = reduce(lambda acc, v: acc * primes[ord(v)], s, 1)
        v_num = reduce(lambda acc, v: acc * vowel_primes_dict[v], vowels, 1)
        return gcd(s_num, v_num) != 1
    except Exception:
        return False

def method_in_set(s: str) -> bool:
    vowels = set("aeiouAEIOU")
    for c in s:
        if c in vowels:
            return True
    return False

def method_in_set_hardcode(s: str) -> bool:
    vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
    for c in s:
        if c in vowels:
            return True
    return False

def method_in_set_hardcode_in_loop(s: str) -> bool:
    for c in s:
        if c in {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}:
            return True
    return False

def method_in_set_break(s: str) -> bool:
    vowels = set("aeiouAEIOU")
    for c in s:
        if c in vowels:
            break
    else:
        return False
    return True

def method_in_set_predefined(s: str) -> bool:
    for c in s:
        if c in SET_VOWELS:
            break
    else:
        return False
    return True

def method_in_set_predefined_local_lookup(s: str) -> bool:
    vowels = SET_VOWELS
    for c in s:
        if c in vowels:
            break
    else:
        return False
    return True


# --- List of all functions ---
functions = [
    method_loop_or,
    method_loop_in,
    method_any_gen,
    method_set_intersection,
    method_regex,
    # method_regex_compiled,
    method_regex_replace,
    method_filter,
    method_map,
    method_recursion, # Comment this out with long strings
    method_nested_loop,
    method_prime,
    method_in_set_hardcode_in_loop,
    method_in_set_break,
    method_in_set_predefined,
    method_in_set,
    method_in_set_hardcode,
]

# --- Benchmarking ---
benchmark_results = []
Result = collections.namedtuple('Result', 'time,name')

max_func_len = 0
for func in functions:
    def run():
        for _ in range(REPEATS):
            for s in test_strings:
                func(s)
    exec_time = min(timeit.repeat(run, repeat=3, number=1))
    max_func_len = max(max_func_len, len(func.__name__))
    benchmark_results.append(Result(name=func.__name__, time=exec_time))

with open(f'vowels_benchmark_{STRING_LENGTH}_{VOWELS_AT_END}.csv', 'w') as f:
    csvwriter = csv.writer(f)
    print(f'{"Function":<{max_func_len}}\tTotal Time (seconds) over {NUM_STRINGS * REPEATS} calls with {STRING_LENGTH} length')
    for result in sorted(benchmark_results):
        print(f'{result.name:<{max_func_len}}\t{result.time:.6f}')
        csvwriter.writerow(result)
