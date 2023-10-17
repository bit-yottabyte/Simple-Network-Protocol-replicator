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

    if(split == 0): #If our input is smaller than our sections we need to have 1
        splits = len(input_str)
        split = 1
    print(split)
    print(f'Splits:{splits}')

    for section in range(splits): # Sections the string for search
        if section < splits-1: #to deal with odd sectioning
            sections.append(input_str[split*section:split*(section+1)])
        else:
            print(remainder-split*section)
            sections.append(input_str[remainder-(remainder-split*section):])
    print(sections)

    for section in sections: # Processes the sections
        if processString(section) != correctString(section): # Check Sections
            problem += section

    print(f'problem so far: {problem}')
    if problem == "": #This is situation where there is nothing wrong in the input
        return ""
    elif len(problem)*2 == len(processString(problem)): 
        return problem
    elif problem == input_str:
        return delta_debugger(problem, splits+1) #If the problem is still the same size as the input then we need to split it further
    else:
      return delta_debugger(problem, splits) #If the problem persists and there was progress then continue the search as normal 

print(f'The issue is: {delta_debugger("abcdefG1", 2)}')
#strings = {["abcdefG1"], ["CCDDEExy"], ["1234567b"], ["8655"]}

# for string in strings:
#     print(delta_debugger("abcdefG1", 2))
