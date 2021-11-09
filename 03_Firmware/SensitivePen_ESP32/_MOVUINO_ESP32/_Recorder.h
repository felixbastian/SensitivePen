#if !defined(_MOVUINO_RECORD_MANAGER_)
#define _MOVUINO_RECORD_MANAGER_

#include <Arduino.h>
#include <SPIFFS.h>

class MovuinoRecorder
{
private:
  String _dirPath = "/data";
  String _fileName;
  String _filePath;

  File file;
  char sep = ',';
  bool _initRow = false; // avoid pushdata on same row as columns definition
  int _nRow = 0;         // count recorded row data

  long unsigned _timeRecord0;
  bool _isRecording = false;

  bool isEditable = false;
  bool isReadable = false;
  bool formatted;

  void initRecordFile();

public:
  MovuinoRecorder();
  ~MovuinoRecorder();

  void begin();

  void newRecord(String _fileName_);
  void defineColumns(String cols_);
  void addRow();

  template <typename DataType>
  void pushData(DataType data_);
  void stop();
  bool isRecording()
  {
    return this->_isRecording;
  };

  int getFileNumber();

  void addNewRecord();
  void readAllRecords();
  void readFile(String filePath_);
  void writeData();

  void formatSPIFFS();
  void printStateSPIFFS();
  void listDirectory();
};

MovuinoRecorder::MovuinoRecorder()
{
}

MovuinoRecorder::~MovuinoRecorder()
{
}

void MovuinoRecorder::begin()
{
  if (!SPIFFS.begin())
  {
    Serial.println("An Error has occurred while mounting SPIFFS");
  }
}

void MovuinoRecorder::newRecord(String _fileName_ = "untitled")
{
  /*
   * Create the file for the movuino
   */
  // add current file index
  int indx_ = this->getFileNumber();
  char indxChar_[3];
  sprintf(indxChar_, "%03d", indx_);
  this->_fileName = indxChar_[0];
  this->_fileName += indxChar_[1];
  this->_fileName += indxChar_[2];

  // add file name
  this->_fileName += "_" + _fileName_;
  this->_filePath = this->_dirPath + "/" + this->_fileName + ".txt";
  this->file = SPIFFS.open(this->_filePath, "w");

  if (!this->file)
  {
    Serial.println("Error opening file for writing");
    return;
  }

  Serial.print("Create ");
  Serial.println(this->_filePath);
  this->_isRecording = true;
  this->_timeRecord0 = millis();
  this->_initRow = true;
  this->_nRow = 0;
  Serial.println("Start recording...");
}

void MovuinoRecorder::stop()
{
  if (_isRecording)
  {
    this->file.close();
    this->_isRecording = false;

    Serial.print("Stop recording in ");
    Serial.println(this->_filePath);
    Serial.print("Recorded ");
    Serial.print(this->_nRow);
    Serial.println(" data row(s)");
  }
}

void MovuinoRecorder::readAllRecords()
{
  File dir = SPIFFS.open(this->_dirPath);
  this->file = dir.openNextFile();
  Serial.println("XXX_beginning");
  bool isFirst_ = true;
  while (this->file)
  {
    if(!isFirst_)
      Serial.println("XXX_newRecord");
    this->readFile(this->file.name());
    this->file = dir.openNextFile();
    isFirst_ = false;
  }
  Serial.println("XXX_end");
}

void MovuinoRecorder::readFile(String filePath_)
{
  /*
   * Read the file in the position "_filepath"
   * Print a line "XXX_beginning" at the beginning and a line "XXX_end" at the end of the this->file.
   */
  this->file = SPIFFS.open(filePath_, "r");

  if (!this->file)
  {
    Serial.println("Error opening file for reading");
    return;
  }

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
      Serial.println(l_);
      l_ = "";
    }
  }
  this->file.close();
}

void MovuinoRecorder::defineColumns(String cols_)
{
  this->file.print("time,");
  this->file.print(cols_);
  this->_initRow = false;
}

void MovuinoRecorder::addRow()
{
  this->file.println();
  this->file.print(millis() - this->_timeRecord0);
  if (!this->_initRow)
    this->_initRow = true;
  this->_nRow++;
}

template <typename DataType>
void MovuinoRecorder::pushData(DataType data_)
{
  if (this->_isRecording)
  {
    if (!this->_initRow)
      this->addRow();
    this->file.print(this->sep);
    this->file.print(data_);
  }
}

void MovuinoRecorder::formatSPIFFS()
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

void MovuinoRecorder::printStateSPIFFS()
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

void MovuinoRecorder::listDirectory()
{
  /*
   * Print the directory of the spiffs and the size of each file
   */
  Serial.println("Listing dir :");
  File dir = SPIFFS.open(this->_dirPath);
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

int MovuinoRecorder::getFileNumber()
{
  int nFile_ = 0;
  File dir = SPIFFS.open(this->_dirPath);
  this->file = dir.openNextFile();
  while (this->file)
  {
    nFile_++;
    this->file = dir.openNextFile();
  }
  return nFile_;
}

#endif // _MOVUINO_RECORD_MANAGER_
