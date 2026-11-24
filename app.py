import json
#from flask import Flask, render_template

#forms
from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__)


# Display dashboard
@app.route("/")
def dashboard():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Get the number of records in each table
        tables = ["companies", "jobs", "applications", "contacts"]
        counts = {}

        for table in tables:
            query = f"SELECT COUNT(*) AS total FROM {table}"
            cursor.execute(query)
            result = cursor.fetchone()
            counts[table] = result["total"]

        return render_template("dashboard.html", counts=counts)

    finally:
        cursor.close()
        db.close()


# Display companies from database
@app.route("/companies")
def companies():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM companies"
        cursor.execute(query)
        company_list = cursor.fetchall()

        return render_template(
            "companies.html",
            companies=company_list
        )

    finally:
        cursor.close()
        db.close()


# Addnew company
@app.route("/companies/add", methods=["GET", "POST"])
def add_company():

    if request.method == "POST":
        name = request.form.get("company_name", "").strip()
        industry = request.form.get("industry", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()

        # Verify company name was entered
        if not name:
            return "Company name is required.", 400

        db = get_db_connection()

        if db is None:
            return "Could not connect to the database.", 500

        cursor = db.cursor()

        try:
            query = """
                INSERT INTO companies
                (company_name, industry, city, state)
                VALUES (%s, %s, %s, %s)
            """

            values = (name, industry, city, state)

            cursor.execute(query, values)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

        return redirect(url_for("companies"))

    return render_template("add_company.html")


# Edit existing company
@app.route("/companies/edit/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Find the company using its ID
        query = "SELECT * FROM companies WHERE company_id = %s"
        cursor.execute(query, (company_id,))
        company = cursor.fetchone()

        if company is None:
            return "Company not found.", 404

        if request.method == "POST":
            name = request.form.get("company_name", "").strip()
            industry = request.form.get("industry", "").strip()
            city = request.form.get("city", "").strip()
            state = request.form.get("state", "").strip()

            if not name:
                return "Company name is required.", 400

            # Update the company information
            query = """
                UPDATE companies
                SET company_name = %s,
                    industry = %s,
                    city = %s,
                    state = %s
                WHERE company_id = %s
            """

            values = (name, industry, city, state, company_id)

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("companies"))

        return render_template("edit_company.html", company=company)

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Delete
@app.route("/companies/delete/<int:company_id>", methods=["POST"])
def delete_company(company_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor()

    try:
        # Check ifcompany has any jobs
        query = "SELECT COUNT(*) FROM jobs WHERE company_id = %s"
        cursor.execute(query, (company_id,))
        job_count = cursor.fetchone()[0]

        # Domt delete companies w existing jobs
        if job_count > 0:
            return "This company has jobs associated with it and cannot be deleted.", 400

        # Check if the company has any contacts
        query = "SELECT COUNT(*) FROM contacts WHERE company_id = %s"
        cursor.execute(query, (company_id,))
        contact_count = cursor.fetchone()[0]

        if contact_count > 0:
            return "This company has contacts associated with it and cannot be deleted.", 400

        # Delete selected company
        query = "DELETE FROM companies WHERE company_id = %s"
        cursor.execute(query, (company_id,))
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("companies"))


# Display jobs and their companies
@app.route("/jobs")
def jobs():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Join job to display company names
        query = """
            SELECT jobs.*, companies.company_name
            FROM jobs
            LEFT JOIN companies
            ON jobs.company_id = companies.company_id
            ORDER BY jobs.job_id
        """

        cursor.execute(query)
        job_list = cursor.fetchall()

        return render_template("jobs.html", jobs=job_list)

    finally:
        cursor.close()
        db.close()


# Add a new job
@app.route("/jobs/add", methods=["GET", "POST"])
def add_job():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Companies for the dropdown menu
        cursor.execute("SELECT company_id, company_name FROM companies")
        company_list = cursor.fetchall()

        if request.method == "POST":
            company_id = request.form.get("company_id")
            title = request.form.get("job_title", "").strip()
            job_type = request.form.get("job_type")
            salary_min = request.form.get("salary_min") or None
            salary_max = request.form.get("salary_max") or None

            if not company_id or not title:
                return "Company and job title are required.", 400

            # Save the new job
            query = """
                INSERT INTO jobs
                (company_id, job_title, job_type, salary_min, salary_max)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (company_id, title, job_type, salary_min, salary_max)

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("jobs"))

        return render_template("add_job.html", companies=company_list)

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Edit existing jobs
@app.route("/jobs/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Find the selected job
        query = "SELECT * FROM jobs WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        job = cursor.fetchone()

        if job is None:
            return "Job not found.", 404

        # Get companies for the dropdown
        cursor.execute("SELECT company_id, company_name FROM companies")
        company_list = cursor.fetchall()

        if request.method == "POST":
            company_id = request.form.get("company_id")
            title = request.form.get("job_title", "").strip()
            job_type = request.form.get("job_type")
            salary_min = request.form.get("salary_min") or None
            salary_max = request.form.get("salary_max") or None

            if not company_id or not title:
                return "Company and job title are required.", 400

            # Update the job information
            query = """
                UPDATE jobs
                SET company_id = %s,
                    job_title = %s,
                    job_type = %s,
                    salary_min = %s,
                    salary_max = %s
                WHERE job_id = %s
            """

            values = (
                company_id, title, job_type,
                salary_min, salary_max, job_id
            )

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("jobs"))

        return render_template(
            "edit_job.html",
            job=job,
            companies=company_list
        )

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Delete jobs
@app.route("/jobs/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor()

    try:
        # Check if job has any applications
        query = "SELECT COUNT(*) FROM applications WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        application_count = cursor.fetchone()[0]

        if application_count > 0:
            return "This job has applications associated with it and cannot be deleted.", 400

        # Delete selected job
        query = "DELETE FROM jobs WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("jobs"))


# Display all job applications
@app.route("/applications")
def applications():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Get applications with their job and company names
        query = """
            SELECT applications.*,
                   jobs.job_title,
                   companies.company_name
            FROM applications
            JOIN jobs
            ON applications.job_id = jobs.job_id
            JOIN companies
            ON jobs.company_id = companies.company_id
            ORDER BY applications.application_date DESC
        """

        cursor.execute(query)
        application_list = cursor.fetchall()

        return render_template(
            "applications.html",
            applications=application_list
        )

    finally:
        cursor.close()
        db.close()


# Add a new job application
@app.route("/applications/add", methods=["GET", "POST"])
def add_application():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Get jobs and company names for the dropdown
        query = """
            SELECT jobs.job_id, jobs.job_title, companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
            ORDER BY companies.company_name, jobs.job_title
        """
        cursor.execute(query)
        job_list = cursor.fetchall()

        if request.method == "POST":
            job_id = request.form.get("job_id")
            application_date = request.form.get("application_date")
            status = request.form.get("status")
            resume_version = request.form.get("resume_version", "").strip()
            cover_letter_sent = 1 if request.form.get("cover_letter_sent") else 0
            notes = request.form.get("notes", "").strip()

            if not job_id or not application_date:
                return "Job and application date are required.", 400

            # Save the application to MySQL
            query = """
                INSERT INTO applications
                (job_id, application_date, status,
                 resume_version, cover_letter_sent, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                job_id, application_date, status,
                resume_version, cover_letter_sent, notes
            )

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("applications"))

        return render_template("add_application.html", jobs=job_list)

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Edit existing job applications
@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Find selected application
        query = "SELECT * FROM applications WHERE application_id = %s"
        cursor.execute(query, (application_id,))
        application = cursor.fetchone()

        if application is None:
            return "Application not found.", 404

        # Jobs dropdown
        query = """
            SELECT jobs.job_id, jobs.job_title, companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
            ORDER BY companies.company_name, jobs.job_title
        """
        cursor.execute(query)
        job_list = cursor.fetchall()

        if request.method == "POST":
            job_id = request.form.get("job_id")
            application_date = request.form.get("application_date")
            status = request.form.get("status")
            resume_version = request.form.get("resume_version", "").strip()
            cover_letter_sent = 1 if request.form.get("cover_letter_sent") else 0
            response_date = request.form.get("response_date") or None
            interview_date = request.form.get("interview_date") or None
            notes = request.form.get("notes", "").strip()

            if not job_id or not application_date:
                return "Job and application date are required.", 400

            # Update the application
            query = """
                UPDATE applications
                SET job_id = %s,
                    application_date = %s,
                    status = %s,
                    resume_version = %s,
                    cover_letter_sent = %s,
                    response_date = %s,
                    interview_date = %s,
                    notes = %s
                WHERE application_id = %s
            """

            values = (
                job_id, application_date, status,
                resume_version, cover_letter_sent,
                response_date, interview_date,
                notes, application_id
            )

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("applications"))

        return render_template(
            "edit_application.html",
            application=application,
            jobs=job_list
        )

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Delete a job application
@app.route("/applications/delete/<int:application_id>", methods=["POST"])
def delete_application(application_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor()

    try:
        # Delete selected application
        query = "DELETE FROM applications WHERE application_id = %s"
        cursor.execute(query, (application_id,))
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("applications"))


# Display all contacts and their companies
@app.route("/contacts")
def contacts():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Contacts company names
        query = """
            SELECT contacts.*, companies.company_name
            FROM contacts
            JOIN companies
            ON contacts.company_id = companies.company_id
            ORDER BY contacts.last_name, contacts.first_name
        """

        cursor.execute(query)
        contact_list = cursor.fetchall()

        return render_template(
            "contacts.html",
            contacts=contact_list
        )

    finally:
        cursor.close()
        db.close()


# Add a new contact
@app.route("/contacts/add", methods=["GET", "POST"])
def add_contact():
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Get companies dropdown menu
        cursor.execute("""
            SELECT company_id, company_name
            FROM companies
            ORDER BY company_name
        """)
        company_list = cursor.fetchall()

        if request.method == "POST":
            company_id = request.form.get("company_id")
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            job_title = request.form.get("job_title", "").strip()
            linkedin_url = request.form.get("linkedin_url", "").strip()
            notes = request.form.get("notes", "").strip()

            # Check required fields
            if not company_id or not first_name or not last_name:
                return "Company, first name, and last name are required.", 400

            # Inser new contact
            query = """
                INSERT INTO contacts
                (company_id, first_name, last_name, email,
                 phone, job_title, linkedin_url, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                company_id, first_name, last_name,
                email or None, phone or None,
                job_title or None, linkedin_url or None,
                notes or None
            )

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("contacts"))

        return render_template(
            "add_contact.html",
            companies=company_list
        )

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Edit an existing contact
@app.route("/contacts/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor(dictionary=True)

    try:
        # Get contact being edited
        query = "SELECT * FROM contacts WHERE contact_id = %s"
        cursor.execute(query, (contact_id,))
        contact = cursor.fetchone()

        if contact is None:
            return "Contact not found.", 404

        # Get companies fordropdown menu
        cursor.execute("""
            SELECT company_id, company_name
            FROM companies
            ORDER BY company_name
        """)
        company_list = cursor.fetchall()

        if request.method == "POST":
            company_id = request.form.get("company_id")
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            job_title = request.form.get("job_title", "").strip()
            linkedin_url = request.form.get("linkedin_url", "").strip()
            notes = request.form.get("notes", "").strip()

            # Check required fields
            if not company_id or not first_name or not last_name:
                return "Company, first name, and last name are required.", 400

            # Update contact information
            query = """
                UPDATE contacts
                SET company_id = %s,
                    first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone = %s,
                    job_title = %s,
                    linkedin_url = %s,
                    notes = %s
                WHERE contact_id = %s
            """

            values = (
                company_id, first_name, last_name,
                email or None, phone or None,
                job_title or None, linkedin_url or None,
                notes or None, contact_id
            )

            cursor.execute(query, values)
            db.commit()

            return redirect(url_for("contacts"))

        return render_template(
            "edit_contact.html",
            contact=contact,
            companies=company_list
        )

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# Delete an existing contact
@app.route("/contacts/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    db = get_db_connection()

    if db is None:
        return "Could not connect to the database.", 500

    cursor = db.cursor()

    try:
        # Delete selected contact
        query = "DELETE FROM contacts WHERE contact_id = %s"
        cursor.execute(query, (contact_id,))
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("contacts"))


# Match user skills with job requirements
@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    results = []
    user_skills = ""

    if request.method == "POST":
        user_skills = request.form.get("skills", "")

        # Separate the skills entered by the user
        skills = [
            skill.strip().lower()
            for skill in user_skills.split(",")
            if skill.strip()
        ]

        db = get_db_connection()

        if db is None:
            return "Could not connect to the database.", 500

        cursor = db.cursor(dictionary=True)

        try:
            # Get jobs with their company names and requirements
            query = """
                SELECT jobs.job_id, jobs.job_title,
                       jobs.requirements, companies.company_name
                FROM jobs
                JOIN companies
                ON jobs.company_id = companies.company_id
                WHERE jobs.requirements IS NOT NULL
            """

            cursor.execute(query)
            job_list = cursor.fetchall()

            for job in job_list:
                # Convert JSON text to a Python dictionary
                requirements = job["requirements"]

                if isinstance(requirements, str):
                    requirements = json.loads(requirements)

                if not isinstance(requirements, dict):
                    continue

                required_skills = requirements.get("required_skills", [])

                if not isinstance(required_skills, list) or not required_skills:
                    continue

                # Find which required skills the user has
                matched_skills = [
                    skill for skill in required_skills
                    if skill.lower() in skills
                ]

                # Find which required skills are missing
                missing_skills = [
                    skill for skill in required_skills
                    if skill.lower() not in skills
                ]

                # Calculate match percentage
                match_percentage = round(
                    len(matched_skills) / len(required_skills) * 100
                )

                results.append({
                    "job_title": job["job_title"],
                    "company_name": job["company_name"],
                    "match_percentage": match_percentage,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "total_skills": len(required_skills)
                })

            # Rank jobs from highest to lowest match
            results.sort(
                key=lambda job: job["match_percentage"],
                reverse=True
            )

        finally:
            cursor.close()
            db.close()

    return render_template(
        "job_match.html",
        results=results,
        user_skills=user_skills
    )


if __name__ == "__main__":
    app.run(debug=True)
