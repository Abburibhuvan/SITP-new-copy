# Student Complaint Management System - User Manual

## 📋 Table of Contents
1. [What is this System?](#what-is-this-system)
2. [How to Start the System](#how-to-start-the-system)
3. [User Types and Access](#user-types-and-access)
4. [Student Portal Guide](#student-portal-guide)
5. [Department Admin Portal Guide](#department-admin-portal-guide)
6. [System Administrator Guide](#system-administrator-guide)
7. [Common Issues and Solutions](#common-issues-and-solutions)
8. [Contact Support](#contact-support)

---

## 🎯 What is this System?

The **Student Complaint Management System** is a web-based application that helps manage student complaints and support tickets at Apollo University. Think of it like a digital help desk where:

- **Students** can submit complaints and track their status
- **Department Admins** can manage and respond to complaints
- **System Admins** can oversee everything and create student accounts

### Key Features:
- ✅ Submit and track complaints
- ✅ Automatic email notifications
- ✅ SLA (Service Level Agreement) tracking
- ✅ Priority-based ticket management
- ✅ Department-specific routing
- ✅ Mobile-friendly interface

---

## 🚀 How to Start the System

### Prerequisites (One-time Setup)
Before you can use the system, you need to set up your computer:

1. **Install Python** (if not already installed)
   - Go to https://www.python.org/downloads/
   - Download and install Python 3.11 or later
   - Make sure to check "Add Python to PATH" during installation

2. **Download the Project Files**
   - Make sure all project files are in a folder on your computer

### Starting the System (Every Time)

**Step 1: Open Command Prompt/PowerShell**
- Press `Windows + R`
- Type `cmd` or `powershell` and press Enter

**Step 2: Navigate to Project Folder**
```bash
cd "C:\backup_2025-07-30_13-44-38"
```

**Step 3: Activate Virtual Environment**
```bash
.\env\Scripts\Activate.ps1
```
*You'll see `(env)` appear at the beginning of the command line*

**Step 4: Start the Server**
```bash
python manage.py runserver
```

**Step 5: Open Your Web Browser**
- Go to: http://localhost:8000
- The system is now running!

---

## 👥 User Types and Access

### 1. **Students** 👨‍🎓
- **Purpose**: Submit complaints and track their status
- **Access**: http://localhost:8000/student/
- **Login**: Use your student email and password
- **What they can do**:
  - Submit new complaints
  - View their complaint history
  - Track complaint status
  - Receive email updates

### 2. **Department Administrators** 👨‍💼
- **Purpose**: Manage complaints for their department
- **Access**: http://localhost:8000/department/
- **Login**: Use admin username and password
- **What they can do**:
  - View and respond to complaints
  - Update complaint status
  - Escalate urgent issues
  - Manage SLA settings
  - Generate reports

### 3. **System Administrators** 🔧
- **Purpose**: Oversee the entire system
- **Access**: http://localhost:8000/admin/
- **Login**: Use superuser credentials
- **What they can do**:
  - Create student accounts
  - Manage all departments
  - System configuration
  - User management
  - Database administration

---

## 🎓 Student Portal Guide

### Getting Started
1. **Access the Portal**
   - Go to: http://localhost:8000/student/
   - Click "Student Login"

2. **First Time Login**
   - Username: Your roll number (12 digits)
   - Password: The temporary password sent to your email
   - **Important**: You'll be asked to change your password on first login

3. **Submit a Complaint**
   - Click "Submit New Complaint"
   - Fill in the form:
     - **Subject**: Brief description of your issue
     - **Description**: Detailed explanation
     - **Priority**: Choose Low/Medium/High
     - **Attachment**: Upload any relevant files (optional)
   - Click "Submit"

4. **Track Your Complaints**
   - View all your complaints on the dashboard
   - Click on any complaint to see details
   - Check status updates and responses

### Student Features
- 📝 **Submit Complaints**: Create new support tickets
- 👀 **View History**: See all your past complaints
- 📊 **Status Tracking**: Monitor complaint progress
- 📧 **Email Notifications**: Get updates via email
- 🔒 **Secure Login**: Password-protected access

---

## 👨‍💼 Department Admin Portal Guide

### Getting Started
1. **Access the Portal**
   - Go to: http://localhost:8000/department/
   - Enter your admin credentials

2. **Dashboard Overview**
   - View pending complaints
   - See SLA breach alerts
   - Check department statistics

3. **Managing Complaints**
   - **View Complaints**: See all complaints for your department
   - **Respond to Complaints**:
     - Click on a complaint
     - Add your response
     - Update status (Open, In Progress, Resolved, Closed)
     - Set priority level
   - **Escalate Complaints**: Send urgent issues to higher authorities

4. **SLA Management**
   - Configure response times for different priorities
   - Monitor SLA breaches
   - Generate SLA reports

### Admin Features
- 📋 **Complaint Management**: Handle all department complaints
- ⚡ **SLA Monitoring**: Track response times
- 📊 **Reporting**: Generate department reports
- 📧 **Email Notifications**: Send updates to students
- 🔄 **Status Updates**: Change complaint status
- 📈 **Analytics**: View department performance

---

## 🔧 System Administrator Guide

### Getting Started
1. **Access Admin Panel**
   - Go to: http://localhost:8000/admin/
   - Login with superuser credentials

2. **Create Student Accounts**
   - Go to Department Admin Portal
   - Click "Create Student"
   - Fill in student details:
     - Email (must end with @apollouniversity.edu.in)
     - First Name
     - Last Name
     - Phone Number
   - System automatically:
     - Creates username (roll number)
     - Sets temporary password
     - Sends welcome email

3. **Bulk Student Creation**
   - Download Excel template
   - Fill in student details
   - Upload the file
   - System creates all accounts automatically

### System Admin Features
- 👥 **User Management**: Create and manage all user accounts
- 🏢 **Department Management**: Configure departments and admins
- ⚙️ **System Settings**: Configure email, SLA, and other settings
- 📊 **Global Reports**: View system-wide statistics
- 🔒 **Security Management**: Manage passwords and access

---

## 🛠️ Common Issues and Solutions

### System Won't Start
**Problem**: "Python was not found"
**Solution**:
1. Make sure Python is installed
2. Activate virtual environment: `.\env\Scripts\Activate.ps1`
3. Try again: `python manage.py runserver`

### Can't Login
**Problem**: "Invalid credentials"
**Solutions**:
1. Check username and password
2. Make sure you're using the correct portal
3. Contact admin to reset password

### Email Not Working
**Problem**: Welcome emails not being sent
**Solution**:
1. Check email configuration in settings
2. Verify internet connection
3. Check spam folder

### Slow Performance
**Problem**: System is slow
**Solutions**:
1. Close other applications
2. Restart the server
3. Check database size

### Browser Issues
**Problem**: Page not loading
**Solutions**:
1. Clear browser cache
2. Try different browser
3. Check if server is running

---

## 📞 Contact Support

### For Technical Issues:
- **Email**: support@apollouniversity.edu.in
- **Phone**: [Your Support Phone Number]
- **Hours**: Monday-Friday, 9 AM - 5 PM

### For Student Issues:
- Contact your department administrator
- Use the complaint system itself
- Visit the student support office

### Emergency Contact:
- **System Administrator**: [Admin Contact]
- **IT Support**: [IT Contact]

---

## 📋 Quick Reference Commands

### Starting the System
```bash
cd "C:\backup_2025-07-30_13-44-38"
.\env\Scripts\Activate.ps1
python manage.py runserver
```

### Creating Admin User
```bash
python manage.py createsuperuser
```

### Database Maintenance
```bash
python manage.py migrate
python manage.py collectstatic
```

### Stopping the System
- Press `Ctrl + C` in the command prompt
- Close the browser window

---

## 🎉 Congratulations!

You now have a complete understanding of the Student Complaint Management System. Whether you're a student submitting a complaint, a department admin managing tickets, or a system administrator overseeing everything, this manual should help you use the system effectively.

**Remember**: The system is designed to be user-friendly. If you get stuck, don't hesitate to ask for help!

---

*Last Updated: August 2025*
*Version: 1.0*
*System: Student Complaint Management System - Apollo University* 