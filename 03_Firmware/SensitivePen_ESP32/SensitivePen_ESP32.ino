void setup() {

}

void loop() {

}

void printMovuinoData() 
{
  /*
   * Print 9 axes data from the movuino
   */
  Serial.print(currentTime);
  Serial.print("\t ");
  Serial.print(-ax);
  Serial.print("\t ");
  Serial.print(ay);
  Serial.print("\t ");
  Serial.print(az);
  Serial.print("\t ");
  Serial.print(gx);
  Serial.print("\t ");
  Serial.print(-gy);
  Serial.print("\t ");
  Serial.print(-gz);
  Serial.print("\t ");
  Serial.print(mx);
  Serial.print("\t ");
  Serial.print(-my);
  Serial.print("\t ");
  Serial.print(-mz);
  Serial.print("\t ");
  Serial.print(pressure);
  Serial.println();
}

void formatingSPIFFS(){
  /*
   * Formate the spiffs
   */
  bool formatted = SPIFFS.format();
  if(formatted)
  {
    Serial.println("\nSuccess formatting");
  }
  else
  {
    Serial.println("\nError formatting");
  }
}

void getInfoAboutSpiff(){
      /* 
       * Get all information about SPIFFS 
       */
    // FSInfo fsInfo;
    // SPIFFS.info(fsnfo);
    
    Serial.println("File system info");
    
    // Taille de la zone de fichier
    Serial.print("Total space:      ");
    Serial.print(SPIFFS.totalBytes());
    Serial.println("byte");
    
    // Espace total utilise
    Serial.print("Total space used: ");
    //Serial.print(fsInfo.usedBytes);
    Serial.print(SPIFFS.usedBytes());
    Serial.println("byte");
 
    // Taille d un bloc et page
    /*
    Serial.print("Block size:       ");
    Serial.print(fsInfo.blockSize);
    Serial.println("byte");
 
    Serial.print("Page size:        ");
    Serial.print(fsInfo.totalBytes);
    Serial.println("byte");
 
    Serial.print("Max open files:   ");
    Serial.println(fsInfo.maxOpenFiles);
 
    // Taille max. d un chemin
    Serial.print("Max path lenght:  ");
    Serial.println(fsInfo.maxPathLength);
    */
 
    Serial.println();
}