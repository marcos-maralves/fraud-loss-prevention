# fraud-loss-prevention aka Checkout Compliance

Use Meraki Vision (MV) Cameras APIs and embedded analytics capabilities, together with Machine Learning image analysis solutions to provide insights about suspicious people and transactions, alerting the store team and helping on loss prevention, using via Webex Teams Collaboration platform as the frontend. All the project was done using NodeRed, which requires lower coding skills, take advantage of hundreds or existent nodes and make easier to modify and evolve the project.


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

* [Meraki Cameras](https://developer.cisco.com/meraki/mv-sense/#!overview/camera-apis-breakdown)
* [Webex Teams](https://developer.webex.com/docs/api/getting-started)

### 3rd party software

* [Node-Red](https://nodered.org/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/?n=sn&p=sm)


## Team Members

* Marcos Alves <maralves@cisco.com> - TSS GVE Brazil
* Lucas Pavanelli <lpavanel@cisco.com> - SE Brazil
* Daniel Vicentini <dvicenti@cisco.com> - SA Partner Organization Brazil
* Flavio Correa <flcorrea@cisco.com> - TSA EN Architecture Brazil


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

To use the solution you must have the following equipment, services and tokens:

**Cisco Meraki**

- Api Key to access Meraki Dashboard and MV Cameras
- Meraki MV12 or other model that supports snapshot and analytics (MV Sense)

**Webex Teams**

- Webex Teams Bot Id
- Webex Teams RoomId (to be used as user interface)

**AWS**

- Api Key with read & write Access to:
  - S3 Storage
  - Rekognition - Face Recognition and Comparison

**Virtual Machine Linux-Based (to host Node-Red /the app)**

## Installation

<!-- How to install or setup the project for use. -->

**Cisco Meraki:**

You need to have a least one camera to be installed at the checkout. Make sure you fix the camera in a position that the customer face can be recorded during the checkout process.
If you have a second camera, install it at the entrance of the store. This second camera will allow the automatic image recognition process and let the store teams knows about a suspect before the user is at the cashier for checkout.

At the Meraki Dashboard, copy the Meraki API in a safe location. You will have to configure it at Node-Red later on. Check this [link](https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API) to know how to enable the Dashboard API and get the key.

You will also need to setup at Node-Red the Meraki Network ID and Meraki MV Camera SN.
Meraki Network ID is only available at the API. The Meraki MV Camera SN can be obtained using the GUI or API.
[Meraki API documentation](http://postman.meraki.com/)

- NetworkId
curl --location --request GET 'https://api.meraki.com/api/v0/networks/' \
--header 'Accept: */*' \
--data-raw ''

- CameraSN
curl --location --request GET 'https://api.meraki.com/api/v0/networks//devices' \
--header 'Accept: */*' \
--data-raw ''


**Webex Teams:**

You will need a Bot to be used as the frontend, interacting with the cashier or store manager for the different functions implemented.

- Webex Teams Bot Id
- Webex Teams RoomId (to be used as user interface)

[Webex Teams Bots Documentation]T(https://developer.webex.com/docs/bots)

**AWS - To Continue from Here**

- Api Key with read & write Access to:
  - S3 Storage
  - Rekognition - Face Recognition and Comparison

**Node-Red:**

**Virtual Machine Linux-Based (to host Node-Red /  the app)**

## Documentation

Pointer to reference documentation for this project.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
