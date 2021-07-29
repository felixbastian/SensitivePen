

#if (RAMEND < 1000)
  #define SERIAL_BUFFER_SIZE 16
#else
  #define SERIAL_BUFFER_SIZE 64
#endif

#include "MuCa_firmware_raw.h"


MuCa muca;

void setup()
{
  Serial.begin(115200);
  muca.init(false);
  muca.useRaw = true;
  muca.calibrate(1.0);
}

void loop()
{
      String u ="";
      u= GetRaw()+";";
      Serial.println(u);
      delay(3000);
}

String GetRaw() {
  String sFt="";
  if (muca.updated()) {
   for (int i = 0; i < ROWS_USE * NUM_COLUMNS; i++) {
      if (muca.grid[i] > 0)sFt+=muca.grid[i];
      if (i != ROWS_USE * NUM_COLUMNS - 1)
        sFt+=",";//Serial.print(",");
    }
  }
  return sFt;
}
