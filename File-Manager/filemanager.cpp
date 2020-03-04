#include "FILEMANAGER.h"
#include <windows.h>
#include <string>
#include <stdio.h>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;

bool dirExists(const std::string& dirName_in)
{
  DWORD ftyp = GetFileAttributesA(dirName_in.c_str());
  if (ftyp == INVALID_FILE_ATTRIBUTES)
    return false;

  if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
    return true;

  return false;
}


bool IsDots(char chartocheck[])
{
    if (chartocheck[0] == '.')
        {
            return true;
        }
    else
        {
            return false;
        }

}


bool FileExists(const string &szPath)
{
    DWORD dwAttrib = GetFileAttributes(szPath.c_str());

    return (dwAttrib != INVALID_FILE_ATTRIBUTES &&
            !(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}



FILEMANAGER::FILEMANAGER() : currentDir("C:")
{

}

FILEMANAGER::FILEMANAGER(string Dir) : currentDir(Dir)
{

}

FILEMANAGER::~FILEMANAGER()
{
}


void FILEMANAGER::PrintDirFiles()
{
    // Print All The Files/Folders in a Directory
    WIN32_FIND_DATA ffd;
    cout << currentDir << endl << endl;
    string currentDir2 = currentDir + "\\*";
    const char* szDir = currentDir2.c_str();
    LARGE_INTEGER filesize;
    HANDLE hFind = INVALID_HANDLE_VALUE;
    hFind = FindFirstFile(szDir, &ffd);
    do
   {
       if(IsDots(ffd.cFileName)) continue;
      if (ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
      {
         printf(TEXT("%s   <DIR>\n"), ffd.cFileName);
      }
      else
      {
         filesize.LowPart = ffd.nFileSizeLow;
         filesize.HighPart = ffd.nFileSizeHigh;
         printf(TEXT("%s   %ld bytes\n"), ffd.cFileName, filesize.QuadPart);
      }
   }
   while (FindNextFile(hFind, &ffd) != 0);

    FindClose(hFind);

}

bool FILEMANAGER::SetCurrentDir(const string &NewDir)
{
    // Change current Directory;
    if (dirExists(NewDir))
    {
        currentDir = NewDir;
        return true;
    }
    else
    {
        return false;
    }

}

void FILEMANAGER::GoBack()
{
    // Go Back from one directory
    int pos;
    for(int i = currentDir.size()-1; i > 0; i--)
        {
            if (currentDir[i] == '\\')
                {
                    pos = i;
                    break;
                }
        }
    string newString;
    for(int i = 0; i< pos+1; i++)
        {
            newString += currentDir[i];
        }
    currentDir = newString;
}

bool FILEMANAGER::AppendDir(const string &DirToAdd)
{
    //Appends a directory at the end
    string newDir = currentDir + "\\" + DirToAdd;
    if (dirExists(newDir))
    {
    currentDir = newDir;
    return true;
    }
    else
    {
        return false;
    }
}

bool FILEMANAGER::CreateFolder(const string &FolderName)
{
    string newDir = currentDir + "\\" + FolderName;
    if (!dirExists(newDir))
    {
        if (CreateDirectory(newDir.c_str(), NULL))
            {
                return true;
            }
        else
            {
                return false;
            }
    }
    else
    {
        return false;
    }

}

bool FILEMANAGER::RemoveFile(const string &FileName)
{
    string FileLoc = currentDir + "\\" + FileName;
    if(DeleteFile(FileLoc.c_str()))
    {
        return true;
    }
    else
    {
        return false;
    }

}


bool FILEMANAGER::RemoveFolder(const string &DirectoryName)
{
    string FolderName = currentDir + "\\" + DirectoryName;
    HANDLE hFind = INVALID_HANDLE_VALUE;
    WIN32_FIND_DATA FindFileData;

    string DirPath = FolderName + "\\*";
    string FileName = FolderName + "\\";
    hFind = FindFirstFile(DirPath.c_str(), &FindFileData);
    if (hFind == INVALID_HANDLE_VALUE)
        {
            return false;
        }
    DirPath = FileName;

    do
    {
        if(IsDots(FindFileData.cFileName)) continue;
        FileName += FindFileData.cFileName;
        cout << FileName << endl;
        if ((FindFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
        {

            if (!RemoveFolder(FileName))
                {
                    FindClose(hFind);
                    return false;
                }

        }

        else
        {
            if(FindFileData.dwFileAttributes & FILE_ATTRIBUTE_READONLY)
            {
                _chmod(FileName.c_str(), _S_IWRITE);
            }
            if(!DeleteFile(FileName.c_str()))
            {
                FindClose(hFind);
                return false;
            }
        }

        FileName = DirPath;

    } while (FindNextFile(hFind, &FindFileData));

    FindClose(hFind);
    if(RemoveDirectory(FolderName.c_str()))
    {
        return true;
    }
    else
    {
        return false;
    }

}

bool FILEMANAGER::SetCopiedFile(const string &FileToCopy)
{
    string FileToCopyDir = currentDir + "\\" + FileToCopy;
    if(FileExists(FileToCopyDir))
        {
            EmptyCutFile();
            copiedFile = FileToCopyDir;
            return true;
        }
    else
    {
        return false;
    }

}


bool FILEMANAGER::SetCutFile(const string &FileToCut)
{
    string FileToCutDir = currentDir + "\\" + FileToCut;
    if(FileExists(FileToCutDir))
        {
            EmptyCopiedFile();
            cutFile = FileToCutDir;
            return true;
        }
    else
    {
        return false;
    }

}

void FILEMANAGER::EmptyCopiedFile()
{
    copiedFile = "";
}

void FILEMANAGER::EmptyCutFile()
{
    cutFile = "";
}


bool FILEMANAGER::ApplyCutFile(const std::string &NewName)
{
    string NewFileLocation = currentDir + "\\" + NewName;
    if(MoveFile(cutFile.c_str(), NewFileLocation.c_str()))
    {
        EmptyCutFile();
        return true;
    }
    else
    {
        return false;
    }
}

bool FILEMANAGER::ApplyCopyFile(const std::string &NewName, BOOL type)
{
    string NewLocation = currentDir + "\\" + NewName;
    if(CopyFile(copiedFile.c_str(),  NewLocation.c_str(), type))
    {
        EmptyCopiedFile();
        return true;
    }

    else
    {
        return false;
    }
}

bool FILEMANAGER::PasteFile(string const &NewName)
{
    if(copiedFile != "")
    {
        if (ApplyCopyFile(NewName, FALSE))
        {
            return true;
        }
        else
        {
            return false;
        }

    }
    else if(cutFile != "")
    {
        if (ApplyCutFile(NewName))
        {
            return true;
        }
        else
        {
            return false;
        }

    }
    else
    {
        return false;
    }
}

bool FILEMANAGER::RenameFile(const string &OldName, const string &NewName)
{
    string OldFileLocation = currentDir + "\\" + OldName;
    string NewFileLocation = currentDir + "\\" + NewName;
    return MoveFile(OldFileLocation.c_str(), NewFileLocation.c_str());
}

void FILEMANAGER::OpenFile(const string &FileName)
{
    string FileLocation = currentDir + "\\" + FileName;
    ShellExecute(NULL,"open",FileLocation.c_str(),NULL,NULL,SW_HIDE);
}


string FILEMANAGER::GetCurrentDir()
{
    return currentDir;
}

string FILEMANAGER::GetCopiedFile()
{
    return copiedFile;
}

string FILEMANAGER::GetCutFile()
{
    return cutFile;
}

string FILEMANAGER::GetFileToPaste()
{
    if(copiedFile != "")
    {
        return copiedFile;
    }
    else if (cutFile != "")
    {
        return cutFile;
    }
    else
    {
        return "No file Selected";
    }
}
