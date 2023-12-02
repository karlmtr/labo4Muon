/*----- kbhit()  emulation ----D.Rapin DPNC-UNI-GE--2004----*/
// obtenu d'apres: http://www.cppfrance.com/code.aspx?ID=10611
//
// retourne la valeur 1 si un caractere a ete tape au clavier.
// retourne 0 sinon.
// le code ASCII (ou -1) se retrouve dans l'integer "kbhitchar"
//
#include <termios.h>
#include <unistd.h>
static int kbhitchar;
int kbhit() {
// variables de lecture
char ch;
int nread;
struct termios origTerm, newTerm;

// preparation du terminal
tcgetattr(0, &origTerm);
newTerm = origTerm;
newTerm.c_lflag &= ~ICANON;
newTerm.c_lflag &= ~ECHO;
newTerm.c_lflag &= ~ISIG;
newTerm.c_cc[VMIN] = 1;
newTerm.c_cc[VTIME] = 0;
tcsetattr(0, TCSANOW, &newTerm);

// ecoute clavier
newTerm.c_cc[VMIN]=0;
tcsetattr(0, TCSANOW, &newTerm);
nread = read(0,&ch,1);
newTerm.c_cc[VMIN]=1;
tcsetattr(0, TCSANOW, &newTerm);

// Retablissement du terminal
tcsetattr(0,TCSANOW, &origTerm);

// test de lecture et retourne le code ascii
kbhitchar=-1;
if (nread == 1) {
                 kbhitchar= ch;
                      return 1;}
return 0;
} // fin de la fonction kbhit()

