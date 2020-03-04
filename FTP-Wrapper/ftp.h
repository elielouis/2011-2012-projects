#include <Windows.h>
#include <WinInet.h>
#include <iostream>
#pragma comment (lib, "wininet.lib")

class FTP
{
	public:
		FTP();
		~FTP();
		bool connect(LPCWSTR lpszServerName, LPCWSTR lpszUser, LPCWSTR lpszPassword);
		bool upload(LPCWSTR lpszLocation, LPCWSTR lpszRemFile);
		bool download(LPCWSTR lpszRemName, LPCWSTR lpszLocation);
		bool mkdir(LPCWSTR lpszDirectory);
		bool cd(LPCWSTR lpszDirectory);
		bool remove(LPCWSTR lpszFileName);
		bool rename(LPCWSTR lpszOldFileName, LPCWSTR lpszNewFileName);
		bool rmdir(LPCWSTR lpszDirectory);
		int getfilesize(LPCWSTR lpszFileName);
		HINTERNET gethandle();
		std::string getcd();


	private:
		bool m_connected;
		HINTERNET m_hInternet;
		HINTERNET m_hFtpSession;
};