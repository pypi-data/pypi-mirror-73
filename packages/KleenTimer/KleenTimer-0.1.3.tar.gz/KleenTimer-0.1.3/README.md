<div align="center">
  <img src="https://raw.githubusercontent.com/Edenskull/KleenTimer/master/.github/_static/KleenTimer.png">
</div>

<div align="center">

[![GitHub license](https://img.shields.io/github/license/Edenskull/KleenTimer?color=blue&style=for-the-badge)](https://github.com/Edenskull/KleenTimer/blob/master/LICENSE)
![GitHub repo size](https://img.shields.io/github/repo-size/Edenskull/KleenTimer?color=green&style=for-the-badge)
![GitHub repo size](https://img.shields.io/badge/Python-3.6%20%7C%203.7-yellow?style=for-the-badge)

</div>

# Kleen-Timer
Simple python library that handle execution time of a script and display the result in many way.

## Table of contents
* [Installation](#installation)
* [Documentation](#documentation)

## Installation

You can install the module via pip :  
```pip install kleentimer```

or via wheel file [From PyPi](https://pypi.org/project/KleenTimer/#modal-close) :  
```
pip install wheel
python -m wheel install wheel_file.whl
```

## Documentation

The aim of kleentimer is to make it simple for the user to get a script made timer.  
First import it to your script : 
```PYTHON3
from kleentimer import kleentimer
```

Then you can setup the format that will be displayed at the end of the execution : 

* You got three usable variables (those are not mandatory, you can print only secondes and minutes and all possibility like that)
    * hours
    * minutes
    * secondes
```PYTHON3
kleentimer.init_timer("The script run for {hours}h {minutes}min and {secondes}sec")
```

When you want to set the start of your script you can use the function start_timer()

```PYTHON3
kleentimer.start_timer()
```

And when you want to stop the timer simply call end_timer()

```PYTHON3
kleentimer.end_timer()
```

Then the function elapsed_time() return the string formatted with the right formatting

```PYTHON3
output = kleentimer.elapsed_time()
print(output)
```

```PYTHON
>> The script run for 0h 10min and 20sec
```
