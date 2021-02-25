# Dog feeding tracker
Answers the question of "Did anyone feed the dog yet?"

A sensor detects when the door to the dog food container is opened/closed and colors the LED to indicate when the dog was fed last:

🟢 Green indicates that the dog has been fed her breakfast / dinner (or at least that the food container has been opened within the last 8 hours)
<br>
🔴 Red indicates the dog has not been fed her current meal
<br>
🔵 Blue indicates the door is opened now, or the wire is disconnected, or the microcontroller rebooted and doesn't know the last time the door was opened. After the door has been opened for a brief period, it switches to rainbow to indicate that the timer has been reset.

![open](pics/open.jpg) ![closed](pics/closed.jpg)

Built with
* Adafruit QT Py - https://www.adafruit.com/product/4600
* Magnetic contact switch (door sensor) - https://www.adafruit.com/product/375
* 2-pin JST SM Plug + Receptacle Cable Set (optional) -https://www.adafruit.com/product/2880
* USB C Raspberry Pi Power Supply (any USB-C power supply will work here) - https://www.adafruit.com/product/4298
* Solder, cardboard, tape, hot-melt glue

![parts](pics/parts.jpg) ![soldered](pics/soldered.jpg)

Todo:
* Add a way to see exactly how long it's been and perhaps set the time
* Mount and enclose things properly

![the dog adjusting the code to get an extra meal](pics/dog-computer.jpg)

Rut roh...
