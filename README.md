# 🏋️‍♂️ Fitness Center Management API

A secure and flexible **Django REST Framework** based API to manage fitness centers like gyms, yoga studios, and more. The API supports full CRUD operations, JWT authentication, and custom filtering options for listing and managing centers.

---

## 📌 Features

- ✅ **User Registration & JWT Authentication**
- ✅ **Create, Read, Update, Delete (CRUD)** Fitness Centers
- ✅ **Role-Based Permissions** (Owner, Admin)
- ✅ **Filter & Sort** Centers by:
  - Monthly fee (min/max)
  - Facilities (search)
  - Verified status
  - Category (via URL param)
  - Established date and fee (ordering)
- ✅ **Owner-only** update/delete
- ✅ **Test Coverage** using `APITestCase`

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Auth**: JWT (`djangorestframework-simplejwt`)
- **Database**: SQLite (default)
- **Testing**: Django `APITestCase`

---
## 📁 Project Structure
<pre>
fitness_app/
│
├── models.py           # FitnessCenter model
├── views.py            # API views with permissions
├── serializers.py      # Serializers (not shown here)
├── tests.py            # Full test cases using APITestCase

fitness/
├── urls.py             # Routes for API endpoints
</pre>
---

## 🔐 Authentication

Uses **JWT Authentication** for secure login.

- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`  
  Returns `access` and `refresh` tokens.

Include `Authorization: Bearer <access_token>` in headers for protected routes.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Login and get JWT token |
| `GET` | `/api/centers/` | List all centers (with filters) |
| `POST` | `/api/centers/` | Create a new center *(Authenticated)* |
| `GET` | `/api/centers/<pk>/` | Get details of a center |
| `PUT`/`PATCH` | `/api/centers/<pk>/` | Update center *(Owner only)* |
| `DELETE` | `/api/centers/<pk>/` | Delete center *(Owner only)* |
| `GET` | `/api/centers/<category>/` | Get centers by category (e.g., `YOGA`) |

---

## 🧪 Key Test Cases Covered

- ✅ User registration & JWT login
- ✅ Fetching center list with filters
- ✅ Ordering by monthly fee and established date
- ✅ Owner-based update and delete permission checks
- ✅ Validation:
  - Minimum `monthly_fee`
  - Valid `established_date`
  - Unique `name`

---

## 📊 Filtering & Sorting Query Params

You can pass query parameters like:
/api/centers/?min_fee=1000&max_fee=1500&facilities=Showers&ordering=-established_date
- `min_fee`: Minimum monthly fee
- `max_fee`: Maximum monthly fee
- `facilities`: Case-insensitive match in facilities text
- `is_verified`: Filter by verification status
- `ordering`: Fields like `monthly_fee` or `-established_date`

---

## 🧮 Bonus Field (Derived)

- `price_per_session` is calculated as:
- price_per_session = monthly_fee / total_sessions


Returned as part of the center's response.

---
<h2>🧪 Running Tests</h2>

<pre><code>python manage.py test</code></pre>

<p>Runs all test cases under <code>fitness_app/tests.py</code>.</p>

<hr/>

<h2>🚀 Getting Started (Locally)</h2>

<pre><code>
git clone https://github.com/yourusername/fitness-api.git
cd fitness-api
</code></pre>

<h3>Install dependencies</h3>

<pre><code>pip install -r requirements.txt</code></pre>

<h3>Run migrations</h3>

<pre><code>
python manage.py makemigrations
python manage.py migrate
</code></pre>

<h3>Create superuser (optional)</h3>

<pre><code>python manage.py createsuperuser</code></pre>

<h3>Run server</h3>

<pre><code>python manage.py runserver</code></pre>

<hr/>

<h2>📌 Requirements</h2>

<ul>
  <li>Django >= 4.0</li>
  <li>djangorestframework</li>
  <li>djangorestframework-simplejwt</li>
</ul>

<hr/>

<h2>👨‍💻 Author</h2>

<p><strong>Md Javed</strong><br/>
Django & DRF Developer | Data Scientist<br/>
<a href="https://github.com/mdjaved24">GitHub Profile</a></p>

<hr/>
