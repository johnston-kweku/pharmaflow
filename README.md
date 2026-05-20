# PharmaFlow - Pharmacy Management System

PharmaFlow is a modern, responsive, and robust Pharmacy Management System built with Django and Tailwind CSS. It is designed to streamline pharmaceutical inventory management, handle complex sales workflows (Wholesale & Retail), and provide deep business insights through real-time analytics.

---

## 🚀 Key Features

### 🔐 User Management & Security
*   **Role-Based Access Control (RBAC):** Distinct permissions for `Admin`, `Manager`, `Wholesaler`, and `Retailer`.
*   **Custom User Profiles:** Extended user model with full name, phone number, and role-specific redirection.
*   **Staff Control:** Create, list, and toggle active status for staff accounts.

### 📦 Inventory & Stock Control
*   **Comprehensive Catalog:** Track medications with wholesale, retail, and cost pricing.
*   **Real-time Stock Tracking:** Automatic inventory updates synced with sales processing.
*   **Safety Guards:** Validation logic to prevent negative stock and ensure pricing integrity.

### 💰 Dual-Channel Sales
*   **Wholesale & Retail UI:** Specialized interfaces for bulk hospital/clinic orders and individual walk-in customers.
*   **AJAX-Powered Cart:** Seamless shopping experience without page reloads.
*   **Digital Receipts:** Auto-generated, printable receipts for every transaction.

### 📊 Business Analytics
*   **Live Dashboard:** Real-time revenue, profit, and sales volume tracking.
*   **Historical Trends:** Interactive charts (Chart.js) showing 6-month growth patterns.
*   **Performance Metrics:** Automatic calculation of month-over-month growth.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.10+, Django 4.x/5.x
*   **Frontend:** Tailwind CSS 4.x, Vanilla JavaScript
*   **Database:** SQLite (Default)
*   **Analytics:** Chart.js
*   **Authentication:** Django Auth (Extended)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pharmacy-management-system
```

### 2. Environment Setup
Create a `.env` file from the template:
```bash
cp .env.example .env
# Edit .env and add your SECRET_KEY
```

### 3. Install Dependencies
**Python:**
```bash
pip install -r requirements.txt
# OR if using Pipenv
pipenv install && pipenv shell
```

**Node.js (for Tailwind CSS):**
```bash
npm install
```

### 4. Database Setup
```bash
python manage.py migrate
```

### 5. Initial Data (Optional)
Load sample items from the provided JSON:
```bash
python manage.py load_items --file load_data.json
```

---

## 🏃 Running the Application

### Start the Django Server:
```bash
python manage.py runserver
```

### Start Tailwind CSS Watcher (Development only):
```bash
npm run dev
```


---

## 🛠️ Management Commands

PharmaFlow includes several custom CLI tools for data management:

*   `load_items --file <path>`: Bulk import drugs from a JSON file.
*   `clear`: Wipe the database of all drugs and sales records (Development only).
*   `clean_drugs`: Deletes drug entries with inconsistent names (over 50 chars).
*   `edit --model <app.Model> --field <field>`: Populates specific fields with random data using Faker.

---

## 📂 Project Structure

```text
├── accounts/          # User management, roles, and profiles
├── inventory/         # Drug catalog, stock logic, and dashboard
├── sales/             # Wholesale/Retail workflows and receipt generation
├── static/            # CSS (Tailwind), JS (Chart.js, AJAX logic), Images
├── templates/         # Global and app-specific HTML templates
├── manage.py          # Django management script
└── Features.md        # Detailed feature breakdown
```

---

## 👥 Contributors
*   **Lead Developer**: Johnston Kweku Abubakar

---

*Generated on: May 20, 2026*
