"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

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
    title, description, max_grade = hackbright.get_project_by_title(title)
    students = hackbright.get_grades_by_title(title)

    html = render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           students=students)
    return html

@app.route("/assign-for-grading")
def show_grading_form():
    """Render grading page"""

    students = hackbright.get_students()
    projects = hackbright.get_projects()

    return render_template("grading.html", 
                            students = students, 
                            projects=projects)


@app.route("/assign-grade", methods=['POST'])
def grade_student_for_project():
    """Grade student on project"""

    # raise "Aaaaa"

    github = request.form.get("github")
    title = request.form.get("title")
    grade = request.form.get("grade")

    # validate if grade is not exided a max_grade
    hackbright.assign_grade(github, title, grade)

    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)
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


    if first_name == "" or last_name == "" or github == "":
        # need to add parameter flash_msg to session and remove it in "/" after display
        return redirect('/')
    else:
        msg = hackbright.make_new_student(first_name, last_name, github)

        return render_template("student_info.html",
                            first = first_name,
                            last = last_name,
                            github = github,
                            msg = msg)


@app.route("/project-add", methods=['POST'])
def project_add():
    """Add a project."""

    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    if title == "" or description == "" or max_grade == "":
        # need to add parameter flash_msg to session and remove it in "/" after display
        return redirect('/')
    else:
        msg = hackbright.make_new_project(title, description, max_grade)

        return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
