//TODO

#define LED 2
#define BUTTON 3

#define SERIAL_RATE 9600

#define DEBOUNCE_TIME 200
#define CONNECTION_TIMEOUT 250
#define BLINK_RATE 100

//States
#define DISCONNECTED 0
#define CONNECTED 1

//Communication
const String stop_command = "STOP\r";
const String connected_command = "CONNECTED";

void stop() {
  static volatile unsigned long time = 0;

  if (millis() - time > DEBOUNCE_TIME) {
    Serial.print(stop_command);
    time = millis();
  }
}

void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  pinMode(BUTTON, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON), stop, FALLING);
  Serial.begin(SERIAL_RATE);
}

void loop() {
  static unsigned long last_connection_time = 0;
  static unsigned long last_blink_time = 0;
  static int state = DISCONNECTED;

  // Switch State
  if (Serial.available()) {
    if (Serial.readStringUntil('\r') == connected_command) {
      state = CONNECTED;
      last_connection_time = millis();
    }
  }
  if (millis() - last_connection_time > CONNECTION_TIMEOUT)
    state = DISCONNECTED;

  // Execute State
  if (state == CONNECTED)
    digitalWrite(LED, HIGH);
  else if (millis() - last_blink_time > BLINK_RATE) {
    digitalWrite(LED, !digitalRead(LED));
    last_blink_time = millis();
  }
    
}
