import os
from flask import Flask, jsonify
import sqlalchemy

# Initialize Flask App
app = Flask(__name__)

# Cloud SQL Connector
def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"] # e.g. 'project:region:instance'#
# db_user = os.environ["DB_USER"]
   # db_pass = os.environ["DB_PASS"]
   # db_name = os.environ["DB_NAME"]

    from google.cloud.sql.connector import Connector
    connector = Connector()

    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user="htiwary7",
            password="htiwarydbpassword",
            db="postgress",
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool

# Initialize the connection pool
db = connect_with_connector()

# Create table if it doesn't exist and insert sample data
@app.before_first_request
def setup_database():
    with db.connect() as conn:
        conn.execute(sqlalchemy.text(
            """CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    tech_stack VARCHAR(255),
                    image_name VARCHAR(255)
                );
            """
        ))
        # Clear existing data to prevent duplicates on redeploy
        conn.execute(sqlalchemy.text("DELETE FROM projects;"))
        conn.execute(sqlalchemy.text(
            """INSERT INTO projects (title, description, tech_stack, image_name) VALUES
               ('Cloud Native CI/CD Pipeline', 'Architected a multi-service CI/CD pipeline using Cloud Build, Artifact Registry, and Cloud Run, showcasing IaC principles with Terraform.', 'GCP, Terraform, Cloud Build, GKE', 'project1.jpg'),
               ('Hybrid Cloud Data Migration', 'Designed and implemented a data streaming solution from AWS to GCP using Datastream and Data Migration Service for a seamless transfer.', 'AWS, GCP, Datastream, Cloud SQL', 'project2.jpg'),
               ('GKE Network Policy Hardening', 'Implemented fine-grained network policies using Calico on GKE to secure pod-to-pod communication and reduce attack surface.', 'GKE, Calico, Kubernetes, Security', 'project3.jpg');
            """
        ))
        conn.commit()


@app.route("/api/projects")
def get_projects():
    projects = []
    with db.connect() as conn:
        results = conn.execute(sqlalchemy.text("SELECT * FROM projects ORDER BY id;")).fetchall()
        for row in results:
            projects.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "tech_stack": row[3],
                "image_name": row[4]
            })
    return jsonify(projects)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
