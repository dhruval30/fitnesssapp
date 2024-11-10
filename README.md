# **Fitness App - Dockerized & Deployed on AWS EC2**

This project is a **Dockerized** fitness web application deployed on an **AWS EC2 instance**. The app is built with **Flask** and **MongoDB**, featuring functionalities like user authentication, activity tracking, exercise recommendations, and AI-powered diet plans. The focus of this project is on containerization with Docker and deployment using AWS EC2, allowing for scalable and portable deployment of the application.

## **Features**

- **Docker Containerization**: The app is packaged into a Docker container for easy deployment and scalability.
- **AWS EC2 Deployment**: The app is deployed on an AWS EC2 instance, ensuring that it is publicly accessible and can scale with traffic.
- **MongoDB Integration**: The app connects to MongoDB (either local or MongoDB Atlas) for storing user data.
- **User Authentication**: Secure login and signup functionalities.
- **Real-time Activity Tracking**: Display steps, heart rate, and calories burned.
- **Exercise Recommendations**: Personalized workout plans based on user profile.
- **AI-Powered Diet Plans**: Customized diet plans generated based on the user’s goals.

## **Tech Stack**

- **Backend**: Flask (Python)
- **Database**: MongoDB (MongoDB Atlas or local MongoDB)
- **Containerization**: Docker
- **Hosting**: AWS EC2
- **Frontend**: HTML templates (for user interface)

## **Setup Instructions**

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/fitnessapp.git
```

### **2. Build the Docker Image Locally**

Navigate to the project directory where the `Dockerfile` is located.

Build the Docker image using the following command:

```bash
docker build -t fitnessapp .
```

This will create the Docker image tagged as `fitnessapp`.

### **3. Run the Docker Container Locally**

To run the app locally within the Docker container, use this command:

```bash
docker run -p 5000:5000 fitnessapp
```

Now, you can access the app locally at `http://localhost:5000`.

---

## **Deploying the App on AWS EC2**

### **1. Launch an AWS EC2 Instance**

1. Go to the **EC2 Dashboard** in the AWS console and launch a new instance.
2. Choose an Amazon Linux 2 or Ubuntu image.
3. Create or select an existing **Security Group** allowing:
   - **SSH** (port 22) to access the instance.
   - **HTTP** (port 80) to serve the web app.

### **2. Connect to the EC2 Instance**

Once your EC2 instance is up and running, SSH into it:

```bash
ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-ip
```

### **3. Install Docker on EC2**

Run the following commands to install Docker on your EC2 instance (for Amazon Linux 2):

```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo systemctl enable docker
```

If you are using Ubuntu, use:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### **4. Transfer Project Files to EC2**

Use `scp` to transfer your project files to the EC2 instance:

```bash
scp -i /path/to/your-key.pem -r /path/to/your/project ec2-user@your-ec2-public-ip:/home/ec2-user/
```

This will upload the project to `/home/ec2-user/` on your EC2 instance.

### **5. Build and Run Docker Container on EC2**

1. SSH into your EC2 instance and navigate to the project directory:

```bash
cd /home/ec2-user/fitnessapp
```

2. Build the Docker image on the EC2 instance:

```bash
docker build -t fitnessapp .
```

3. Run the Docker container:

```bash
docker run -d -p 80:5000 fitnessapp
```

This will run the container in detached mode, mapping port 80 on the EC2 instance to port 5000 inside the Docker container.

### **6. Access the App**

Now, you can access your app by visiting `http://your-ec2-public-ip` in a web browser. The app should be accessible publicly.

---

## **Optional: Configure Docker to Restart on Reboot**

To ensure the Docker container starts automatically if the EC2 instance is rebooted, run:

```bash
docker run -d --restart unless-stopped -p 80:5000 fitnessapp
```

This will make sure the container restarts automatically when the instance reboots.

---

## **Troubleshooting**

- **MongoDB Connectivity**: If you are using **MongoDB Atlas**, ensure that the IP of your EC2 instance is added to the MongoDB Atlas whitelist under **Network Access**.
- **Security Group**: If you can't access the app from a browser, check that the EC2 security group allows **HTTP (port 80)** access.

---


