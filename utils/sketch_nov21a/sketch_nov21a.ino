// Define the pin where the sensor is connected
const int sensorPin = 14;

void setup() {
  // Initialize the sensor pin as an input
  pinMode(sensorPin, INPUT);

  // Begin serial communication at 9600 baud rate
  Serial.begin(115200);
}

void loop() {
  // Read the sensor value
  while (!Serial.available()); 
  int sensorValue = analogRead(sensorPin);

  // Print the sensor value to the Serial Monitor
  Serial.println(sensorValue);
}