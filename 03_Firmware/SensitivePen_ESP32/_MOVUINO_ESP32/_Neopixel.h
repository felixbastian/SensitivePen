#if !defined(_MOVUINO_NEOPIXEL_)
#define _MOVUINO_NEOPIXEL_

#include <Adafruit_NeoPixel.h>

#define PIN_NEOPIX 15

class MovuinoNeopixel
{
private:
    Adafruit_NeoPixel _pix;
    unsigned long _timeShow0;
    int _brightness = 255;
    int _color;

    bool _isBlinking = false;
    bool _isBlinkOn = false;
    unsigned long _timeBlink0;
    int _timeBlinkOn;
    int _timeBlinkOff;
    int _nBlink;

    bool _isBreathing = false;
    float _breathIntens = 1.0f;
    int _timeBreath;

public:
    MovuinoNeopixel();
    ~MovuinoNeopixel();

    void begin();
    void update();
    void forceUpdate();

    // Setters
    void turnOff();
    void turnOn();
    void setColor(int color_);
    void setColor(int red_, int green_, int blue_);
    void setBrightness(int bright_);

    // Animations
    void breathOn(int periodMs_);
    void breathOn(int periodMs_, float intensity_);
    void breathOff();
    void blinkOn(int timeOn_);
    void blinkOn(int timeOn_, int nBlink_);
    void asyncBlinkOn(int timeOn_, int timeOff_);
    void asyncBlinkOn(int timeOn_, int timeOff_, int nBlink_);
    void blinkOff();

    // Getters
    int getColor();
};

MovuinoNeopixel::MovuinoNeopixel() : _pix(1, PIN_NEOPIX, NEO_GRB + NEO_KHZ800)
{
}

MovuinoNeopixel::~MovuinoNeopixel()
{
}

void MovuinoNeopixel::begin()
{
    this->_pix.begin();
    this->_pix.show();
    this->_color = this->getColor();
    ;
    this->_timeShow0 = millis();
}

void MovuinoNeopixel::update()
{
    if (millis() - this->_timeShow0 > 20)
    {
        if (this->_isBreathing)
        {
            float r_ = 0.5 * (1 + sin(PI * (millis() / (float)(this->_timeBreath))));
            r_ = 1 - r_ * this->_breathIntens;
            int bright_ = (int)(this->_brightness * r_);
            this->_pix.setBrightness(bright_);
            this->_pix.setPixelColor(0, this->_color); // loose color when brightness = 0
        }

        if (this->_isBlinking)
        {
            int period_ = this->_timeBlinkOn + this->_timeBlinkOff;
            unsigned long blkTime_ = millis() - this->_timeBlink0;
            int tCycle_ = blkTime_ % period_;
            if (tCycle_ < this->_timeBlinkOn)
            {
                if (!this->_isBlinkOn)
                {
                    this->_isBlinkOn = true;
                    this->turnOn();
                }
            }
            else
            {
                if (this->_isBlinkOn)
                {
                    this->_isBlinkOn = false;
                    this->turnOff();
                }
            }

            if (this->_nBlink != -1 && (blkTime_ > this->_nBlink * period_))
            {
                this->blinkOff(); // stop blinking after _nBlink cycles
            }
        }

        this->_timeShow0 = millis();
        this->_pix.show();
    }
}

void MovuinoNeopixel::forceUpdate()
{
    this->_pix.show();
}

// -----------------------------------------
//                SETTERS
// -----------------------------------------
void MovuinoNeopixel::turnOff()
{
    this->_pix.setBrightness(0);
}
void MovuinoNeopixel::turnOn()
{
    this->_pix.setBrightness(this->_brightness);
    this->_pix.setPixelColor(0, this->_color);
}
void MovuinoNeopixel::setColor(int color_)
{
    this->_color = color_;
    this->_pix.setPixelColor(0, color_);
}
void MovuinoNeopixel::setColor(int red_, int green_, int blue_)
{
    int col_ = _pix.Color(red_, green_, blue_);
    this->setColor(col_);
}
void MovuinoNeopixel::setBrightness(int bright_)
{
    this->_brightness = bright_;
    this->_pix.setBrightness(bright_);
}

// -----------------------------------------
//                ANIMATIONS
// -----------------------------------------
void MovuinoNeopixel::blinkOn(int timeOn_)
{
    this->asyncBlinkOn(timeOn_, timeOn_, -1);
}
void MovuinoNeopixel::blinkOn(int timeOn_, int nBlink_)
{
    this->asyncBlinkOn(timeOn_, timeOn_, nBlink_);
}
void MovuinoNeopixel::asyncBlinkOn(int timeOn_, int timeOff_)
{
    this->asyncBlinkOn(timeOn_, timeOff_, -1);
}
void MovuinoNeopixel::asyncBlinkOn(int timeOn_, int timeOff_, int nBlink_)
{
    if (!timeOn_)
        this->turnOff();
    else
    {
        this->_timeBlinkOn = timeOn_;
        this->_timeBlinkOff = timeOff_;
        this->_nBlink = nBlink_;
        this->_isBlinkOn = false;
        this->_timeBlink0 = millis();
        this->_isBlinking = true;
    }
}
void MovuinoNeopixel::blinkOff()
{
    this->_isBlinking = false;
    this->_pix.setBrightness(this->_brightness);
}

void MovuinoNeopixel::breathOn(int periodMs_)
{
    this->breathOn(periodMs_, 1.0f);
}
void MovuinoNeopixel::breathOn(int periodMs_, float intensity_)
{
    if (intensity_ > 1)
        intensity_ = 1;
    this->_breathIntens = abs(intensity_);
    this->_timeBreath = periodMs_;
    this->_isBreathing = true;
}
void MovuinoNeopixel::breathOff()
{
    this->_isBreathing = false;
    this->_pix.setBrightness(this->_brightness);
}

// -----------------------------------------
//                GETTERS
// -----------------------------------------
int MovuinoNeopixel::getColor()
{
    return this->_pix.getPixelColor(0);
}

#endif // _MOVUINO_NEOPIXEL_
