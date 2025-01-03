// Blink example for testing Arduino without external hardware
// This code toggles the built-in LED on and off

void setup()
{
    // Initialize the built-in LED pin as an output
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    // Turn the LED on
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200); // Wait for 1 second

    // Turn the LED off
    digitalWrite(LED_BUILTIN, LOW);
    delay(200); // Wait for 1 second
}
