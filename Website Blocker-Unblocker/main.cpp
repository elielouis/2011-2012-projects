#
ifndef UNICODE# define UNICODE# endif#include <windows.h>

#include <fstream>

#include <iostream>

#include <string>


# define BUTTON_SAVE 100# define IDC_LIST 101# define IDC_ADD 102# define IDC_REMOVE 103# define IDC_TEXT 104

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void GetBlockedSites();
void AddSiteToList(LPCWSTR lpszSite);
void CrackLine(std::string);
void ExtractSite(std::string strLine, int iStart, int iEnd);
void RemoveFromList();
void AddToList();
void SaveChanges();

HWND hwnd;
int len;
bool FillList = false;

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow) {

    const wchar_t CLASS_NAME[] = L "Sample Window Class";

    WNDCLASS wc = {};

    wc.style = WS_MINIMIZEBOX | WS_MAXIMIZEBOX;
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH) GetStockObject(WHITE_BRUSH);

    if (!RegisterClass( & wc)) {
        MessageBox(NULL, TEXT("This program requires Windows NT!"),
            CLASS_NAME, MB_ICONERROR);
        return 0;
    }

    hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L "Website Blocker/Unblocker",
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX,

        CW_USEDEFAULT, CW_USEDEFAULT, 400, 300,

        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessage( & msg, NULL, 0, 0)) {
        TranslateMessage( & msg);
        DispatchMessage( & msg);
    }

    return msg.wParam;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;

    case WM_CREATE:
        {

            CreateWindow(TEXT("button"),
                TEXT("Save Changes"),
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                240, 180, 100, 30,
                hwnd, (HMENU) BUTTON_SAVE,
                ((LPCREATESTRUCT) lParam) - > hInstance, NULL);

            CreateWindowEx(WS_EX_CLIENTEDGE,
                L "LISTBOX", NULL,
                WS_CHILD | WS_VISIBLE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | WS_VSCROLL | LBS_EXTENDEDSEL,
                7, 35, 200, 180,
                hwnd, (HMENU) IDC_LIST, ((LPCREATESTRUCT) lParam) - > hInstance, NULL);

            CreateWindow(TEXT("button"),
                TEXT("Remove"),
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                240, 50, 100, 30,
                hwnd, (HMENU) IDC_REMOVE,
                ((LPCREATESTRUCT) lParam) - > hInstance, NULL);

            CreateWindowEx(WS_EX_CLIENTEDGE, //special border style for textbox
                TEXT("EDIT"), TEXT("Website"), WS_VISIBLE | WS_CHILD | ES_AUTOHSCROLL,
                220, 100, 150, 25, hwnd, (HMENU) IDC_TEXT, ((LPCREATESTRUCT) lParam) - > hInstance, NULL
            );

            CreateWindow(TEXT("button"),
                TEXT("Add"),
                WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                240, 130, 100, 30,
                hwnd, (HMENU) IDC_ADD,
                ((LPCREATESTRUCT) lParam) - > hInstance, NULL);

        }
        return 0;

    case WM_PAINT:
        {
            if (!FillList) {
                GetBlockedSites();
                FillList = true;
            }
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, & ps);
            LPCWSTR lpszText = L "Coded by Elie Louis";
            TextOut(hdc, 125, 10, lpszText, lstrlen(lpszText));
            EndPaint(hwnd, & ps);

        }
        return 0;

    case WM_KEYDOWN:
        {
            int nVirtKey = (int) wParam;
            if (nVirtKey == VK_RETURN) {
                AddToList();
            }
            return 0;
        }

    case WM_COMMAND:
        {
            switch (LOWORD(wParam)) {

            case IDC_REMOVE:
                {
                    RemoveFromList();
                    break;
                }

            case IDC_ADD:
                {
                    AddToList();
                    break;
                }

            case BUTTON_SAVE:
                {
                    SaveChanges();
                    break;
                }

            }
        }
        return 0;

    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

void AddSiteToList(LPCWSTR lpszSite) {
    // Add to ListBox
    int index = SendDlgItemMessage(hwnd, IDC_LIST, LB_ADDSTRING, 0, (LPARAM) lpszSite);

}

void ExtractSite(std::string strLine, int iBeg, int iEnd) {
    wchar_t * lpszBuffer = (wchar_t * ) GlobalAlloc(GPTR, (iEnd - iBeg + 1) * sizeof(wchar_t));
    for (int i = 0; i < iEnd - iBeg; i++)
        lpszBuffer[i] = strLine[iBeg + i];
    lpszBuffer[iEnd - iBeg] = '\0';
    AddSiteToList(lpszBuffer);
    GlobalFree((HANDLE) lpszBuffer);
}

void CrackLine(std::string strLine) {
    std::string strFiltered;
    bool passed = false;
    for (int i = 0; i < strLine.length(); i++) {
        if (strLine[i] == ' ')
            passed = true;
        if (passed) {
            if (strLine[i] != ' ') {
                strFiltered += strLine[i];
            }
        }
    }
    int iBeg = 0;
    for (int iEnd = 0; iEnd < strFiltered.length(); iEnd++) {
        if (strFiltered[iEnd] == ',') {
            ExtractSite(strFiltered, iBeg, iEnd);
            iBeg = iEnd + 1;
        } else if (iEnd == (strFiltered.length() - 1)) {
            ExtractSite(strFiltered, iBeg, iEnd + 1);
            iBeg = iEnd + 1;
        }
    }
}

void GetBlockedSites() {
    char * szDir = "C:\\WINDOWS\\system32\\drivers\\etc\\hosts";
    std::string strLine;
    std::ifstream inFile;
    inFile.open(szDir);
    if (!inFile.is_open()) {
        MessageBox(NULL, TEXT("Cannot open host file!"), TEXT("Error!"), MB_OK | MB_ICONERROR);
        ExitProcess(0);
    }

    while (inFile.good()) {
        std::getline(inFile, strLine);
        if (strLine.length() == 0)
            continue;
        if (strLine[0] == '#')
            continue;
        if (strLine == "127.0.0.1      localhost") {
            continue;
        }

        int length = strLine.length();

        //Add a check to see if it's localhost, reverse the string, then do substring.. don't use IF with length-1,-2...

        CrackLine(strLine);

    }
}

void RemoveFromList() {
    // get the number of items in the box.
    HWND hListbox = GetDlgItem(hwnd, IDC_LIST);
    int count = SendMessage(hListbox, LB_GETCOUNT, 0, 0);

    // go through the items
    for (int i = 0; i < count; i++) {
        // check if this item is selected or not..
        if (SendMessage(hListbox, LB_GETSEL, i, 0) > 0) {
            SendMessage(hListbox, LB_DELETESTRING, (WPARAM) i, 0);

        }
    }

}

void AddToList() {
    HWND hwndTextbox = GetDlgItem(hwnd, IDC_TEXT);
    int size = GetWindowTextLength(hwndTextbox) + 1;
    LPWSTR lpszMem = (LPWSTR) VirtualAlloc((LPVOID) NULL, (DWORD)(size), MEM_COMMIT, PAGE_READWRITE);
    GetWindowText(hwndTextbox, lpszMem, size);
    SendDlgItemMessage(hwnd, IDC_LIST, LB_ADDSTRING, 0, (LPARAM) lpszMem);
    VirtualFree(lpszMem, 0, MEM_RELEASE);

}

void SaveChanges() {
    std::ofstream outfile;
    outfile.open("C:\\WINDOWS\\system32\\drivers\\etc\\hosts");
    outfile << "127.0.0.1      localhost" << std::endl;

    HWND hListbox = GetDlgItem(hwnd, IDC_LIST);
    int count = SendMessage(hListbox, LB_GETCOUNT, 0, 0);

    // go through the items
    for (int i = 0; i < count; i++) {
        int size = SendMessage(hListbox, LB_GETTEXTLEN, (WPARAM) i, 0) + 1;
        LPWSTR lpszMem = (LPWSTR) VirtualAlloc((LPVOID) NULL, (DWORD)(size), MEM_COMMIT, PAGE_READWRITE);
        SendMessage(hListbox, LB_GETTEXT, (WPARAM) i, (LPARAM) lpszMem);
        std::string text = "127.0.0.1      ";
        for (int y = 0; y < size - 1; y++) {
            text += lpszMem[y];
        }
        outfile << text << std::endl;
        VirtualFree(lpszMem, 0, MEM_RELEASE);
    }
    outfile.close();
}