# Secret Encrypter
This is a program to encrypt the values of several key-value pairs

# Commands
* create-store
* list-secrets
* get <secret-name>
* set <secret-name> <secret-value>
* remove <secret-name>

# Improvements
* Do not show the password when typing in
* Password change
* Request entire JSON object
* Create store from JSON object
* Better handling of the salt
* Provide password only once to start program

# Make it executable
* An .exe file can be generated with auto-py-to-exe
* https://pypi.org/project/auto-py-to-exe/

# Used environment
* Following packages have been installed manually for the anaconda environment (The other packages are implicit dependencies):
    * Cryptography  
* An anaconda environment has been used for this project. A related environment.yml file is located in the project directory. Create conda environment with following command:
<br>`conda env create -n <environmentName> -f environment.yml`
* You might need to change the prefix entry within the environment file to specify the location for the environment