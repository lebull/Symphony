## UDP Protocol

[ Instruction - 1 Byte ]
[ Payload - ????]

### Messages

* Broadcast Status - [0x0]
* Set Mode - [0x1]
  *  Off - [0x10]
  * Solid Color - [0x11] [0xRRGGBB]
  * Color Wheel - [0x12]
  * Reflect Live Values -[0x13]
* Set Live Values
  * 128 FTT Buckets
  * [0x2] - [0x0000....]