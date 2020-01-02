#include<stdio.h>
#include <stddef.h>
#include "hash_table.h"


int main(int argc, char** argv){


    ht_hash_table* ht = ht_new();
    ht_insert(ht, "key",  "val");
    ht_insert(ht, "one",  "1");
    ht_insert(ht, "key",  "1");

    ht_delete(ht, "one");

    char* s = ht_search(ht, "one");
    printf("s: %s \n", s);

    return 0;
}
