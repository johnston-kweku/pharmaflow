# Pharmacy Management System - Features

A comprehensive system designed to manage pharmaceutical inventory, sales (wholesale and retail), and user roles within a pharmacy environment.

## 1. User Management & Security
*   **Role-Based Access Control (RBAC):** Implementation of distinct roles including `Admin`, `Manager`, `Wholesaler`, and `Retailer`.
*   **Custom User Model:** Extended Django's AbstractUser to include full names, phone numbers, and specific roles.
*   **Permission Decorators:** Custom view decorators (`@role_required`) to ensure only authorized users access specific functionalities.
*   **User Lifecycle Management:** Admins and Managers can create, list, and toggle the active status of staff accounts.
*   **Secure Authentication:** Integrated login/logout system with role-specific redirection.
*   **Password Validation:** Custom logic for password confirmation and security during user creation.

## 2. Inventory Management
*   **Drug Catalog:** Detailed tracking of medications including name, description, wholesale price, retail price, and cost price.
*   **Stock Tracking:** Real-time inventory monitoring with automated updates upon sales.
*   **CRUD Operations:** Specialized interfaces for adding, updating, and deleting drugs (with protection against deleting items with sale history).
*   **Price Validation:** Built-in logic to ensure retail prices remain higher than wholesale prices.
*   **Advanced Forms:** Styled Django forms with Tailwind CSS integration and custom widgets for enhanced usability.

## 3. Sales & Transactions
*   **Dual Sales Channels:** Support for both **Wholesale** (bulk) and **Retail** (individual) transaction workflows.
*   **Automated Cost Calculation:** System automatically calculates total costs based on sale type and quantity.
*   **Atomic Transactions:** Uses database atomicity to ensure data integrity during complex sale processing.
*   **Receipt Generation:** Dynamic generation of digital receipts for completed transactions.
*   **Sales History:** Comprehensive logging of all sales for auditing and tracking purposes.
*   **Dynamic Cart System:** Real-time cart management using AJAX for seamless shopping experience.

## 4. Analytics & Dashboard
*   **Performance Metrics:** Real-time tracking of monthly revenue, profit margins, and sales counts.
*   **Comparative Analytics:** Automatic calculation of percentage changes in revenue and sales compared to the previous month.
*   **Visual Data Representation:** Integrated **Chart.js** for interactive monthly revenue, profit, and sales volume trends.
*   **Recent Activity Feed:** Quick view of the latest 5 sales directly on the home dashboard.
*   **Historical Data Analysis:** Tracking of 6-month historical trends for informed business decisions.

## 5. Data Management & Tools
*   **Bulk Data Loading:** Custom management command (`load_items`) to import drug data from JSON files.
*   **Database Cleaning:** Command-line utilities (`clear`, `clean_drugs`) for database maintenance and cleanup of inconsistent data.
*   **Random Data Generator:** Advanced command (`edit`) to populate any model field with random data for testing and development using Faker and RandomWords.

## 6. Technical Stack & UX
*   **Backend:** Python / Django Web Framework.
*   **Database:** SQLite (Relational).
*   **Frontend Styling:** Tailwind CSS for a modern, responsive user interface.
*   **Interactive UI:** 
    *   **Custom Toast Notifications:** Global `ToastManager` for real-time success and error feedback.
    *   **AJAX Sales Processing:** Seamless cart management and sale processing without page reloads.
    *   **Responsive Layouts:** Mobile-first design with a fixed navigation system and consistent spacing.
    *   **Dynamic UI Elements:** SVG-based iconography and smooth transitions for a polished feel.

---
*Generated on: May 20, 2026*
