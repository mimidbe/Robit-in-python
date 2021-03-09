# Robit in python
A Robit package in python, for the [ElecFreaks](https://www.elecfreaks.com/robit-diy-mini-smart-cars-robot-development-platform-chassis-for-micro-bit-compatible-with-mbot.html) kit Robit.

## Code Example
```Python
from microbit import *
from Robit import *

item = 0
Mbit = Robit() 
Mbit.init_line_follow("J1")

while True:
  if Mbit.left_line_follow() == 1 and Mbit.right_line_follow() == 0:
    item = 1
    Mbit.motorOn(3, "forward", 20)
    Robit.motorOn(4, "forward", 0)  
  elif Mbit.left_line_follow() == 0 and Mbit.right_line_follow() == 1:
    item = 2
    Robit.motorOn(3, "forward", 0)
    Robit.motorOn(4, "forward", 20)
  elif Mbit.left_line_follow() == 0 and Mbit.right_line_follow() == 0:
      item = 0
      Mbit.motorOn(3, "forward", 20)
      Mbit.motorOn(4, "forward", 20)
  else :
      if item == 1:
	 Mbit.motorOn(3, "forward", 20)
	 Mbit.motorOn(4, "forward", 0)
      elif item == 2:
	 Mbit.motorOn(3, "forward", 0)
	 Mbit.motorOn(4, "forward", 20) 
 
```

## License
MIT

## Supported targets
for BBC micro:bit embeded on Robit board
