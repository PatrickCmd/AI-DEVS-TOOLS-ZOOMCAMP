Below is a **structured, step-by-step implementation plan** for an **intermediate developer** building a **Django TODO application** using:

* Django (web app) - latest version of django
* PostgreSQL (database)
* Docker & Docker Compose (containers)
* Pytest (test runner)
* The exercise file you attached as the reference 

No code is included—this is **only the implementation plan**.

---

# **Django TODO App – Full Implementation Plan (Containerized + Pytest)**

*Reference: the instructions from the attached exercise* 

---

# **1. Project Setup**

## **1.1. Create Project Structure**

Plan:

* Create a root folder for the project.
* Define typical Django project structure inside it.
* Create a folder for Docker configuration (e.g., `compose/` or root-level).
* Add standard files:

  * `Dockerfile` for Django app
  * `docker-compose.yml` for Django + PostgreSQL
  * `.env` for environment variables
  * `requirements.txt` or `pyproject.toml` (Recommended is uv setup here)

This will prepare the workspace for containerized development.

---

# **2. Install Django (Exercise Question 1)**

Plan:

* Inside the web container context, install Django using your dependency manager (`uv`).
* Confirm installation by running `django-admin --version` inside the container.

The exercise simply asks “What command did you use to install Django?”—your plan is to document whatever installation method you choose, but in the container.

---

# **3. Create Django Project & Application (Exercise Question 2)**

## **3.1. Start a Django Project**

Plan:

* Create Django project inside the web app container.
* Name it something like `todo_project`.
* Confirm key project files are created (`settings.py`, `urls.py`, `wsgi.py`, `manage.py`).

## **3.2. Create the App**

Plan:

* Create an app named `todo`.
* Register it inside `INSTALLED_APPS` in `settings.py`.

The exercise asks which file to edit → `settings.py`.

---

# **4. Configure PostgreSQL (Environment + Docker)**

## **4.1. Set up Docker Compose**

Plan:

* Define two services:

  * `web`: Django app container
  * `db`: PostgreSQL container
* Expose required ports.
* Add volume for persistent DB storage.

## **4.2. Configure Django to Use PostgreSQL**

Plan:

* Update `DATABASES` settings inside `settings.py` to point to the PostgreSQL service.
* Load sensitive values from `.env` (db name, user, password, host).

## **4.3. Test DB Connectivity**

Plan:

* Run migrations to ensure the database is reachable.
* Confirm creation of default Django tables.

---

# **5. Create Django Models (Exercise Question 3)**

The exercise asks: **What models do we need?**
For a TODO app, typical fields include:

* title
* description
* due_date
* is_resolved
* created_at
* updated_at

Plan:

* Define a `Todo` model with required fields.
* Register model in `admin.py`.
* Run migrations (the required next step per exercise).

---

# **6. Implement TODO Logic (Exercise Question 4)**

The exercise indicates logic goes in `views.py`.

Plan:

* Create views to handle:

  * listing todos
  * creating todos
  * editing todos
  * marking as resolved
  * deleting todos
* Create corresponding URL routes in `urls.py`.
* Ensure proper separation of concerns (view functions or class-based views).

---

# **7. Templates Setup (Exercise Question 5)**

The exercise says templates should include:

* `base.html`
* `home.html`

Plan:

* Create a `templates/` directory in the project.
* Configure `TEMPLATES['DIRS']` in project’s `settings.py` (correct answer from exercise).
* Ensure template inheritance (`home.html` extends `base.html`).
* Add UI components for form submission, editing, and listing TODOs.

---

# **8. Static Files Setup (Optional but Recommended)**

Plan:

* Create `static/` folder.
* Configure `STATIC_URL` and `STATICFILES_DIRS`.
* Add CSS file for basic styling.

---

# **9. Implement Pytest Test Suite (Exercise Question 6)**

## **9.1. Install Pytest + Django Integration**

Plan:

* Add `pytest`, `pytest-django`, and `pytest-cov` to project dependencies.

## **9.2. Configure Pytest**

Plan:

* Create root-level `pytest.ini`.
* Configure Django settings module.
* Set up fixture for `db` or `transactional_db`.

## **9.3. Write Tests for All Core Scenarios**

Use exercise guidance:
“Ask what scenarios we should cover—make sure they make sense.”

Plan to test:

1. **Model Tests**

   * Creating a todo
   * Editing a todo
   * Marking resolved
   * Deleting a todo
2. **View Tests**

   * List view loads correctly
   * Create view inserts into DB
   * Edit view updates DB
   * Delete view removes item
3. **Template Rendering Tests**

   * Templates render correct content
4. **URL resolution tests**

## **9.4. Run Tests**

Per exercise, correct answer is: `pytest`.

Plan:

* Execute tests inside the container.
* Ensure all pass before deployment.

---

# **10. Compose-based Local Development Workflow**

Plan:

* Run app with `docker-compose up`.
* Ensure DB migrates on startup (entrypoint or manual).
* Use `docker-compose exec web` for Django commands.

---

# **11. Deployment Preparation**

Plan:

* Decide if production container differs (gunicorn, whitenoise, etc.).
* Create a production `Dockerfile` (optional at this stage).
* Add `.dockerignore`.
* Add initial CI pipeline (pytest, linting).

---

# **12. Logging, Error Handling & Basic Hardening**

Plan:

* Configure logging in Django settings.
* Add validation on forms.
* Add error templates (404.html, 500.html).

---

# **13. Final Run (Exercise Conclusion)**

Exercise ends with:

```bash
python manage.py runserver
```

Your plan:

* Run the Django server inside Docker once everything is tested.
* Visit the TODO UI in a browser.
* Confirm all CRUD operations function with PostgreSQL.

---

