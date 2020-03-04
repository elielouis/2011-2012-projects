#ifndef UNICODE
#define UNICODE
#endif 
#include <windows.h>


#define BUTTON 100
#define TEXTBOX 101
#define TIMER_FLOOD 105
#define MAX_LENGTH 1000
#define TIME 100
#define TIMERCHECK 123

#define KEYDOWN(vkey) (GetAsyncKeyState(vkey) & 0x8000)
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void SendKeys();
void CheckForStop();

HWND hwnd;
HWND hwndButton;
HWND hwndTextBox;
HANDLE hThread = NULL;
int len;
bool TimerRunning = false;
LPWSTR lpszMem;








int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow)
{

    const wchar_t CLASS_NAME[]  = L"Sample Window Class";
    
    WNDCLASS wc = { };

	wc.style		 = WS_MINIMIZEBOX | WS_MAXIMIZEBOX;
    wc.lpfnWndProc   = WindowProc ; 
    wc.hInstance     = hInstance ; 
    wc.lpszClassName = CLASS_NAME ; 
	wc.cbClsExtra    = 0 ; 
	wc.cbWndExtra    = 0 ; 
	wc.hIcon		 = LoadIcon (NULL, IDI_APPLICATION) ; 
	wc.hCursor		 = LoadCursor (NULL, IDC_ARROW) ; 
	wc.hbrBackground = (HBRUSH) GetStockObject (WHITE_BRUSH);

    if (!RegisterClass(&wc))
	{
		MessageBox (NULL, TEXT ("This program requires Windows NT!"),
					CLASS_NAME , MB_ICONERROR);
		return 0;
	}


	hwnd = CreateWindowEx(
        0,                             
        CLASS_NAME,                  
        L"Toki's Flooding Tool",   
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX,         


        CW_USEDEFAULT, CW_USEDEFAULT, 300, 200,

        NULL,       
        NULL,       
        hInstance,  
        NULL       
        );

    if (hwnd == NULL)
    {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
	UpdateWindow(hwnd);


    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

	return msg.wParam;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_DESTROY:
		KillTimer(hwnd, TIMERCHECK);
		KillTimer(hwnd, TIMER_FLOOD);
		if (TimerRunning)
			VirtualFree(lpszMem, 0, MEM_RELEASE);
        PostQuitMessage(0);
        return 0;

	case WM_CREATE:
		{
			hwndButton			= CreateWindow ( TEXT("button"), 
									   TEXT("Start"),
									   WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
									   90, 125, 100, 30,
									   hwnd, (HMENU) 100,
									   ((LPCREATESTRUCT) lParam)->hInstance, NULL) ;

			hwndTextBox			=  CreateWindowEx(WS_EX_CLIENTEDGE, TEXT("Edit"), TEXT("Enter your message here"),
                               WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL|ES_MULTILINE|WS_VSCROLL|WS_HSCROLL, 30, 35, 220,
                               75, hwnd, (HMENU)101, ((LPCREATESTRUCT) lParam)->hInstance, NULL);

			SetTimer(hwnd, TIMERCHECK, 300, (TIMERPROC)NULL);



		}		
		return 0;



    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
			LPCWSTR lpszText	= L"Coded by Elie Louis";
			TextOut(hdc, 75, 10, lpszText, lstrlen(lpszText));
            EndPaint(hwnd, &ps);
			
        }
        return 0;



	case WM_COMMAND:
		{
			switch(LOWORD(wParam))
			{
				case BUTTON:
					{
						if (TimerRunning)
						{
							SendMessage(hwndButton, WM_SETTEXT, 0, (LPARAM)(LPCTSTR)L"Start");
							KillTimer(hwnd, TIMER_FLOOD);
							TimerRunning = false;
							VirtualFree(lpszMem, 0, MEM_RELEASE);
						}
						else
						{
							len = GetWindowTextLength(hwndTextBox) + 1;
							if (len == 1)
								{
									MessageBox(hwnd, TEXT("Please enter a message"), TEXT("Error"),  MB_OK | MB_ICONERROR);
									return 0;
								}
							lpszMem = (LPWSTR) VirtualAlloc((LPVOID)NULL, (DWORD) (len), MEM_COMMIT, PAGE_READWRITE);
							GetWindowText(hwndTextBox, lpszMem, len);
							lpszMem[len] = '\0';
							SendMessage(hwndButton, WM_SETTEXT, 0, (LPARAM)(LPCTSTR)L"Stop");
							SetTimer(hwnd, TIMER_FLOOD, TIME, (TIMERPROC)NULL);
							TimerRunning = true;

							// Deselect the button, in case it hits space (it will hit the stop button)
							SetFocus(hwnd);

						}
					}
					break;
			}
		}
		return 0;
	
	case WM_TIMER:
		{
			switch(wParam)
			{
				case TIMER_FLOOD:
					SendKeys();
				case TIMERCHECK:
					CheckForStop();
			}
		}
		return 0;


    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}


void SendKeys()
{
	for (int i = 0; i < len; i++)
	{
		if (lpszMem[i] == '\0')
			break;
		BYTE bVk	= VkKeyScan(lpszMem[i]);
		keybd_event(bVk, 0, KEYEVENTF_EXTENDEDKEY, NULL); 
		keybd_event(bVk, 0, KEYEVENTF_KEYUP, NULL); 
	}
}


void CheckForStop()
{
	if (KEYDOWN(VK_LSHIFT) && KEYDOWN(VK_RSHIFT))
	{
		PostMessage(hwnd, WM_COMMAND, (WPARAM)100, 0);
	}
}