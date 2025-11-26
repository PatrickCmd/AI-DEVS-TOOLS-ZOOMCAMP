# Deployment Guide

This guide covers deploying the Snake Game to three popular platforms: Vercel, GitHub Pages, and AWS S3/CloudFront. Each section includes both manual deployment steps and automated CI/CD setup using GitHub Actions.

## Table of Contents
- [Vercel](#vercel)
- [GitHub Pages](#github-pages)
- [AWS S3/CloudFront](#aws-s3cloudfront)

---

## Vercel

Vercel is the easiest platform for deploying Vite applications with zero configuration.

### Manual Deployment

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Build the project**:
   ```bash
   npm run build
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

   Follow the prompts to link your project and deploy.

4. **Production deployment**:
   ```bash
   vercel --prod
   ```

### GitHub Actions CI/CD

Create `.github/workflows/deploy-vercel.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --run

      - name: Build project
        run: npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

**Setup Secrets**:
1. Get your Vercel token from https://vercel.com/account/tokens
2. Get your Org ID and Project ID by running `vercel link` locally
3. Add these as GitHub repository secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`

---

## GitHub Pages

GitHub Pages is free and perfect for hosting static sites directly from your repository.

### Manual Deployment

1. **Update `vite.config.js`** to set the correct base path:
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig({
     plugins: [react()],
     base: '/snake-game-claude/', // Replace with your repo name
     test: {
       globals: true,
       environment: 'jsdom',
       setupFiles: './src/test/setup.js',
       css: true,
     },
   })
   ```

2. **Build the project**:
   ```bash
   npm run build
   ```

3. **Deploy using gh-pages**:
   ```bash
   npm install -D gh-pages
   npx gh-pages -d dist
   ```

4. **Enable GitHub Pages**:
   - Go to your repository Settings > Pages
   - Select "gh-pages" branch as source
   - Save

### GitHub Actions CI/CD

Create `.github/workflows/deploy-github-pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --run

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Enable GitHub Pages**:
1. Go to Settings > Pages
2. Select "GitHub Actions" as the source
3. The workflow will automatically deploy on push to main

**Update vite.config.js** for correct base path:
```javascript
base: process.env.GITHUB_ACTIONS ? '/snake-game-claude/' : '/',
```

---

## AWS S3/CloudFront

AWS S3 with CloudFront provides a scalable, high-performance hosting solution with CDN distribution.

### Prerequisites

1. **AWS Account**: Create one at https://aws.amazon.com
2. **AWS CLI**: Install from https://aws.amazon.com/cli/
3. **Configure AWS CLI**:
   ```bash
   aws configure
   ```
   Enter your Access Key ID, Secret Access Key, region, and output format.

### Manual Deployment

1. **Create S3 Bucket**:
   ```bash
   aws s3 mb s3://snake-game-yourname --region us-east-1
   ```

2. **Enable static website hosting**:
   ```bash
   aws s3 website s3://snake-game-yourname \
     --index-document index.html \
     --error-document index.html
   ```

3. **Set bucket policy for public access**:

   Create `bucket-policy.json`:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::snake-game-yourname/*"
       }
     ]
   }
   ```

   Apply policy:
   ```bash
   aws s3api put-bucket-policy \
     --bucket snake-game-yourname \
     --policy file://bucket-policy.json
   ```

4. **Build and upload**:
   ```bash
   npm run build
   aws s3 sync dist/ s3://snake-game-yourname --delete
   ```

5. **Create CloudFront Distribution** (Optional but recommended):
   ```bash
   aws cloudfront create-distribution \
     --origin-domain-name snake-game-yourname.s3-website-us-east-1.amazonaws.com \
     --default-root-object index.html
   ```

### GitHub Actions CI/CD

Create `.github/workflows/deploy-aws.yml`:

```yaml
name: Deploy to AWS S3/CloudFront

on:
  push:
    branches:
      - main

env:
  AWS_REGION: us-east-1
  S3_BUCKET: snake-game-yourname
  CLOUDFRONT_DISTRIBUTION_ID: YOUR_DISTRIBUTION_ID

jobs:
  deploy:
    runs-on: ubuntu-latest

    permissions:
      id-token: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --run

      - name: Build project
        run: npm run build

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Sync to S3
        run: |
          aws s3 sync dist/ s3://${{ env.S3_BUCKET }} \
            --delete \
            --cache-control "public, max-age=31536000, immutable" \
            --exclude "index.html" \
            --exclude "*.map"

          # Upload index.html with no-cache
          aws s3 cp dist/index.html s3://${{ env.S3_BUCKET }}/ \
            --cache-control "public, max-age=0, must-revalidate"

      - name: Invalidate CloudFront cache
        if: env.CLOUDFRONT_DISTRIBUTION_ID != ''
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ env.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"

      - name: Deployment successful
        run: |
          echo "✅ Deployed to S3: http://${{ env.S3_BUCKET }}.s3-website-${{ env.AWS_REGION }}.amazonaws.com"
```

**Setup GitHub Secrets**:
1. Go to repository Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
3. Update the environment variables in the workflow:
   - `S3_BUCKET`: Your S3 bucket name
   - `CLOUDFRONT_DISTRIBUTION_ID`: Your CloudFront distribution ID (optional)

**Create IAM User for GitHub Actions**:
1. Go to AWS IAM Console
2. Create a new user: `github-actions-deploy`
3. Attach policy with these permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:PutObject",
           "s3:GetObject",
           "s3:ListBucket",
           "s3:DeleteObject"
         ],
         "Resource": [
           "arn:aws:s3:::snake-game-yourname",
           "arn:aws:s3:::snake-game-yourname/*"
         ]
       },
       {
         "Effect": "Allow",
         "Action": [
           "cloudfront:CreateInvalidation"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

---

## Comparison Table

| Feature | Vercel | GitHub Pages | AWS S3/CloudFront |
|---------|--------|--------------|-------------------|
| **Cost** | Free tier available | Free | Pay as you go (~$1-5/month) |
| **Setup Complexity** | Very Easy | Easy | Moderate |
| **Build Time** | Fast | Medium | Medium |
| **Custom Domain** | ✅ Free SSL | ✅ Free (with limitations) | ✅ (DNS config required) |
| **CDN** | ✅ Global | ✅ GitHub CDN | ✅ CloudFront |
| **Auto Deployments** | ✅ | ✅ | ✅ (with Actions) |
| **Preview Deployments** | ✅ | ❌ | ❌ |
| **Rollback** | ✅ Easy | Manual | Manual |
| **Analytics** | ✅ Built-in | ❌ | With CloudWatch |

---

## Tips & Best Practices

### Performance Optimization

1. **Enable compression** in your deployment:
   ```bash
   # For S3
   aws s3 sync dist/ s3://your-bucket --content-encoding gzip
   ```

2. **Set proper cache headers**:
   - HTML files: `no-cache` or `max-age=0`
   - JS/CSS/Assets: `max-age=31536000` (1 year)

3. **Use environment variables** for different environments:
   ```javascript
   // vite.config.js
   export default defineConfig({
     define: {
       'import.meta.env.VITE_API_URL': JSON.stringify(
         process.env.VITE_API_URL || 'https://api.example.com'
       )
     }
   })
   ```

### Security

1. **Never commit AWS credentials** to your repository
2. **Use IAM roles** with minimal required permissions
3. **Enable HTTPS** on all platforms
4. **Set up security headers**:
   ```nginx
   # For S3/CloudFront, use Lambda@Edge or CloudFront Functions
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
   ```

### Monitoring

1. **Set up uptime monitoring**: Use services like UptimeRobot or Pingdom
2. **Enable error tracking**: Integrate Sentry or similar service
3. **Monitor performance**: Use Lighthouse CI in your GitHub Actions

---

## Troubleshooting

### Common Issues

**Vercel:**
- If deployment fails, check build logs in Vercel dashboard
- Ensure `package.json` has correct build command

**GitHub Pages:**
- 404 errors: Check base path in `vite.config.js`
- Assets not loading: Verify paths are relative, not absolute

**AWS S3:**
- 403 Forbidden: Check bucket policy and public access settings
- Slow loading: Enable CloudFront distribution
- CORS issues: Set CORS configuration on S3 bucket

---

## Additional Resources

- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [AWS S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
