int value;

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available()); 
  if(Serial.readString()!="TRIG:IMM") return;
  value = analogRead(12);
  Serial.println(value);
}
