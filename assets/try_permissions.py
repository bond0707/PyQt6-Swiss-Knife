import ctypes
import os
import subprocess
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    download_path = os.path.abspath(os.path.expanduser("~\\Downloads"))
    internal_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".."))
    paths = [download_path, internal_path]
    for path in paths:
        try:
            result = subprocess.run(
                ['icacls', path], capture_output=True, text=True)
            if 'Users:(M)' in result.stdout:
                print(
                    f"The necessary permissions are already in place for {path}.")
            else:
                exit_code = os.system(f"icacls \"{path}\" /grant Users:(M)")
                if exit_code != 0:
                    raise Exception(
                        f'icacls command failed with exit code: {exit_code} for path: {path}')
        except Exception as e:
            print(f"An error occurred for path: {path}. Error: {e}")
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
