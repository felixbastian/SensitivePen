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
        if (muca.grid[i*12+j] > 0)
        {
          Serial.printf("%03X", muca.grid[i*12+j]);  
        } else {
          Serial.printf("%03X", 0); 
        }
        
        if (j != NUM_COLUMNS - 1) 
        {
        Serial.print("x");
        }
        
      }
      Serial.print('q'); 
    }
  }
  delay(1);
}
