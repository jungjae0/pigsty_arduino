// led 및 환기팬이 아두이노의 몇 번에 연결되어 있는지 정의
int CHEAT = 5; //발열장치
int CFOG = 6; //안개분무
int CFAN = 3; //환기팬
int NHEAT = 9; //발열장치
int NFOG = 10; //안개분무
int NFAN =11; //환기팬

int FFAN = 13; //진짜 환기팬

// 사용할 함수들을 선언
// 모두 코드를 통해 아두이노(환기팬,led)로 보낼 것이므로 OUTPUT
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(CHEAT, OUTPUT);
  pinMode(CFAN, OUTPUT);
  pinMode(CFOG, OUTPUT);
  pinMode(NHEAT, OUTPUT);
  pinMode(NFAN, OUTPUT);
  pinMode(NFOG, OUTPUT);

  pinMode(FFAN, OUTPUT);
}

// LED 깜빡임 제어 - 천천히 깜빡임
void flick_slow(int pin) {
  // i++  == i = i + 1
  for (int i = 0; i < 3; i++) {
    digitalWrite(pin, HIGH);
    delay(600);
    digitalWrite(pin, LOW);
    delay(600);
  }
  digitalWrite(pin, HIGH);
}

// LED 깜빡임 제어 - 빠르게 깜빡임
void flick_fast(int pin) {
  // i++  == i = i + 1
  for (int i = 0; i < 3; i++) {
    digitalWrite(pin, HIGH);
    delay(300);
    digitalWrite(pin, LOW);
    delay(300);
  }
  digitalWrite(pin, HIGH);
}

// 각 LED의 깜빡임이 동시에 진행될 수 있도록 함수 정의
void flick_sensors(int* slow_pin, int* fast_pin) {
  int total_flick = 5;
  for (int i = 0; i < total_flick*2; i++) {
    if (i % 2 == 0) {
      for (int j = 0; j < 3; j++) {
          if (slow_pin[j] >= 0) {
            digitalWrite(slow_pin[j], HIGH);
          }
      }
    } else {
      for (int j = 0; j < 3; j++) {
          if (slow_pin[j] >= 0) {
            digitalWrite(slow_pin[j], LOW);
          }
      }
    }
    if (i < total_flick * 2) {
      for (int j = 0; j < 3; j++) {
        if (fast_pin[j] >= 0) {
          digitalWrite(fast_pin[j], HIGH);
        }
      }
    }
    delay(100);
    if (i < total_flick*2) {
      for (int j = 0; j < 3; j++) {
        if (fast_pin[j] >= 0) {
          digitalWrite(fast_pin[j], LOW);
        }
      }
    }
    delay(100);
    if (i >= total_flick*2) {
      delay(300);
    }
    if (i == total_flick*2) {
      for (int j = 0; j < 3; j++) {
        digitalWrite(fast_pin[j], HIGH);
      }
    }
  }
  for (int j = 0; j < 3; j++) {
    if (fast_pin[j] >= 0) {
      digitalWrite(fast_pin[j], HIGH);
    }
    if (slow_pin[j] >= 0) {
      digitalWrite(slow_pin[j], HIGH);
    }
  }
}

// python에서 보낸 신호에 맞게 작동할 수 있는 함수 정의
void loop() {
  if (Serial.available() > 0) {
    String strRead = Serial.readStringUntil("\n");
    int slow_pin[3] = {-1, -1, -1};
    int fast_pin[3] = {-1, -1, -1};
    // 환경제어
    // 환경제어_환기팬
    if (strRead.indexOf("CFAN-1") >= 0) {
      // digitalWrite(CFAN, HIGH);
      // delay(600);
      // digitalWrite(CFAN, LOW);
      // delay(600);
      // flick_slow(CFAN);
      slow_pin[0] = CFAN;
      digitalWrite(FFAN, HIGH);
    } else if (strRead.indexOf("CFAN-2") >= 0) {
      digitalWrite(CFAN, HIGH);
      // delay(300);
      // flick_fast(CFAN);
      fast_pin[0] = CFAN;
      digitalWrite(FFAN, HIGH);
    } else if (strRead.indexOf("CFAN-3") >= 0) {
      digitalWrite(CFAN, HIGH);
      digitalWrite(FFAN, HIGH);
    } else if (strRead.indexOf("CFAN-0") >= 0) {
      digitalWrite(CFAN, LOW);
      digitalWrite(FFAN, LOW);
    }
    // } else if (strRead.indexOf("FAN-6") >= 0) {
    //   digitalWrite(CFAN, 0);
    // } else if (strRead.indexOf("FAN-5") >= 0) {
    //   digitalWrite(CFAN, 0);
    // } else if (strRead.indexOf("FAN-4") >= 0) {
    //   digitalWrite(CFAN, 0);
    // }
    // 환경제어_발열장치등
    if (strRead.indexOf("CHEAT-1") >= 0) {
      digitalWrite(CHEAT, HIGH);
      // delay(600);
      // flick_slow(CHEAT);
      slow_pin[1] = CHEAT;
    } else if (strRead.indexOf("CHEAT-2") >= 0) {
      digitalWrite(CHEAT, HIGH);
      // flick_fast(CHEAT);
      fast_pin[1] = CHEAT;
    } else if (strRead.indexOf("CHEAT-3") >= 0) {
      digitalWrite(CHEAT, HIGH);
    } else if (strRead.indexOf("CHEAT-0") >= 0) {
      digitalWrite(CHEAT, LOW);
    }
    // 환경제어_안개분무등
    if (strRead.indexOf("CFOG-1") >= 0) {
      digitalWrite(CFOG, HIGH);
    } else if (strRead.indexOf("FOG-0") >= 0) {
      digitalWrite(CFOG, LOW);
    }

    // 미설치
    // 환경제어_환기팬
    if (strRead.indexOf("NFAN-1") >= 0) {
      digitalWrite(NFAN, HIGH);
      // delay(600);
      slow_pin[2] = NFAN;
    } else if (strRead.indexOf("NFAN-2") >= 0) {
      digitalWrite(NFAN, HIGH);
      // delay(300);
      fast_pin[2] = NFAN;
    } else if (strRead.indexOf("NFAN-3") >= 0) {
      digitalWrite(NFAN, HIGH);
    } else if (strRead.indexOf("NFAN-0") >= 0) {
      digitalWrite(NFAN, 0);
    }
    // } else if (strRead.indexOf("FAN-6") >= 0) {
    //   digitalWrite(CFAN, 0);
    // } else if (strRead.indexOf("FAN-5") >= 0) {
    //   digitalWrite(CFAN, 0);
    // } else if (strRead.indexOf("FAN-4") >= 0) {
    //   digitalWrite(CFAN, 0);
    // }
    // 환경제어_발열장치등
    if (strRead.indexOf("NHEAT-1") >= 0) {
      digitalWrite(NHEAT, HIGH);
      // delay(600);
      slow_pin[3] = NHEAT;
    } else if (strRead.indexOf("NHEAT-2") >= 0) {
      digitalWrite(NHEAT, HIGH);
      // delay(300);
      fast_pin[3] = NHEAT;
    } else if (strRead.indexOf("NHEAT-3") >= 0) {
      digitalWrite(NHEAT, HIGH);
    } else if (strRead.indexOf("NHEAT-0") >= 0) {
      digitalWrite(NHEAT, LOW);
    }
    // 환경제어_안개분무등
    if (strRead.indexOf("NFOG-1") >= 0) {
      digitalWrite(NFOG, HIGH);
    } else if (strRead.indexOf("NFOG-0") >= 0) {
      digitalWrite(NFOG, LOW);
    }
    flick_sensors(slow_pin, fast_pin);
  }
}

// void loop() {
//   // put your main code here, to run repeatedly:
//   if (Serial.available() > 0) {
//     String strRead = Serial.readStringUntil("\n"); // a\nb\nc\n  => a\n , b\n, c\n  
//     Serial.print(strRead);
//     if (strRead.indexOf("a") >= 0) {
//       digitalWrite(RED, HIGH);
//     }
//     if (strRead.indexOf("b") >= 0) {
//       digitalWrite(BLUE, HIGH);
//     }
//     if (strRead.indexOf("c") >= 0) {
//       digitalWrite(GREEN, HIGH);
//     }
//       // Serial.print(strRead);
//       delay(1000);
//       // digitalWrite(RED, LOW);
//       // delay(1000);
//       // digitalWrite(RED, HIGH);
//       // delay(500);
//       // digitalWrite(RED, LOW);
//       // delay(500);
//       // digitalWrite(GREEN, HIGH);
//       // delay(1000);
//       // digitalWrite(GREEN, LOW);
//       // delay(1000);
//       // digitalWrite(BLUE, HIGH);
//       // delay(1000);
//       // digitalWrite(BLUE, LOW);
//       // delay(1000);
//   }
//   digitalWrite(RED, LOW);
//   digitalWrite(GREEN, LOW);
//   digitalWrite(BLUE, LOW);
// }
