#include "Sensor.h"

Sensor pressSensor = Sensor(A0);

void setup()
{
  pressSensor.begin();
  Serial.begin(115200);
}
void loop()
{
  pressSensor.update();
  Serial.print(pressSensor.getSensorVal());
  Serial.print("\t");
//  Serial.print(pressSensor.getSensorMean());
//  Serial.print("\t");
  Serial.print(pressSensor.getWindowMin());
  Serial.println();
  delay(10);
}
