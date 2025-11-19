# Quick Setup Guide for MediCart

This guide will help you get MediCart up and running in minutes.

## Prerequisites

- Python 3.8 or higher installed
- pip (comes with Python)
- Basic command line knowledge

## Step-by-Step Setup

### 1. Open Terminal/Command Prompt

Navigate to the project directory:
```bash
cd Pharmacy_Ecom
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (takes about 1-2 minutes).

### 4. Setup Database

Run these commands one by one:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Start the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### 7. Access the Application

Open your web browser and visit:
- **Main Application**: http://127.0.0.1:8000/
- **API Browser**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Quick Test

### Test via Web Interface:

1. Go to http://127.0.0.1:8000/
2. Click "Add New Medicine"
3. Fill in the form:
   - Name: `Aspirin`
   - Description: `Pain reliever`
   - Price: `9.99`
   - Stock: `100`
   - Expiry Date: Choose a future date
4. Click "Add Medicine"
5. Go to "Place Order" and create an order

### Test via API:

Open a new terminal and run:

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/medicines/" -Method GET | ConvertTo-Json
```

**macOS/Linux/Git Bash:**
```bash
curl http://127.0.0.1:8000/api/medicines/
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Or using pytest
pytest

# Verbose output
pytest -v
```

## Common Issues & Solutions

### Issue: "python: command not found"
**Solution**: Try `python3` instead of `python`

### Issue: "No module named django"
**Solution**: Make sure virtual environment is activated (you should see `(venv)`)

### Issue: "Port already in use"
**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

### Issue: "Access denied" on Windows
**Solution**: Run Command Prompt as Administrator

## Next Steps

1. Read `README.md` for complete documentation
2. Check `API_DOCUMENTATION.md` for API details
3. Explore the admin panel at `/admin/`
4. Try creating medicines and orders
5. Test the API endpoints

## Need Help?

- Check the README.md file
- Review the API documentation
- Check Django documentation: https://docs.djangoproject.com/

## Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## Deactivating Virtual Environment

When you're done:
```bash
deactivate
```

---

Happy coding! 🚀

