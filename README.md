# Robit-in-python
A Robit package in python, for the [ElecFreaks](https://www.elecfreaks.com/) kit Robit.

## Code Example
```Python
from microbit import *
import Robit
from Robit import J1

item = 0
Robit.line_follow(J1)

while True:
  if Robit.left_line_follow() == 1 and Robit.right_line_follow() == 0:
    item = 1
    Robit.motorOn(3, "forward", 20)
    Robit.motorOn(4, "forward", 0)  
  elif Robit.left_line_follow() == 0 and Robit.right_line_follow() == 1:
    item = 2
    Robit.motorOn(3, "forward", 0)
    Robit.motorOn(4, "forward", 20)
    elif Robit.left_line_follow() == 0 and Robit.right_line_follow() == 0:
      item = 0
      Robit.motorOn(3, "forward", 20)
      Robit.motorOn(4, "forward", 20)
    else :
      if item == 1:
	 Robit.motorOn(3, "forward", 20)
	 Robit.motorOn(4, "forward", 0)
      elif item == 2:
	 Robit.motorOn(3, "forward", 0)
	 Robit.motorOn(4, "forward", 20) 
```

## License
MIT

## Supported targets
for BBC micro:bit (The metadata above is needed for package search.
