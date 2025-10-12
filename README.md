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

- **Tailwind CSS v3** with standard configuration
- **Flowbite** plugin and components integrated
- **Dark mode** support using Tailwind's class-based dark mode
- **Static files** properly configured for Django

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

1. Build the CSS:
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

## License

MIT
