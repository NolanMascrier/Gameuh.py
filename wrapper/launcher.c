#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <gtk/gtk.h>

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
    #define LAUNCH_GAME "cd Gameuh.py && ..\\python-win\\python.exe main.py"
#else
    #define PYTHON_PATH "python3"
    #define PIP_CMD "Gameuh.py/venv/bin/python3 -m pip"
    #define ENSURE_PIP "Gameuh.py/venv/bin/python3 -m ensurepip --upgrade"
    #define GIT_CMD "git"
    #define PATH_SEP "/"
    #define VENV_PYTHON "Gameuh.py/venv/bin/python3"
    #define VENV_PATH "Gameuh.py/venv"
    #define PYTHON_VENV_CMD "python3 -m venv Gameuh.py/venv"
    #define LAUNCH_GAME "cd Gameuh.py && venv/bin/python3 main.py"
#endif

GtkWidget *update_button;
GtkWidget *text_view;

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

gboolean is_update_available() {
    system("git -C ./ remote update > /dev/null 2>&1");

    FILE *local = popen("git -C ./ rev-parse HEAD", "r");
    FILE *remote = popen("git -C ./ rev-parse @{u}", "r");

    if (!local || !remote) return FALSE;

    char local_hash[100], remote_hash[100];
    fgets(local_hash, sizeof(local_hash), local);
    fgets(remote_hash, sizeof(remote_hash), remote);

    // Clean newline
    local_hash[strcspn(local_hash, "\n")] = 0;
    remote_hash[strcspn(remote_hash, "\n")] = 0;

    pclose(local);
    pclose(remote);

    // Compare hashes
    return strcmp(local_hash, remote_hash) != 0;
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

static void on_launch_clicked(GtkWidget *widget, gpointer data) {
    // Replace with your game's executable path
    system(LAUNCH_GAME);
}

static void on_exit_clicked(GtkWidget *widget, gpointer data) {
    gtk_main_quit();
}

/**
 * git -C ./ pull runs git pull in the current directory.
 * If your game is in a subfolder (like ./game/), use git -C ./game pull.
 */
static void on_update_clicked(GtkWidget *widget, gpointer data) {
    int result = system("git -C ./ pull");
    GtkWidget *dialog;

    if (result != 0) {
        dialog = gtk_message_dialog_new(NULL,
            GTK_DIALOG_DESTROY_WITH_PARENT,
            GTK_MESSAGE_ERROR,
            GTK_BUTTONS_CLOSE,
            "Update failed.\nCheck Git or network connection.");
    } else {
        dialog = gtk_message_dialog_new(NULL,
            GTK_DIALOG_DESTROY_WITH_PARENT,
            GTK_MESSAGE_INFO,
            GTK_BUTTONS_CLOSE,
            "Game successfully updated!");
        gtk_widget_set_sensitive(update_button, FALSE);  // Disable after update
    }

    gtk_dialog_run(GTK_DIALOG(dialog));
    gtk_widget_destroy(dialog);
}


void load_patch_notes() {
    const char *url = "https://raw.githubusercontent.com/NolanMascrier/Gameuh.py/refs/heads/main/PATCHNOTE.md";
    const char *tmp_file = "/tmp/patch_notes.txt";

    char curl_cmd[512];
    snprintf(curl_cmd, sizeof(curl_cmd),
             "curl -s -L \"%s\" -o \"%s\"", url, tmp_file);
    int res = system(curl_cmd);
    if (res != 0) return;

    FILE *f = fopen(tmp_file, "r");
    if (!f) return;

    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *text = malloc(len + 1);
    fread(text, 1, len, f);
    text[len] = '\0';
    fclose(f);

    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
    gtk_text_buffer_set_text(buffer, text, -1);
    free(text);
}

int main(int argc, char *argv[]) {
        gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Game Launcher");
    gtk_window_set_default_size(GTK_WINDOW(window), 600, 400);
    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);

    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), vbox);

    // Top Buttons
    GtkWidget *hbox = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 5);
    gtk_box_pack_start(GTK_BOX(vbox), hbox, FALSE, FALSE, 5);

    GtkWidget *launch_button = gtk_button_new_with_label("Launch");
    update_button = gtk_button_new_with_label("Update");
    GtkWidget *exit_button = gtk_button_new_with_label("Exit");

    gtk_box_pack_start(GTK_BOX(hbox), launch_button, TRUE, TRUE, 5);
    gtk_box_pack_start(GTK_BOX(hbox), update_button, TRUE, TRUE, 5);
    gtk_box_pack_start(GTK_BOX(hbox), exit_button, TRUE, TRUE, 5);

    g_signal_connect(launch_button, "clicked", G_CALLBACK(on_launch_clicked), NULL);
    g_signal_connect(update_button, "clicked", G_CALLBACK(on_update_clicked), NULL);
    g_signal_connect(exit_button, "clicked", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    // Patch Notes Label
    GtkWidget *label = gtk_label_new("Patch Notes:");
    gtk_box_pack_start(GTK_BOX(vbox), label, FALSE, FALSE, 5);

    // Scrollable Patch Notes TextView
    GtkWidget *scrolled = gtk_scrolled_window_new(NULL, NULL);
    gtk_widget_set_vexpand(scrolled, TRUE);
    gtk_scrolled_window_set_policy(GTK_SCROLLED_WINDOW(scrolled),
                                   GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);
    gtk_box_pack_start(GTK_BOX(vbox), scrolled, TRUE, TRUE, 5);

    text_view = gtk_text_view_new();
    gtk_text_view_set_wrap_mode(GTK_TEXT_VIEW(text_view), GTK_WRAP_WORD);
    gtk_text_view_set_editable(GTK_TEXT_VIEW(text_view), FALSE);
    gtk_text_view_set_cursor_visible(GTK_TEXT_VIEW(text_view), FALSE);
    gtk_container_add(GTK_CONTAINER(scrolled), text_view);

    // Initial Setup
    if (!is_update_available())
        gtk_widget_set_sensitive(update_button, FALSE);

    load_patch_notes();

    gtk_widget_show_all(window);
    gtk_main();
    return 0;
}

/*
int main(void)
{
    #ifdef _WIN32
        run_windows();
    #else
        run_linux();
    #endif
    return (0);
}
*/