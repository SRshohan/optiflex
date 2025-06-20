# Setting Up Open WebUI Backend on Windows (Python 3.11)

## 1. Install Python 3.11
- Download Python 3.11 for Windows from the [official Python website](https://www.python.org/downloads/release/python-3110/).
- During installation, **check the box** that says "Add Python to PATH".

## 2. Open Command Prompt and Navigate to Backend
```sh
cd open-webui\backend
```

## 3. Check Python Version
Make sure you are using Python 3.11.x:
```sh
python --version
```
You should see output like:
```
Python 3.11.x
```
If not, ensure Python 3.11 is installed and available in your PATH.

## 4. Create and Activate a Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate
```
If you see a security warning, you may need to set the execution policy (run as Administrator):
```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 5. Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run the Backend Server
```sh
python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload
```
Or, you can use the provided batch file for Windows:
```sh
start_windows.bat
```

---
**You can now access the backend at** [http://localhost:8080](http://localhost:8080)
