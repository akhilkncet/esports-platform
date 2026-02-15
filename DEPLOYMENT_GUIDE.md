# Deploying Esports Tournament Platform to Zoho Catalyst

This guide will walk you through deploying your Django backend to Zoho Catalyst.

---

## Prerequisites

Before you begin, ensure you have:

1. **Zoho Catalyst Account**: Sign up at [https://catalyst.zoho.com](https://catalyst.zoho.com)
2. **Zoho Catalyst CLI**: Install the CLI tool
3. **Python 3.11+** installed locally
4. **Git** installed (for version control)

---

## Step 1: Install Zoho Catalyst CLI

### For Windows:
```powershell
npm install -g zcatalyst-cli
```

### For Mac/Linux:
```bash
npm install -g zcatalyst-cli
```

### Verify Installation:
```bash
catalyst --version
```

---

## Step 2: Initialize Catalyst Project

1. **Login to Catalyst CLI:**
```bash
catalyst login
```

2. **Initialize your project:**
```bash
cd esports_platform
catalyst init
```

Follow the prompts:
- **Project Type**: Select "Python"
- **Framework**: Select "Django"
- **Project Name**: `esports-tournament-platform`

---

## Step 3: Set Up Database (Catalyst DataStore)

Catalyst supports PostgreSQL through its DataStore service.

### Option 1: Using Catalyst Console (Recommended)

1. Go to [Catalyst Console](https://console.catalyst.zoho.com)
2. Navigate to **Data Store** → **Tables**
3. Create a new PostgreSQL instance
4. Note down the connection details:
   - Host
   - Port
   - Database name
   - Username
   - Password

### Option 2: Using CLI

```bash
catalyst datastore:create --type postgresql
```

---

## Step 4: Configure Environment Variables

1. **Create a `.env` file** in your project root (copy from `.env.example`):

```bash
cp .env.example .env
```

2. **Edit `.env` file** with your production values:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=.catalyst.zoho.com,yourdomain.com

# Database Configuration (from Step 3)
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://yourfrontend.com
```

3. **Add environment variables to Catalyst:**

```bash
catalyst config:set SECRET_KEY="your-secret-key"
catalyst config:set DEBUG="False"
catalyst config:set DATABASE_URL="postgresql://user:pass@host:port/db"
catalyst config:set ALLOWED_HOSTS=".catalyst.zoho.com"
catalyst config:set CORS_ALLOWED_ORIGINS="https://yourfrontend.com"
catalyst config:set CSRF_TRUSTED_ORIGINS="https://yourfrontend.com"
```

**Generate a secure SECRET_KEY:**
```python
# Run this in Python shell locally
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Step 5: Prepare for Deployment

1. **Install production dependencies locally (for testing):**

```bash
pip install -r requirements.txt
```

2. **Run migrations locally to verify:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

3. **Create `.gitignore` if not exists:**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
```

---

## Step 6: Deploy to Catalyst

### Method 1: Using Catalyst CLI (Recommended)

1. **Deploy the application:**

```bash
catalyst deploy
```

2. **Follow the deployment wizard:**
   - Confirm project details
   - Select Python runtime version (3.11)
   - Confirm deployment

3. **Wait for deployment to complete** (5-10 minutes)

### Method 2: Using Git Push

```bash
git add .
git commit -m "Initial deployment"
catalyst push
```

---

## Step 7: Run Database Migrations

After deployment, run migrations on the production database:

```bash
catalyst run python manage.py migrate
```

Or access the Catalyst console and run migrations from there.

---

## Step 8: Create Superuser (Admin Account)

Create an admin user for Django admin panel:

```bash
catalyst run python manage.py createsuperuser
```

Follow the prompts to create your admin account.

---

## Step 9: Verify Deployment

1. **Get your application URL:**
```bash
catalyst status
```

Your app will be available at: `https://your-app-name.catalyst.zoho.com`

2. **Test API endpoints:**
   - **API Root**: `https://your-app.catalyst.zoho.com/api/`
   - **Swagger Docs**: `https://your-app.catalyst.zoho.com/api/docs/`
   - **Admin Panel**: `https://your-app.catalyst.zoho.com/admin/`

3. **Check application logs:**
```bash
catalyst logs
```

---

## Step 10: Domain Configuration (Optional)

### Add Custom Domain

1. Go to **Catalyst Console** → **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` in your environment variables:

```bash
catalyst config:set ALLOWED_HOSTS=".catalyst.zoho.com,yourdomain.com,www.yourdomain.com"
```

---

## Post-Deployment Tasks

### 1. Load Initial Data (Optional)

If you have initial data to load:

```bash
# Upload your data file first
catalyst run python manage.py loaddata initial_data.json
```

### 2. Set Up Monitoring

1. Go to **Catalyst Console** → **Monitoring**
2. Set up alerts for:
   - High error rates
   - Slow response times
   - Resource usage

### 3. Configure Backups

1. Go to **DataStore** → **Backups**
2. Enable automatic daily backups
3. Set retention policy

---

## Updating Your Application

When you make changes to your code:

1. **Test locally first:**
```bash
python manage.py test
```

2. **Commit your changes:**
```bash
git add .
git commit -m "Description of changes"
```

3. **Deploy the update:**
```bash
catalyst deploy
```

4. **Run migrations if needed:**
```bash
catalyst run python manage.py migrate
```

---

## Troubleshooting

### Issue: Application Won't Start

**Check logs:**
```bash
catalyst logs --tail
```

**Common causes:**
- Missing environment variables
- Database connection issues
- Syntax errors in code

### Issue: Static Files Not Loading

**Collect static files:**
```bash
catalyst run python manage.py collectstatic --noinput
```

### Issue: Database Connection Failed

**Verify DATABASE_URL:**
```bash
catalyst config:list
```

**Test connection:**
```bash
catalyst run python manage.py check --database default
```

### Issue: CORS Errors

Update CORS settings:
```bash
catalyst config:set CORS_ALLOWED_ORIGINS="https://frontend1.com,https://frontend2.com"
```

Then redeploy.

---

## Performance Optimization

### 1. Enable Caching

Add to your `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
```

Create cache table:
```bash
catalyst run python manage.py createcachetable
```

### 2. Database Query Optimization

- Use `select_related()` and `prefetch_related()` for foreign keys
- Add database indexes to frequently queried fields
- Monitor slow queries in Catalyst console

### 3. Enable Gzip Compression

Already configured via WhiteNoise in your settings.

---

## Security Checklist

- [x] `DEBUG = False` in production
- [x] Strong `SECRET_KEY` set
- [x] HTTPS enabled (automatic on Catalyst)
- [x] `ALLOWED_HOSTS` configured
- [x] CORS origins restricted
- [x] CSRF protection enabled
- [x] Secure cookies configured
- [x] SQL injection protection (Django ORM)
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Set up rate limiting (optional)

---

## Alternative Deployment Options

If Zoho Catalyst doesn't work for you, consider:

1. **Heroku** - Easy Django deployment with PostgreSQL
2. **Railway** - Modern platform with free tier
3. **DigitalOcean App Platform** - Simple deployment
4. **PythonAnywhere** - Django-specific hosting
5. **AWS Elastic Beanstalk** - Scalable AWS solution
6. **Google Cloud Run** - Serverless containers
7. **Azure App Service** - Microsoft's PaaS

---

## Support & Resources

- **Zoho Catalyst Documentation**: [https://docs.catalyst.zoho.com](https://docs.catalyst.zoho.com)
- **Django Deployment Checklist**: [https://docs.djangoproject.com/en/stable/howto/deployment/checklist/](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- **Catalyst Community**: [https://community.catalyst.zoho.com](https://community.catalyst.zoho.com)

---

## Quick Command Reference

```bash
# Login
catalyst login

# Deploy
catalyst deploy

# View logs
catalyst logs --tail

# Run management commands
catalyst run python manage.py <command>

# Set environment variable
catalyst config:set KEY="value"

# List environment variables
catalyst config:list

# Check status
catalyst status

# Scale application
catalyst scale --instances 3

# Roll back to previous version
catalyst rollback
```

---

## Costs

Zoho Catalyst offers:
- **Free Tier**: 
  - 1 GB RAM
  - 1 GB Storage
  - 10 GB Bandwidth/month
  
- **Paid Plans**: Start at $10/month for more resources

Check current pricing at: [https://www.zoho.com/catalyst/pricing.html](https://www.zoho.com/catalyst/pricing.html)

---

## Need Help?

If you encounter issues during deployment:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review Catalyst logs: `catalyst logs`
3. Consult Zoho Catalyst documentation
4. Contact Zoho support

---

**Good luck with your deployment! 🚀**
