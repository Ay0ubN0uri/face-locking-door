#include<Servo.h>
#include <LiquidCrystal.h>

int D7_pin = 4;
int D6_pin = 5;
int D5_pin = 6;
int D4_pin =  7;
int EN_pin = 11;
int RS_pin = 12;
LiquidCrystal lcd(RS_pin, EN_pin, D4_pin, D5_pin, D6_pin, D7_pin);

Servo myservo;
int pos;
char d;
void setup(){
	d = "";
	Serial.begin(9600);
	Serial.println("DTHXX test");
	myservo.attach(9); 
	myservo.write(0);
	lcd.begin(16, 2);
}

void loop(){
	if (Serial.available()) {
		d = Serial.read();
		Serial.println(d);
		if (d == 'o')
		{
			Serial.println("openning the door...");
			lcd.clear();
			lcd.print("Welcome Sir!");
			lcd.setCursor(0, 1);
			lcd.print("Openning door");
			delay(300);
			for (pos = 0; pos <= 92; pos += 4)
			{
			  myservo.write(pos);
			  delay(20);
			}
			delay(5000);
			for (pos = 92; pos >= 0; pos -= 4)
			{
			  myservo.write(pos);
			  delay(20);
			}
			lcd.clear();
		}
		else{
			Serial.println("Unknown person detected");
			lcd.clear();
			lcd.print("Unknown person!");
			delay(2000);
			lcd.clear();
		}
		d = "";
	}
}