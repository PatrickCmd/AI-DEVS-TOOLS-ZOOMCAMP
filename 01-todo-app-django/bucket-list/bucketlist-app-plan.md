# Bucket list application

✔ User authentication (register, login, logout)
✔ User profiles & social graph (follow/unfollow)
✔ Bucket list items (private by default, public when shared)
✔ Viewing public bucket lists only from people you follow
✔ Comments on public bucket list items
✔ Dockerized Django + PostgreSQL
✔ Pytest as test runner

(No code included—**this is a pure implementation plan**.)

---

# **Updated Implementation Plan for the Bucket List Django Application**

*Reference to the exercise structure* 
(but expanded to meet real-world application requirements)

---

# **1. Project Setup**

### **1.1. Create Project Structure**

* Create project root folder.
* Add:

  * `Dockerfile` for Django app
  * `docker-compose.yml` for app + PostgreSQL
  * `.env` for sensitive values
  * `requirements.txt` or `pyproject.toml`
  * `/src` or root-level Django project folder
  * `tests/` folder for pytest

### **1.2. Establish Version Control**

* Initialize Git repository.
* Add `.gitignore` (Python, Django, IDEs, Docker artifacts).

---

# **2. Install Django & Required Packages**

(Relates to Question 1 of the exercise)
Plan to install:

* django
* psycopg2 or psycopg2-binary
* django-allauth (optional) or implement custom auth manually
* pytest
* pytest-django
* pytest-cov

Confirm Django installation inside the app container.

---

# **3. Create the Django Project & Core App**

(Relates to Question 2 of the exercise)

### **3.1. Create Django Project**

* Create project: `bucketlist_project/`
* Ensure default files:

  * `settings.py`
  * `urls.py`
  * `manage.py`
  * `wsgi.py`

### **3.2. Create Apps**

1. `accounts` – user authentication & profile
2. `bucket` – bucket list items & visibility rules
3. `social` – follow/unfollow relationships
4. `comments` – commenting system

Register apps in `INSTALLED_APPS`.

---

# **4. Configure PostgreSQL with Docker**

### **4.1. Docker Compose**

* Define services:

  * `web` (Django)
  * `db` (PostgreSQL)
* Add persistent volume for DB.

### **4.2. Django DB Settings**

* Update `DATABASES` section in `settings.py`.
* Import variables from `.env`.

### **4.3. Migrations Test**

* Run migrations inside container to confirm the setup.

---

# **5. User Authentication (Accounts App)**

### **5.1. Models**

Plan for:

* Custom `User` model OR extend via `UserProfile` (recommended for intermediate developer).
* Fields for profile:

  * bio
  * profile_image (optional)
  * date_joined
  * updated_at

### **5.2. Views**

* Registration view (signup)
* Login view
* Logout view
* Profile view (own profile)
* Public profile of other users (limited visibility)

### **5.3. URLs**

* `/register/`
* `/login/`
* `/logout/`
* `/profile/<username>/`

### **5.4. Forms**

* Registration form
* Login form
* Profile update form

### **5.5. Templates**

* `accounts/register.html`
* `accounts/login.html`
* `accounts/profile.html`

### **5.6. Access Control**

* Use Django’s `LoginRequiredMixin`.
* Redirect anonymous users to login page.

---

# **6. Social Graph (Follow/Unfollow)**

(New functionality)

### **6.1. Models (social app)**

Plan for:

* `Follow` model containing:

  * follower (ForeignKey to User)
  * following (ForeignKey to User)
  * created_at

### **6.2. Views**

* Follow a user
* Unfollow a user
* List followers
* List following

### **6.3. Rules**

* User A can see User B’s public bucket list items **only if** A follows B.

### **6.4. URLs**

* `/follow/<username>/`
* `/unfollow/<username>/`
* `/following/`
* `/followers/`

### **6.5. Templates**

* Follow/unfollow buttons on profile pages.
* Followers list page.
* Following list page.

---

# **7. Bucket List Items (Bucket App)**

(Main feature)

### **7.1. Models**

Plan for fields in `BucketItem`:

* user (owner)
* title
* description
* category (optional)
* is_public (default: False)
* image (optional)
* created_at
* updated_at

### **7.2. Visibility Logic**

Private by default:

* Only the owner sees private items.
* A user sees another user’s bucket list items **only when**:

  1. They follow them, **and**
  2. Item is public.

### **7.3. Views**

* Create bucket list item
* Edit bucket list item
* Delete bucket list item
* Share (toggle privacy)
* View list of own items
* View list of followed users’ public items

### **7.4. URLs**

* `/bucket/create/`
* `/bucket/<id>/edit/`
* `/bucket/<id>/delete/`
* `/bucket/<id>/share/`
* `/bucket/mine/`
* `/bucket/following/`

### **7.5. Templates**

* `bucket/create.html`
* `bucket/edit.html`
* `bucket/list.html`
* `bucket/following_list.html`

---

# **8. Comments on Public Bucket List Items (Comments App)**

### **8.1. Model**

`Comment`:

* user
* bucket_item
* text
* created_at

### **8.2. Views**

* Add comment to a public bucket item.
* Delete comment (owner only).
* Display comments under bucket item page.

### **8.3. Permissions**

* Users can comment only on public bucket items.
* Only comment owners can delete their comments.

### **8.4. URLs**

* `/bucket/<id>/comment/`
* `/comment/<id>/delete/`

### **8.5. Templates**

* Form for add comment
* Comment rendering partial template

---

# **9. Templates Setup (Relates to Exercise Question 5)**

### **9.1. Template Directory**

* Create `templates/` at project root.
* Register in `TEMPLATES['DIRS']`.

### **9.2. Shared Templates**

* `base.html` (navigation, user info, follow/unfollow links)
* `navbar.html` include

### **9.3. Page Templates**

* Registration
* Login
* Profile
* Bucket list and detail pages
* Followers/following pages

---

# **10. Static & Media Files**

### **10.1. Static Files**

* Add global `static/` directory.
* Collect static with Django `STATICFILES_DIRS`.

### **10.2. Media Uploads**

* User profile images
* Optional bucket item images

Configure storage settings and media URL.

---

# **11. Implement Tests with Pytest (Relates to Exercise Question 6)**

### **11.1. Test Structure**

Create `tests/` directory with subfolders:

* `tests/accounts/`
* `tests/social/`
* `tests/bucket/`
* `tests/comments/`

### **11.2. Scenarios to Test**

#### **Accounts**

* User registration
* Login/logout
* Profile visibility
* Unauthorized access redirect

#### **Social**

* Follow user
* Unfollow user
* Cannot follow oneself
* Visibility logic for bucket items

#### **Bucket Items**

* Create item (private by default)
* Owner sees private items; others cannot
* Share (toggle to public)
* Following user can see public items
* Editing and deleting (owner only)

#### **Comments**

* Add comment to public item
* Cannot comment on private item
* Delete comment

#### **Integration Tests**

* End-to-end flow:
  register → follow → create item → share → comment

### **11.3. Running Tests**

* Use `pytest` as per exercise
* Ensure database fixtures work with PostgreSQL

---

# **12. Local Development with Docker Compose**

### **12.1. Workflow**

* Build containers
* Run `docker-compose up`
* Run migrations
* Create superuser
* Access app via browser

### **12.2. Useful Commands**

* Shell access:
  `docker-compose exec web bash`
* Migrations:
  `docker-compose exec web python manage.py migrate`
* Tests:
  `docker-compose exec web pytest`

---

# **13. Documentation & API Design (Optional but recommended)**

### **13.1. Provide Basic Documentation**

* Markdown file: `README.md`
* Setup instructions
* Endpoints overview
* Testing instructions
* Architecture diagram

### **13.2. API Endpoints (Optional if planning API)**

* `/api/auth/`
* `/api/bucket/`
* `/api/follow/`
* `/api/comments/`

---

# **14. Deployment Preparation**

(Optional for now)

### **14.1. Production Dockerfile**

* Use Gunicorn
* Use Whitenoise or S3 for static files

### **14.2. Environment Configuration**

* Production `.env`
* Secure cookie and session settings

---

# **15. Final Run (Relates to Exercise Ending)**

Even in Docker, provide Django run command for reference:

```
python manage.py runserver
```

Inside container, exposed via `docker-compose`.

---
