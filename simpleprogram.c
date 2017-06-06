#include <stdio.h>

int main( int argc, char *argv[] )  {
    if( argc == 2 ) {
        printf("%s", argv[1]); //To test the behavior of the future checking binary just return 1 or 0 if we send 1 or 0
    }
    else if( argc > 2 ) {
        printf("Too many arguments supplied.\n");
    }
    else {
        printf("One argument expected.\n");
    }
}
