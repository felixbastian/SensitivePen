#if !defined(_MOVUINOESP32_BUTTON_)
#define _MOVUINOESP32_BUTTON_

#include <Yabl.h>

#define PIN_BUTTON 13

unsigned long __timerPress0;
bool __isPressed = false;
bool __isReleased = false;
bool __isHold = false;
bool __isDoubleTap = false;

class MovuinoButton
{
private:
  Button _button;

public:
  MovuinoButton(/* args */);
  ~MovuinoButton();

  void begin();
  void update();

  static void onPress();
  static void onRelease();
  static void onHold();
  static void onDoubleTap();

  bool isPressed();
  bool isReleased();
  bool isDoubleTap();
  unsigned int timeHold();
};

MovuinoButton::MovuinoButton(/* args */)
{
}

MovuinoButton::~MovuinoButton()
{
}

void MovuinoButton::begin()
{
  this->_button.attach(PIN_BUTTON, INPUT_PULLUP); // pin configured to pull-up mode

  this->_button.callback(this->onPress, PRESS);
  this->_button.callback(this->onRelease, RELEASE);
  this->_button.callback(this->onHold, HOLD);
  this->_button.callback(this->onDoubleTap, DOUBLE_TAP);
}

void MovuinoButton::update()
{
  __isPressed = false;
  __isReleased = false;
  __isDoubleTap = false;

  this->_button.update();
}

void MovuinoButton::onPress()
{
  __isPressed = true;
  __timerPress0 = millis();
}

void MovuinoButton::onRelease()
{
  __isReleased = true;
  __isHold = false;
}

void MovuinoButton::onHold()
{
  __isHold = true;
}

void MovuinoButton::onDoubleTap()
{
  __isDoubleTap = true;
}

bool MovuinoButton::isPressed()
{
  return __isPressed;
}

bool MovuinoButton::isReleased()
{
  return __isReleased;
}

bool MovuinoButton::isDoubleTap()
{
  return __isDoubleTap;
}

unsigned int MovuinoButton::timeHold()
{
  unsigned int time_ = 0;
  if (__isHold)
  {
    time_ = millis() - __timerPress0;
  }
  return time_;
}

#endif // _MOVUINOESP32_BUTTON_