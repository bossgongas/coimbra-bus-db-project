# 🚌 Coimbra Bus – Database Management System

This project was developed for the **Databases** course (2023),  
**Bachelor in Electrical and Computer Engineering**,  
**Department of Informatics Engineering – University of Coimbra**.

---

## 🎯 Objective

Develop a fully functional database-backed application in Python to manage the operations of **Coimbra Bus**, a fictional public transport company based in Coimbra.

The system supports the management of:
- Clients (normal and gold)
- Reservations (including waitlists and cancellation policies)
- Buses and routes
- Trips (with pricing history)
- Messaging (manual and automated)
- Statistics and administrative tools

---

## 🧱 Technologies

- **PostgreSQL** (database)
- **Python** with `psycopg2` for DB connectivity
- **PL/pgSQL** (stored procedures, triggers, functions)
- **ONDA** (data modeling tool used in ER and Physical design)

---

## 📂 Project Structure

### 🔹 `meta1/` – First milestone
- ER and physical diagrams (from ONDA)
- Interface specification
- Planning and initial modeling

### 🔹 `meta2/` – Final delivery
- Full Python implementation with all required functionalities
- Database creation and population scripts
- Use of at least one transaction and one PL/pgSQL function
- Updated diagrams and user interface screenshots

---

## 💡 Key Features

### 👤 Client interface
- Register, login, view and book trips
- Cancel reservations and handle waitlists
- View messages from admins
- View travel history and personal stats

### 🛠️ Admin interface
- Add/edit/remove trips and buses
- Manage clients and promote to gold status
- View advanced statistics
- Send messages to individual clients or all users

---

## 📄 Files

- `2023-bd-projeto.pdf`: Project specification
- `meta1/BD_project_report.pdf`: First milestone report
- `meta2/Coimbra_Bus_Rel.pdf`: Final report with diagrams and screenshots
- `meta2/src/`: Python source code and SQL scripts

---

## 👨‍🎓 Authors

- **Leonardo Cordeiro Gonçalves** – 2020228071  
- **Gonçalo Tavares Bastos** – 2020238997  

📅 Meta I: March 2023  
📅 Meta II: May 2023

