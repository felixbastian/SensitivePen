#if !defined(_MOVUINOESP32_BUTTON_)
#define _MOVUINOESP32_BUTTON_

#include <Yabl.h>

#define PIN_BUTTON 13

class MovuinoButton
{
private:
    Button button;
    bool buttonHold = false;
    bool buttonPressed = false;
    bool doubleTap = false;
    float startPush;
public:
    MovuinoButton(/* args */);
    ~MovuinoButton();

    #define PIN_BUTTON 13

};

MovuinoButton::MovuinoButton(/* args */)
{
    this->button.attach(PIN_BUTTON, INPUT_PULLUP); // pin configured to pull-up mode

    this->button.callback(this->onButtonPress, PRESS);
    this->button.callback(this->onButtonRelease, RELEASE);
    this->button.callback(this->onButtonHold, HOLD);
    this->button.callback(this->onButtondoubleTap, DOUBLE_TAP);
}

MovuinoButton::~MovuinoButton()
{
}

void MovuinoButton::onButtonPress() {
//   digitalWrite(pinLedESP, HIGH);
  this->buttonPressed = true;
  this->startPush = millis();
}

void MovuinoButton::onButtonRelease() {
  //digitalWrite(pinLedESP, LOW);
  this->buttonHold = false;
  this->buttonPressed = false;
  this->startPush = 0;
}

void MovuinoButton::onButtonHold() {
  this->buttonHold = true;
}

void MovuinoButton::onButtonthis->doubleTap(){
  this->doubleTap = true;
}

#endif // _MOVUINOESP32_BUTTON_