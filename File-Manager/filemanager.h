#ifndef FILEMANAGER_H_INCLUDED
#define FILEMANAGER_H_INCLUDED

#include <string>
#include <windows.h>

class FILEMANAGER
{
    public:
        FILEMANAGER();
        FILEMANAGER(std::string Dir);
        void PrintDirFiles();
        bool SetCurrentDir(const std::string &NewDir);
        void GoBack();
        bool AppendDir(const std::string &DirToAdd);
        bool CreateFolder(const std::string &FolderName);
        bool RemoveFile(const std::string &FileName);
        bool RemoveFolder(const std::string &DirectoryName);
        bool SetCopiedFile(const std::string &FileToCopy);
        bool SetCutFile(const std::string &FileToCut);
        void EmptyCopiedFile();
        void EmptyCutFile();
        bool ApplyCutFile(const std::string &NewName);
        bool ApplyCopyFile(const std::string &NewName, BOOL type);
        bool RenameFile(const std::string &OldName,const std::string &NewName);
        bool PasteFile(const std::string &NewName);
        void OpenFile(const std::string &FileName);
        std::string GetCurrentDir();
        std::string GetCopiedFile();
        std::string GetCutFile();
        std::string GetFileToPaste();
        virtual ~FILEMANAGER();

    private:
        std::string currentDir;
        std::string copiedFile;
        std::string cutFile;

};


#endif // FILEMANAGER_H_INCLUDED
