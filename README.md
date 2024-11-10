# **Fitness App - Dockerized & Deployed on AWS EC2**

Hi, welcome to the **Fitness App**, a small web app that’s **Dockerized** and deployed on **AWS EC2**. It's built using **Flask** and **MongoDB** to give you some features like user login/signup, tracking your activity, personalized exercise recommendations, and even an AI-powered diet plan. It’s all wrapped up in a **Docker container** and running on **AWS EC2**, making it **scalable** and **portable**!

## **What It Does**

- **Dockerized**: The app is packed in a Docker container so it's easy to deploy anywhere. 
- **AWS EC2**: Hosted on an EC2 instance so it's always online and available. 
- **MongoDB**: Stores your user data securely with MongoDB.
- **User Authentication**: Secure login and signup so only you get access to your fitness data.
- **Real-Time Activity Tracking**: Get your steps, heart rate, and calories burned in real-time. 
- **Exercise Recommendations**: Personalized workout plans to help you crush your fitness goals. 
- **AI-Powered Diet Plans**: Get a custom diet plan from an AI that understands your body type and goals. 

## **Tech Stack**

- **Backend**: Flask (Python)
- **Database**: MongoDB 
- **Containerization**: Docker
- **Hosting**: AWS EC2
- **Frontend**: HTML templates for the UI

## **How to Set It Up**

### **1. Clone the Repo**

Clone the repo to your machine:

```bash
git clone https://github.com/yourusername/fitnessapp.git
```

### **2. Build the Docker Image Locally**

Now, go to the project directory where your `Dockerfile` is, and build the Docker image:

```bash
docker build -t fitnessapp .
```

This creates an image tagged as `fitnessapp`.

### **3. Run the Docker Container Locally**

To run the app inside the Docker container, just do this:

```bash
docker run -p 5000:5000 fitnessapp
```

You can now access your app locally at `http://localhost:5000`.

---

## **Deploying the App on AWS EC2**

### **1. Fire Up an EC2 Instance**

Go to the **EC2 Dashboard** on AWS and launch a new instance. Choose either **Amazon Linux 2** or **Ubuntu**.

Make sure you create a **Security Group** that allows:
- **SSH (port 22)** for accessing the instance.
- **HTTP (port 80)** to serve the app.

### **2. SSH Into the EC2 Instance**

Once your EC2 instance is up, SSH into it:

```bash
ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-ip
```

### **3. Install Docker on EC2**

Run the following commands to get Docker running on your EC2 instance (for **Amazon Linux 2**):

```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo systemctl enable docker
```

If you’re using **Ubuntu**, do this instead:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### **4. Transfer Project Files to EC2**

Use `scp` to move the project files to your EC2 instance:

```bash
scp -i /path/to/your-key.pem -r /path/to/your/project ec2-user@your-ec2-public-ip:/home/ec2-user/
```

### **5. Build and Run Docker Container on EC2**

SSH into your EC2 instance and go to your project directory:

```bash
cd /home/ec2-user/fitnessapp
```

Then build the Docker image on the EC2 instance:

```bash
docker build -t fitnessapp .
```

Next, run the Docker container:

```bash
docker run -d -p 80:5000 fitnessapp
```

This will run your app in **detached mode**, with port 80 on the EC2 instance pointing to port 5000 inside the container.

### **6. Access the App**

Once your container is up and running, just open a browser and go to:

```
http://your-ec2-public-ip
```

You should see your app running! 

