/*
  SlidingWindowFilter.h
  Copyright (c) 2013 Phillip Schmidt.  All right reserved.

  !!! All data must be type INT.  !!!
*/

#ifndef SlidingWindowFilter_h

#define SlidingWindowFilter_h

class SlidingWindowFilter
{

  public:
    SlidingWindowFilter(byte size, int seed);
    int in(int value);
    int out();


    //private:
    byte filterWindowSize;  // number of samples in sliding window
    byte OldestDataPoint; // oldest data point location
    byte shiftOffset;

    int * DataList;     // array for data
    int currentResult;    // most recent result

    long dataSum;       // total of all current samples
};

#endif

//-------------------------------------------------------
//-------------------------------------------------------
//-------------------------------------------------------

int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

#define N 100
int dataCollect[N];
int curIndex = 0;
float curMean = 0.0f;
float oldMean = 0.0f;

#define WINDOW 1000
int indxWindw = 0;
float minWindw = 1024;
float maxWindw = 0;
float curMinWindow = 0;
float curMaxWindow = 1024;
float curMeanWindow = 512;
float oldRangeWindow = 512;

long timePrint0 = 0;
int dlyPrint = 10;

boolean isPress = false;


//--------------------------------------
float last_filtered_value = 0.0f;

// SlidingWindowFilter slidWindFilt = SlidingWindowFilter(10, 10);
//--------------------------------------

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  // init data collection
  for (int i = 0; i < N; i++) {
    dataCollect[i] = 0;
  }
}

void loop() {
  // update index
  if (curIndex < N && curIndex >= 0) {
    curIndex++;
  }
  else {
    curIndex = 0;
  }

  // update data collection
  dataCollect[curIndex] = analogRead(sensorPin);

  // get moving mean
  oldMean = curMean;
  curMean = 0.0f;
  for (int i = 0; i < N; i++) {
    curMean += dataCollect[i];
  }
  curMean /= N;

  // update window
  if (indxWindw < WINDOW) {
    indxWindw++;
    if (curMean < minWindw) {
      minWindw = curMean;
    }
    if (curMean > maxWindw) {
      maxWindw = curMean;
      curMaxWindow = maxWindw; // TEST CUSTOM
      curMeanWindow = (curMinWindow + curMaxWindow) / 2.0; // TEST CUSTOM
    }
  }
  else {
    // update new thresholds
    curMinWindow = minWindw;
    curMaxWindow = maxWindw;
    curMeanWindow = (curMinWindow + curMaxWindow) / 2.0;

    // reset
    indxWindw = 0;
    minWindw = 1024;
    maxWindw = 0;
  }

  // TEST THRESHOLDS
  if (!isPress) {
    if (oldMean <= curMaxWindow && curMean >= curMaxWindow) {
      isPress = true;
    }
  } else {
    if (oldMean >= curMeanWindow && curMean <= curMeanWindow) {
      isPress = false;
    }
  }

  // ---------------------------------------------
  // float filtered_value = 0.996 * (last_filtered_value + dataCollect[curIndex] - dataCollect[curIndex-1]);
  // float filtered_value = last_filtered_value + 0.004 * (dataCollect[curIndex] - dataCollect[curIndex-1]);
  float filtered_value = 0.969 * last_filtered_value + 0.0155 * dataCollect[curIndex] + 0.0155 * dataCollect[curIndex - 1];
  last_filtered_value = filtered_value;

  // slidWindFilt.in(dataCollect[curIndex]);

  // ---------------------------------------------

  isPress = false;
  if (curMaxWindow - curMinWindow + oldRangeWindow / 2. > 25.0 && curMean > curMeanWindow) {
    isPress = true;
  }
  oldRangeWindow = curMaxWindow - curMinWindow ;

  if (millis() - timePrint0 > dlyPrint) {
    //    Serial.print(curMean);
    //    Serial.print('\t');
    //    Serial.print(185);
    //    Serial.print('\t');
    //    Serial.print(204);
    //    Serial.print('\t');
    //        Serial.print(curMaxWindow - curMinWindow + oldRangeWindow / 2.);
    //        oldRangeWindow = curMaxWindow - curMinWindow ;
    //    Serial.print('\t');
    //    Serial.print(curMinWindow);
    //    Serial.print('\t');
    //    Serial.print(curMaxWindow);
    //    Serial.print('\t');
    //    Serial.print(curMeanWindow);
    //    Serial.print('\t');
    if (isPress) {
      Serial.print(700);
    } else {
      Serial.print(600);
    }
    Serial.println("");
    // analogWrite(ledPin, curMean);
    timePrint0 = millis();
  }
}
