int sleep = 2;
const int stepPin = 3;
const int dirPin = 4;
int vooruit = 8;
int achteruit = 9;


int stap = 0;
int terug = 0;

int counter = 0;

void setup()
{
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    pinMode(vooruit, INPUT);
    pinMode(achteruit, INPUT);
    pinMode(sleep, OUTPUT);

    Serial.begin(115200);
}

uint8_t buf[50];
uint8_t cnt = 0;
uint8_t pck_ready = 0;
void loop()
{
    while(Serial.available() == 1)
    {
        buf[cnt] = Serial.read();
        //Serial.print(buf[cnt]);
        cnt++;
        if(buf[cnt-1] == '\n')
        {
            pck_ready = 1;
            cnt = 0;
        }
        
    }
    uint64_t then = 0;
    uint64_t now = 0;
    uint32_t elapsed_time = 0;

    if (pck_ready == 1)
    {
        Serial.println("MOVE CMD");
        pck_ready = 0;
        switch(buf[0])
        {
            case 'S':
                then = millis();
                digitalWrite(sleep, HIGH);
                digitalWrite(dirPin, HIGH);
                for (int x = 0; x < 1100; x++) {
                    digitalWrite(stepPin, HIGH);
                    delayMicroseconds(7000);
                    digitalWrite(stepPin, LOW);
                    delayMicroseconds(7000);
                    counter ++;
                }
                now = millis();
                elapsed_time = now - then;
                //Serial.println(elapsed_time);
                break;
            case 'R':
                then = millis();
                digitalWrite(sleep, HIGH);
                digitalWrite(dirPin, LOW);
                for (int x = 0; x < 1100; x++) {
                    digitalWrite(stepPin, HIGH);
                    delayMicroseconds(7000);
                    digitalWrite(stepPin, LOW);
                    delayMicroseconds(7000);
                    counter ++;
                }
                now = millis();
                elapsed_time = now - then;
                //Serial.println(elapsed_time);
                break;
            case 'B':
                digitalWrite(sleep, HIGH);
                digitalWrite(dirPin, LOW);
                for (int x = 0; x < counter; x++)
                {
                    digitalWrite(stepPin, HIGH);
                    delayMicroseconds(2000);
                    digitalWrite(stepPin, LOW);
                    delayMicroseconds(2000);
                }
                counter = 0;
                Serial.println("Go Back - done");
                break;
        }
    }
    else
    {
       digitalWrite(sleep, LOW);
    }
}
