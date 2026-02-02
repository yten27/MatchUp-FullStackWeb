# Contents of this repository

Das Repository ist angelegt für das Projekt im Modul FSWD an der HWR Berlin von Ayten Teshome und Leon Terencio Otte. 

# Steps to execute the app

**Step 1:** set up and activate a [Python Virtual Environment](https://hwrberlin.github.io/fswd/python-vscode.html#32-use-the-python-virtual-environment-as-default-for-this-workspace).

**Step 2:** install the required Python packages from the terminal with the command `pip install -r requirements.txt`:

```console
(venv) C:\Users\me\projects\webapp> pip install -r requirements.txt
```

**Step 3**: initialize the app's SQLite database via `flask init-db`:

```console
(venv) PS C:\Users\me\projects\webapp> flask init-db
Database has been initialized.
```

**Step 4:** start the web server via `flask run --reload`:

```console
(venv) PS C:\Users\me\projects\webapp> flask run --reload
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
```

**Step 5:** visit [http://127.0.0.1:5000/insert/sample](http://127.0.0.1:5000/insert/sample) to populate the app's database with some sample data.

**Step 6:** visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the landing page

# Dokumentation dieses Projekt über GitHub Pages:
https://yten27.github.io/MatchUp-FullStackWeb/
