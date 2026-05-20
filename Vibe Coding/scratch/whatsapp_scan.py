import uiautomation as auto
import time

def scan_whatsapp():
    # Find the main WhatsApp window
    wa_windows = []
    
    # Iterate all top level windows
    for control in auto.GetRootControl().GetChildren():
        name = control.Name
        if "WhatsApp" in name or "whatsapp" in name.lower():
            wa_windows.append(control)
            
    if not wa_windows:
        print("No WhatsApp window found.")
        return
        
    print(f"Found {len(wa_windows)} WhatsApp windows.")
    for win in wa_windows:
        print(f"\nScanning Window: {win.Name}")
        # Try to find common Buttons inside it
        buttons = []
        try:
            for item in win.GetChildren():
                 print(f" - Child Name: {item.Name}, Class: {item.ClassName}, ControlType: {item.ControlType}")
        except Exception as e:
            print(f"Error accessing children: {e}")

if __name__ == "__main__":
    scan_whatsapp()
