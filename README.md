## UDP Protocol

[ Instruction - 1 Byte ]
[ Payload - ????]

### Messages

* Broadcast Status - [0x0]
* Set Mode - [0x1]
  *  Solid Color - [0x10] [0xRRGGBB]
  * Color Wheel - [0x11]
  * Reflect Live Values - [0x12]
* Set Live Values (128 FTT Buckets)
  * [0x2] - [0x0000....]