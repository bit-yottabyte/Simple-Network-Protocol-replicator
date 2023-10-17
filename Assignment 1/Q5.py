# Athavan Jesunesan
# Assignment 1



# program under analysis
def processString(input_str):
    output_str = ""
    for char in input_str:
        if char.isupper():
            output_str += char.lower()
        elif char.isnumeric():
            output_str += char * 2  
        else:
            output_str += char.upper()

    return output_str

# This is to recognize errors
def correctString(input_str):
    output_str = ""
    for char in input_str:
        if char.isupper():
            output_str += char.lower()
        elif char.isnumeric():
            output_str += char  
        else:
            output_str += char.upper()

    return output_str

# Delta Debugger
def delta_debugger(input_str, splits):
    # Setting Variables
    sections = [] #contains all string sections
    problem = "" #Keeps strings with problems
    remainder = len(input_str)

    
    split = int(len(input_str)/splits)#number of characters in each section
    if(split == 0):
        splits = len(input_str)
        split = 1
    print(split)
    for section in range(splits):
        if section+1 < splits: #to deal with odd sectioning
            sections.append(input_str[split*section:split*(section+1)])
            remainder-=split
        else:
            print(remainder)
            sections.append(input_str[remainder:])
    print(sections)

    for section in sections:
        if processString(section) != correctString(section): # Check Left Half
            problem += section

    print(problem)
    if problem == "": #This is situation where there is nothing wrong in the input
        return ""
    elif problem == input_str:
        return delta_debugger(problem, split+1)
    elif splits == len(input_str):
        return problem
    else:
      return delta_debugger(problem, splits)

print(f'The issue is: {delta_debugger("abcdefG1", 2)}')
#strings = {["abcdefG1"], ["CCDDEExy"], ["1234567b"], ["8655"]}

# for string in strings:
#     print(delta_debugger("abcdefG1", 2))