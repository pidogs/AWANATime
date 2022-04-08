# AWANA Timing system for MVBC Tucson AWANA club.

---

## Circuit

<ul>
   <li>PhotoTransistors are placed under the lanes and are pulled down at the sensor.</li>
   <li>All sensors go into comparators that are comparing the voltage of the Potentiometer.</li>
   <li>The out put of the comparators are pulled up and fed into the the arduino nano every.</li>
   <li>The starting hall effect sensor is placed on the end of the electro magnet.</li>
   <ul><li>That sensor is plugged into the phone cable.</li></ul>
</ul>

---

## Arduino

- The arduino is running PORTRead.ino which is reading the virtual port and outputted into the serial buffer.
- PORT reading is simply reading 8 pins at the same time.
- VPORT is the chip on the nano every making reading the port a one cycle operation (it go *burrr*).

---

## Raspberry pi

- Reads the buffer and calculates if the gate has stared or if the car has passed over the line.
- Displays the information on the hdmi output.
