# fraud-loss-prevention

Use Meraki Vision (MV) together with ML image recognition capabilities to provide insights during retail checkout time about suspicious people and transactions, alerting the store team, helping on loss prevention.

## Business/Technical Challenge

Retail companies have every year large losses caused my theft and fraud. Some of these losses happen at the checkout. Smart monitoring of the checkout and data correlation with customer credit card transactions can potentially identify suspicious buyers and activities, bringing the attention of the store manager or security.

## Proposed Solution


The solution will encompass Cisco Meraki Cameras that will capture snapshots based on the credit card customer transactions timestamps and send it to a ML based image recognition cloud services like Amazon Rekognition. The objective of the project is to explore two use cases of image analysis: 

* Face recognition of buyers that were in the store before and had their purchases flagged as fraud. Alarm when this person is identified again in the store.
* Identify products purchased – type and quantity – and compare with the sales transaction information to determine if the transaction has a potential to be fraud. Alarm the store manager team.  

Final goal is to identify patterns and create rules that will trigger alarms for the store team to act. An integration with Webex Teams will provide realtime information for company security teams and store managers.


### Cisco Products Technologies/ Services

Our solution will leverage the following Cisco technologies

* [Meraki Cameras](https://developer.cisco.com/meraki/mv-sense/#!overview/camera-apis-breakdown)
* [Webex Teams](https://developer.webex.com/docs/api/getting-started)

### 3rd party software

* Payment APIs
* [Amazon Rekognition](https://aws.amazon.com/rekognition/?n=sn&p=sm)


## Team Members


* Marcos Alves <maralves@cisco.com> - GVE Brazil
* Lucas Pavanelli <lpavanel@cisco.com> - GVE Brazil
* Daniel Vicentini <dvicenti@cisco.com> - Partner Organization Brazil
* Flavio Correa <flcorrea@cisco.com> - EN Architecture Brazil
* Alberto Froscht <afroscht@cisco.com> - Enterprise Brazil
* Rafael Lupiano <rlupiano@cisco.com> - Enterprise Brazil



## Solution Components


<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of the components involved with this project. e.g Python /  -->


## Usage

<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of how to use the solution  -->



## Installation

How to install or setup the project for use.


## Documentation

Pointer to reference documentation for this project.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
