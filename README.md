# ZIMAYBLOG - Deployment Guide

## Render Deployment

This Django project is configured for deployment on Render.

### Prerequisites
- A Render account
- Git repository pushed to GitHub/GitLab/Bitbucket

### Deployment Steps

1. **Connect Repository**: In Render dashboard, connect your Git repository containing this project.

2. **Create Web Service**: 
   - Choose "Web Service" from the service type
   - Select your repository
   - The `render.yaml` file will automatically configure the service

3. **Environment Variables**: Set the following environment variables in Render:
   - `SECRET_KEY`: Generate a secure secret key (50+ characters)
   - `DATABASE_URL`: Will be automatically set by Render's PostgreSQL service
   - `DEBUG`: Set to `False` (already configured)
   - `ALLOWED_HOSTS`: Set to `*.onrender.com` (already configured)

4. **Database Setup**: 
   - Render will automatically create a PostgreSQL database
   - The app will run migrations automatically on first deploy

5. **Deploy**: Click "Create Web Service" to deploy

### Post-Deployment
- The app will be available at `https://your-app-name.onrender.com`
- Static files are served via WhiteNoise
- SSL is automatically configured

### Local Development
```bash
cd zimayblog
python manage.py runserver
```

### Production Checks
- All Django security checks pass
- Static files are properly collected
- Database migrations are applied
- HTTPS enforced