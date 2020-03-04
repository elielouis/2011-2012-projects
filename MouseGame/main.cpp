#include <iostream>
#include <windows.h>
#include <cstdlib>
#include <string>
#include <ctime>
using namespace std;

int genRandom(int min, int max)
{
    //Generates a random num between min and max
    int num = rand() %(max-min) +min;
    return num;
}

int main()
{
    srand(time(0));
    POINT myPoint; // A windows API structure which contains X and Y

    while (1)
    {
        int randX = genRandom(100,500); //first random number
        char charfromintX[5];
        itoa (randX,charfromintX,10); //converting from int to char[]
        string secondconvX = charfromintX; // converting from char[] to string
        int randY = genRandom(100, 500); // second random number
        char charfromintY[5];
        itoa(randY, charfromintY, 10);
        string secondconvY = charfromintY;

        string messageText = "You will have to go on " + secondconvX + " x and " + secondconvY + " y \nDo you want to continue playing?"; // the message to display
        int continue_playing = MessageBox
        (
         NULL,
         messageText.c_str(),
         "Continue",
         MB_YESNO
        );

   */
        if (continue_playing == IDYES) // IDYES is the state we want
        {
            while (1)
            {

                if(GetCursorPos(&myPoint)) //function to get the cursor position and put it in the POINT structure myPoint
                {
                    cout << "x: " << myPoint.x << " y:" << myPoint.y; // priting the coordonates
                    cout << endl;
                    if(myPoint.x == randX && myPoint.y == randY) // comparing
                        {
                            cout << "You won" << endl;
                            break;
                        }
                }
                else
                {
                    cout << "Error" << endl;
                }
            }
        }
        else
        {
            break;
        }
    }
    return 0;
}
