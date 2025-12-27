# To-Do List Web Application (Django)

## Objective
A To-Do List web application built using Python and Django.
The project provides RESTful APIs for task management and HTML templates for UI rendering.
Django ORM and generic viewsets are not used.

---

## Features
- Create, Read, Update, Delete tasks
- Task status: Pending / Completed
- Due date display
- API endpoints with JSON responses
- Template-based user interface
- SQLite database
- Logging and exception handling

---

## Tech Stack
- Python
- Django
- SQLite
- HTML/CSS
- JavaScript (basic)

---

## Database Schema
| Field | Type |
|------|------|
| title | Text |
| description | Text |
| due_date | Date |
| status | Text |

---

## API Endpoints

### Create Task
**POST** `/api/tasks/`
```json
{
  "title": "Task title",
  "description": "Task description",
  "due_date": "2025-01-10",
  "status": "Pending"
}
