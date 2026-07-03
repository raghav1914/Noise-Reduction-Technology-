//this is the working code without importing wifi module, ye direct connect krne k baad proper run ho rha h



#include <SoftwareSerial.h>

const int soundDetectorPin = A0;
const int gpsTXPin = 2;
const int gpsRXPin = 3;
const int wifiTXPin = 0;
const int wifiRXPin = 1;

volatile unsigned int pulseCount = 0; // Counter variable for the number of pulses
volatile bool counting = false;       // Flag to indicate when to start/stop counting
unsigned long previousMillis = 0;    // Variable to store the last time the pulseCount was reset
const unsigned long measurementPeriod = 1000; // Measurement period in milliseconds

SoftwareSerial gpsSerial(gpsTXPin, gpsRXPin);
SoftwareSerial wifiSerial(wifiTXPin, wifiRXPin);

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  wifiSerial.begin(9600);

  pinMode(soundDetectorPin, INPUT);

  // Set up timer interrupt for frequency measurement
  noInterrupts(); // Disable interrupts during setup
  TCCR1A = 0;     // Timer/Counter Control Register A
  TCCR1B = 0;     // Timer/Counter Control Register B

  // Set timer prescaler to 64
  TCCR1B |= (1 << CS11);
  TCCR1B |= (1 << CS10);

  // Enable Input Capture Interrupt (for detecting rising edges)
  TIMSK1 |= (1 << ICIE1);

  interrupts(); // Enable interrupts after setup
}

void loop() {
  if (millis() - previousMillis >= measurementPeriod) {
    noInterrupts(); // Disable interrupts to read pulseCount safely
    float frequency = calculateFrequency();
    pulseCount = 0; // Reset the pulse count for the next measurement period
    counting = true; // Start counting pulses again
    interrupts(); // Enable interrupts after reading pulseCount

    // Print the frequency to Serial Monitor
    Serial.print("Frequency: ");
    Serial.print(frequency);
    Serial.println(" Hz");

    // Transmit the frequency over Wi-Fi to Python
    wifiSerial.print(frequency);
    wifiSerial.print('\n'); // Add a newline character as a separator

    previousMillis = millis(); // Reset the measurement period timer
  }
}

float calculateFrequency() {
  // Calculate the frequency based on the number of pulses counted and the measurement period
  float frequency = static_cast<float>(pulseCount) / (measurementPeriod / 1000.0);
  return frequency;
}

// Interrupt Service Routine (ISR) for Input Capture Interrupt
ISR(TIMER1_CAPT_vect) {
  if (counting) {
    pulseCount++; // Increment pulse count on each rising edge of the square wave
    counting = false; // Stop counting until the measurement period ends
  }
}