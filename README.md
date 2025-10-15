# Tokinomo Control Dashboard with Flet and Flask

This project is a **Dashboard built with Flet** to control a Tokinomo and its features via a **Raspberry Pi 5**.

![](fletdash.png)

## Features

- **Login Section:** License authentication to access the Dashboard.  
- **Feature Controls:** buttons to manage illumination, sound, and DC motor.  
- **Automatic Routine:** A button triggers the full routine in an automate way.  
- **Speed Control:** A slider adjusts the spin motor speed via PWM signals.

## Raspberry Pi Communication

The Dashboard communicates remotely with the Raspberry Pi using a **Flask server**:

1. The Dashboard sends **HTTP POST requests** with JSON data that contains button states (on/off or PWM values).  
2. The Flask server decodes the data and executes the programmed logic to:y i
   - Turn GPIOs on or off.  
   - Adjust PWM signals according to user input.

This setup enables full remote control of the Tokinomo through the Dashboard.

## Table of contents
- Requirements
- Installation
- Operation
- Project Structure
- Specs
- Troubleshooting
- Contributing

## Requirements
**Hardware**
- Functional Laptop or PC
- Raspberry pi 5
- DC Motor
- PIR Movement Sensor
- Any sound output
- Any ilumination output
- Actuator to simulate Tokinomo arm.

**Software**
- Ubuntu **v22.04**
- Flet **v0.28.3**
- Flask **v3.1.2**
- Python **v3**

## Installation
The project contains modularized scripts, so *app.py* just contains programming related to the graphic interface in flet. It also imports 2 functions from other script called *service.py*, it also contains communication info, such as the destination IP address, the buttons state to turn off or turn on a Tokinomo gadget, the slide button state to control PWM output to a DC motor, the management of HTTP POST petitions to the Rspberry via JSON and also recives JSON from the server to print the state confirmation or the state error.

The project also contains *Tokinomo.py* script that you should copy inside your desired folder in your Raspberry pi 5. The followoing script raise the Flask server, it receive the HTTP POSTOS petitions and use them with the buttons logic to make the components work via Raspberry pinout. The scripts allows to prove each component individually such as the sound, ilumination outputs such as led strips or the motor wich you can modifTy its velocity with the slide button, control the PWM output. Finally the server contains a thread that allows the user to automate the whole routine by pushing the *routine* button, the complete routine is going to work after the PIR movement sensor detect something in the area. The routine will stay working as much as the *routine* button is pushed.

So, clone this repository to start:

```bash
git clone https://github.com/aTrujillo04/Remote-Dashboard-for-Tokinomo-in-Flet
```
**Now, let's work first in the remote laptop/PC.**
First, let's create a virtual enviroment. This virtual enviroment should be created **inside this repository**, it will contain Flet. 

```bash
cd /route/to/this/repository
python3 -m venv virtual_enviroment_name
source virtual_enviroment_name/bin/activate
```
The previous lines place you in the repository location inside your computer, create your virtual enviroment and activate it. When the virtual enviroment is activated you should see something like this:
**(.virtual_enviroment_name) user@computer:~/route/to/repository$**

Now let's download Flet **inside the new virtual enviroment** and verify it installation by seeing the downloaded version:

```bash
pip install flet
pip show flet
```
You should be able to see something like this: **Flet vX.X.X**
Then, you wil be able to visualize the graphic interface by entering the following command in the terminal:

```bash
python3 app.py
```
First, you will see a login section wich you can pass by writting as user: *adm* and for password: *1*. Although you will see the Tokinomo dashboard and push the buttons, none of them will work because the missing Flask server in the Raspberry. So now **in the Raspberry** you will create a new folder and inside this copy and paste the [Tokinomo.txt] (Tokinomo.txt) content.
In addition, a virtual enviroment should be created and activated inside the same folder:

```bash
cd /route/to/this/repository
python3 -m venv virtual_enviroment_name
source virtual_enviroment_name/bin/activate
```
Then, when the virtual enviroment is activated, you must download Flask and verify its installation like this:

```bash
pip install flask
python3 -m flask --version
```
You should be able to se something like this: **Flask vX.X.X** 









