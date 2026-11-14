# RU Organization Management System

A Python-based desktop application for managing organization entries, built with **customtkinter** and **SQLite**.

## Project Structure

```
.
├── main_code.py          # Main application source code
├── secured_sys.db        # SQLite database file
├── logo.png              # Application logo
├── .git/                 # Git repository directory
├── .ruff_cache/          # Python linter cache
└── README.md             # This file
```

## Features

- **Login System**: Authentication screen to access the application
- **Data Entry**: Form to insert new records with unique ID, name, phone, vehicle number, type, and description
- **Search Data**: Search records by unique ID or name
- **View Data**: Treeview display of all records with filtering options
- **Update Data**: Modify existing records
- **Dashboard**: Overview of total entries, entries today, and current date
- **Barcode Scanning**: optional QR/code scanning functionality

## Requirements

- Python 3.8+
- customtkinter
- PIL (Pillow)
- numpy
- opencv-python (cv2)
- pyzbar (for barcode scanning)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install customtkinter pillow numpy opencv-python pyzbar
   ```
3. Ensure the database file `secured_sys.db` is present in the project directory
4. Run the application:
   ```bash
   python main_code.py
   ```

## Usage

1. **Login**: Use the default credentials or update them in the code
2. **Navigate**: Use the side menu to access different sections:
   - Dashboard: Overview statistics
   - New Entry: Add new records
   - View Data: Browse all records with filtering
   - Search Data: Find records by ID or name
   - Update Data: Modify existing records
3. **Database**: All data is stored in `secured_sys.db` SQLite database

## Notes

- The application uses hardcoded login credentials (`admin` / `0000`) - update these in `main_code.py` for production use
- The barcode scanner feature requires a camera and the `pyzbar` library with ZBar DLL
- Database path is relative to the script location (`secured_sys.db`)