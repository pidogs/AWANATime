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

const uint8_t pin[6] = {23,24,25,27,28,29};



//seting up gpio to be tested for
//wrighting gpio (BCM) number to /sys/class/gpio/export
int gpio_setup(uint8_t gpio){
  //setup gpio for io
  int fd, len;
  char buf[MAX_BUF],num[256];

  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/export");
  fd = open(buf, O_WRONLY);

  if (fd < 0) {
    perror("Error: could not wright to " SYSFS_GPIO_DIR "/export");
    return fd;
  }
  len = sprintf(num,"%d",gpio);
  write(fd,num,strlen(num)+1);
  close(fd);


  //setup gpio for input only
  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/direction",gpio);
  fd = open(buf, O_WRONLY);

  if (fd < 0) {
    sprintf(num,"Error: could not wright to %s/gpio%d/direction",SYSFS_GPIO_DIR,gpio);
    perror(num);
    return fd;
  }
  write(fd,direction,strlen(direction)+1);
  close(fd);

  return(0);
}

//opening the gpio value file to be read when ready
int gpio_open(uint8_t gpio){
  int fd, len;
  char buf[MAX_BUF],num[256];

  len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/value", gpio);
 
  fd = open(buf, O_RDONLY | O_NONBLOCK );
  if (fd < 0) {

    sprintf(num,"Could not open gpio value of %d file",gpio);
    perror(num);
  }
  return fd;
}


//closing file
int gpio_close(int fd){
  return close(fd);
}

#define INT_TRUE 49 //49 ascii for 1, 48 ascii for 0

int main(void){
  //time delay setup
  struct timespec tm;


  char buf[2];
  char *myTrue[1];
  //memset(*myTrue,1,sizeof(myTrue));
  //printf("%c\n",myTrue);
  //fflush(stdout);
  bool b=0;
  int pinfile = 0;
  int a=1;
  int error = 0;
  
  gpio_setup(PIN_IN);
  pinfile = gpio_open(PIN_IN);

  clock_t start = clock();
  clock_t begin = clock();
  while(a<=20){
    start = clock();
    a++;
    error = read(pinfile,buf,2);

    if(error < 0) {
      printf("\nSomething fails!\n");
      return -1;
    }
    b= *buf == INT_TRUE;

    printf("%s|%d|%d\n",b? "1" : "0",clock()-start,CLOCKS_PER_SEC);

    // clock_gettie(CLOCK_REALTIME, &tm);
    // usleep(lasttime+20000-now);
    // static uint64_t lasttime
  }
  clock_t end = clock();
  double time_spend = (double)(end-begin)/CLOCKS_PER_SEC; printf("\n%f\n",time_spend);
  gpio_close(pinfile);
  return 0;
}
