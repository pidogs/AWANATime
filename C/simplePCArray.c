


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

const uint8_t pin[6] = {13,19,26,16,20,21};

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
  clock_t timeME[6] = {0, 0, 0, 0, 0, 0};
  char buf[2];
  char *myTrue[1];
  // memset(*myTrue,1,sizeof(myTrue));
  // printf("%c\n",myTrue);
  // fflush(stdout);
  bool b = 0;
  int pinfile[6];
  int a = 1;
  int error = 0;

  
  for (uint8_t c = 0; c <= 5; c++){
    gpio_setup(pin[c]);
    pinfile[c] = gpio_open(pin[c]);
  }

  

  
  uint8_t c;
  clock_t begin = clock();
  while (a <= 500000)
  {
    a++;
    for (c = 0; c <= 5; c++)
    {
      error = read(pinfile[c], buf, 2);
      if (error < 0)
      {
        printf("\nSomething fails!\n");
        return -1;
      }
      if(*buf == INT_TRUE){
        timeME[c]=clock();
      }
      
      lseek(pinfile[c],0,SEEK_SET);
    }
  }
    clock_t end = clock();

  printf("\nTime\n");
  for (uint8_t c = 0; c <= 5; c++){
    printf("%f,",((double)(timeME[c] - begin) / CLOCKS_PER_SEC));
  }
  printf("\n");


  double time_spend = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("\n%f\n", time_spend);
  for (uint8_t c = 0; c <= 5; c++){
    gpio_close(pinfile[c]);
  }
  return 0;
}
