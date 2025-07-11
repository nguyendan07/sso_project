# SSO Project

A Django-based Single Sign-On (SSO) system using OpenID Connect (OIDC) for authentication.

## 🚀 Features

- **OpenID Connect Integration**: Seamless authentication with OIDC providers
- **Custom User Management**: Extended user model with custom authentication backend
- **Django 5.2 Compatible**: Built with latest Django framework
- **Responsive UI**: Clean, modern interface for all authentication flows
- **Debug Tools**: Comprehensive debugging interface for development
- **Production Ready**: WSGI/ASGI deployment configuration

## 🏗️ Architecture

```
sso_project/
├── accounts/           # Custom user management app
│   ├── auth.py        # Custom OIDC authentication backend
│   ├── models.py      # Custom user model
│   ├── views.py       # Authentication views
│   └── templates/     # HTML templates
├── sso_project/       # Main Django project
│   ├── settings.py    # Project configuration
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI deployment
└── manage.py          # Django management script
```

## 📋 Prerequisites

- Python 3.13+
- Django 5.2+
- OIDC Provider (e.g., Keycloak, Auth0, Google, etc.)

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/nguyendan07/sso_project.git
cd sso_project
```

2. **Install dependencies**:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. **Create configuration file**:
```bash
cp config.ini.example config.ini
```

4. **Configure OIDC settings** in `config.ini`:
```ini
[DEFAULT]
SECRET_KEY = your-secret-key-here
DEBUG = True
DATABASE_URL = sqlite:///db.sqlite3

# OIDC Configuration
OIDC_RP_CLIENT_ID = your-client-id
OIDC_RP_CLIENT_SECRET = your-client-secret
OIDC_OP_AUTHORIZATION_ENDPOINT = https://your-provider/auth/realms/master/protocol/openid-connect/auth
OIDC_OP_TOKEN_ENDPOINT = https://your-provider/auth/realms/master/protocol/openid-connect/token
OIDC_OP_USER_ENDPOINT = https://your-provider/auth/realms/master/protocol/openid-connect/userinfo
OIDC_OP_JWKS_ENDPOINT = https://your-provider/auth/realms/master/protocol/openid-connect/certs
```

5. **Run database migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser** (optional):
```bash
python manage.py createsuperuser
```

7. **Start development server**:
```bash
python manage.py runserver
```

## Loading Sample Data

To create sample data for the application, including an admin account:

```bash
python manage.py loaddata dev_data.json
```

After loading the sample data, you can log in to the admin page with:
- Username: admin
- Email: admin@project.com
- Password: dZ4$1Jq86&=+


## 🔐 OIDC Configuration

### Required OIDC Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `OIDC_RP_CLIENT_ID` | Your application's client ID | `django-sso-client` |
| `OIDC_RP_CLIENT_SECRET` | Your application's client secret | `supersecret123` |
| `OIDC_OP_AUTHORIZATION_ENDPOINT` | Authorization endpoint URL | `https://provider/auth` |
| `OIDC_OP_TOKEN_ENDPOINT` | Token endpoint URL | `https://provider/token` |
| `OIDC_OP_USER_ENDPOINT` | User info endpoint URL | `https://provider/userinfo` |
| `OIDC_OP_JWKS_ENDPOINT` | JWKS endpoint URL | `https://provider/certs` |

### Provider-Specific Examples

#### Keycloak
```ini
OIDC_OP_AUTHORIZATION_ENDPOINT = https://keycloak.example.com/auth/realms/master/protocol/openid-connect/auth
OIDC_OP_TOKEN_ENDPOINT = https://keycloak.example.com/auth/realms/master/protocol/openid-connect/token
OIDC_OP_USER_ENDPOINT = https://keycloak.example.com/auth/realms/master/protocol/openid-connect/userinfo
OIDC_OP_JWKS_ENDPOINT = https://keycloak.example.com/auth/realms/master/protocol/openid-connect/certs
```

#### Google
```ini
OIDC_OP_AUTHORIZATION_ENDPOINT = https://accounts.google.com/o/oauth2/v2/auth
OIDC_OP_TOKEN_ENDPOINT = https://oauth2.googleapis.com/token
OIDC_OP_USER_ENDPOINT = https://openidconnect.googleapis.com/v1/userinfo
OIDC_OP_JWKS_ENDPOINT = https://www.googleapis.com/oauth2/v3/certs
```

## 🛣️ URL Structure

- `/` - Home dashboard (requires authentication)
- `/accounts/login/` - Login page
- `/accounts/logout/` - Logout page
- `/accounts/profile/` - User profile page
- `/oidc/authenticate/` - OIDC authentication initiation
- `/oidc/callback/` - OIDC callback handler
- `/oidc/logout/` - OIDC logout handler
- `/admin/` - Django admin interface

## 🎨 Templates

The project includes responsive templates:

- [`base.html`](accounts/templates/base.html) - Base template with common layout
- [`login.html`](accounts/templates/registration/login.html) - Login interface
- [`logout.html`](accounts/templates/registration/logout.html) - Logout confirmation
- [`profile.html`](accounts/templates/registration/profile.html) - User profile
- [`index.html`](accounts/templates/home/index.html) - Debug dashboard

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Format code
ruff format .

# Lint code
ruff check .

# Sort imports
isort .
```

### Database Operations
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush
```

## 🚀 Production Deployment

### Environment Variables

For production, use environment variables instead of config file:

```bash
export SECRET_KEY="your-production-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
export DATABASE_URL="postgresql://user:password@localhost/dbname"
export OIDC_RP_CLIENT_ID="your-client-id"
export OIDC_RP_CLIENT_SECRET="your-client-secret"
```

### WSGI Deployment
```python
# wsgi.py is configured for production deployment
# Use with gunicorn, uWSGI, or similar WSGI server
```

### Docker Deployment
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sso_project.wsgi:application"]
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS in production
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure secure session cookies
- [ ] Enable CSRF protection
- [ ] Set up proper logging
- [ ] Regular security updates

### OIDC Security

- [ ] Validate `OIDC_RP_CLIENT_SECRET` is secure
- [ ] Use HTTPS for all OIDC endpoints
- [ ] Configure proper redirect URIs
- [ ] Implement token refresh logic
- [ ] Set appropriate token lifetimes

## 🐛 Troubleshooting

### Common Issues

1. **OIDC Authentication Fails**
   - Check OIDC provider configuration
   - Verify client ID and secret
   - Ensure redirect URIs are correctly configured

2. **Template Not Found**
   - Check `TEMPLATES` configuration in [`settings.py`](sso_project/settings.py)
   - Verify template file paths

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATICFILES_DIRS` settings

### Debug Mode

Enable debug mode to see detailed session and token information:

```ini
DEBUG = True
```

Visit the home page (`/`) to see debug information including:
- User details
- OIDC tokens (length only for security)
- Session information
- Request headers

## 📚 Dependencies

- **Django 5.2.4+**: Web framework
- **mozilla-django-oidc 4.0.1+**: OIDC authentication
- **dj-database-url 3.0.1+**: Database URL parsing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Mozilla Django OIDC](https://mozilla-django-oidc.readthedocs.io/)
- [OpenID Connect Specification](https://openid.net/connect/)
- [OIDC Debugger](https://oidcdebugger.com/)

---

For more information or support, please open an issue in the project repository.