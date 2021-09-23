#ifndef DEF_SENSOR
#define DEF_SENSOR

// ----------------------------------------------------------------------
// -----------------------      CLASS DEF       -------------------------
// ----------------------------------------------------------------------

#define NRAW 40 // number of input to compute moving mean
#define NMEAN 3

class Sensor
{
public:
  Sensor(int pinSens_);   // constructor
  void begin();
  void update();
  float getSensorVal();
  float getSensorMean();
  float getWindowMin();

private:
  bool isTouched = false;
  int pinSens;
  int dataCollect[NRAW];
  float rangeDataCollect = 0;
  float meanCollect[NRAW];

  int curWindowIndex = 0;
  float meanWindow = 0.0f;
  int maxWindow = 700; //1024; // init at max ----> ??
  float threshold = 700; //1024.0f;

  bool getTouched();
};

#endif
