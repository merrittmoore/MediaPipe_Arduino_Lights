int ledPin = 13;  // Connect LED to digital pin 13

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char state = Serial.read();
    if (state == '1') {
      digitalWrite(ledPin, HIGH);  // Turn on LED
    } else if (state == '0') {
      digitalWrite(ledPin, LOW);   // Turn off LED
    }
  }
}
