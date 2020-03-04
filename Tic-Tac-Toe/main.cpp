#include <iostream>
#include <ctime>
#include <cstdlib>
#include <string>

using namespace std;

bool checkforwin(char board[], char user)
{
    if (board[0] && board[1] && board [2] == user)
        return 1;
    else if (board[3] && board[4] && board[5] == user)
        return 1;
    else if (board[6] && board[7] && board[8] == user)
        return 1;
    else if (board[0] && board[3] && board[6] == user)
        return 1;
    else if (board[1] && board[4] && board[7] == user)
        return 1;
    else if (board[2] && board[5] && board[8] == user)
        return 1;
    else if (board[0] && board[4] && board[8] == user)
        return 1;
    else if (board[2] && board[4] && board[6] == user)
        return 1;
    else
        return 0;
}

int main()
{
    srand(time(0));
    while(1)
    {
        int nb; int turn;
        char firstplayer = 'x', secondplayer = 'o';
        char board[9];
        nb = rand() % 2;
        if (nb == 0)
        {
            turn = 0;
            cout << "Player " << firstplayer << " begins" << endl;
        }
        else
            turn = 1;
            cout << "Player " << secondplayer << " begins" << endl;
        while (1)
        {
            cout << board[0] << " " << "|" << " " << board[1] << " " << "|"  << board[2] << endl;
            cout<<" | | | "<<endl;
            cout << board[3] << " " << "|" <<""<<board[4]<<" "<<"|"<<board[5]<<endl;
            cout<<" | | | "<<endl;
            cout << board[6] << " " << "|" <<""<<board[7]<<" "<<"|"<<board[8]<<endl;

            if (turn==1)
            {
                cout << firstplayer << "'s turn" << endl;
                while (1)
                {
                    int placetofill;
                    cout << "Where do you want to place? "; cin >> placetofill;
                    if (board[placetofill-1] == ''){
                        board[placetofill-1] = firstplayer;
                        break;}
                    else
                        cout << "Please enter a good place!" << endl;
                        }
                bool iswin  = checkforwin(board, firstplayer);
                if (iswin)
                { cout << firstplayer << " wins" << endl;
                break;
                turn = 2;
            }
            else
            {
                cout << secondplayer << "'s turn" << endl;
                while (1)
                {
                    int placetofill;
                    cout << "Where do you want to place? "; cin >> placetofill;
                    if (board[placetofill-1]==''){
                        board[placetofill-1] = firstplayer;
                        break;}
                    else
                        cout << "Please enter a good place!" << endl;
                        }
                    bool iswin  = checkforwin(board, secondplayer);
                    if (iswin)
                    { cout << secondplayer << " wins" << endl;
                    break;
                    }
                    turn = 1;
                    }
            string pAgain;
            cout << "Do you want to play again? "; cin >> pAgain;
            if (pAgain[0]== 'y')
                continue;
            else
                break;


            }

        }


    }


}
