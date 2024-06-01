+++
title = 'Botion Cube'
date = 2024-04-18T09:46:08-07:00
draft = false
[cover]
    image = "/posts/botion_cube_cover.png"
    relative = true
+++

# Botion Cube
The Botion Cube is a productivity cube that syncs with Notion. 

Feel free to play around with the 3D model below:
{{< gltf-viewer "1" "/posts/notion_cube.gltf" >}}

## Technical Details

## Flashing Firmware
Flashing firmware to the Botion Cube is done through the Micro USB Port. 

Please clone the code from here: [Botion Cube Firmware](https://github.com/abenstirling/BotionCube)

The key steps are as follows: 
```
1. Flash the filesystem to the Botion Cube (PIO)
2. Flash the firmware to the Botion Cube (ArduinoIDE)
```
First, we flash the filesystem to the Botion Cube (PIO). You click the PIO logo on the left, then click the `Upload Filesystem Image` button when having the firmware open in VSCode. 

![Botion Cube](/posts/botion_cube_1.png)

You need to have your Botion Cube plugged in, then you should see the following output in the terminal: 
```
SUCCESS: Filesystem image uploaded and flashed!
```

After you do the filesystem, we can hop into the ArduinoIDE to flash the firmware.

The following dependencies are needed: 
```
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include "SPIFFS.h"
#include <mbedtls/md5.h>
```
You can install these in the Library Manager in ArduinoIDE.

Then you can plug in the Botion Cube and flash the firmware. You should see the following output in the terminal: 
```
Success! Firmware uploaded and flashed!
```

![Botion Cube](/posts/botion_cube_2.png)


Note: there were some weird dependency issues that PIO couldn't resolve so we use ArduinoIDE to flash the firmware `MAIN.ino` to the Botion Cube.
