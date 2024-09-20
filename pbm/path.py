import os
import winreg


def add_to_system_path(new_path):
    # Check if the new path is already in the system PATH
    current_path = os.environ['PATH']
    if new_path in current_path:
        print(f"Path '{new_path}' is already in the system PATH.")
        return

    # Open the registry key where the system environment variables are stored
    reg_key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        0,
        winreg.KEY_ALL_ACCESS
    )

    try:
        # Retrieve the current PATH from the registry
        value, regtype = winreg.QueryValueEx(reg_key, 'PATH')
        new_path_value = value + ';' + new_path

        # Update the PATH value
        winreg.SetValueEx(reg_key, 'PATH', 0, regtype, new_path_value)
        print(f"Successfully added '{new_path}' to the system PATH.")

        # Notify the system about the changes
        os.system('setx PATH "%PATH%;{new_path}"')

    finally:
        winreg.CloseKey(reg_key)


# Example usage
bat_file_path = ""
add_to_system_path(os.path.dirname(bat_file_path))