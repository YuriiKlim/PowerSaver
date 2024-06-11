import subprocess
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_powershell_command(command):
    result = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running PowerShell command: {result.stderr}")
    return result.returncode


def create_task():
    try:
        create_task_command = (
            'schtasks /create /tn "SetBalancedPowerOnShutdown" /tr '
            '"powershell.exe -ExecutionPolicy Bypass -Command \\"powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e; schtasks /delete /tn \\\\\\"SetBalancedPowerOnShutdown\\\\\\" /f\\"" '
            '/sc onstart /ru "SYSTEM" /rl HIGHEST /f'
        )
        result = subprocess.run(create_task_command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print(f"Error creating scheduled task: {result.stderr}")
        else:
            print("Scheduled task created successfully.")
    except Exception as e:
        print(f"Error creating scheduled task: {e}")


def check_task_exists(task_name):
    try:
        result = subprocess.run(["schtasks", "/query", "/tn", task_name], capture_output=True, text=True, check=True)
        if "ERROR:" in result.stdout:
            print(f"Task '{task_name}' does not exist.")
        else:
            print(f"Task '{task_name}' exists.")
    except subprocess.CalledProcessError as e:
        print(f"Error querying task: {e}")


if __name__ == "__main__":
    if is_admin():
        power_saver_command = 'powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a'
        run_powershell_command(power_saver_command)

        create_task()

        check_task_exists("SetBalancedPowerOnShutdown")
    else:
        print("Script is not running with administrative privileges. Please run as administrator.")
