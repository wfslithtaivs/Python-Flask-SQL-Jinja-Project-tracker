"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def index():
    """Render initial page with choice of actions """

    students = hackbright.get_students()
    projects = hackbright.get_projects()

    return render_template("index.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)

    return html


@app.route("/project")
def get_project():
    """Show information about a project."""

    title = request.args.get('title')
    title, description, max_grade = hackbright. get_project_by_title(title)
    students = hackbright.get_grades_by_title(title)

    html = render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           students=students)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    msg = hackbright.make_new_student(first_name, last_name, github)

    html = render_template("student_info.html",
                        first = first_name,
                        last = last_name,
                        github = github,
                        msg = msg)
    return html

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
