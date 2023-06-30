#include <BluetoothSerial.h>

BluetoothSerial SerialBT;
int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT);
  SerialBT.begin("ESP32 Bluetooth"); // Set the Bluetooth name
}

void loop() {
  if (SerialBT.available()) {
    char value = SerialBT.read();
    if (value == '1') {
      digitalWrite(ledPin, HIGH); // Turn on the LED
    } else if (value == '0') {
      digitalWrite(ledPin, LOW); // Turn off the LED
    }
  }
  delay(20);
}