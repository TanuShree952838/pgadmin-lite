# pgadmin-lite
pgAdmin Lite is a simple, user-friendly web application that lets anyone—especially non-technical users—interact with a PostgreSQL database without writing SQL manually. It’s inspired by pgAdmin, but much lighter and cleaner, focusing on core features with an intuitive interface.

---

## Tech Stack

- **Backend:** Python 3, Django 5
- **Database:** PostgreSQL
- **Frontend:** Django Templates, Bootstrap 5, Font Awesome 6
- **Icons:** Custom template tags and Font Awesome

---

## Key Highlights

- **Dashboard:** View all tables and their columns in your PostgreSQL database.
- **Query Runner:** Run SQL queries and view results with error handling.
- **CRUD Operations:** Create, Read, Update, and Delete records via forms—no SQL required!
- **Responsive UI:** Modern Bootstrap-based design, mobile-friendly.
- **Dynamic Icons:** Uses Font Awesome for action icons (edit, delete).
- **Authentication:** (Optional) Add Django’s built-in authentication for user access.
- **Error Handling:** User-friendly error and success messages.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd pgadmin-lite/pgadmin-lite
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your database

Edit `pgadmin_lite/settings.py` with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pgadmin_lite_db',
        'USER': 'pguser',
        'PASSWORD': 'pgpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) in your browser.

---

## Notes

- Make sure PostgreSQL is running and accessible.
- Font Awesome is loaded via CDN in `base.html`.
