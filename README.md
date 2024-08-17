# DiverseProducts Web Application

It is a simple web application in which you have to create an account to be able to maange your own
inventory, by adding deleting updating or searching through your products table. You can upload images
of your products in the jpg or png format. You also get access to a marketplace where you can check the 
products of other users and their prices.

## Prerequisites

Before setting up the project, ensure you have the following installed on your Linux system:

- Python 3.x
- Pip (Python package manager)
- MariaDB server
- Git (to clone the repository)

## Setup Instructions

### 1. Clone the Repository

First, clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/yourusername/upbnotes.git
cd upbnotes
```
### 2. Install Python Dependencies

Install the necessary Python packages using pip. This project uses Flask 
and mysql-connector-python for interacting with the MariaDB database

```bash
# Update pip to the latest version
pip install --upgrade pip

# Install dependencies
pip install flask mysql-connector-python
```

### 3. Set Up MariaDB Database

Install MariaDB server if it's not already installed and start it:

```bash
sudo apt update
sudo apt install mariadb-server

sudo systemctl start mariadb
```

### 4. Configure the Database

Log in to MariaDB as the root user and create the UpbNotes database:

```bash
sudo mysql -u root -p
```

Inside the MariaDB shell, run the SQL commands from the [script](db_creation_script.sql), then run the following command and make sure you get the same result as in the [picture](Tables%20in%20DB.png).

### 5. Upload Directory
The application saves uploaded files in the static directory. Ensure this directory exists and has the appropriate permissions:

```bash
mkdir -p static
chmod 755 static
```
### 6. Running the Application

To run the Flask application, execute the following command in the project directory:

```bash
python3 your_script_name.py
```
