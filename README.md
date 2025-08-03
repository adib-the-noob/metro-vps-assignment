### MetroVPS assignment
This repository contains the code for the MetroVPS assignment, which is a part of the interview process for the position of Software Engineer L2 at MetroVPS.

> You can download the `.env` file required for the project from [this link](https://drive.google.com/file/d/11I6ZTbwzH2SsH1HwHlCWQPIkoJY_2VdN/view?usp=drive_link).

#### Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adib-the-noob/metro-vps-assignment.git
   ```
2. Navigate into the project directory:
   ```bash
   cd metro-vps-assignment
   ```
3. Stop Redis and MySQL services if they are running:
   ```bash
   sudo systemctl stop redis-server
   sudo systemctl stop mysql
   ```
4. Build the Docker containers:
   ```bash
   docker-compose build
   ```
5. Start the Docker containers:
   ```bash
   docker-compose up -d
   ```
6. List all the Running Docker containers to verify:
   ```bash
   docker ps
   ```
   You should see the following containers running:
   - `metro-vps-assignment-web-1`
    - `metro-vps-assignment-db-1`
    - `metro-vps-assignment-redis-1`
    - `metro-vps-assignment-celery-1`
    - `metro-vps-assignment-celery-beat-1`

7. Bash into the Django container:
   ```bash
   docker exec -it metro-vps-assignment-web-1 bash 
   ```
8. Inside the container, run the following commands to set up the database and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
    ```
9. Exit the container:
    ```bash
    exit
    ```
10. Open your web browser and navigate to `http://localhost:8000/admin` to access the Django admin panel.

