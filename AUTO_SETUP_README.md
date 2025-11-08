# Automatic Setup on Deployment

This project includes automatic setup that runs on every deployment.

## What Gets Set Up Automatically

1. **Database Migrations** - All database tables are created/updated
2. **Admin User** - A superuser is created automatically
3. **Departments** - Default departments (Finance, Hostel, Mess, etc.)
4. **SLA Configurations** - Service Level Agreements for all departments

## Default Admin Credentials

```
Username: admin
Password: Admin@2024
Email: admin@apollouniversity.edu
```

## Customizing Admin Credentials

You can customize the admin credentials by setting environment variables in Zeabur:

```
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
ADMIN_EMAIL=your_email@example.com
```

## How It Works

The `start.sh` script runs automatically when the container starts:

1. Runs `python manage.py migrate`
2. Collects static files
3. Runs `python auto_setup.py` (creates admin & departments)
4. Starts Gunicorn server

## Manual Setup (if needed)

If you need to run setup manually:

```bash
python auto_setup.py
```

Or individual scripts:

```bash
python setup_admin.py
python setup_departments.py
```

## Checking Setup Status

After deployment, check the logs in Zeabur dashboard to see:
- Migration status
- Admin user creation
- Department setup
- SLA configuration

## Troubleshooting

If setup fails:
1. Check Zeabur logs for error messages
2. Verify environment variables are set correctly
3. Ensure database is accessible
4. Try running `python auto_setup.py` manually in Zeabur console

## Security Note

**Important:** Change the default admin password after first login!

You can do this by:
1. Login to Django admin
2. Go to Users
3. Click on admin user
4. Change password
