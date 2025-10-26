# AWS IoT Core MQTT Publisher-Subscriber Setup

Complete guide for setting up AWS IoT Core with a Raspberry Pi publisher and laptop subscriber using MQTT.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [AWS IoT Core Setup](#aws-iot-core-setup)
3. [Project Setup](#project-setup)
4. [Running the Publisher](#running-the-publisher)
5. [Running the Subscriber](#running-the-subscriber)
6. [Verify the Output](#verify-the-output)
7. [Project Structure](#project-structure)
8. [Security Notes](#security-notes)

## Prerequisites

### Required
- AWS Account (with appropriate permissions for IoT Core)
- Raspberry Pi (any model with network connectivity)
- Laptop/Smart Phone for subscriber
- Network connectivity for both devices

## AWS IoT Core Setup

### Step 1: Create an IoT Thing

1. Log into the **AWS Management Console**
2. Navigate to **AWS IoT Core**
3. In the left sidebar, go to **Manage** → **All devices** → **Things**
4. Click **Create things**
5. Select **Create single thing**
6. Enter a thing name (e.g., `RaspberryPi_Test`)
7. Click **Next**

### Step 2: Generate Certificates

1. On the "Configure device certificate" page, select **Auto-generate a new certificate**
2. Click **Next**
3. On the next screen, you'll need to create a policy first (see Step 3)

### Step 3: Create and Attach a Policy

1. Click **Create policy** (opens in new tab)
2. Enter a policy name (e.g., `IoT_Full_Access_Policy`)
3. In the **Policy document** section, click **JSON** tab
4. Paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}
```

5. Click **Create**
6. Go back to the certificate creation tab and refresh the policies list
7. Select your newly created policy
8. Click **Create thing**

### Step 4: Download Certificates

**CRITICAL: You can only download these once!**

Download and save the following files:
- **Device certificate** (xxxxx-certificate.pem.crt)
- **Private key** (xxxxx-private.pem.key)
- **Amazon Root CA 1** (click the link to download AmazonRootCA1.pem)

Click **Done**

### Step 5: Get Your Device Endpoint

1. In AWS IoT Core, Look for **Domain configuration** in the left sidebar of **Connect**.
2. Copy your **Device data endpoint** (format: `xxxxx-ats.iot.region.amazonaws.com`)
   - Note: You can confirm the correct endpoint by checking the latest "Date updated."
3. Save this - you'll need it for both publisher and subscriber

---

## Project Setup

### Step 1: Create the Project Directory

```bash
git clone https://github.com/HMC03/imu-door-classifier.git
```

### Step 2: Create the virtual environment

```bash
# Ensured you are in the project root directory.
python -m venv .venv
```

### Step 3: Create the Certificates Directory

```bash
# Confirmed you at the root-level for the repo.
mkdir .certs 
```

### Step 4: Copy Certificates

Copy the three certificate files you downloaded to the `.certs/` folder:
- `xxxxxx-certificate.pem.crt`
- `xxxxxx-private.pem.key`
- `AmazonRootCA1.pem`

### Step 5: Create Environment File

Create a `.env` file in the project root:

```bash
touch .env
nano .env
```

Add the following (replace with your actual values):

```
ENDPOINT=xxxxx-ats.iot.us-east-2.amazonaws.com
CERT_PATH=./.certs/xxxxx-certificate.pem.crt
PRIKEY_PATH=./.certs/xxxxx-private.pem.key
ROOT_PATH=./.certs/AmazonRootCA1.pem
```

Notes:
- Recommend learning AWS IoT Core basics first.

## Running the Publisher

### Step 1: Before Running Publisher

**IMPORTANT**: This code can be ran on any device with network connectivity. Ensured AWS IoT Core is set up properly.

```bash
# Confirmed you are in the root-level directory of the project
cd {your-project-directory}
```

### Step 2: Run Publisher

```bash
# Ensured that environment variables are loaded properly
# Confirmed you are in the root-level of the project, otherwise errors.

# Run the publisher script
python ./src/aws_test/publisher_pi.py
```

You should see:
```
Connecting to xxxxx-ats.iot.us-east-2.amazonaws.com with client 'testpi'...
Connected Successfully!

Published message to topic 'led/testpi': {'status': 'ON'}
Published message to topic 'led/testpi': {'status': 'OFF'}
Published message to topic 'led/testpi': {'status': 'ON'}
Published message to topic 'led/testpi': {'status': 'OFF'}
...
```

## Running the Subscriber

**IMPORTANT**: This code can be ran on any device with network connectivity. Ensured AWS IoT Core is set up properly.

### Step 1: Before Running Subscriber

```bash
# Confirmed you are in the root-level directory of the project
cd {your-project-directory}
```

### Step 2: Run Receiver

```bash
# Ensured that environment variables are loaded properly
# Confirmed you are in the root-level of the project, otherwise errors.

# Run the publisher script
python ./src/aws_test/receiver.py
```

You should see:
```
Connecting to xxxxx-ats.iot.us-east-2.amazonaws.com with client 'laptop_subscriber'...
Connected Successfully!
Subscribing to topic 'led/testpi'...
Subscribed to: 'led/testpi'

Waiting for messages... (Press Ctrl+C to exit)

--- Message Received ---
Topic: led/testpi
Device LED Status: OFF
--- End Message ---

--- Message Received ---
Topic: led/testpi
Device LED Status: ON
--- End Message ---
...
```

## Verify the Output

### Method 1: Run Both Scripts

1. **Start the subscriber first** on your laptop/smart phone:
   ```bash
   python ./src/aws_test/receiver.py
   ```

2. **Start the publisher** on Raspberry Pi:
   ```bash
   python ./src/aws_test/publisher_pi.py
   ```

3. You should see LED status messages appearing on the subscriber terminal in real-time

### Method 2: Use AWS IoT MQTT Test Client

1. Go to **AWS IoT Core Console**
2. Click **MQTT test client** in the left sidebar
3. Click **Subscribe to a topic** tab
4. Enter topic: `led/testpi`
5. Click **Subscribe**
6. Run your publisher and watch messages appear in the AWS console

## Project Structure

**NOTE**: Code structure is subject to change. This is just a rough outline how the code should look like after setup.

### Raspberry Pi (Publisher) and Laptop/Smart Phone (Subscriber)
```
~/imu-door-classifier/
├── .venv/                    # Virtual environment
├── .certs/                    # Certificates folder
│   ├── xxxxx-certificate.pem.crt
│   ├── xxxxx-private.pem.key
│   └── AmazonRootCA1.pem
├── media/                    # IMU circuit diagram
├── src/
│   └── aws_test/            # Your AWS test code
│       ├── publisher_pi.py
│       └── receiver.py
├── .env                      # Environment variables
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Security Notes

- **Never commit certificates or `.env` files to version control**
- The policy in this guide is permissive (`iot:*`) - for production, use more restrictive policies
- Certificates should be kept secure and not shared
