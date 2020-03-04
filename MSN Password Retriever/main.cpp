#include <windows.h>

#include <commctrl.h>

#include "WinCred.h"

#include "Wincrypt.h"


#
pragma comment(lib, "crypt32.lib")# pragma comment(lib, "Advapi32.lib")# pragma comment(lib, "comctl32.lib")

# define IDC_LISTVIEW 300

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void InitWindow(HWND hwnd, HINSTANCE hInstance);
HWND hwnd;

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow) {

    const wchar_t CLASS_NAME[] = L "Sample Window Class";

    WNDCLASS wc = {};

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
        L "MSN Password Retriever",
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,

        CW_USEDEFAULT, CW_USEDEFAULT, 400, 300,

        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    InitWindow(hwnd, hInstance);

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

        }
        return 0;

    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, & ps);
            LPCWSTR lpszText = L "Coded by Elie Louis";
            TextOut(hdc, 125, 10, lpszText, lstrlen(lpszText));
            EndPaint(hwnd, & ps);

        }
        return 0;

    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

void InitWindow(HWND hwnd, HINSTANCE hInstance) {
    INITCOMMONCONTROLSEX icex; // Structure for control initialization.
    icex.dwICC = ICC_LISTVIEW_CLASSES;
    InitCommonControlsEx( & icex);

    HWND hWndListView = CreateWindow(WC_LISTVIEW, NULL, WS_VISIBLE | WS_CHILD | LVS_REPORT | LVS_EDITLABELS | WS_VSCROLL | WS_HSCROLL,
        17, 40, 340, 200,
        hwnd,
        (HMENU) IDC_LISTVIEW,
        hInstance, NULL);

    // Initializing columns
    LV_COLUMN LvCol;
    memset( & LvCol, 0, sizeof(LvCol)); // Zero Members
    LvCol.mask = LVCF_TEXT | LVCF_WIDTH | LVCF_SUBITEM; // Type of mask
    LvCol.cx = 170; // width between each coloum
    LvCol.pszText = L "Email"; // First Header Text                
    SendMessage(hWndListView, LVM_INSERTCOLUMN, 0, (LPARAM) & LvCol);
    LvCol.pszText = L "Password";
    LvCol.cx = 400 - 170 - 40 - 17 - 2;
    SendMessage(hWndListView, LVM_INSERTCOLUMN, 1, (LPARAM) & LvCol);

    // Initializing items
    LV_ITEM LvItem;
    LvItem.mask = LVIF_TEXT; // Text Style
    LvItem.iItem = 0; // choose item  
    LvItem.iSubItem = 0; // Put in first coluom

    LPCWSTR lpszComp = L "WindowsLive:name=";

    DWORD dwCount;
    PCREDENTIAL * Credential;
    if (CredEnumerate(NULL, 0, & dwCount, & Credential)) {
        for (int i = 0; i < (int) dwCount; i++) {
            if (Credential[i] - > Type == CRED_TYPE_GENERIC) {

                if (wcsstr(Credential[i] - > TargetName, lpszComp)) {
                    LvItem.iSubItem = 0;
                    LvItem.iItem = i;
                    LvItem.pszText = (LPWSTR) Credential[i] - > UserName;
                    SendMessage(hWndListView, LVM_INSERTITEM, 0, (LPARAM) & LvItem);

                    if (Credential[i] - > CredentialBlob != NULL) // Check if password is saved
                    {
                        LvItem.iSubItem = 1;
                        LvItem.pszText = (LPWSTR) Credential[i] - > CredentialBlob;
                        SendMessage(hWndListView, LVM_SETITEM, 1, (LPARAM) & LvItem);
                    }

                }
            }
        }
        CredFree(Credential);
    }

}