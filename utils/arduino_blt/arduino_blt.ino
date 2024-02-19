#include <ArduinoBLE.h>

void setup() {
  Serial.begin(9600); // Starte die serielle Kommunikation
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("BLE initialization failed!");
    while (1);
  }

  Serial.println("BLE Central started...");
  BLE.scan(true); // start scanning for devices
}

void loop() {
  BLEDevice peripheral = BLE.available();

  if (peripheral) {
    Serial.print("Found ");
    Serial.print(peripheral.advertisedServiceUuid());
    Serial.print(" '");
    Serial.print(peripheral.localName());
    Serial.print("' ");
    Serial.print(peripheral.address());
    Serial.print(" ");
    Serial.print(peripheral.rssi());
    Serial.println(" dBm");

    // Manufacter data
    uint8_t manufacturerData[255];
    int manufacturerDataLength = peripheral.manufacturerData(manufacturerData, sizeof(manufacturerData));
    if (manufacturerDataLength > 0) {
      Serial.print("Manufacturer Data: ");
      printData(manufacturerData, manufacturerDataLength);
    }
    
    Serial.println();
  }
  sleep_ms(100);
}

void printData(const uint8_t* data, size_t length) {
  for (size_t i = 0; i < length; i++) {
    Serial.print("0x");
    if (data[i] < 0x10) {
      Serial.print("0");
    }
    Serial.print(data[i], HEX);
    Serial.print(" ");
  }
  Serial.println();
}