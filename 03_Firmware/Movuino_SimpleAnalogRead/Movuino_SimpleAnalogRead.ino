#include <i2c_adc_ads7828.h>
// Analgo Input
ADS7828 device(0, SINGLE_ENDED | REFERENCE_ON | ADC_ON/*, 0x0F*/); //no mask to do find how it works
ADS7828* adc = &device;
ADS7828Channel* Analog1= adc->channel(1);

void setup() {
  Serial.begin(115200);

  //   enable I2C communication
  ADS7828::begin();
  //   adjust scaling on an individual channel basis 12 bits = 4096
  Analog1->minScale = 0;
  Analog1->maxScale = 4095;
}

void loop() {
  ADS7828::updateAll();
  Serial.println(Analog1->value(), DEC);

  delay(10);
}
