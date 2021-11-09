#if !defined(_MOVUINO_RECORD_MANAGER_)
#define _MOVUINO_RECORD_MANAGER_

#include <Arduino.h>
#include <SPIFFS.h>

class MovuinoRecord
{
private:
  String dirPath = "/data";
  String fileName;
  String filePath;

  File file;
  char sep = ',';
  bool initRow = false; // avoid pushdata on same row as columns definition

  long unsigned timeRecord0;
  bool isRecording = false;

  bool isEditable = false;
  bool isReadable = false;
  bool formatted;

  void initRecordFile();

public:
  MovuinoRecord();
  ~MovuinoRecord();

  void begin();

  void newRecord(String fileName_);
  void defineColumns(String cols_);
  void newRow();
  int nRow = 0;

  template <typename DataType>
  void pushData(DataType data_);
  void stop();

  int getFileNumber();

  void addNewRecord();
  void readFile();
  void writeData();

  void formatSPIFFS();
  void printStateSPIFFS();
  void listDirectory();
};

MovuinoRecord::MovuinoRecord()
{
}

MovuinoRecord::~MovuinoRecord()
{
}

void MovuinoRecord::begin()
{
  if (!SPIFFS.begin())
  {
    Serial.println("An Error has occurred while mounting SPIFFS");
  }
}

void MovuinoRecord::newRecord(String fileName_ = "untitled")
{
  /*
   * Create the file for the movuino
   */
  // add current file index
  int indx_ = this->getFileNumber();
  char indxChar_[3];
  sprintf(indxChar_, "%03d", indx_);
  this->fileName = indxChar_[0];
  this->fileName += indxChar_[1];
  this->fileName += indxChar_[2];

  // add file name
  this->fileName += "_" + fileName_;
  this->filePath = this->dirPath + "/" + this->fileName + ".txt";
  this->file = SPIFFS.open(this->filePath, "w");

  if (!this->file)
  {
    Serial.println("Error opening file for writing");
    return;
  }

  Serial.print("Success creating ");
  Serial.println(this->filePath);
  this->isRecording = true;
  this->timeRecord0 = millis();
  this->initRow = true;
  this->nRow = 0;
}

void MovuinoRecord::defineColumns(String cols_)
{
  this->file.print("time,");
  this->file.print(cols_);
  this->initRow = false;
}

void MovuinoRecord::stop()
{
  if (isRecording)
  {
    this->file.close();
    this->isRecording = false;
  }
}

void MovuinoRecord::newRow()
{
  this->file.println();
  this->file.print(millis() - this->timeRecord0);
  if(!this->initRow)
    this->initRow = true;
  this->nRow++;
}

// void MovuinoRecord::addNewRecord()
// {
//   /*
//    * Add a new record in the file ine the location filepath
//    * The separation between the 2 file is the lign "XXX_newRecord"
//    */
//   this->file = SPIFFS.open(this->filePath, "a");
//   if (!this->file)
//   {
//     Serial.println("Error opening file for writing");
//     return;
//   }
//   this->file.println("XXX_newRecord");
//   initRecordFile();
// }

void MovuinoRecord::readFile()
{
  /*
   * Read the file in the position "filepath"
   * Print a line "XXX_beginning" at the beginning and a line "XXX_end" at the end of the this->file.
   */
  this->file = SPIFFS.open(this->filePath, "r");

  if (!this->file)
  {
    Serial.println("Error opening file for reading");
    return;
  }

  Serial.println("XXX_beginning");
  String l_ = "";
  while (this->file.available())
  {
    char c_ = this->file.read();
    if (c_ != '\n')
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

// void MovuinoRecord::writeData()
// {
//   /*
//    * Write in the file in the position "filepath"
//    */
//   this->file = SPIFFS.open(this->filePath, "a");

//   if (!this->file)
//   {
//     //   digitalWrite(pinLedBat, HIGH);
//     // this->pushData();
//     Serial.println("Error opening file for writing");
//     return;
//   }

//   this->file.close();
// }

void MovuinoRecord::initRecordFile()
{
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

template <typename DataType>
void MovuinoRecord::pushData(DataType data_)
{
  // Serial.println(data_);
  if (this->isRecording)
  {
    if(!this->initRow)
      this->newRow();
    // Serial.println("writting...");
    this->file.print(this->sep);
    this->file.print(data_);
    // Serial.println("writted.");
  }
}

void MovuinoRecord::formatSPIFFS()
{
  /*
   * Formate the spiffs
   */
  bool formatted = SPIFFS.format();
  if (formatted)
  {
    Serial.println("\nSuccess formatting");
  }
  else
  {
    Serial.println("\nError formatting");
  }
}

void MovuinoRecord::printStateSPIFFS()
{
  /*
    * Get all information about SPIFFS
  */

  Serial.println("File system info");

  // Taille de la zone de fichier
  Serial.print("Total space:      ");
  Serial.print(SPIFFS.totalBytes());
  Serial.println("byte");

  // Espace total utilise
  Serial.print("Total space used: ");
  Serial.print(SPIFFS.usedBytes());
  Serial.println("byte");
  Serial.println();
}

void MovuinoRecord::listDirectory()
{
  /*
   * Print the directory of the spiffs and the size of each file
   */
  Serial.println("Listing dir :");
  File dir = SPIFFS.open(this->dirPath);
  this->file = dir.openNextFile();
  while (this->file)
  {
    Serial.print(this->file.name());
    Serial.print(" ");
    Serial.println(this->file.size());
    this->file = dir.openNextFile();
  }
  Serial.println("End of listing");
}

int MovuinoRecord::getFileNumber()
{
  int nFile_ = 0;
  File dir = SPIFFS.open(this->dirPath);
  this->file = dir.openNextFile();
  while (this->file)
  {
    nFile_++;
    this->file = dir.openNextFile();
  }
  return nFile_;
}

#endif // _MOVUINO_RECORD_MANAGER_
