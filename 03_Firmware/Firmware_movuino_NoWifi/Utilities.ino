void blink3Times()
{
  //USed when the record start
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
}
void blinkLongTimes()
{
  //Used when the record stop
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
}
