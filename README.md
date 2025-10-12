# Django HTMX Demo with Flowbite

A Django application demonstrating HTMX capabilities with Flowbite UI components.

## Features

- HTMX for dynamic interactions
- Flowbite components with dark mode support
- Tailwind CSS for styling
- Server-Sent Events (SSE) demo
- Responsive design

## Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- pip

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Build CSS

For development (with watch mode):
```bash
npm run dev
```

For production (minified):
```bash
npm run build
```

### 4. Run Django Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

In a separate terminal (keep the CSS watch running):
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
.
├── example_django/           # Django app
│   ├── templates/           # HTML templates
│   │   ├── home.html       # Main demo page
│   │   └── registration/
│   │       └── login.html  # Login page
│   ├── settings.py         # Django settings
│   └── views.py            # View functions
├── static/
│   └── src/
│       ├── input.css       # Tailwind/Flowbite source CSS
│       └── output.css      # Compiled CSS (generated)
├── package.json            # Node.js dependencies
└── requirements.txt        # Python dependencies
```

## Flowbite Configuration

This project follows the [Flowbite Django setup guide](https://flowbite.com/docs/getting-started/django/):

- **Tailwind CSS v3** with standard configuration (v4 not yet fully compatible with Flowbite)
- **Flowbite v2.5** plugin and components integrated
- **Dark mode** support using Tailwind's class-based dark mode
- **django-compressor** for static file optimization
- **Static files** properly configured for Django

### Why Tailwind v3?

While Tailwind CSS v4 introduces a new CSS-first configuration approach with `@import "tailwindcss"` and `@theme`, **Flowbite is currently built for Tailwind v3** and its plugin system isn't yet fully compatible with v4's alpha releases. We use v3 with the traditional `tailwind.config.js` approach for maximum compatibility.

### Installed Apps
- `compressor` - Django Compressor for CSS/JS compression
- `example_django` - Main application (equivalent to `flowbiteapp` in docs)

### Configuration Files
- **`tailwind.config.js`** - Tailwind configuration with Flowbite plugin
- **`static/src/input.css`** - Source CSS with `@tailwind` directives
- **`static/src/output.css`** - Compiled CSS (tracked in git)

### Django Compressor Settings
```python
COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = True
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
```

## Development

### CSS Development

The CSS is compiled from `static/src/input.css` to `static/src/output.css` using Tailwind CLI.

Run the watch command during development:
```bash
npm run dev
```

### Theme Toggle

The application includes a dark/light theme toggle that:
- Persists the user's preference in localStorage
- Uses Flowbite's theme toggle component
- Applies Tailwind's dark mode classes

## Production Deployment

### Deployment Strategy

This project **tracks the compiled CSS** (`static/src/output.css`) in git, which means:
- ✅ No Node.js required in production
- ✅ Simpler deployment process
- ✅ Works on all Django hosting platforms
- ⚠️ Remember to rebuild CSS before committing style changes

### Steps:

1. **Before committing style changes**, rebuild the CSS:
   ```bash
   npm run build
   ```

2. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. Set environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS`
   - Database settings (if using PostgreSQL)

### Alternative: Build CSS During Deployment

If you prefer not to track `output.css` in git, you can:
1. Add `static/src/output.css` to `.gitignore`
2. Ensure Node.js is available in your deployment environment
3. Add a build step: `npm install && npm run build` before `collectstatic`

## License

MIT
