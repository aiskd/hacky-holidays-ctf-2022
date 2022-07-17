#include <stdio.h>

int main()
{
    char param_1[34];
    //
    param_1[0xd] = 0x31;
    param_1[0x1f] = (char)param_1[0xd] * '\x02' + 1;
    param_1[0x16] = (char)param_1[0x1f] | 0x61 - 2;
    param_1[6] = (char)param_1[0x16] >> 1;
    *param_1 = (char)param_1[6] * '\x02' - 0x1d;
    param_1[0xf] = *param_1 ^ 5;
    param_1[3] = (char)param_1[0xf] + 0x35;
    param_1[4] = (char)param_1[3] + 0xbc;
    param_1[0x1b] = (char)param_1[4] + 0x7b * '\x02';
    param_1[0x20] = (char)param_1[4] + param_1[0xf];
    //
    param_1[0x17] = 0x39;
    param_1[0x12] = param_1[0x17] ^ 10;
    param_1[0x10] = (char)(char)param_1[0x12] >> 1 * '\x02';
    param_1[0x18] = (char)param_1[0x12] * '\x02';
    param_1[0xb] = (char)param_1[0x10] * '\x02';
    param_1[0x1a] = (char)(char)param_1[0xb] / '\x02' + 7U;
    param_1[0x1e] = (char)param_1[0x1f] - param_1[0x10];
    param_1[10] = (char)param_1[0x1e] + 7;
    param_1[0x19] = (char)param_1[0x10] + param_1[0x1a];
    param_1[0x15] = (char)param_1[0x19] >> 1;
    param_1[7] = param_1[0xb] ^ param_1[0x15];
    param_1[0x13] = (char)param_1[7] - 2;
    param_1[1] = (char)param_1[0x13] + 5;
    param_1[0x1c] = (char)param_1[1] - 0x13;
    param_1[0x1c] = (char)param_1[1] - 0x13;
    param_1[0x14] = param_1[10] ^ param_1[0x1c];
    param_1[0x11] = param_1[0x14] ^ 0x40;
    param_1[5] = (char)param_1[0x11] + 0x28;
    param_1[8] = param_1[5] ^ 7;
    param_1[2] = (char)(char)param_1[8] >> 1 + 0x13U;
    //
    param_1[0x1d] = (char)param_1[0x20] + 0xb3;
    param_1[0xc] = (char)param_1[0x1d] + param_1[9];
    param_1[0xe] = (char)param_1[0x1d] * '\x02' + 3;
    param_1[9] = (char)param_1[0xe] - 0x21;

    printf("%c", param_1[0xd]);
    printf("=== After ===\n");
    int loop2;
    for (loop2 = 0; loop2 <= 33; loop2++)
        printf("%c", param_1[loop2]);
    return 0;
}