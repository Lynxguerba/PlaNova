PlaNova/
│
├── main.py                        # Entry point for the app
│
├── config/
│   ├── __init__.py
│   ├── settings.py                 # App-wide constants (colors, fonts, paths)
│   └── themes.py                   # Theme definitions (dark/light)
│
├── core/
│   ├── __init__.py
│   ├── app.py                      # Tkinter root window setup
│   ├── database.py                 # Database or JSON file handling
│   ├── utils.py                    # Helper functions (formatting, timers, etc.)
│
├── assets/
│   ├── icons/                      # App icons, buttons, etc.
│   ├── images/                     # Static images
│   └── fonts/                      # Custom fonts if needed
│
├── components/
│   ├── __init__.py
│   ├── navbar.py                   # Navigation bar widget
│   ├── sidebar.py                  # Sidebar (if used)
│   ├── task_card.py                # Custom frame to display a single task
│   ├── note_widget.py              # Widget to display/edit notes
│   └── button.py                   # Reusable styled button class
│
├── pages/
│   ├── __init__.py
│   ├── dashboard_page.py           # Dashboard view
│   ├── tasks_page.py               # Task management view
│   ├── notes_page.py               # Notes management view
│   └── settings_page.py            # Settings and preferences
│
└── data/
    ├── database.db                 # SQLite database (or JSON file)
    └── preferences.json            # User settings storage
