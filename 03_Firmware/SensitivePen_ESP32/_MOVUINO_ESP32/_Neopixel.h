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
    int _timeBlink;

    bool _isBreathing = false;
    int _timeBreath;

public:
    MovuinoNeopixel();
    ~MovuinoNeopixel();

    void begin();
    void update();

    // Setters
    void turnOff();
    void turnOn();
    void setColor(int color_);
    void setColor(int red_, int green_, int blue_);
    void setBrightness(int bright_);
    
    // Animations
    void breathOn(int periodMs_);
    void breathOff();
    void blinkOn(int periodMs_);
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
    this->_color = this->getColor();;
    this->_timeShow0 = millis();
}

void MovuinoNeopixel::update()
{
    if (millis() - this->_timeShow0 > 20)
    {
        if(this->_isBlinking) {
            if((millis() / this->_timeBlink) % 2 == 0)
                this->_pix.setBrightness(this->_brightness);
            else this->_pix.setBrightness(0);

            if((millis() / this->_timeBlink) % 2 == 0) {
                this->setColor(255,255,0);
                Serial.println("O");
            }
            else {
                this->setColor(0,255,255);
                Serial.println("X");;
            }
            
        }

        if(this->_isBreathing) {
            float r_ = (millis() % this->_timeBreath) / (float)(this->_timeBreath);
            if((millis() / this->_timeBreath) % 2 != 0)
                r_ = 1 - r_;
            // Serial.println(ceil(this->_brightness * r_));
            this->_pix.setBrightness(ceil(this->_brightness * r_));
        }

        this->_timeShow0 = millis();
        this->_pix.show();
    }
}

// -----------------------------------------
//                SETTERS
// -----------------------------------------
void MovuinoNeopixel::turnOff() {
    this->_color = this->getColor();
    this->setColor(0);
}
void MovuinoNeopixel::turnOn() {
    this->setColor(this->_color);
}
void MovuinoNeopixel::setColor(int color_)
{
    this->_pix.setPixelColor(0, color_);
}
void MovuinoNeopixel::setColor(int red_, int green_, int blue_)
{
    this->_pix.setPixelColor(0, _pix.Color(red_, green_, blue_));
}
void MovuinoNeopixel::setBrightness(int bright_)
{
    this->_brightness = bright_;
    this->_pix.setBrightness(bright_);
}

// -----------------------------------------
//                ANIMATIONS
// -----------------------------------------
void MovuinoNeopixel::blinkOn(int periodMs_) {
    this->_timeBlink = periodMs_;
    this->_isBlinking = true;
}
void MovuinoNeopixel::blinkOff() {
    this->_isBlinking = false;
}
void MovuinoNeopixel::breathOn(int periodMs_) {
    this->_timeBreath = periodMs_;
    this->_isBreathing = true;
}
void MovuinoNeopixel::breathOff() {
    this->_isBreathing = false;
    this->_pix.setBrightness(this->_brightness);
}

// -----------------------------------------
//                GETTERS
// -----------------------------------------
int MovuinoNeopixel::getColor() {
    return this->_pix.getPixelColor(0);
}

#endif // _MOVUINO_NEOPIXEL_
