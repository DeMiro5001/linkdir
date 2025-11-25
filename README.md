# LinkHub - Django Link Directory

A beautiful, responsive link directory built with Django that allows you to create a public page of links with Font Awesome icons. Perfect for personal link hubs, resource directories, or team bookmark collections.

![LinkHub](https://img.shields.io/badge/Django-4.2-green) ![License](https://img.shields.io/badge/License-MIT-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Project](https://img.shields.io/badge/Learning-Django-violet)

## ✨ Features

- 🎨 **Beautiful Design** - Responsive layout with dark/light mode toggle
- 🔧 **Easy Admin** - Simple Django admin interface for managing links
- 🎯 **Font Awesome Icons** - Support for all Font Awesome icons with easy copy-paste
- 🌙 **Dark Mode** - Automatic dark/light mode with system preference detection
- 📱 **Mobile Friendly** - Fully responsive design that works on all devices
- ⚙️ **Configurable** - Easy customization via environment variables
- 🔍 **Search** - Client-side search functionality
- 🗂️ **Categories** - Organize links into categories with custom colors

## 🚀 Quick Start

### Prerequisites

- Python 3.8-3.11
- Django 4.2+
- A web server (for production)

### Installation

1. **Clone or download the project**
```bash
   git clone https://github.com/DeMiro5001/linkdir
   cd linkdir
```

3. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Configure environment variables**
```bash
   cp .env.example .env
   # Edit .env with your preferences
```

6. **Run migrations**
```bash
   python manage.py migrate
```

7. **Create superuser**
```bash
   python manage.py createsuperuser
```

8. **Run development server**
```bash
   python manage.py runserver
```

9. **Access your site**
   - Public page: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## ⚙️ Configuration

### Environment Variables

Check `.env` file in your project root.

### Required Settings

- `SECRET_KEY`: Django secret key (change in production!)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains
- `SITE_TITLE`: Main heading on the public page
- `SITE_SUBTITLE`: Subtitle below the main heading
- `NAVBAR_BRAND`: Text in the navigation bar
- `CSRF_TRUSTED_ORIGINS`: Comma-separated URLs for CSRF protection (https://domain and not domain)

## 👨‍💻 Admin Guide

### Adding Categories

1. Go to `/admin` and log in
2. Click "Link Categories"
3. Click "Add Link Category"
4. Fill in:
   - **Name**: Category title (e.g., "Social Media")
   - **Description**: Optional description
   - **Order**: Display order (lower numbers first)
   - **Color**: Hex color for the category (e.g., `#0d6efd`)

### Adding Links

1. Go to `/admin` and log in
2. Click "Links"
3. Click "Add Link"
4. Fill in:
   - **Title**: Link display name
   - **URL**: The actual link URL
   - **Description**: Optional description
   - **Category**: Select a category
   - **Icon class**: Font Awesome icon classes

### Finding Icons

1. Visit [Font Awesome Icons](https://fontawesome.com/icons)
2. Search for an icon
3. Click the icon you want
4. Copy the HTML snippet: `<i class="fas fa-star"></i>`
5. Paste it in the "Icon class" field (the app will automatically extract the classes)

**Common icon examples:**
- `fas fa-star` - Solid star
- `fab fa-github` - GitHub logo
- `fas fa-envelope` - Email
- `fas fa-globe` - Website
- `fas fa-file-pdf` - PDF file

## 🎨 Customization

### Adding Custom CSS

Add your custom CSS to the `<style>` section in `base.html` or create a separate static CSS file.

### Modifying Layout

Edit the templates in `links/templates/links/`:
- `base.html` - Main layout and header/footer
- `public_page.html` - Links display page

## 🚀 Deployment

### Production Checklist

1. **Update environment variables:**
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

2. **Collect static files:**
```bash
python manage.py collectstatic
```

3. **Set up a production database** (PostgreSQL if you like, but I think sqlite is enough for this app):
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linkhub',
        'USER': 'linkhub',
        'PASSWORD': 'linkhub_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Deployment Options

#### Traditional VPS/server (Debian/Ubuntu + Nginx + Gunicorn)

1. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. **Set up project directory:**
```bash
sudo mkdir -p /var/www/linkhub
sudo chown $USER:$USER /var/www/linkhub
```
Where USER is a dedicated user for your app, with limited privileges.

3. **Copy the project files**
Using your preffered way (sftp, git clone, etc...)

4. **Create systemd service:**
```bash
sudo nano /etc/systemd/system/linkhub.service
```
   
```ini
[Unit]
Description=LinkHub Django application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/linkhub
Environment="PATH=/var/www/linkhub/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=linkdir.settings"
ExecStart=/var/www/linkhub/venv/bin/gunicorn \
    --access-logfile - \
    --error-logfile - \
    --workers 3 \
    --bind unix:/var/www/linkhub/linkhub.sock \
    linkdir.wsgi:application
Restart=always
RestartSec=5

StandardOutput=file:/var/log/linkhub/access.log
StandardError=file:/var/log/linkhub/error.log

[Install]
WantedBy=multi-user.target
```

5. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/linkhub
```
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        root /var/www/linkhub;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/linkhub/linkhub.sock;
    }
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Icons not showing in admin:**
   - Check that Font Awesome CSS is loading
   - Verify icon classes use correct Font Awesome version

2. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Verify web server static file configuration

3. **CSRF errors:**
   - Add your domain to `CSRF_TRUSTED_ORIGINS`
   - Ensure `ALLOWED_HOSTS` is set correctly

4. **Database errors:**
   - Run `python manage.py migrate`
   - Check database permissions and connection

### Debug Mode

For development, set `DEBUG=True` in `.env` file to see detailed error pages.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Submit a pull request
5. Wait till I review your PR and understand what it is about as I am newbie in django

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Python Dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

---

**Need help?** Check the [Django documentation](https://docs.djangoproject.com/) or create an issue in the project repository.
