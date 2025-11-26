# 🚀 Quick Deployment Reference Card

## Choose Your Platform

### 🟢 Vercel (Recommended for Beginners)
**Best for:** Quick deployments, automatic SSL, preview deployments

```bash
# One-time setup
npm install -g vercel
vercel login

# Deploy
vercel                    # Preview
vercel --prod            # Production
```

**CI/CD Setup:**
1. Run `vercel link` to get IDs
2. Add to GitHub Secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
3. Workflow: `.github/workflows/deploy-vercel.yml`

---

### 🔵 GitHub Pages (Free Forever)
**Best for:** Personal projects, open source, free hosting

```bash
# One-time setup
npm install -D gh-pages

# Update vite.config.js
base: '/snake-game-claude/',  # Your repo name

# Deploy
npm run build
npx gh-pages -d dist
```

**CI/CD Setup:**
1. Settings > Pages > Source: "GitHub Actions"
2. Update `vite.config.js`:
   ```js
   base: process.env.GITHUB_ACTIONS ? '/repo-name/' : '/'
   ```
3. Workflow: `.github/workflows/deploy-github-pages.yml`
4. Push to `main`

---

### 🟠 AWS S3 + CloudFront (Professional)
**Best for:** Enterprise, custom domains, full control

```bash
# One-time setup
aws configure

# Create bucket
aws s3 mb s3://snake-game-yourname

# Deploy
npm run build
aws s3 sync dist/ s3://snake-game-yourname --delete
```

**CI/CD Setup:**
1. Create IAM user for deployments
2. Add to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
3. Update workflow environment variables:
   - `S3_BUCKET`
   - `CLOUDFRONT_DISTRIBUTION_ID`
4. Workflow: `.github/workflows/deploy-aws.yml`

---

## Comparison At-a-Glance

| Feature | Vercel | GitHub Pages | AWS S3 |
|---------|--------|--------------|--------|
| 💰 Cost | Free tier | Free | ~$1-5/mo |
| ⚡ Speed | ★★★★★ | ★★★★☆ | ★★★★★ |
| 🔧 Setup | ★★★★★ | ★★★★☆ | ★★☆☆☆ |
| 🌍 CDN | ✅ Global | ✅ GitHub | ✅ CloudFront |
| 🔐 SSL | ✅ Auto | ✅ Auto | Configure |
| 👀 Preview | ✅ Yes | ❌ No | ❌ No |

---

## Common Commands

### Build & Test
```bash
npm test              # Run tests
npm test -- --run    # Run tests once (CI)
npm run build        # Build for production
npm run preview      # Preview build locally
```

### Quick Checks
```bash
# Check if build works
npm run build && ls -lh dist/

# Test build locally
npm run build && npm run preview

# Verify tests pass
npm test -- --run
```

---

## Troubleshooting

### Build Fails
```bash
# Clear cache and rebuild
rm -rf node_modules dist .vite
npm install
npm run build
```

### GitHub Pages 404
```bash
# Check base path in vite.config.js
base: '/your-exact-repo-name/'  # Must match!
```

### AWS Permission Denied
```bash
# Verify bucket policy allows public read
aws s3api get-bucket-policy --bucket your-bucket
```

### Workflow Not Running
- ✅ Pushed to `main` branch?
- ✅ Workflow file in `.github/workflows/`?
- ✅ Actions enabled in Settings?

---

## Emergency Rollback

### Vercel
```bash
vercel list              # See deployments
vercel rollback          # Roll back to previous
```

### GitHub Pages
```bash
# Revert last commit
git revert HEAD
git push
```

### AWS S3
```bash
# Enable versioning first!
aws s3api put-bucket-versioning \
  --bucket your-bucket \
  --versioning-configuration Status=Enabled
```

---

## Need Help?

📖 **Full Guide:** See [DEPLOYMENT.md](./DEPLOYMENT.md)
🔧 **Workflows:** See [.github/workflows/README.md](./.github/workflows/README.md)
🐛 **Issues:** Check GitHub Actions logs in "Actions" tab

---

## Pro Tips

1. **Test locally first**: Always run `npm run build` before deploying
2. **Start with Vercel**: Easiest to get started, can migrate later
3. **Use staging**: Deploy to staging URL before production
4. **Monitor performance**: Use Lighthouse to check load times
5. **Set up alerts**: Get notified when deployments fail

---

## Security Checklist

- [ ] Never commit API keys or secrets
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (all platforms support it)
- [ ] Set proper CORS headers if needed
- [ ] Review IAM permissions (AWS)
- [ ] Enable 2FA on deployment accounts

---

## Quick Links

- [Vercel Dashboard](https://vercel.com/dashboard)
- [GitHub Actions](https://github.com/USERNAME/REPO/actions)
- [AWS S3 Console](https://s3.console.aws.amazon.com/)
- [CloudFront Console](https://console.aws.amazon.com/cloudfront/)

---

**Last Updated:** 2025-11-26
**Version:** 1.0.0
