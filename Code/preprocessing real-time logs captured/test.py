import subprocess


# PowerShell script path that capture the Sysmon Logs
powershell_script = r"D:\\New folder-Copy\\logsCapture.ps1"  

# Run PowerShell script using subprocess
try:
    subprocess.run(["powershell", "-File", powershell_script], check=True)
    print("PowerShell script executed successfully")
except subprocess.CalledProcessError as e:
    print(f"PowerShell script failed with error: {e}")


# python script path that makes preprocessing of extracted logs
script_to_run = "function_script.py"

# Run the script using subprocess
subprocess.run(["python", script_to_run])


