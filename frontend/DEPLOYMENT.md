# Deployment Guide

## Overview

This guide covers deploying the ITSM Frontend application to production and staging environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Deployment](#local-deployment)
4. [Docker Deployment](#docker-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Production Deployment](#production-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools
- Node.js 18+ or 20+
- npm 9+
- Docker & Docker Compose (for containerized deployment)
- Git

### Required Accounts
- GitHub (for CI/CD)
- Netlify (for hosting)
- Sentry (for error tracking)
- Datadog or similar (for monitoring)

### Environment Variables
- `NETLIFY_AUTH_TOKEN` - Netlify authentication token
- `NETLIFY_SITE_ID_PROD` - Production site ID
- `NETLIFY_SITE_ID_STAGING` - Staging site ID
- `GITHUB_TOKEN` - GitHub token for actions

---

## Environment Setup

### 1. Create Environment Files

```bash
# Production
cp .env.example .env.production
# Update with production values

# Staging
cp .env.example .env.staging
# Update with staging values

# Development
cp .env.example .env.development
# Update with development values
```

### 2. Environment Variables

**Production (.env.production)**
```
VITE_API_BASE_URL=https://api.itsm.example.com/api/v1
VITE_WEBSOCKET_URL=wss://api.itsm.example.com/ws
VITE_ENVIRONMENT=production
VITE_LOG_LEVEL=ERROR
```

**Staging (.env.staging)**
```
VITE_API_BASE_URL=https://staging-api.itsm.example.com/api/v1
VITE_WEBSOCKET_URL=wss://staging-api.itsm.example.com/ws
VITE_ENVIRONMENT=staging
VITE_LOG_LEVEL=INFO
```

---

## Local Deployment

### Development Server

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Server runs at http://localhost:5173
```

### Production Build

```bash
# Build for production
npm run build:prod

# Preview production build
npm run preview

# Build for staging
npm run build:staging
```

### Build Output

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── vendor-[hash].js
└── manifest.json
```

---

## Docker Deployment

### Build Docker Image

```bash
# Build image
docker build -t itsm-frontend:latest .

# Build with specific tag
docker build -t itsm-frontend:1.0.0 .
```

### Run Docker Container

```bash
# Run container
docker run -p 3000:80 itsm-frontend:latest

# Run with environment variables
docker run -p 3000:80 \
  -e VITE_API_BASE_URL=https://api.example.com/api/v1 \
  itsm-frontend:latest

# Run in background
docker run -d -p 3000:80 --name itsm-frontend itsm-frontend:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache
```

### Docker Health Check

```bash
# Check container health
docker ps

# Manual health check
curl http://localhost:3000/health
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

The `.github/workflows/deploy.yml` file defines the CI/CD pipeline:

1. **Checkout Code** - Clone repository
2. **Setup Node** - Install Node.js
3. **Install Dependencies** - Run `npm ci`
4. **Lint Code** - Run ESLint
5. **Run Tests** - Run Jest with coverage
6. **Upload Coverage** - Send to Codecov
7. **Build** - Build for staging or production
8. **Deploy** - Deploy to Netlify
9. **Lighthouse CI** - Run performance tests

### Trigger Deployment

```bash
# Push to staging branch
git push origin staging
# Automatically deploys to staging

# Push to main branch
git push origin main
# Automatically deploys to production
```

### View Deployment Status

```bash
# GitHub Actions
https://github.com/your-org/SNowProject/actions

# Netlify Deployments
https://app.netlify.com/sites/your-site/deploys
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] API endpoints verified
- [ ] SSL certificates valid
- [ ] Backups created
- [ ] Monitoring configured

### Deployment Steps

1. **Merge to Main Branch**
   ```bash
   git checkout main
   git pull origin main
   git merge staging
   git push origin main
   ```

2. **Monitor Deployment**
   - Watch GitHub Actions workflow
   - Check Netlify deployment status
   - Verify health checks passing

3. **Post-Deployment Verification**
   ```bash
   # Check application health
   curl https://itsm.example.com/health

   # Check API connectivity
   curl https://itsm.example.com/api/v1/health

   # Check performance metrics
   # Visit Lighthouse dashboard
   ```

4. **Smoke Tests**
   - Login to application
   - Navigate to dashboard
   - Check incident list
   - Verify notifications
   - Test API calls

### Rollback Procedure

```bash
# If deployment fails, rollback
git revert HEAD
git push origin main

# Or redeploy previous version
git checkout <previous-commit>
git push origin main --force

# Monitor rollback in Netlify
```

---

## Monitoring & Maintenance

### Performance Monitoring

```bash
# Lighthouse CI
npm run lighthouse

# View results
# https://your-lighthouse-dashboard.com
```

### Error Tracking

- **Sentry Integration**
  - Errors automatically reported
  - View at https://sentry.io/organizations/your-org
  - Configure alerts for critical errors

### Application Monitoring

- **Uptime Monitoring**
  - Health check: `/health`
  - Monitored every 5 minutes
  - Alerts on failure

- **Performance Metrics**
  - Page load time
  - API response time
  - Error rate
  - User sessions

### Log Management

```bash
# View application logs
docker logs itsm-frontend

# View nginx logs
docker exec itsm-frontend tail -f /var/log/nginx/access.log

# View error logs
docker exec itsm-frontend tail -f /var/log/nginx/error.log
```

### Database Backups

```bash
# Backup database
docker-compose exec db pg_dump -U user itsm > backup.sql

# Restore from backup
docker-compose exec -T db psql -U user itsm < backup.sql
```

---

## Troubleshooting

### Common Issues

#### 1. Build Fails

```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm ci
npm run build:prod
```

#### 2. Container Won't Start

```bash
# Check logs
docker logs itsm-frontend

# Rebuild image
docker build --no-cache -t itsm-frontend:latest .

# Check port availability
lsof -i :3000
```

#### 3. API Connection Issues

```bash
# Verify API URL
echo $VITE_API_BASE_URL

# Test API connectivity
curl $VITE_API_BASE_URL/health

# Check CORS headers
curl -i https://api.example.com/api/v1/health
```

#### 4. Performance Issues

```bash
# Run Lighthouse
npm run lighthouse

# Check bundle size
npm run build:prod
du -sh dist/

# Analyze bundle
npm run analyze
```

#### 5. Deployment Stuck

```bash
# Cancel current deployment
# Via GitHub Actions UI or:
gh run cancel <run-id>

# Retry deployment
git push origin main --force
```

---

## Maintenance Tasks

### Weekly
- [ ] Review error logs
- [ ] Check performance metrics
- [ ] Verify backups completed
- [ ] Monitor disk usage

### Monthly
- [ ] Update dependencies
- [ ] Review security updates
- [ ] Audit access logs
- [ ] Performance review

### Quarterly
- [ ] Security audit
- [ ] Disaster recovery test
- [ ] Capacity planning
- [ ] Documentation review

---

## Support & Resources

### Documentation
- [Vite Documentation](https://vitejs.dev)
- [React Documentation](https://react.dev)
- [Netlify Documentation](https://docs.netlify.com)
- [Docker Documentation](https://docs.docker.com)

### Monitoring Tools
- [Sentry](https://sentry.io)
- [Datadog](https://www.datadoghq.com)
- [New Relic](https://newrelic.com)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

### Support Contacts
- DevOps Team: devops@example.com
- Security Team: security@example.com
- Performance Team: performance@example.com

---

**Last Updated:** 2026-07-10
**Version:** 1.0.0
**Status:** Production Ready
