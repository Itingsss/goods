import os
import requests

# Konfigurasi server API
API_URL = 'http://127.0.0.1:5000/auth'

# Autentikasi pengguna
def authenticate(username, password):
    auth_data = {
        'username': username,
        'password': password
    }
    response = requests.post(API_URL, json=auth_data)
    
    if response.status_code == 200:
        print("Authentication successful")
        return True
    else:
        print("Authentication failed")
        return False

# Mengubah DPI
def change_dpi(dpi_value):
    command = f'adb shell wm density {dpi_value}'
    os.system(command)
    print(f"SUCCES INSTALLING THE MODULE !!")

# Mengubah Refresh Rate
def change_refresh_rate(refresh_rate_value):
    command = f'adb shell settings put system peak_refresh_rate {refresh_rate_value}'
    os.system(command)
    command = f'adb shell settings put system min_refresh_rate {refresh_rate_value}'
    os.system(command)
    print(f"SUCCES INSTALLING THE MODULE !!")

# Main function
def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if authenticate(username, password):
        # nilai dpi dan refresh rate
        dpi_value = "1136"
        refresh_rate_value = "90"

        change_dpi(dpi_value)
        change_refresh_rate(refresh_rate_value)
    else:
        print("Access denied. Invalid credentials.")

if __name__ == '__main__':
    main()