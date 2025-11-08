# Deployment Guide for Zeabur

## Prerequisites
- GitHub repository connected to Zeabur
- Zeabur account

## Environment Variables to Set in Zeabur

Go to your Zeabur project settings and add these environment variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.zeabur.app
CSRF_TRUSTED_ORIGINS=https://your-app-name.zeabur.app
BREVO_API_KEY=your-brevo-api-key
PORT=8080
```

## Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Connect to Zeabur**
   - Go to Zeabur dashboard
   - Create new project
   - Connect your GitHub repository
   - Zeabur will automatically detect the Dockerfile

3. **Set Environment Variables**
   - In Zeabur project settings, add all the environment variables listed above
   - Replace `your-app-name` with your actual Zeabur app URL

4. **Deploy**
   - Zeabur will automatically build and deploy using the Dockerfile
   - Wait for the build to complete

5. **Run Migrations** (First time only)
   - Access Zeabur console/terminal
   - Run: `python manage.py migrate`
   - Run: `python manage.py createsuperuser`
   - Or use the setup scripts:
     ```bash
     python setup_admin.py
     python setup_departments.py
     ```

## Post-Deployment

### Create Admin User
```bash
python manage.py createsuperuser
```

### Setup Departments and SLA
```bash
python setup_departments.py
```

## Troubleshooting

### Static Files Not Loading
Make sure `collectstatic` runs during build (it's in the Dockerfile)

### Database Issues
Zeabur uses SQLite by default. For production, consider using PostgreSQL:
1. Add PostgreSQL service in Zeabur
2. Update DATABASE_URL environment variable
3. Install psycopg2 in requirements.txt

### CSRF Errors
Make sure CSRF_TRUSTED_ORIGINS includes your Zeabur domain with https://

## Monitoring

Check logs in Zeabur dashboard:
- Build logs for deployment issues
- Runtime logs for application errors

## Updating

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Zeabur will automatically rebuild and redeploy.
