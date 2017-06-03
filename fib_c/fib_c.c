#include "stdio.h"
#include "stdlib.h"
#include "string.h"

typedef unsigned long long u64;
typedef unsigned long u32;
typedef unsigned short u16;
typedef unsigned char u8;

typedef long long i64;
typedef long i32;
typedef short i16;
typedef char i8;

enum error_codes {
   RC_CODE_OK = 0,
   RC_CODE_ALLOC_FAIL,
   RC_CODE_OVERRUN
};

#define OUTPUT_BUF_SZ 4096
static double *rst_a = NULL;
static char output_buf[OUTPUT_BUF_SZ];

int alloc_rstarray( u32 count )
{
  rst_a = (double*)malloc((count + 2) * sizeof(double));
  return (rst_a == NULL) ? RC_CODE_ALLOC_FAIL: RC_CODE_OK;
}

int fib(double start_val1, double start_val2, u32 count )
{
   // will not check the value is correct or not.
   // trust the start_val
   // start_val1 is fib(n-2)
   // start_val2 is fib(n-1)
   if (alloc_rstarray(count) == RC_CODE_ALLOC_FAIL)
     return RC_CODE_ALLOC_FAIL;
   rst_a[0] = start_val1;
   rst_a[1] = start_val2;
   u32 i = 0;
   for ( ; i<count; i++ )
   {
     rst_a[i+2] = rst_a[i] + rst_a[i+1];
     // stop on overrun
     if ( rst_a[i+2] < rst_a[i+1])
        return RC_CODE_OVERRUN;
   }
   return RC_CODE_OK;
}

int show_fib( u32 count )
{
   u32 i = 0;
   u32 char_cnt = 0;
   for (; i< count + 2; i++)
   {
     if (char_cnt > OUTPUT_BUF_SZ - 96)
     {
        printf("%s", output_buf);
        memset(output_buf, 0, OUTPUT_BUF_SZ);
        char_cnt = 0;
     }
     if ( rst_a[i] < (u64)(-1))
       char_cnt += sprintf(output_buf+char_cnt, "%.0lf, ", rst_a[i]);
     else
       char_cnt += sprintf(output_buf+char_cnt, "%.16e, ", rst_a[i]);
   }
   printf("%s", output_buf);
   return RC_CODE_OK;
}
void usage (char *cmd)
{
   printf("%s: init_v1 init_v2 nsteps\n", cmd);
   printf("     where: init_v1 >= 0, init_v2 > init_v1, nsteps\n");
}
int main(int argc, char **argv)
{
   if ( argc != 4) {
     usage(argv[0]);
     return -1;
   }
   double v1 = strtof(argv[1],NULL);
   double v2 = strtof(argv[2],NULL);
   i32 nstep = strtol(argv[3],NULL, 10);
   if ( v1 < 0 || v2 < 0 || nstep < 0 || v2 < v1 || (v1 == 0 && v2 == 0))
   {
      usage(argv[0]);
      return -1;
   }
   fib(v1,v2,nstep);
   show_fib(nstep);
}
