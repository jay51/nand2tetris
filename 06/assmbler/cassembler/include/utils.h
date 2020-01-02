#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#ifndef UTILS_FILE
#define UTILS_FILE


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// HSAH TABLE CAN HOLD MAX VALUE OF 53

typedef struct node {
    char* key;
    char* value;
} Node;

typedef struct table{
    int size;
    int count;
    Node **items;
}Table;

#define HT_PRIME_1 179
#define HT_PRIME_2 173


Node deleted_item = {NULL, NULL};
#define DELETED_ITEM deleted_item

Node* new_node(const char* k, const char* v) {
    Node* i = malloc(sizeof(Node));
    i->key = strdup(k);
    i->value = strdup(v);
    return i;
}


Table* new_table() {
    Table* ht = malloc(sizeof(Table));

    ht->size = 53;
    ht->count = 0;
    ht->items = calloc((size_t)ht->size, sizeof(Node*));
    return ht;
}


void del_node(Node* i) {
    free(i->key);
    free(i->value);
    free(i);
}


void del_table(Table* ht) {
    for (int i = 0; i < ht->size; i++) {
        Node* item = ht->items[i];
        if (item != NULL) {
            del_node(item);
        }
    }
    free(ht->items);
    free(ht);
}

int ht_hash(const char* s, const int a, const int m) {
    long hash = 0;
    const int len_s = strlen(s);
    for (int i = 0; i < len_s; i++) {
        hash += (long)pow(a, len_s - (i+1)) * s[i];
        hash = hash % m;
    }
    return (int)hash;
}


int get_hash( const char* s, const int num_buckets, const int attempt) {
    const int hash_a = ht_hash(s, HT_PRIME_1, num_buckets);
    const int hash_b = ht_hash(s, HT_PRIME_2, num_buckets);
    return (hash_a + (attempt * (hash_b + 1))) % num_buckets;
}

void insert(Table* ht, const char* key, const char* value) {
    Node* item = new_node(key, value);
    int index = get_hash(item->key, ht->size, 0);
    printf("index: %i\n", index);
    Node* cur_item = ht->items[index];
    int i = 1;
    
    while (cur_item != NULL) {
        if(cur_item != &DELETED_ITEM){
            if(strcmp(cur_item->key, key) == 0){
                del_node(cur_item);
                ht->items[index] = item;
                return;
            }
        }
        index = get_hash(item->key, ht->size, i);
        cur_item = ht->items[index];
        i++;
    } 
    ht->items[index] = item;
    ht->count++;
}


char* search(Table* ht, const char* key) {
    int index = get_hash(key, ht->size, 0);
    Node* item = ht->items[index];
    int i = 1;
    while (item != NULL) {
        if (item != &DELETED_ITEM) {
            if (strcmp(item->key, key) == 0) {
                return item->value;
            }
        }
        index = get_hash(key, ht->size, i);
        item = ht->items[index];
        i++;
    } 
    return NULL;
}



void delete(Table* ht, const char* key) {
    int index = get_hash(key, ht->size, 0);
    Node* item = ht->items[index];
    int i = 1;
    while (item != NULL) {
        if (item != &DELETED_ITEM) {
            if (strcmp(item->key, key) == 0) {
                del_node(item);
                ht->items[index] = &DELETED_ITEM;
            }
        }
        index = get_hash(key, ht->size, i);
        item = ht->items[index];
        i++;
    } 
    ht->count--;
}


#endif
