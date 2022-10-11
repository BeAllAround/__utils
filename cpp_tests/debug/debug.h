#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <regex.h>
#include <errno.h>
#include <assert.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

static int __c  = 0;


extern void __pause();

#define newLine printf("\n");
#define BREAK printf("---LINE: %d - BREAK %d---", __LINE__, ++__c); \
		newLine; \
		__pause();
#define _print(s) printf(s); \
		newLine;

#define RESET __c = 0

#define start_time clock_t s_t_a_r_t = clock();
#define end_time printf("[Cpu_time_used: %f]\n", ((double) (clock() - s_t_a_r_t)) / CLOCKS_PER_SEC);

void __pause(){
	char s[2];
	_print("PAUSED");
	fgets(s, sizeof s, stdin);
}
