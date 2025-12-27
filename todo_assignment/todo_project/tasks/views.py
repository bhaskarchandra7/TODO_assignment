import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .db import get_connection, create_table

create_table()

# ---------------- API ---------------- #

@csrf_exempt
def task_api(request, task_id=None):
    conn = get_connection()
    cur = conn.cursor()

    try:
        if request.method == "GET":
            if task_id:
                cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
                r = cur.fetchone()
                return JsonResponse({
                    "id": r[0], "title": r[1], "description": r[2],
                    "due_date": r[3], "status": r[4]
                })
            else:
                cur.execute("SELECT * FROM tasks")
                rows = cur.fetchall()
                data = [{
                    "id": r[0], "title": r[1],
                    "description": r[2], "due_date": r[3], "status": r[4]
                } for r in rows]
                return JsonResponse(data, safe=False)

        if request.method == "POST":
            data = json.loads(request.body)
            cur.execute(
                "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
                (data["title"], data.get("description"), data.get("due_date"), "pending")
            )
            conn.commit()
            return JsonResponse({"message": "Task created"}, status=201)

        if request.method == "PUT":
            data = json.loads(request.body)
            cur.execute(
                "UPDATE tasks SET title=?, description=?, due_date=?, status=? WHERE id=?",
                (data["title"], data["description"], data["due_date"], data["status"], task_id)
            )
            conn.commit()
            return JsonResponse({"message": "Task updated"})

        if request.method == "DELETE":
            cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            return JsonResponse({"message": "Task deleted"})

    finally:
        conn.close()


# ---------------- TEMPLATE VIEWS ---------------- #

def dashboard(request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return render(request, "tasks/list.html", {"tasks": tasks})


def task_detail(request, task_id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE tasks SET title=?, description=?, due_date=?, status=?
            WHERE id=?
        """, (
            request.POST["title"],
            request.POST["description"],
            request.POST["due_date"],
            request.POST["status"],
            task_id
        ))
        conn.commit()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cur.fetchone()
    conn.close()

    return render(request, "tasks/detail.html", {"task": task})


def delete_task(request, task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")


def add_task(request):
    if request.method == "POST":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
            (request.POST["title"], request.POST["description"], request.POST["due_date"], "pending")
        )
        conn.commit()
        conn.close()
        return redirect("/")
    return render(request, "tasks/add.html")

from datetime import date

def today_tasks(request):
    today = date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE due_date = ?", (today,))
    tasks = cur.fetchall()
    conn.close()
    return render(request, "tasks/list.html", {
        "tasks": tasks,
        "page": "Today"
    })


def upcoming_tasks(request):
    today = date.today().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE due_date > ?", (today,))
    tasks = cur.fetchall()
    conn.close()
    return render(request, "tasks/list.html", {
        "tasks": tasks,
        "page": "Upcoming"
    })


def completed_tasks(request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status = 'done'")
    tasks = cur.fetchall()
    conn.close()
    return render(request, "tasks/list.html", {
        "tasks": tasks,
        "page": "Completed"
    })
