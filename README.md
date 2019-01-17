# AWSIoTRaspberryWorkshop

## Introduction
We are going to setup the hardware to send data about the soil moisture to the cloud.
Later on, in the second phase of the workshop, we are going to take a decision about watering the plant if needed.

Summary of the steps for measuring the soil moisture:
- setup the Raspberry PI 
- create an IoT Shadow for it in the AWS console
- create a rule to send the data to S3
- wire the soil moisture sensor to the breadboard
- write the code to read the data from the sensor
- write the code to send the data to the cloud by integrating a mqtt client
- monitor the IoT device by using the IoT core interface and visualize the data in the cloud
  

In the second phase we are going to water the plant programmatically.
Steps:
- setup the peristaltic pump
- control the pump to water programmatically

### Tools
The hardware that we are going to use in this workshop consists of:

- a Raspberry PI with Raspbian OS preinstalled
- electronic components: soil moisture sensor, ADC, relay, peristaltic pump
- display, keyboard and mouse for the raspberry PI device
- wifi internet connection

From a software point of view Software
- AWS account
- Mosquitto clients

   
##Workshop
 
### Measure soil moisture and send the data to the cloud

##### a. Setup the Raspberry PI 
1. Connect the peripherals (display, mouse and keyboard) to the Raspberry PI then plug it in. 
You should see on the display the operating system (Raspbian OS) loading.
2. On the desktop, create a folder named *soil-moisture-project* where we are going to save our files.

##### b. Create an IoT shadow for the PI
An AWS IoT Shadow is a digital representation of the a device used to both identify the device as well as help with the data acquisition in cloud.

To create an IoT shadow for the Raspberry click on the following link but first read some instructions below. This is the tutorial to follow [this aws docs link](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdk-setup.html). 
Tutorial instructions:
- At the beginning it says to got to AWS IoT, it should actually say that you should go to AWS IoT Core
- Use the name *workshopiot* to name your device.
- When downloading the root CA, click on the `RSA 20148 but key` link and copy the content in a file with the name `AmazonRootCA1.pem`.
 
After registering the Raspberry (by following the link below) we will: create an IoT shadow of the Raspberry, generate and save the certificates. 
This will create a IoT Shadow for our device - a list of APIs that we can use to put the data into the cloud. 
Before clicking the link for the tutorial below, you can read the following actions that we are going to take while doing the tutorial. 

1. Go to `Downloads` and see all the certificates downloaded. 

1.1. You should also see the root named `AmazonRootCA1.pem`.   

1.2. Create a folder called `certs` in the `soil-moisture-project` folder that you created earlier.

1.3. Go to the `downloads` folder and copy all the files inside the `certs` folder.  
 
2. Go to the `certs` folder and rename the files as described below. We do this to have common naming in the scripts that we are going to write to be easier to sync among ourselves.
2.1. Rename the file with the "x-certificate.pem.crt" extension to "raspberry-certificate.pem.crt".
2.2. Rename the file with the ".pem.key" extension to "raspberry-private.pem.key"
2.3. Make sure the root CA pem file is named "AmazonRootCA1.pem"



##### c. Create a rule to send the data to Elasticsearch

From the left hand side menu of the IoT Core page in the AWS console, go to the `Act` section and start creating a rule. Gave it a name of your choice.

- On the `Rule query statement`, select all the fields from a topic named 'soil-moisture', this is the topic name we are going to use. For the statement, have a look at the example in the line above.
- Add and configure an action to store message in an Elasticsearch domain (`Add action` button under the `Set one or more actions` section)                     
        - Click create a resource. This will open up the Elasticsearch create domain page. Gave it a name of your choice.            
        - Leave the defaults until you get to the `Network Configuration` page. 
            - Select the `Public access` configuration.
            - On the `Set the domain access policy to` dropdown select `Open access to the domain`, then click `ok`, `next` and `confirm`
        - Go back to the create rule tab. Select the Elasticsearch domain (you will need to click on the refresh icon first).        
        - Add the following values for the Elasticsearch configuration
            - id = ${newuuid()}
            - index = moisture
            - type = data                                         
        - From the roles list select the `sit_workshop_role` role and click `Configure`    

##### d. Wire up the sensor to the breadboard 
Depending on the case, you may need to use female-female wires or male-female wires.
1. Connect the two parts of the sensor to each other: the `sensor platine` to its `controller chip`. Use two wires female-female.
2. Connect the sensor to the breadboard.  
Start by connecting the pin marked VCC on the `sensor` to the 3V3 pin on the `breadboard` (GPIO Pin 1). 
Then wire up the pin marked GND on the `sensor` to any of the GND pins on the `breadboard`. 
3. Wire up the analogue output from the sensor to the input on the ADC. For this, connect A0 from the sensor to A0 on our ADC.
Then connect the ADC to the breadboard:
 * ADC VCC (V) to Raspberry Pi 3.3V
 * ADC GND (G) to Raspberry Pi GND
 * ADC SCL to Raspberry Pi SCL
 * ADC SDA to Raspberry Pi SDA
Having now all the wiring done, connect the breadboard to the Raspberry PI.
Then grab the prongs of the sensor and insert them into the plant's soil.

##### e. Write the code to read the sensor's output 
Write code to read the sensor's output.
1. Create a file called `main.py` inside the `soil-moisture-project` 
2. Use the partial code from here:  
[partial code](https://gist.github.com/bproca/ba86bac188ebd5ffa4ce4b2d8c80f014)


3. [complete code](https://gist.github.com/bproca/b7cd83ca631f31f6190982acab08b70c)
Run the script to print the output to the console. 

##### f. Write the code to send the data to the cloud
1. Create a file called `publisher.py` in the `soil-moisture-project` folder
2. [partial code](https://gist.github.com/bproca/ba86bac188ebd5ffa4ce4b2d8c80f014)
3. [complete code]()
Run the script to send the data to the cloud.

##### Visualize the data and water the plant programmatically  
In the AWS console, go to the Elasticsearch service. There, click on the domain, then on the Kibana link.
For our index
##### g. Water the plant then get the second set of probes 
1. Water the plant with a small amount of water. 
(We may need to water the plant several times during the workshop, that's why we don't want to pour lots of water at once).
2. Run the script to get the output.


##### Water the plant programmatically
a. Wire the peristaltic pump to our system.

The relay that we are going to use has two channels. We are going to use only one of them.
To wire the relay we are going to use a new type of wiring and ports called terminal screws.
1. Disconnect the Raspberry PI from the breadboard by taking out the connector band.

2. Connect the Raspberry PI to the relay:
- connect a GND pin on the Raspberry Pi to the GND pin on the relay
- connect one of the 5v pins on the Raspberry Pi to the VCC pin on the relay
- connect the GPIO 11 pin on the raspberry pi to the IN1 pin on the relay

3. Then, we are going to connect the external power supply to the relay.
- the positive end of the power supply (of the peristaltic pump) will go to COM1 (in the middle of the 3 ports)  
- the negative end of the power supply will go to the negative end of the peristaltic pump
- take a wire and connect the Normally Open port (NO1) of the relay to the positive end of the peristaltic pump


 Add the plant to the wate
