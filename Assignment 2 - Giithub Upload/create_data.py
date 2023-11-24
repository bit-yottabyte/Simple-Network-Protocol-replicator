import os

def generate_file(file_size, file_name):

    # Generate random data
    data = os.urandom(file_size)

    # Write data to the file
    with open(file_name, 'wb') as file:
        file.write(data)

#These for loops generate the files and place them in the 'Client_folder' folder (which needs to be there for this to work)

#Generating the files between the size of 10KB -> 100KB
#Creating 10 files of this size
for i in range(1, 11):
    file_size = i * 10 * 1024
    file_name = f"./client_folder/file_{i}.bin"
    generate_file(file_size, file_name)
    print(f"File '{file_name}' created with a size of {file_size/1024} KB.")

# Generating the files between the size of 10MB -> 100MB
for i in range(1, 11):
    file_size = i * 10 * 1024 * 1024
    file_name = f"./client_folder/file_{i+10}.bin"
    generate_file(file_size, file_name)
    print(f"File '{file_name}' created with a size of {file_size/(1024*1024)} MB.")