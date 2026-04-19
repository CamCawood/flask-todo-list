from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """Return the next task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


@app.route("/")
def index():
    """Display all tasks."""
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task."""
    title = request.form.get("title", "").strip()

    if title:
        tasks = load_tasks()
        new_task = {
            "id": get_next_id(tasks),
            "title": title,
            "completed": False
        }
        tasks.insert(0, new_task)
        save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    """Toggle a task between completed and not completed."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)