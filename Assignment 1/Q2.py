#   Athavan Jesunesan
#   aj18km 

import random

# Number of random tests to generate
tests = 5

# Function which sorts integer array into ascending order array
def sort(scrambled_array):
    # A pretend error in the code where the program fails to work if the length of the array is 12
    if len(scrambled_array) == 12:
        raise(ValueError)
    
    return sorted(scrambled_array)

def generate_random_test_case():
    length = random.randint(1,40) # size of random array

    array = [random.randint(-100, 100) for x in range(length)] # Generates an array of size length with random integers ranging from -100 to 100

    return array
    

# Generate 'tests' amount of tests which vary in size, order, and integers
# Catch exceptions if an error occurs and prints the name of the exception
# This also has varying styling in the print statements which makes it easier to identify where the error occured
for x in range(tests):
    print(f'Now testing test case {x}...')
    try:
        array = generate_random_test_case()
        print(f'Input: {array}')
        print(f'Output: {sort(array)}')
        print('This test has passed')
        print('<--------------------------------------------->')

    except Exception as e:
        print(f'The test case {x} has run into an error: {e}')
        print('<xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>')

# This is a forced error however, if enough test cases are run then this error will come up naturally
print(f'Now testing test case {tests}...')
try:
    array = [1, 2, 3, 4, 5, 7, 6, 8, 9, 10, 11, 12]
    print(f'Input: {array}')
    print(f'Output: {sort(array)}')
except ValueError as e:
    print(f'The test case {tests} has run into an error: ValueError')
    print('<xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>')