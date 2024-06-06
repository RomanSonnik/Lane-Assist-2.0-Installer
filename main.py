import time
import urllib.request
import os
import sys
import subprocess
import ctypes


test_mode = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


program_path = resource_path("")
if "Temp" in program_path:
    program_path = os.path.dirname(sys.executable)
lane_assist_path = os.path.join(program_path, 'ETS2_Lane_Assist')
frontend_path = os.path.join(lane_assist_path, 'frontend')
start_script_path = os.path.join(lane_assist_path, 'start.bat')


def print_error_message(error_type, error):
    print("Sorry, there was an error during your installation:")
    if error_type != "warning":
        if error_type == "download":
            if error == "node":
                link = "https://nodejs.org/dist/v20.13.1/node-v20.13.1-x64.msi"
            elif error == "python":
                link = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
            elif error == "git":
                link = "https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe"
            print(f"Failed to download {error}, try to download {error} using this link: {link}")
        else:
            print(f"{error}")
        print("Installation failed, please try installing ETS2 Lane assist manually")
        print("There is the guide how to do it: https://ets2la.github.io/documentation/installation/beta-1/")
        input("Hit enter to exit.")
        sys.exit(-1)
    else:
        print(error)
        print("This error is not fatal and installation will try to continue, but there might be errors.")
        print("To solve error we would recommend to delete all files, except this installer and try again")
        input("Hit enter to continue installation")


def check_program_version(program):
    if program == "nodejs":
        print("Checking for installed nodejs...")
        result = subprocess.run(['node', '--version'], stdout=subprocess.PIPE)
        final = result.stdout.decode('utf-8')
        if "20" in final:
            return True
        else:
            return None
    elif program == "python311":
        print("Checking for installed python 3.11...")
        result = subprocess.run(['python', '--version'], stdout=subprocess.PIPE)
        final = result.stdout.decode('utf-8')
        if "3.11" in final:
            return True
        else:
            return None
    elif program == "git":
        print("Checking for installed git...")
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE)
        final = result.stdout.decode('utf-8')
        if "2." in final:
            return True
        else:
            return None


def check_node():
    node_version = check_program_version("nodejs")
    if node_version:
        print("Node.js exists on your PC")
        return True
    else:
        return None


def check_python():
    python311_installed = check_program_version("python311")
    if python311_installed:
        print("Python 3.11 exists on your PC")
        return True
    else:
        return None


def check_git():
    git_installed = check_program_version("git")
    if git_installed:
        print("Git exists on your PC")
        return True
    else:
        return None


def main():
    global test_mode
    if os.path.exists("./ETS2_Lane_Assist"):
        print("Installing requirements")
        time.sleep(1)
        os.system(f"cd ETS2_Lane_Assist && pip install -r requirements.txt")
        time.sleep(1)
        os.system(f"cd ETS2_Lane_Assist/frontend && npm install")
        time.sleep(1)
        print("Successful installed all needed requirements")
        time.sleep(1)
        with open("ETS2_Lane_Assist/start.bat", 'w') as file:
            # Write some text to the file
            file.write('python main.py')
        print("Start script created successfully.")
        time.sleep(1)
        print("Now you can delete installer and launch ETS 2 Lane Assist beta using start.bat")
        time.sleep(1)
        print("If there will be any errors please contact us in our official discord:")
        print("https://discord.gg/DpJpkNpqwD")
        input("Hit enter to exit")
        sys.exit(0)
    else:
        print_error_message("fail", "Target directory not exist")


print("Welcome to ETS 2 Lane Assist 2.0 installer. It will install all necessary programs.")
time.sleep(1)
print("Checking for needed programs")
time.sleep(1)
if not test_mode:
    errors = False
    if not check_node():
        errors = True
        print("Failed to find NodeJS on your system, installing...")
        if not test_mode:
            urllib.request.urlretrieve("https://nodejs.org/dist/v20.13.1/node-v20.13.1-x64.msi", "node.msi")
            command = 'msiexec /i node.msi TARGETDIR="C:\\Program Files\\nodejs\\" /passive'
            os.system(command)
            os.remove("node.msi")
        if not check_node():
            errors = False
            print_error_message("download", "node")
    time.sleep(1)
    if not check_python():
        errors = True
        print("Failed to find python 3.11 on your system, installing...")
        if not test_mode:
            urllib.request.urlretrieve("https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe", "python.exe")
            command = 'python.exe'
            WS_EX_TOPMOST = 0x40000
            windowTitle = "Please, read message above!"
            message = "Hello, please select ADD TO PATH option in installer, otherwise it will not work!"

            # display a message box; execution will stop here until user acknowledges
            ctypes.windll.user32.MessageBoxExW(None, message, windowTitle, WS_EX_TOPMOST)

            os.system(command)
            os.remove("python.exe")
        if not check_python():
            errors = False
            print_error_message("download", "python")
    time.sleep(1)
    if not check_git():
        errors = True
        print("Failed to find git on your system, installing...")
        if not test_mode:
            urllib.request.urlretrieve(
                "https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe",
                "git.exe")
            command = 'git.exe /SILENT /NOCANCEL /NORESTART'
            os.system(command)
            os.remove("git.exe")
        if not check_git():
            errors = False
            print_error_message("download", "git")
    time.sleep(1)
    if errors:
        print("Please relaunch app to continue installation!")
        input("Hit enter to exit")
    else:
        print("Successful checked all needed programs")
        print("Downloading files, please be patient and DONT CLOSE INSTALLER, thanks!")
        if not os.path.exists("./ETS2_Lane_Assist"):
            command = f"git clone https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist.git ./ETS2_Lane_Assist"
            subprocess.call(command)
        else:
            print_error_message("warning", "Target directory already exists or not empty.")
        command = f"cd ETS2_Lane_Assist && git checkout rewrite"
        os.system(command)
        main()
else:
    main()
