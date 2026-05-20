import os
import sys

def install():
    cwd = os.getcwd()
    bat_path = os.path.join(cwd, "jarvis_bootloader.bat")
    
    if not os.path.exists(bat_path):
        print(f"Error: {bat_path} not found!")
        sys.exit(1)
        
    # Target the Windows user Startup directory
    startup_dir = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
    vbs_path = os.path.join(startup_dir, "jarvis_boot.vbs")
    
    # Create the Visual Basic Script to launch the BAT file completely invisibly (0 flag means hidden window)
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{bat_path}" & Chr(34), 0
Set WshShell = Nothing
'''
    
    with open(vbs_path, "w") as f:
        f.write(vbs_content)
        
    print("=" * 50)
    print("JARVIS OS INTEGRATION SUCCESSFUL")
    print("=" * 50)
    print(f"Bootloader installed to: {vbs_path}")
    print("Jarvis will now silently boot your servers and launch a native chromeless window every time you turn on your PC.")

if __name__ == "__main__":
    install()
