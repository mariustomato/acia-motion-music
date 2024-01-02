
const int sensorPin = 14;
void setup()
{
  pinMode(sensorPin, INPUT);
  Serial.begin(9600); //Open the serial to set the baud rate for 9600bps
}

void loop()
{
  //if(!Serial.available()); 
  int sensorValue=analogRead(sensorPin); //Connect the analog piezoelectric ceramic vibration sensor to analog interface 0
  Serial.println(sensorValue);//Print the analog value read via serial port
}