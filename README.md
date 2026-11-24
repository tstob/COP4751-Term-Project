# Job Application Tracker

## Project Overview

This project was developed for Florida International University COP4751 course; Advanced Database Management.

The Job Application Tracker is a web application that allows users to organize job opportunities, track applications, and manage company and contact information. It also includes a Job Match feature that compares a user's skills with the requirements of available jobs.

## Technologies Used

- Python 3
- Flask
- MySQL
- HTML and CSS
- GitHub

## Features

- **Dashboard:** Displays the total number of companies, jobs, applications, and contacts.
- **Companies:** Add, view, edit, and delete company records.
- **Jobs:** Add, view, edit, and delete job postings associated with companies.
- **Applications:** Track job applications, application dates, statuses, and interview information.
- **Contacts:** Manage professional contacts associated with companies.
- **Job Match:** Compare user-entered skills with job requirements and display match percentages and missing skills.

## Database Structure

The application uses a MySQL database named `job_tracker`.

The four main tables are:

- `companies`
- `jobs`
- `applications`
- `contacts`

Foreign keys maintain the relationships between companies, jobs, applications, and contacts.

The database also includes an `application_summary` table and JSON columns for storing job requirements and interview information.

Two SQL files are provided:

- **schema.sql:** Creates the database and its tables.
- **sample_data.sql:** Inserts sample records for testing and demonstrating the application.

The sample data includes 6 companies, 18 jobs, 6 applications, and 6 contacts. Two jobs contain JSON skill requirements that can be used to test Job Match.

## Installation and Setup

### 1. Install the required software

Install Python 3 and MySQL Server. MySQL Workbench is recommended for importing the SQL files.

### 2. Download the project

Clone or download this GitHub repository and open the project folder in VS Code.

### 3. Set up the database

Open MySQL Workbench and connect to your MySQL server.

Run the following SQL files in order:

1. `schema.sql` — Creates the `job_tracker` database and tables.
2. `sample_data.sql` — Populates the tables