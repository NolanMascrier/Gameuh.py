#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#ifdef _WIN32
    #define PYTHON_PATH "venv\\Scripts\\python.exe"
    #define GIT_CMD "git"
    #define PATH_SEP "\\"
#else
    #define PYTHON_PATH "venv/bin/python3"
    #define GIT_CMD "git"
    #define PATH_SEP "/"
#endif

int directory_exists(const char *path)
{
    struct stat stats;

    return (stat(path, &stats) == 0 && S_ISDIR(stats.st_mode));
}

int file_exists(const char *path)
{
    struct stat stats;

    return (stat(path, &stats) == 0);
}

int main()
{
    char command[512];

    if (!directory_exists(".git"))
    {
        printf("Cloning repository...\n");
        system(GIT_CMD " clone https://github.com/NolanMascrier/Gameuh.py .");
    }
    else
    {
        printf("Pulling latest changes...\n");
        system(GIT_CMD " pull");
    }
    if (!file_exists(PYTHON_PATH))
    {
        printf("Setting up virtual environment...\n");
        #ifdef _WIN32
            system("python -m venv venv");
            system("venv\\Scripts\\pip install -r requirements.txt");
        #else
            system("python3 -m venv venv");
            system("venv/bin/pip install -r requirements.txt");
        #endif
    }
    snprintf(command, sizeof(command), "%s main.py", PYTHON_PATH);
    system(command);
    return 0;
}