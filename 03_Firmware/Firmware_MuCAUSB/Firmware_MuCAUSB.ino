#if (RAMEND < 1000)
  #define SERIAL_BUFFER_SIZE 16
#else
  #define SERIAL_BUFFER_SIZE 64
#endif

#include "MuCa_firmware_raw.h"
//MuCa
MuCa muca;

#define ROWS 6
#define COLS 4 // OU L'INVERSE (ou 4x4 pour tester)

void setup()
{
  Serial.begin(115200);
  
  // A CHANGER POUR FT5316 : initialisation de la communication
  muca.init(true); // useInterrupt ne fonctionne pas bien
  muca.useRaw = true;
  muca.calibrate(1.0);
}


void loop()
{
  if (muca.updated()) // à adapter avec librairie ft5316
  {
    for (int i = 0; i < COLS; i++) 
    {
      Serial.print("z");
      Serial.printf("%02X", i);
      Serial.print("x");
      for( int j = 0; j < ROWS; j++)
      {
        if (muca.grid[i*COLS+j] > 0)
        {
          // Serial.printf("%03X", muca.grid[i*12+j]);  
          Serial.print(muca.grid[i*COLS+j]);  
        } else {
          Serial.print(0); 
        }
        
        if (j < COLS + 1) 
        {
          Serial.print("x");
        }
      }
      Serial.println('q'); 
    }
  }
  delay(1);
}
