#if !defined(_MOVUINOESP32_BUTTON_)
#define _MOVUINOESP32_BUTTON_

#include <Yabl.h>

#define PIN_BUTTON 13

unsigned long timerPress0;
bool _isPressed = false;
bool _isHold = false;
bool _isDoubleTap = false;

class MovuinoButton
{
private:
  Button button;

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
  this->button.attach(PIN_BUTTON, INPUT_PULLUP); // pin configured to pull-up mode

  this->button.callback(this->onPress, PRESS);
  this->button.callback(this->onRelease, RELEASE);
  this->button.callback(this->onHold, HOLD);
  this->button.callback(this->onDoubleTap, DOUBLE_TAP);
}

void MovuinoButton::update()
{
  _isPressed = false;
  _isDoubleTap = false;

  this->button.update();
}

void MovuinoButton::onPress()
{
  _isPressed = true;
  timerPress0 = millis();
}

void MovuinoButton::onRelease()
{
  _isHold = false;
  timerPress0 = 0;
}

void MovuinoButton::onHold()
{
  _isHold = true;
}

void MovuinoButton::onDoubleTap()
{
  _isDoubleTap = true;
}

bool MovuinoButton::isPressed()
{
  return _isPressed;
}

bool MovuinoButton::isDoubleTap()
{
  return _isDoubleTap;
}

unsigned int MovuinoButton::timeHold()
{
  unsigned int time_ = 0;
  if (_isHold)
  {
    time_ = millis() - timerPress0;
  }
  return time_;
}

#endif // _MOVUINOESP32_BUTTON_