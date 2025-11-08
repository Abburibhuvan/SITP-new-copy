# Student Complaint Management System - Requirements

## 📋 System Requirements

### 🖥️ Operating System
- **Windows 10/11** (Recommended)
- **macOS 10.15+** (Compatible)
- **Linux Ubuntu 18.04+** (Compatible)

### 💻 Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 2GB free space
- **Processor**: Any modern CPU (Intel i3/AMD Ryzen 3 or better)
- **Internet**: Required for email functionality

### 🌐 Internet Connection
- **Required**: For email notifications and API calls
- **Speed**: Minimum 1 Mbps download/upload
- **Stability**: Consistent connection for reliable email delivery

---

## 🐍 Python Requirements

### Python Version
- **Python 3.11+** (Required)
- **Python 3.12** (Recommended)
- **Python 3.10** (Minimum supported)

### Python Installation
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation: `python --version`

---

## 📦 Required Python Packages

### Core Django Framework
```bash
Django==5.2.4
```

### Database
```bash
# SQLite (included with Python)
# No additional installation needed for development
```

### Environment Management
```bash
python-dotenv==1.1.1
```

### Data Processing & Excel Support
```bash
pandas==2.3.1
openpyxl==3.1.5
numpy==2.3.2
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
et-xmlfile==2.0.0
```

### HTTP Requests & API Communication
```bash
requests==2.32.4
urllib3==2.5.0
certifi==2025.8.3
charset-normalizer==3.4.2
idna==3.10
```

### Django Dependencies (Auto-installed)
```bash
asgiref==3.9.1
sqlparse==0.5.3
tzdata==2025.2
```

---

## 🔧 Installation Commands

### Complete Installation Script
```bash
# 1. Create virtual environment
python -m venv env

# 2. Activate virtual environment
# Windows:
.\env\Scripts\Activate.ps1
# macOS/Linux:
source env/bin/activate

# 3. Install all required packages
pip install django==5.2.4 python-dotenv==1.1.1 pandas==2.3.1 openpyxl==3.1.5 requests==2.32.4

# 4. Verify installation
python -c "import django; print(f'Django {django.get_version()}')"
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
python -c "import openpyxl; print('OpenPyXL installed successfully')"
python -c "import requests; print(f'Requests {requests.__version__}')"
```

### Individual Package Installation
```bash
# Core framework
pip install django==5.2.4

# Environment variables
pip install python-dotenv==1.1.1

# Data processing
pip install pandas==2.3.1
pip install openpyxl==3.1.5

# HTTP requests
pip install requests==2.32.4
```

---

## 🌐 External Services & APIs

### Email Service (Brevo API)
- **Service**: Brevo (formerly Sendinblue)
- **Purpose**: Send email notifications
- **API Key**: Required (configured in settings)
- **Endpoint**: https://api.brevo.com/v3/smtp/email
- **Rate Limit**: 300 emails/day (free tier)

### SMTP Configuration (Alternative)
- **Service**: Gmail SMTP
- **Host**: smtp.gmail.com
- **Port**: 587
- **Security**: TLS
- **Authentication**: App password required

---

## 📁 Project Structure Requirements

### Required Directories
```
project_root/
├── env/                          # Virtual environment
├── core/                         # Core app
├── Student/                      # Student app
├── dept_admin/                   # Department admin app
├── TAU/                          # Main project
├── static/                       # Static files
├── media/                        # Uploaded files
├── templates/                    # HTML templates
├── logs/                         # Log files (auto-created)
├── manage.py                     # Django management
├── settings.py                   # Settings file
├── db.sqlite3                    # Database (auto-created)
└── requirements.txt              # Package list
```

### File Permissions
- **Read/Write**: All project directories
- **Execute**: Virtual environment scripts
- **Web Server**: Access to static and media folders

---

## 🔐 Environment Variables

### Required Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
BREVO_API_KEY=your-brevo-api-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Site Configuration
SITE_URL=http://localhost:8000
SERVER_EMAIL=noreply@apollouniversity.edu.in
```

### Optional Environment Variables
```env
# Database (if using external database)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Security (for production)
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
```

---

## 🚀 Quick Start Checklist

### ✅ Pre-Installation
- [ ] Python 3.11+ installed
- [ ] Python added to PATH
- [ ] Project files downloaded
- [ ] Internet connection available

### ✅ Installation
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] All packages installed
- [ ] Installation verified

### ✅ Configuration
- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Admin user created

### ✅ Testing
- [ ] Server starts without errors
- [ ] Website accessible in browser
- [ ] Email functionality tested
- [ ] File uploads working

---

## 🛠️ Troubleshooting Common Issues

### Python Not Found
```bash
# Solution: Install Python and add to PATH
# Windows: Check "Add Python to PATH" during installation
# Verify: python --version
```

### Package Installation Errors
```bash
# Solution: Upgrade pip first
python -m pip install --upgrade pip

# Then install packages
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Windows PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.\env\Scripts\Activate.ps1
```

### Database Issues
```bash
# Reset database
python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
```

### Email Configuration Issues
```bash
# Test email settings
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

---

## 📊 Package Dependencies Tree

```
Django 5.2.4
├── asgiref 3.9.1
├── sqlparse 0.5.3
└── tzdata 2025.2

pandas 2.3.1
├── numpy 2.3.2
├── python-dateutil 2.9.0.post0
├── pytz 2025.2
└── six 1.17.0

openpyxl 3.1.5
└── et-xmlfile 2.0.0

requests 2.32.4
├── urllib3 2.5.0
├── certifi 2025.8.3
├── charset-normalizer 3.4.2
└── idna 3.10

python-dotenv 1.1.1
```

---

## 🔄 Version Compatibility

### Tested Combinations
- **Python 3.11 + Django 5.2.4** ✅ (Recommended)
- **Python 3.12 + Django 5.2.4** ✅ (Latest)
- **Python 3.10 + Django 5.2.4** ✅ (Minimum)

### Browser Compatibility
- **Chrome 90+** ✅
- **Firefox 88+** ✅
- **Safari 14+** ✅
- **Edge 90+** ✅

---

## 📞 Support Information

### Technical Support
- **Email**: support@apollouniversity.edu.in
- **Documentation**: USER_MANUAL.md
- **Issues**: Check troubleshooting section above

### Package Documentation
- **Django**: https://docs.djangoproject.com/
- **Pandas**: https://pandas.pydata.org/docs/
- **OpenPyXL**: https://openpyxl.readthedocs.io/
- **Requests**: https://requests.readthedocs.io/

---

*Last Updated: August 2025*
*Version: 1.0*
*System: Student Complaint Management System - Apollo University* 