# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated deployment to various platforms.

## Available Workflows

### 1. `deploy-vercel.yml` - Deploy to Vercel
**Status**: Disabled by default (requires secrets)

Automatically deploys to Vercel on every push to the `main` branch.

**Required Secrets:**
- `VERCEL_TOKEN`: Your Vercel authentication token
- `VERCEL_ORG_ID`: Your Vercel organization ID
- `VERCEL_PROJECT_ID`: Your Vercel project ID

**Setup:**
1. Run `vercel link` locally to get your IDs
2. Get token from https://vercel.com/account/tokens
3. Add secrets to GitHub: Settings > Secrets and variables > Actions

### 2. `deploy-github-pages.yml` - Deploy to GitHub Pages
**Status**: Ready to use (no secrets needed)

Automatically deploys to GitHub Pages on every push to the `main` branch.

**Setup:**
1. Go to Settings > Pages
2. Select "GitHub Actions" as source
3. Update `vite.config.js` with your repo name:
   ```javascript
   base: process.env.GITHUB_ACTIONS ? '/your-repo-name/' : '/',
   ```
4. Push to `main` branch

### 3. `deploy-aws.yml` - Deploy to AWS S3/CloudFront
**Status**: Disabled by default (requires configuration)

Automatically deploys to AWS S3 and invalidates CloudFront on every push to the `main` branch.

**Required Secrets:**
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

**Required Configuration:**
Update these environment variables in the workflow file:
- `S3_BUCKET`: Your S3 bucket name
- `CLOUDFRONT_DISTRIBUTION_ID`: Your CloudFront distribution ID (optional)
- `AWS_REGION`: Your AWS region (default: us-east-1)

## Enabling a Workflow

### Option 1: Use Only One Platform
If you only want to deploy to one platform, delete or disable the other workflow files:

```bash
# Example: Keep only Vercel
rm .github/workflows/deploy-github-pages.yml
rm .github/workflows/deploy-aws.yml
```

### Option 2: Use Multiple Platforms
You can enable multiple workflows. Each will run independently on push to `main`.

### Option 3: Manual Trigger
To prevent automatic deployments, change the trigger:

```yaml
on:
  workflow_dispatch:  # Manual trigger only
```

## Testing Workflows

All workflows include a test step that runs before deployment:
```yaml
- name: Run tests
  run: npm test -- --run
```

If tests fail, deployment will be cancelled.

## Workflow Status

Check workflow status in your repository:
- Go to "Actions" tab
- View recent workflow runs
- Click on a run to see detailed logs

## Troubleshooting

### Workflow not running
- Check that you're pushing to the `main` branch
- Verify workflow file syntax (use YAML linter)
- Check if workflows are enabled: Settings > Actions > General

### Deployment fails
- Check workflow logs for specific error
- Verify all required secrets are set
- Ensure build succeeds locally: `npm run build`

### Secrets not working
- Secrets are case-sensitive
- Secrets are not visible in logs (for security)
- Re-enter secret if you suspect it's incorrect

## Best Practices

1. **Start with one platform**: Get one deployment working before enabling others
2. **Test locally first**: Always run `npm run build` and `npm test` locally
3. **Use staging environment**: Consider deploying to staging before production
4. **Monitor deployments**: Check the Actions tab after each push
5. **Keep secrets secure**: Never commit AWS keys or tokens to repository

## Quick Start

### For Vercel (Easiest)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel link` in project root
3. Add secrets to GitHub
4. Push to `main`

### For GitHub Pages (Free)
1. Update `vite.config.js` base path
2. Enable GitHub Pages in settings
3. Push to `main`

### For AWS (Most Control)
1. Create S3 bucket and CloudFront distribution
2. Create IAM user with deployment permissions
3. Add AWS credentials to GitHub secrets
4. Update workflow configuration
5. Push to `main`

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Full Deployment Guide](../../DEPLOYMENT.md)
