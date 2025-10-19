# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please send an email to:

**riccardo.tornesello@gmail.com**

Please include the following information:

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

We will acknowledge receipt of your vulnerability report within 48 hours and will send you regular updates about our progress.

## Security Best Practices

When deploying this application, please follow these security best practices:

### Environment Configuration

1. **Never use DEBUG=true in production**
   ```bash
   DEBUG=false
   ```

2. **Use a strong SECRET_KEY**
   - Generate a new secret key for each environment
   - Never commit secret keys to version control
   - Use at least 50 random characters

3. **Configure ALLOWED_HOSTS properly**
   ```bash
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

4. **Restrict CORS origins**
   ```bash
   CORS_ALLOWED_ORIGINS=https://your-frontend.com
   ```

### Database Security

1. **Use strong database passwords**
   - Use a password manager to generate random passwords
   - Rotate credentials regularly

2. **Limit database access**
   - Only allow connections from application servers
   - Use database user with minimal required privileges

3. **Enable SSL/TLS for database connections**

### Authentication & Authorization

1. **Configure Firebase properly**
   - Set up appropriate security rules
   - Use the correct Firebase audience/project ID
   - Validate tokens on every request

2. **Keep authentication dependencies updated**
   ```bash
   uv sync --upgrade
   ```

### HTTPS/SSL

1. **Always use HTTPS in production**
   - The application automatically enables HTTPS settings when DEBUG=false
   - Set up SSL certificates (Let's Encrypt recommended)

2. **HSTS is enabled by default** when DEBUG=false
   - Headers enforce HTTPS for 1 year
   - Includes subdomains

### Headers & Middleware

The application includes security headers by default:

- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` - Enables XSS filter

### Dependency Management

1. **Keep dependencies updated**
   ```bash
   uv sync --upgrade
   ```

2. **Monitor for vulnerabilities**
   - The CI/CD pipeline includes security scanning
   - Review security advisories regularly

3. **Lock dependencies**
   - Use `uv.lock` to ensure consistent versions
   - Review lock file changes in PRs

### File Uploads

1. **Use Google Cloud Storage in production**
   - Never store user uploads on application servers
   - Configure appropriate bucket permissions

2. **Validate file types and sizes**
   - Implement file type validation
   - Set maximum upload sizes

### Logging & Monitoring

1. **Review logs regularly**
   - Monitor for suspicious activity
   - Set up alerts for critical errors

2. **Don't log sensitive data**
   - Avoid logging passwords, tokens, or personal data
   - Use Django's sensitive parameter filtering

### Rate Limiting

The application includes rate limiting for sensitive endpoints:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'scan': '20/minute',
    },
}
```

Consider adding rate limiting for other endpoints based on your needs.

### Regular Security Audits

1. Run security checks regularly:
   ```bash
   uv run python manage.py check --deploy
   ```

2. Review Django security advisories:
   - https://www.djangoproject.com/weblog/

3. Keep Python and system packages updated

## Known Security Considerations

### Firebase Authentication

This application uses Firebase for authentication. Ensure:

1. Firebase project is properly configured
2. `FIREBASE_AUDIENCE` environment variable matches your Firebase project
3. Firebase security rules are restrictive
4. Token verification is performed on every authenticated request

### Static Files

In production, static files should be served by:
- Google Cloud Storage (configured via `GS_BUCKET_NAME`)
- A CDN or reverse proxy (nginx, CloudFlare, etc.)
- Never served directly by Django

## Security Updates

We will publish security advisories for any vulnerabilities discovered in this project. Updates will be communicated through:

- GitHub Security Advisories
- Email to contributors
- Updates to this SECURITY.md file

## Responsible Disclosure

We ask that you:

1. Give us reasonable time to address the issue before public disclosure
2. Make a good faith effort to avoid privacy violations and data destruction
3. Do not exploit the vulnerability beyond what is necessary for demonstration

We commit to:

1. Respond to your report within 48 hours
2. Keep you informed of our progress
3. Credit you in the security advisory (unless you prefer to remain anonymous)

Thank you for helping keep DevFest Lecce 2025 and its users safe!
