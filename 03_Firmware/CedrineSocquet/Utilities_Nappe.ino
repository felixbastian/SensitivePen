void GetRaw() 
{
  
  if (muca.updated()) 
  {
    for (int i = 0; i < ROWS_USE; i++) 
    {
      Serial.print("z");
      Serial.printf("%02X", i);
      Serial.print("x");
      for( int j = 0; j < NUM_COLUMNS; j++)
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
}
