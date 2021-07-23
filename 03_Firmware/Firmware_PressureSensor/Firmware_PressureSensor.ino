int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

#define N 100
int dataCollect[N];
int index = 0;
float curMean = 0.0f;
float oldMean = 0.0f;

#define WINDOW 500
int indxWindw = 0;
float minWindw = 1024;
float maxWindw = 0;
float curMinWindow = 0;
float curMaxWindow = 1024;
float curMeanWindow = 512;

long timePrint0 = 0;
int dlyPrint = 10;

boolean isPress = false;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  // init data collection
  for(int i=0; i<N; i++) {
    dataCollect[i] = 0;
  }
}

void loop() {
  // update index
  if(index < N && index >= 0) {
    index++;
  }
  else {
    index = 0;
  }

  // update data collection
  dataCollect[index] = analogRead(sensorPin);

  // get moving mean
  oldMean = curMean;
  curMean = 0.0f;
  for (int i=0; i<N;i++) {
    curMean += dataCollect[i];
  }
  curMean /= N;

  // update window
  if(indxWindw < WINDOW) {
    indxWindw++;
    if(curMean < minWindw) {
      minWindw = curMean;
    }
    if(curMean > maxWindw) {
      maxWindw = curMean;
    }
  }
  else {
    // update new thresholds
    curMinWindow = minWindw;
    curMaxWindow = maxWindw;
    curMeanWindow = (curMinWindow + curMaxWindow)/2.0;

    // reset
    indxWindw = 0;
    minWindw = 1024;
    maxWindw = 0;
  }

  // TEST THRESHOLDS
  if(!isPress) {
    if (oldMean <= curMaxWindow && curMean >= curMaxWindow) {
      isPress = true;
    }
  } else {
    if (oldMean >= curMeanWindow && curMean <= curMeanWindow) {
      isPress = false;
    }
  }
  
  if(millis() - timePrint0 > dlyPrint) {
    Serial.print(curMean);
    Serial.print('\t');
    // Serial.print(curMinWindow);
    /*Serial.print('\t');
    Serial.print(curMaxWindow);
    Serial.print('\t');
    Serial.print(curMeanWindow);*/
    /*
    Serial.print('\t');
    if(isPress) {
      Serial.print(700);
    } else {
      Serial.print(600);
    }
    */
    Serial.println("");
    analogWrite(ledPin, curMean);
    timePrint0 = millis();
  }
}
