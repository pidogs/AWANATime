

#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>

#define PIN_IN 21
#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define direction "in"

#define MAX_BUF 64

const uint8_t pin[6] = {13, 19, 26, 16, 20, 21};

// seting up gpio to be tested for
// wrighting gpio (BCM) number to /sys/class/gpio/export
int gpio_setup(uint8_t gpio)
{
  // setup gpio for io
  int fd, len;
  char buf[MAX_BUF], num[256];

  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/export");
  fd = open(buf, O_WRONLY);

  if (fd < 0)
  {
    perror("Error: could not wright to " SYSFS_GPIO_DIR "/export");
    return fd;
  }
  len = sprintf(num, "%d", gpio);
  write(fd, num, strlen(num) + 1);
  close(fd);

  // setup gpio for input only
  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/direction", gpio);
  fd = open(buf, O_WRONLY);

  if (fd < 0)
  {
    sprintf(num, "Error: could not wright to %s/gpio%d/direction", SYSFS_GPIO_DIR, gpio);
    perror(num);
    return fd;
  }
  write(fd, direction, strlen(direction) + 1);
  close(fd);

  return (0);
}

// opening the gpio value file to be read when ready
int gpio_open(uint8_t gpio)
{
  int fd, len;
  char buf[MAX_BUF], num[256];

  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/value", gpio);

  fd = open(buf, O_RDONLY | O_NONBLOCK);
  if (fd < 0)
  {

    sprintf(num, "Could not open gpio value of %d file", gpio);
    perror(num);
  }
  return fd;
}

// closing file
int gpio_close(int fd)
{
  return close(fd);
}

#define INT_TRUE 49 // 49 ascii for 1, 48 ascii for 0

int main(void)
{
  // time delay setup
  struct timespec tm;

  bool finished[6] = {0, 0, 0, 0, 0, 0};
  clock_t timeA;
  clock_t timeB;
  clock_t timeC;
  clock_t timeD;
  clock_t timeE;
  clock_t timeF;
  char buf[2];
  char *myTrue[1];
  // memset(*myTrue,1,sizeof(myTrue));
  // printf("%c\n",myTrue);
  // fflush(stdout);
  bool b = 0;
  int pinfile[6];
  int a = 1;
  int error = 0;

  for (uint8_t c = 0; c <= 5; c++)
  {
    gpio_setup(pin[c]);
    pinfile[c] = gpio_open(pin[c]);
  }

  uint8_t pinA = pinfile[0];
  uint8_t pinB = pinfile[1];
  uint8_t pinC = pinfile[2];
  uint8_t pinD = pinfile[3];
  uint8_t pinE = pinfile[4];
  uint8_t pinF = pinfile[5];

  clock_t begin = clock();
  uint8_t c;
  while (a <= 500000)
  {
    a++;
    error = read(pinA, buf, 2);
    lseek(pinA, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeA = clock();
    }

    error = read(pinB, buf, 2);
    lseek(pinB, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeB = clock();
    }

    error = read(pinC, buf, 2);
    lseek(pinC, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeC = clock();
    }

    error = read(pinD, buf, 2);
    lseek(pinD, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeD = clock();
    }

    error = read(pinE, buf, 2);
    lseek(pinE, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeE = clock();
    }
    
    error = read(pinF, buf, 2);
    lseek(pinF, 0, SEEK_SET);
    if (error < 0)
    {
      printf("\nSomething fails!\n");
      return -1;
    }
    if (*buf == INT_TRUE)
    {
      timeF = clock();
    }

    // for (uint8_t c = 0; c <= 5; c++){
    //   //printf("%s,", finished[c] ? "1" : "0");

    // }

    // printf("\r");
    // clock_gettie(CLOCK_REALTIME, &tm);

    // static uint64_t lasttime
  }

  printf("\nTime\n");
  //for (uint8_t c = 0; c <= 5; c++)
  //{
  //  printf("%f,", ((double)(timeME[c] - begin) / CLOCKS_PER_SEC));
  //}
  //printf("\n");

  clock_t end = clock();
  double time_spend = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("\n%f\n", time_spend);
  for (uint8_t c = 0; c <= 5; c++)
  {
    gpio_close(pinfile[c]);
  }
  return 0;
}
