#ifndef MYSQL_NAME_C
#define MYSQL_NAME_C

#include <stdio.h>
#include <string.h>
#include <mysql.h>
#include <my_global.h>
#include <my_sys.h>
#include <m_ctype.h>

typedef unsigned int uint;
uint tablename_to_filename(const char *from, char *to, uint to_length);
extern CHARSET_INFO *system_charset_info;

int
main(int argc, char* argv[]) {
    char out[1024];
    memset(out, '\0', sizeof(out));

    /* Must be initialized early for comparison of service name */
    system_charset_info= &my_charset_utf8_general_ci;
    
    if (argc != 2) {
        fprintf(stderr, "Please specify a database name\n");
        return 1;
    }
    
    tablename_to_filename(argv[1], out, sizeof(out));
    printf("%s\n", out);
      
    return 0;
}

#endif
