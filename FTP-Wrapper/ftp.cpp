#include "ftp.h"

FTP::FTP()
{
	m_hInternet = InternetOpen(NULL,INTERNET_OPEN_TYPE_DIRECT,NULL,NULL,0);
	m_connected = false;
}

FTP::~FTP()
{
	InternetCloseHandle(m_hFtpSession);
	InternetCloseHandle(m_hInternet); 
}


bool FTP::connect(LPCWSTR lpszServerName, LPCWSTR lpszUser, LPCWSTR lpszPassword)
{
	m_hFtpSession = InternetConnect(m_hInternet,lpszServerName,INTERNET_DEFAULT_FTP_PORT, lpszUser,lpszPassword, INTERNET_SERVICE_FTP, 0,0 );
	if (!m_hFtpSession)    { return false; }
	m_connected = true;
	return true;
}

bool FTP::upload(LPCWSTR lpszLocation, LPCWSTR lpszRemFile)
{
	if (!m_connected) return false;

	if (FtpPutFile(m_hFtpSession, lpszLocation, lpszRemFile, FTP_TRANSFER_TYPE_BINARY, 0))
		{
			return true;
		}
	return false; 
}

bool FTP::download(LPCWSTR lpszRemFile, LPCWSTR lpszLocation)
{
	if (!m_connected) return false;


	if (FtpGetFile(m_hFtpSession, lpszRemFile, lpszLocation, 0, 0, FTP_TRANSFER_TYPE_BINARY, 0))
		{
			return true;
		}
	return false; 
}

bool FTP::mkdir(LPCWSTR lpszDirectory)
{
	if (!FtpCreateDirectory(m_hFtpSession, lpszDirectory)) return false;
	return true;
}

bool FTP::cd(LPCWSTR lpszDirectory)
{
	if (!FtpSetCurrentDirectory(m_hFtpSession, lpszDirectory)) return false;
	return true;
}

bool FTP::remove(LPCWSTR lpszFileName)
{
	if (!FtpDeleteFile(m_hFtpSession, lpszFileName)) return false;
	return true;
}

bool FTP::rename(LPCWSTR lpszOldFileName, LPCWSTR lpszNewFileName)
{
	if (!FtpRenameFile(m_hFtpSession, lpszOldFileName, lpszNewFileName)) return false;
	return true;
}

bool FTP::rmdir(LPCWSTR lpszDirectory)
{
	if(!FtpRemoveDirectory(m_hFtpSession, lpszDirectory)) return false;
	return true;
}

HINTERNET FTP::gethandle()
{
	return m_hFtpSession;
}

std::string FTP::getcd()
{
	LPTSTR lpszCurrentDirectory 	= (LPTSTR)GlobalAlloc(GPTR, MAX_PATH + 1);
	DWORD lpdwCurrentDirectory = MAX_PATH;
	std::string strCurrentDirectory;
	
	if (!FtpGetCurrentDirectory(m_hFtpSession, lpszCurrentDirectory, &lpdwCurrentDirectory))
	{
		strCurrentDirectory = "ERROR-1";
		return strCurrentDirectory;
	}

	int len = (int)lpdwCurrentDirectory;
	for (int i = 0; i < len; i++)
	{
		strCurrentDirectory += lpszCurrentDirectory[i];
	}
	GlobalFree((HANDLE)lpszCurrentDirectory);

	return strCurrentDirectory;
}

int FTP::getfilesize(LPCWSTR lpszFileName)
{
	DWORD dwFileSize;
	FtpGetFileSize(m_hFtpSession, &dwFileSize);
	return (int)dwFileSize;
}




