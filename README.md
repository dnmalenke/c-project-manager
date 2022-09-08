# c-project-manager

Create c projects, add source files, and update your makefile automatically with this tool

`c-project-manager.py` scans for new .c/.h files and updates the makefile for the c project in the current directory
`c-project-manager.py test` scans for new .c/.h files and updates the makefile for the c project in the `test` directory
`c-project-manager.py --new test` creates a new c project in the `test` directory
`c-project-manager.py --add code` creates code.c and code.h within the src directory of the c project in the current directory and updates the makefile

Makefile commands
`make` builds the project using optimized settings
`make optimized` builds the project using optimized settings
`make debug` builds the project using debug settings
`make run` builds the project using optimized settings and runs the program
`make gdb` builds the project using debug settings and runs the program within gdb