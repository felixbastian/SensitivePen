#if !defined(_MOVUINO_RECORD_MANAGER_)
#define _MOVUINO_RECORD_MANAGER_

#include <Arduino.h>

class MovuinoRecord
{
private:
    String fileName;
    String filePath;

    File file;
    char sep = ',';
    
    bool isEditable = false;
    bool isReadable = false;
    bool formatted;

    void initRecordFile();
    void addNewRecord();
    void readFile();
    void writeData();

public:
    MovuinoRecord(String fileName_);
    ~MovuinoRecord();

    void createFile();
    void writeInFile();
};

MovuinoRecord::MovuinoRecord(String fileName_)
{
    this->fileName = fileName_;
    this->filePath = "/data/" + this->fileName + ".txt";
}

MovuinoRecord::~MovuinoRecord()
{
}

void MovuinoRecord::createFile()
{
  /*
   * Create the file for the movuino with the filepath "filepath"
   */
  this->file = SPIFFS.open(this->filePath, "w");
 
  if (!this->file) {
    Serial.println("Error opening file for writing");
    return;
  }
  initRecordFile();
}

void MovuinoRecord::addNewRecord()
{
  /*
   * Add a new record in the file ine the location filepath
   * The separation between the 2 file is the lign "XXX_newRecord"
   */
    this->file = SPIFFS.open(this->filePath, "a");     
    if (!this->file) 
    {
      Serial.println("Error opening file for writing");
      return;
    }
    this->file.println("XXX_newRecord");
    initRecordFile();
}

void MovuinoRecord::readFile()
{
  /*
   * Read the file in the position "filepath"
   * Print a line "XXX_beginning" at the beginning and a line "XXX_end" at the end of the this->file.
   */
  this->file = SPIFFS.open(this->filepath, "r");
  
  if (!this->file) {
    Serial.println("Error opening file for reading");
    return;
  }
  
  Serial.println("XXX_beginning");
  String l_ = "";
  while(this->file.available())
  {
    char c_ = this->file.read();
    if(c_ != '\n') 
    {
        l_ += c_;
    }
    else 
    {

      if (l_.startsWith("XXX_newRecord"))
      {
          this->file.flush();
      }
      Serial.println(l_);
      l_ = "";
    }
  }
  this->file.close();
  Serial.println("XXX_end");
}

void MovuinoRecord::writeData()
{
  /*
   * Write in the file in the position "filepath"
   */
  this->file = SPIFFS.open(this->filePath, "a");
  
  if (!this->file) 
  {
    Serial.println();
    Serial.println("Error opening file for writing");
    return;
  }
  
//   digitalWrite(pinLedBat, HIGH);
  this->writeInFile()
  this->file.close();
}

void listingDir(String dirPath)
{
  /*
   * Print the directory of the spiffs and the size of each file
   */
  Serial.println("Listing dir :");
  File dir = SPIFFS.open(dirPath);
  File file = dir.openNextFile();
  while (file) 
  {
    Serial.print(file.name());
    // File f = dir.openFile("r");
    Serial.print(" ");
    Serial.println(file.size());
    
    //Serial.println(f.size());
    // f.close();

    file = dir.openNextFile();
  }
  Serial.println("End of listing");
}

void MovuinoRecord::initRecordFile() {
  this->file.print("time");
  this->file.print(this->sep);
  this->file.print("ax");
  this->file.print(this->sep);
  this->file.print("ay");
  this->file.print(this->sep);
  this->file.print("az");
  this->file.print(this->sep);
  this->file.print("gx");
  this->file.print(this->sep);
  this->file.print("gy");
  this->file.print(this->sep);
  this->file.print("gz");
  this->file.print(this->sep);
  this->file.print("mx");
  this->file.print(this->sep);
  this->file.print("my");
  this->file.print(this->sep);
  this->file.print("mz");
  this->file.print(this->sep);
  this->file.print("pressure");
  this->file.println();
}

void MovuinoRecord::writeInFile() {
  /*
   * Write in the File "file" all 9 axes data from the movuino separate by the String sep
   */
  this->file.print(1);
  this->file.print(this->sep);
  this->file.print(2);
  this->file.print(this->sep);
  this->file.print(3);
  this->file.print(this->sep);
  this->file.print(4);
  this->file.print(this->sep);
  this->file.print(5);
  this->file.print(this->sep);
  this->file.print(6);
  this->file.print(this->sep);
  this->file.print(7);
  this->file.print(this->sep);
  this->file.print(8);
  this->file.print(this->sep);
  this->file.print(9);
  this->file.print(this->sep);
  this->file.print(10);
  this->file.print(this->sep);
  this->file.print(11);
  this->file.println();
}

#endif // _MOVUINO_RECORD_MANAGER_
