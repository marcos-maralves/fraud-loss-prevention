# Checkout Compliance (aka fraud-loss-prevention)

Use Meraki Vision (MV) Cameras APIs and embedded analytics capabilities, together with Machine Learning image analysis solutions to provide insights about suspicious people and transactions, alerting the store team and helping on loss prevention, using via Webex Teams Collaboration platform as the frontend. All the project was done using NodeRed, which requires lower coding skills, take advantage of hundreds or existent nodes and make easier to modify and evolve the project.

[Solution Presentation Video](https://cisco.box.com/s/0vlgza5l24wi1243biu379ta2aroc66s)

*Only available for Cisco employees*

## Business/Technical Challenges

Retail companies have every year large losses caused my theft and different fraud activities. Some of people involved in these losses are doing it multiple times because it's not easy to catch it and prove their involvement. A solution that can identify people when entering at the store, at the checkout and easily allow a suspect person to be flagged, could help in later visits of the same person to alert the different store teams, preventing additional losses.

This business need can be used in other verticals, for instance in Education to alert the security teams about a know suspect person that are in the school or arriving. Also it can be used to instead of detect and flag suspects, do the opposite in verticals like Hospitality or Retail Banking, to detect and flag loyal or VIP customers alerting the teams to better take care of them.


## Proposed Solution and Experience

The solution encompass Cisco Meraki (MV) Cameras that will capture snapshots during the checkout and when customers are entering the store. A ML based face recognition service, in this case Amazon Rekognition, will analyze the image captured, look for faces in the image, and if it finds, it will add the image to an Amazon S3 storage bucket (checkout bucket).

The solution built will trigger the snapshots based on a Webex Team command (checkout <transaction ID>). This is the way that we've implemented the MVP. A production solution can be triggered by credit card transaction, using the transaction ID.

Since another objective of the solution is to be able to flag in an easy way a suspect person, we also added a command in the Webex Teams to mark that a certain person / transaction is suspect (fraud <transaction ID>). When this command is issued, the image (face of the person) associated to that transaction is copied to a different S3 storage bucket (suspects bucket).

At this time we have created a database containing two types of images: checkout images and suspects images. Next checkouts will have their snapshots compared with the suspect images database, using the ML based face comparison service from Amazon Rekognition and if a similar face is detected the Webex Teams Bot will trigger an alarm.

Besides the MV Cameras REST APIs that allow us to take snapshots (latest image or based in a timestamp), they also have a MQTT interface that gives realtime information about number of people detected by the camera and an identifier of the person detected. In order to have the detection of a potential suspect before the checkout or a specific manual input, the solution will trigger a capture automatically, every time a new person is detected entering the store, detected by the camera and signaled via MQTT. This will trigger the same image comparison flow explained before and if a match is found an alert is raised at Webex Teams.

All the interface with the end user is based on Webex Teams. A bot was created with the two commands described earlier (checkout and fraud), but also with information about new checkouts, as well as the alarms when a new suspect was found, at the checkout or entering the store.


### Cisco Products Technologies/ Services

Our solution will leverage the following Cisco technologies

* [Meraki MV Cameras](https://developer.cisco.com/meraki/mv-sense/#!overview/camera-apis-breakdown)
* [Webex Teams](https://developer.webex.com/docs/api/getting-started)

### 3rd party software

Also these additional 3rd party services were used:

* [Node-Red](https://nodered.org/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/?n=sn&p=sm)

### Protocols

All the communications between the services were using:
* REST APIs
* [MQTT](http://mqtt.org/)


## Team Members

* Marcos Alves - <maralves@cisco.com> - TSS EN GVE Brazil
* Lucas Pavanelli - <lpavanel@cisco.com> - SE Brazil
* Daniel Vicentini - <dvicenti@cisco.com> - SA Partner Organization Brazil
* Flavio Correa - <flcorrea@cisco.com> - TSA EN Architecture Brazil


## Solution Components


<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of the components involved with this project. e.g Python /  -->

The solution components are:

* Cisco Meraki MV Cameras - Snapshot API, People Detection and Counting MQTT APIs
* Cisco Webex Teams - Cloud Collaboration platform used to build the Bot used as frontend.
* Amazon Rekognition - Cloud ML image analytics solution to identify faces and to compare faces.
* Amazon S3 - Cloud Storage service required to store images, were also used as a the database of images (checkout and suspects).
* Node-Red - low coding, flow based framework, multiple nodes including Meraki, Webex Teams, AWS Rekognition, AWS S3, etc are available.
* Amazon ECS - VM service running a Ubuntu, whic is where the Node-Red runs (Optional other solutions can be used).

## Usage

<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of how to use the solution  -->

To use the solution you must have the following equipment, services and API tokens:

**Cisco Meraki**

- API Key to access Meraki Dashboard and MV Cameras
- Meraki MV12 or other model that supports snapshot and analytics (MV Sense)

**Webex Teams**

- Webex Teams Bot and BotId
- Webex Teams RoomId to be used as user interface

**AWS**

- API Key with read & write Access to:
  - S3 Storage with two buckets - Storage of the snapshots used by Rekognition service
  - Rekognition - Face recognition and comparison services

**Node-Red**

- Node-Red service with access to the machine CLI

**Virtual Machine Linux-Based (Optional to host Node-Red / the app)**

- There are multiple alternatives to run Node-Red, including the installation in a Raspberry PI
- We decided to host it in a Cloud provider VM free tier, to be able to get connection from the Internet.
- If you host the Node-Red in a LAN you will need to use a service like Ngrok to get inbound connections
- Node-Red as a Service is not recommended since it usually don't let you access the CLI of the machine that is required to install some python modules and do the snapshot image handling - download from the camera and upload to the S3 bucket


## Installation

<!-- How to install or setup the project for use. -->

**Cisco Meraki:**

You need to have a least one camera to be installed at the checkout. Make sure you fix the camera in a position that the customer face can be recorded during the checkout process.
If you have a second camera, install it at the entrance of the store. This second camera will allow the automatic image recognition process and let the store teams knows about a suspect before the user is at the cashier for checkout.

Test your camera using the Meraki Dashboard, to make sure it's working an capture the image in a way that the face of the person doing checkout or entering the store can be easily recorded. The better the image captured you will increase the ML algorithm changes to correctly detect and compare a face.

At the Meraki Dashboard, copy the *Meraki Dashboard API* in a safe location. You will have to configure it at Node-Red later on. Check this [link](https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API) to know how to enable the Dashboard API step by step and get the API key.

You will also need to setup at Node-Red the Meraki *Network ID* and Meraki MV *Camera Serial Number*.
Meraki *Network ID* is only available via Meraki API.
The Meraki MV *Camera SN* can be obtained using the GUI or API.

The easier way to start with the Meraki APIs is using Postman.

[Meraki API documentation](http://postman.meraki.com/)

- *NetworkId* API Call: GET 'https://api.meraki.com/api/v0/networks/'

- *CameraSN* API Call: GET 'https://api.meraki.com/api/v0/networks//devices'


**Virtual Machine Linux-Based (to host Node-Red /  the app)**

Since the APP is built in Node-Red, you will need to first decide where to run Node-Red.
We described above some possibilities and in our case we decided to use AWS VM service (EC2) to host a Ubuntu Linux. We used the AWS ECS free tier in our tests and deployment.

1. If you don't have a AWS account, you can create it on aws.amazon.com

2. At the AWS console look for the EC2 service.

3. Follow the steps: Launch Instance -> Ubuntu (free tier eligible) -> t2.micro (free tier eligible) -> Review and Launch -> Launch.

4. At this point you will need to create a key to access the machine SSH.

5. Access the SSH when the instance is running to install the Node-Red.

You will have to run a command like this in your terminal:
*ssh -i you_key.pem ubuntu@your_instance_id.compute-1.amazonaws.com*

You can get the information about your Public IP / FQDN to access your system at the main VM description dashboard.

6. Create the directories that will store the snapshots

*#mkdir /home/ubuntu/images*

*mkdir /home/ubuntu/compare_images*

If you don't want to use these directories you will need to change it at in the Node-Red flows.

7. Install python and the required python modules:

This Ubuntu comes with Python installed. We will use Python2. Verify if it's working typing #python at the terminal. You should get Python 2.7.17 or LastTermination

*ubuntu@ip_add:~$ python
Python 2.7.17 (default, Nov  7 2019, 10:07:09)*

Now you need to install the modules requests and boto3 (AWS module) using pip:

- First install pip: *#sudo apt install python-pip*

- Install Requests python module: *#pip install requests*

- Install boto3 python module: *pip install boto3*

<!--awscli not in use today -->

8. Open the following ports for inbound connection (from Internet to this VM)
  - At AWS Console, click at the EC2 instance and at the description panel below, look for Security Groups and click in the group created automatically.

  - In the inbound tab add the following Services:
    - SSH should be created automatically
    - Add: HTTP - TCP - 80 - 0.0.0.0/0 - web
    - Add: HTTPS - TCP - 443 - 0.0.0.0/0 - secure web
    - Add: Custom TCP - 1880 - 0.0.0.0/0 - node-red
    - Add: Custom TCP - 1889 - 0.0.0.0/0 - mqtt


**Node-Red:**

Now that you have a place to host Node-Red, follow the instructions to install it.
We will give here the instructions to install it on [Ubuntu/RaspberryPi](https://nodered.org/docs/getting-started/raspberrypi) but there is documentation available to install it in other operational systems. [Node-Red Getting Started](https://nodered.org/docs/getting-started/)

1. Log into the Ubuntu VM via SSH.

2. Install Node-Red:

bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

Answer with Yes the two questions about the installation:
Are you really sure you want to do this ? [y/N] ? Y
Would you like to install the Pi-specific nodes ? [y/N] ? Y

3. Enable it to be started at the boot as a service

sudo systemctl enable nodered.service

4. Start the Node-Red service

node-red-start

5. Access Node-Red using your public IP / FQDN at port 1880 in your browser

http://your_instance_id:1880

6. Setup Node-Red http access security

It's very recommended that you setup a user/password for your Node-Red, specially because it's running with services exposed to the Internet.

For that you need to edit your setting.js file. Details available in the [Securing Node-Red Docs](https://nodered.org/docs/user-guide/runtime/securing-node-red)

Restart Node-Red after the settings: #node-red-restarted

7. Access Node-Red GUI and install the "nodes" required

Node-Red has default nodes but also hundred nodes that can be installed to reduce the ammount of coding required.

Install the following nodes:

Right Upper Menu -> Manage palette -> User Settings -> Palette -> Install -> Search and install:

*node-red-contrib-meraki-dashboard-api

node-red-contrib-spark

node-red-contrib-mqtt-broker

node-red-contrib-python-function*

After installation you should see the new nodes available at the left side of the panel.

8. Import the Node-Red Flows using the flow.json file available in github


9. Configure your setup Ids and tokens

- Webex Teams Flow tab

  Edit the node below the comments node that says "INPUT 1"

  Edit/Create a new Webex Teams Profile by creating a name like "Infobot" and your Webex Teams Bearer Token. If you don't have it go to the Webex Team install session.

  Edit the node below the comments node that says "INPUT 2"

  In the second line of the python code add your Room Id. If you don't have it go to the Webex Team install session.





**Webex Teams:**

You will need a Bot to be used as the frontend, interacting with the cashier or store manager for the different functions implemented - checkout, fraud and checkout analysis.

- Webex Teams BotId
- Webex Teams RoomId (to be used as user interface)

To create your bot please check this documentation.
[Webex Teams Bots Documentation]T(https://developer.webex.com/docs/bots)

After your import the Flows in Node-Red, you will be able to add the BotId and RoomId in to the flows and test the access there. The Webex Teams node for Node-Red will have to be imported as well as part of the Node-Red setup.

**AWS - To Continue from Here**

As described above we will need two services from Amazon: Rekognition and S3.

- Api Key with read & write Access to:
  - S3 Storage
  - Rekognition - Face Recognition and Comparison

Buckets, Region, etc

asicaws
fraudasic
transportasic





## Documentation

Pointer to reference documentation for this project.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
