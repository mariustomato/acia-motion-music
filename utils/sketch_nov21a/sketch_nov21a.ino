// Define the pin where the sensor is connected
//const int sensorPin = 14;
//
//void setup() {
//  // Initialize the sensor pin as an input
//  pinMode(sensorPin, INPUT);
//
//  // Begin serial communication at 9600 baud rate
//  Serial.begin(115200);
//}
//
//void loop() {
//  // Read the sensor value7
//  while (!Serial.available()); 
//  int sensorValue = analogRead(sensorPin);
//
//  // Print the sensor value to the Serial Monitor
//  Serial.println(sensorValue);
//}
const int sensorPin = 14;
void setup()
{
  pinMode(sensorPin, INPUT);
  Serial.begin(9600); //Open the serial to set the baud rate for 9600bps
}
  void loop()
{
  while (!Serial.available()); 
  int sensorValue=analogRead(sensorPin); //Connect the analog piezoelectric ceramic vibration sensor to analog interface 0
  Serial.println(sensorValue);//Print the analog value read via serial port
}