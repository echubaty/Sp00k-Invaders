// Arduino pin numbers
const int SW_pin = 2; // digital pin connected to switch output
const int X_pin = 0; // analog pin connected to X output
const int Y_pin = 1; // analog pin connected to Y output

const int accelX = A3;
const int accelY = A4;
const int accelZ = A5;

const float VOLT_REF = 3.3 / 5.0;
const float zero_G = 512.0;
const float scale = 102.3;

void setup() {
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);
  
  Serial.begin(4800);
}

void loop() {
  Serial.print(digitalRead(SW_pin));
  Serial.print("\t");
  Serial.print(analogRead(X_pin));
  Serial.print("\t");
  Serial.print(analogRead(Y_pin));
  Serial.print("\t");

 // read the input on analog pin 0:
  int x = analogRead(accelX);
  int y = analogRead(accelY);
  int z = analogRead(accelZ);

  Serial.print((((float)(x / VOLT_REF)) - zero_G)/scale);
  Serial.print("\t");
  Serial.print((((float)(y / VOLT_REF)) - zero_G)/scale);
  Serial.print("\t");
  Serial.println((((float)(z / VOLT_REF)) - zero_G)/scale );
}
