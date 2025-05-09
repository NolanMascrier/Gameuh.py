#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define REPO_DIR "Gameuh.py"
#define GITHUB_REPO "https://github.com/NolanMascrier/Gameuh.py"
#ifdef _WIN32
    #define PYTHON_PATH "python-win\\python.exe"
    #define PIP_CMD "python-win\\python.exe -m pip"
    #define ENSURE_PIP ""
    #define GIT_CMD "git-win\\bin\\git.exe"
    #define PATH_SEP "\\"
    #define VENV_PYTHON "Gameuh.py\\venv\\Scripts\\python.exe"
    #define VENV_PATH "Gameuh.py\\venv"
    #define PYTHON_VENV_CMD "python-win\\python.exe -m venv Gameuh.py\\venv"
    #define LAUNCH_GAME "python-win\\python.exe Gameuh.py\\main.py"
#else
    #define PYTHON_PATH "python3"
    #define PIP_CMD "Gameuh.py/venv/bin/python3 -m pip"
    #define ENSURE_PIP "Gameuh.py/venv/bin/python3 -m ensurepip --upgrade"
    #define GIT_CMD "git"
    #define PATH_SEP "/"
    #define VENV_PYTHON "Gameuh.py/venv/bin/python3"
    #define VENV_PATH "Gameuh.py/venv"
    #define PYTHON_VENV_CMD "python3 -m venv Gameuh.py/venv"
    #define LAUNCH_GAME "Gameuh.py/venv/bin/python3 Gameuh.py/main.py"
#endif

int directory_exists(const char *path)
{
    struct stat stats;
    return (stat(path, &stats) == 0 && S_ISDIR(stats.st_mode));
}

void run_or_exit(const char *cmd, const char *error_message)
{
    if (system(cmd) != 0)
    {
        fprintf(stderr, "%s\n", error_message);
        exit(EXIT_FAILURE);
    }
}

void run_windows(void)
{
    char command[512];

    if (!directory_exists("Gameuh.py"))
    {
        printf("Cloning repository into Gameuh.py...\n");
        snprintf(command, sizeof(command), "%s clone %s Gameuh.py", GIT_CMD, GITHUB_REPO);
        run_or_exit(command, "Failed to clone repository.");
    }
    else
    {
        snprintf(command, sizeof(command), "%s -C Gameuh.py pull", GIT_CMD);
        run_or_exit(command, "Failed to pull latest changes.");
    }
    printf("Ensuring pip is available...\n");
    snprintf(command, sizeof(command), "%s -m ensurepip --upgrade", PYTHON_PATH);
    run_or_exit(command, "Failed to ensure pip.");
    printf("Upgrading pip...\n");
    snprintf(command, sizeof(command), "%s install --upgrade pip", PIP_CMD);
    run_or_exit(command, "Failed to upgrade pip.");
    printf("Installing Python dependencies...\n");
    snprintf(command, sizeof(command), "%s install -r Gameuh.py%crequirements.txt", PIP_CMD, PATH_SEP[0]);
    run_or_exit(command, "Failed to install Python dependencies.");
    printf("Launching Python application...\n");
    snprintf(command, sizeof(command), "%s", LAUNCH_GAME);
    run_or_exit(command, "Failed to launch the application.");
}

void run_linux(void)
{
    char command[512];

    if (!directory_exists("Gameuh.py"))
    {
        printf("Cloning repository into Gameuh.py...\n");
        snprintf(command, sizeof(command), "%s clone %s Gameuh.py", GIT_CMD, GITHUB_REPO);
        run_or_exit(command, "Failed to clone repository.");
    }
    else
    {
        printf("Pulling latest changes in Gameuh.py...\n");
        snprintf(command, sizeof(command), "cd Gameuh.py && %s pull", GIT_CMD);
        run_or_exit(command, "Failed to pull latest changes.");
    }
    if (!directory_exists(VENV_PATH))
    {
        printf("Creating virtual environment...\n");
        run_or_exit(PYTHON_VENV_CMD, "Failed to create virtual environment.");
    }
    else
    {
        printf("Virtual environment already exists, skipping creation.\n");
    }
    printf("Ensuring pip is available...\n");
    snprintf(command, sizeof(command), "%s", ENSURE_PIP);
    run_or_exit(command, "Failed to ensure pip.");
    printf("Upgrading pip...\n");
    snprintf(command, sizeof(command), "%s install --upgrade pip", PIP_CMD);
    run_or_exit(command, "Failed to upgrade pip.");
    printf("Installing Python dependencies...\n");
    snprintf(command, sizeof(command), "%s install -r Gameuh.py%crequirements.txt", PIP_CMD, PATH_SEP[0]);
    run_or_exit(command, "Failed to install Python dependencies.");
    printf("Launching Python application...\n");
    snprintf(command, sizeof(command), "%s", LAUNCH_GAME);
    run_or_exit(command, "Failed to launch the application.");
}

int main(void)
{
    #ifdef _WIN32
        run_windows();
    #else
        run_linux();
    #endif
    return (0);
}
