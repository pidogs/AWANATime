//long lastMillis = 0;
//long loops = 0;

void setup() {
  Serial.begin(115200);
  VPORTD.DIR = 0b00000000;

  //PORTD.PIN0CTRL = B1;
  Serial.print(micros(),HEX);
  Serial.println(",S");
}

void loop() {
//  loops++;
  static uint32_t bin = 0b000000000;
  static uint32_t Prebin = 0b000000000;
  bin = VPORTD.IN+0b100000000; //set to allways send 9 bits
  if(Prebin!=bin){
    Serial.print(micros(),HEX);
    Serial.print(",");
    Serial.println(bin,HEX);
    Prebin = bin;
  }
  //Serial.println(micros());
//  if(millis() - lastMillis >= 1000){
//    lastMillis = millis();
//    //Serial.print("Loops last second:");
//    Serial.println(loops);
//    loops = 0;
//  }
}
