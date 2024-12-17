import os
import zipfile
import sys
import platform
import yaml

class VShell:
    def printAll(self):
        print()
        for file in self.file_list:
            print(file)
        print("---------")
        for folder in self.folder_list:
            print(folder)
        print()

    def __init__(self, zip_file):
        self.current_path = '/'  # Current path
        self.zip_file = zip_file
        self.zip = zipfile.ZipFile(zip_file, "r")
        self.file_list = self.zip.namelist()  # List of all files in the zip file
        self.folder_list = list(set(
            os.path.dirname(file) for file in self.file_list if '/' in file
        ))  # Extract unique directories
        self.command_history = []  # Store the command history
        self.printAll()

    def exit(self):
        """ Command 'exit' """
        self.printAll()
        sys.exit(0)

    def ls(self):
        """ Command 'ls' prints all files and directories in current directory """
        files_in_dir = [f for f in self.file_list if f.startswith(self.current_path[1:]) and f != self.current_path]
        subdirs = set()
        for f in files_in_dir:
            relative_path = f[len(self.current_path[1:]):].strip('/')
            subdir = relative_path.split('/')[0]
            subdirs.add(subdir)
        print('  '.join(sorted(subdirs)))

    def cd(self, path):
        """ Command 'cd' changes the current directory """
        if path == '/':
            self.current_path = '/'
            return True
        elif path == '..':
            if self.current_path != '/':
                self.current_path = '/'.join(self.current_path.rstrip('/').split('/')[:-1])
                if not self.current_path:
                    self.current_path = '/'
            return True
        else:
            new_path = os.path.normpath(os.path.join(self.current_path, path))
            if any(f.startswith(new_path.lstrip('/') + '/') for f in self.file_list):
                self.current_path = new_path
                return True
            else:
                print(f"No such directory: {path}")
                return False

    def rmdir(self, dir_name):
        """ Command 'rmdir' deletes an empty directory """
        full_path = os.path.normpath(os.path.join(self.current_path, dir_name)).strip('/')
        
        if full_path in self.folder_list:
            # Check if the directory is empty
            check = [file for file in self.file_list if file.startswith(full_path + "/")]
            if not len(check) > 1:
                self.file_list.remove(full_path + '/')
                self.folder_list.remove(full_path)
                print(f"Directory '{dir_name}' has been removed.")
            else:
                print(f"Directory '{dir_name}' is not empty.")
        else:
            print(f"Directory '{dir_name}' not found.")

    def uname(self):
        """ Command uname displays system information """
        system    = platform.system()
        node      = platform.node()
        release   = platform.release()
        version   = platform.version()
        machine   = platform.machine()
        processor = platform.processor()

        print("System Information:")
        print(f"    System:    {system}")
        print(f"    Node Name: {node}")
        print(f"    Release:   {release}")
        print(f"    Version:   {version}")
        print(f"    Machine:   {machine}")
        print(f"    Processor: {processor}")

    def run_script(self, script_file):
        """ Run commands from script file """
        with open(script_file, 'r') as script:
            for line in script:
                self.execute_command(line.strip())

    def execute_command(self, command):
        """ Processing user commands """
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        # Save command into history
        self.command_history.append(command)

        if cmd == 'exit':
            self.exit()
        elif cmd == 'ls':
            if args:
                if len(args) == 1:
                    CurrentPath = self.current_path
                    check = self.cd(args[0])
                    if check:
                        self.ls()
                        self.cd(CurrentPath)
                else:
                    print("ls: too many arguments")
            else:
                self.ls()
        elif cmd == 'cd':
            if args:
                if len(args) == 1:
                    self.cd(args[0])
                else:
                    print("cd: too many arguments")
            else:
                print("cd: missing argument")
        elif cmd == 'rmdir':
            if args:
                if len(args) == 1:
                    self.rmdir(args[0])
                else:
                    print("rmdir: too many arguments")
            else:
                print("rmdir: missing argument")
        elif cmd == 'uname':
            self.uname()
        else:
            print(f"Command not found: {cmd}")

    def close(self):
        """ Close the zip file"""
        self.zip.close()

def test_commands(vshell):
    """
    Test all implemented commands.
    """
    print("Testing commands...")
    print("======================================")

    # Test ls
    print("Testing ls command:")
    vshell.execute_command("ls")
    vshell.execute_command("ls /test_fs/dir1")
    print("======================================")

    # Test cd
    print("Testing cd command:")
    vshell.execute_command("cd /test_fs/dir1")
    vshell.execute_command("cd /")
    vshell.execute_command("cd filesystem_image")
    print("======================================")
        
    # Test rmdir
    print("Testing rmdir command:")
    vshell.execute_command("rmdir Main.java")
    vshell.execute_command("rmdir test_fs")
    vshell.execute_command("rmdir for--rm")
    vshell.execute_command("rmdir test_fs/dir1/for-rm")
    print("======================================")

    # Test uname
    print("Testing uname command:")
    vshell.execute_command("uname")
    print("======================================")

    # Test exit
    print("Testing exit command:")
    vshell.execute_command("exit")
    print("======================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: vshell.py <yaml_file> [--script]")
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        data = yaml.safe_load(file)

    user = data.get("user", "anonymous")
    host = data.get("host", "vshell")
    filesystem = data.get("filesystem", "file.zip")
    startup_script = data.get("startup_script", "anonymous")

    zip_file = filesystem
    vshell = VShell(zip_file)

    # test_commands(vshell)

    # If option --script added, run commands from script
    if len(sys.argv) == 3 and sys.argv[2] == '--script':
        script_file = startup_script
        vshell.run_script(script_file)
    else:
        # Run the CLI emulator
        while True:
            try:
                command = input(f"{user}@{host}:{vshell.current_path}$ ")
                vshell.execute_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting vshell...")
                break

    vshell.exit()
