# Online

## Compiling the code. 
All files in the `online/` are mandatory to compile the main code. 


The compilation can be done in only one step : 
```console
g++ -o main main.c crate_lib.c kbhit.c -lpthread
```
Once the compilation is done, one can run the code  : 
```console
./main <timeToRun (-1 for unlimited)> <printing every x values> <channel 1 to read from> <channel 2 to read from> ... <channel N to read from>
```
