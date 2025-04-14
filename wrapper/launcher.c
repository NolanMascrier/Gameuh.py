#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#ifdef _WIN32
    #define PYTHON_PATH "Gameuh.py\\venv\\Scripts\\python.exe"
    #define PIP_CMD "Gameuh.py\\venv\\Scripts\\pip"
    #define PATH_SEP "\\"
    #define PYTHON_VENV_CMD "python -m venv Gameuh.py\\venv"
#else
    #define PYTHON_PATH "Gameuh.py/venv/bin/python3"
    #define PIP_CMD "Gameuh.py/venv/bin/pip"
    #define PATH_SEP "/"
    #define PYTHON_VENV_CMD "python3 -m venv Gameuh.py/venv"
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

    if (!directory_exists("Gameuh.py"))
    {
        printf("Cloning repository into Gameuh.py...\n");
        system("git clone https://github.com/NolanMascrier/Gameuh.py Gameuh.py");
    }
    else
    {
        printf("Pulling latest changes in Gameuh.py...\n");
        system("cd Gameuh.py && git pull");
    }
    if (!file_exists(PYTHON_PATH)) {
        printf("Creating virtual environment...\n");
        system(PYTHON_VENV_CMD);
        printf("Updating Pip ...\n");
        snprintf(command, sizeof(command), "%s -m ensurepip --upgrade", PYTHON_PATH);
        system(command);
    }
    printf("Updating Pip ...\n");
    snprintf(command, sizeof(command), "%s install --upgrade pip", PIP_CMD);
    system(command);
    printf("Installing Python dependencies...\n");
    snprintf(command, sizeof(command), "%s install -r Gameuh.py%crequirements.txt", PIP_CMD, PATH_SEP[0]);
    system(command);
    printf("Launching Python application...\n");
    snprintf(command, sizeof(command), "%s Gameuh.py%cmain.py", PYTHON_PATH, PATH_SEP[0]);
    system(command);
    return 0;
}