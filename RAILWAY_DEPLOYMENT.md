# Deploying Esports Tournament Platform to Railway

Railway is a modern, simple deployment platform perfect for Django applications. This guide will walk you through the deployment process.

---

## Why Railway?

✅ **Easy Setup**: Deploy in minutes  
✅ **Free Tier**: $5 free credit per month  
✅ **PostgreSQL Included**: One-click database setup  
✅ **Auto HTTPS**: Automatic SSL certificates  
✅ **Git Integration**: Auto-deploy on push  
✅ **Environment Variables**: Easy configuration  

---

## Prerequisites

1. **Railway Account**: Sign up at [https://railway.app](https://railway.app)
2. **GitHub Account**: (Optional but recommended)
3. **Git Installed**: For version control

---

## Step 1: Push Your Code to GitHub (Recommended)

### Create a New Repository:

```powershell
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Railway deployment"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/esports-platform.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Railway Project

### Option A: Using Railway Dashboard (Easiest)

1. **Go to**: [https://railway.app/new](https://railway.app/new)
2. **Click**: "Deploy from GitHub repo"
3. **Select**: Your `esports-platform` repository
4. Railway will automatically detect it's a Django app

### Option B: Using Railway CLI

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project (from your project directory)
railway init

# Link to new project
railway link
```

---

## Step 3: Add PostgreSQL Database

1. **In Railway Dashboard**:
   - Click **"+ New"** button
   - Select **"Database"** → **"PostgreSQL"**
   - Database will be created and linked automatically

2. **Get Database URL**:
   - Railway automatically sets `DATABASE_URL` environment variable
   - Your Django app will use it automatically (already configured in settings.py)

---

## Step 4: Configure Environment Variables

In Railway Dashboard → **Variables** tab, add:

```env
SECRET_KEY=qu3$)tem=s5%9a8#cidax)=x_lizb0-(nauq^8y%1mi2wlpy1o
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
DJANGO_SETTINGS_MODULE=esports_platform.settings
```

**Important**: 
- `DATABASE_URL` is automatically set by Railway when you add PostgreSQL
- Replace the `SECRET_KEY` with your generated one from `.env` file
- Update `CORS_ALLOWED_ORIGINS` with your actual frontend domain

---

## Step 5: Deploy!

### If using GitHub:
- Railway auto-deploys on every push
- First deployment starts automatically

### If using Railway CLI:
```powershell
railway up
```

### Monitor Deployment:
```powershell
# View logs
railway logs

# Check status
railway status
```

---

## Step 6: Run Database Migrations

After first deployment, run migrations:

```powershell
# Using Railway CLI
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

Or in Railway Dashboard:
- Go to your service
- Click **"Settings"** → **"Deploy"** 
- Under "Deploy Command", temporarily set: `python manage.py migrate && gunicorn esports_platform.wsgi`

---

## Step 7: Access Your Application

Your app will be available at:
```
https://your-app-name.up.railway.app
```

**Test endpoints**:
- API Root: `https://your-app.up.railway.app/api/`
- Swagger Docs: `https://your-app.up.railway.app/api/docs/`
- Admin Panel: `https://your-app.up.railway.app/admin/`

---

## Step 8: Custom Domain (Optional)

1. **In Railway Dashboard**:
   - Go to **Settings** → **Domains**
   - Click **"Generate Domain"** (free Railway subdomain)
   - Or **"Custom Domain"** (your own domain)

2. **Update Environment Variables**:
   ```env
   ALLOWED_HOSTS=.railway.app,yourdomain.com,www.yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

---

## Environment Variables Reference

### Required Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `.railway.app,yourdomain.com` |
| `DATABASE_URL` | PostgreSQL connection | *Auto-set by Railway* |

### Optional Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ALLOWED_ORIGINS` | Frontend domains | `https://frontend.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins | `https://app.railway.app` |

---

## Railway CLI Commands

```powershell
# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell

# Open in browser
railway open

# Get database URL
railway variables

# Deploy
railway up

# Check status
railway status
```

---

## Updating Your Application

### With GitHub:
```powershell
git add .
git commit -m "Update description"
git push
```
Railway auto-deploys! 🚀

### With Railway CLI:
```powershell
railway up
```

---

## Database Management

### Access PostgreSQL Database:

```powershell
# Get database credentials
railway variables

# Connect using Railway CLI
railway connect postgres
```

### Backup Database:

```powershell
# Export data
railway run python manage.py dumpdata > backup.json

# Import data
railway run python manage.py loaddata backup.json
```

---

## Troubleshooting

### Issue: Application Won't Start

**Check logs:**
```powershell
railway logs
```

**Common fixes:**
- Ensure `Procfile` exists and is correct
- Check `requirements.txt` has all dependencies
- Verify `ALLOWED_HOSTS` includes `.railway.app`

### Issue: Static Files Not Loading

Railway handles static files via WhiteNoise (already configured in settings.py).

**Verify:**
```powershell
railway run python manage.py collectstatic --noinput
```

### Issue: Database Connection Error

**Check if PostgreSQL is added:**
```powershell
railway variables | Select-String "DATABASE_URL"
```

**Manually run migrations:**
```powershell
railway run python manage.py migrate
```

### Issue: CORS Errors

Update environment variables:
```env
CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

Then redeploy or restart service.

---

## Monitoring & Logs

### View Logs:
```powershell
# Live logs
railway logs

# Follow logs (continuous)
railway logs -f
```

### Monitor Resources:
- Go to Railway Dashboard
- View **Metrics** tab for CPU, Memory, Network usage

---

## Scaling Your Application

Railway offers:
- **Vertical Scaling**: Increase CPU/RAM in Settings
- **Horizontal Scaling**: Add more instances (Paid tier)

---

## Pricing

**Starter Plan (Free Tier)**:
- $5 free credits/month
- ~500 hours runtime
- Perfect for development/testing

**Developer Plan** ($5/month):
- $5 credit + pay-as-you-go
- Custom domains
- Team collaboration

Check current pricing: [https://railway.app/pricing](https://railway.app/pricing)

---

## Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` set
- [x] HTTPS enabled (automatic on Railway)
- [x] `ALLOWED_HOSTS` configured
- [x] CORS origins restricted
- [x] Database using PostgreSQL (not SQLite)
- [x] Environment variables secured
- [ ] Regular security updates
- [ ] Monitor access logs

---

## Complete Deployment Workflow

```powershell
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Create Railway project (done via dashboard)

# 3. Add PostgreSQL database (done via dashboard)

# 4. Set environment variables (done via dashboard)

# 5. Run migrations
railway run python manage.py migrate

# 6. Create superuser
railway run python manage.py createsuperuser

# 7. Access your app
railway open
```

---

## Alternative: Deploy Without GitHub

If you don't want to use GitHub:

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up

# Add PostgreSQL
# (Do this in Railway Dashboard)

# Set environment variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS=".railway.app"

# Run migrations
railway run python manage.py migrate
```

---

## Next Steps After Deployment

1. **Test all API endpoints** in Swagger: `https://your-app.railway.app/api/docs/`
2. **Create test data** using the admin panel or API
3. **Set up monitoring** (Railway provides basic metrics)
4. **Configure backups** for your database
5. **Add custom domain** if needed
6. **Set up CI/CD** for automated testing before deployment

---

## Support & Resources

- **Railway Docs**: [https://docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [https://discord.gg/railway](https://discord.gg/railway)
- **Railway Status**: [https://status.railway.app](https://status.railway.app)
- **Django Deployment**: [https://docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│     Railway Quick Commands              │
├─────────────────────────────────────────┤
│ railway login          - Login to Railway│
│ railway init           - Create project  │
│ railway link           - Link project    │
│ railway up             - Deploy app      │
│ railway logs           - View logs       │
│ railway open           - Open in browser │
│ railway run <cmd>      - Run command     │
│ railway variables      - List env vars   │
│ railway status         - Check status    │
└─────────────────────────────────────────┘
```

---

**🚀 You're ready to deploy to Railway!**

Your Django app is now configured and ready. Simply push to GitHub or use Railway CLI to deploy.

**Good luck! 🎮🏆**
