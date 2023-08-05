## RoboNodeJSScan

Robot Framework Library for the NodeJSScan SAST Tool

**Supports Python 3.x only**

### Currently version 1.2

### Install Instructions
* You need docker to run this program
* Install the RoboNodeJSScan Library with `pip install RoboNodeJSScan`
* Create a `.robot` file that includes the keywords used by RoboNodeJSScan Library


### Keywords

`run nodejsscan against source`

`| run nodejsscan against source  | source code path  | results path | controls (optional) |`

* source code path: where your ruby source code is located currently
* results path: where your results will be stored. A `.json` are generated as outputs