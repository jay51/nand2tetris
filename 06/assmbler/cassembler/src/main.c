#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<errno.h>
#include<assert.h>

#include "hash_table.h"
#include "const.h"

void read_lines(FILE* fptr, char** arr);
void get_number_lines(FILE* fptr, size_t* n);
char** process_lines(char** lines,
    int num_of_lines,
    int* line_count,
    ht_hash_table* labels,
    char** processed_lines);

void assemble_binary(FILE *out_fptr, ht_hash_table *labels, char **lines, int n_lines);
char* assemble_line(ht_hash_table *labels, char *line);



int main(int argc, char** argv){

    if(argc != 2){
        printf("no file was given!\n");
        exit(1);
    }

    printf("file: %s \n", argv[1]);
    FILE *fptr;
    if((fptr=fopen(argv[1], "r")) == NULL){
        perror("Error");
        exit(EXIT_FAILURE);
    }


    // Free lines[i] and **lines and destory ht_hash_table 
    
    size_t num_of_lines = 0;
    // get line numbers before malloc
    get_number_lines(fptr, &num_of_lines);
    int good_lines = 0;
    char **lines = (char**) malloc(num_of_lines * sizeof(char*));

    int current_free_addr = 16;
    char **processed_lines =(char**) malloc(num_of_lines * sizeof(char*)); 
    ht_hash_table* labels = ht_new();


    read_lines(fptr, lines);
    process_lines(lines, num_of_lines, &good_lines, labels, processed_lines);



    // TODO:
    // file reading and parseing is. DONE
    // write the assemble_line function
    // define instruction type and translate instruction
    // put output inside array and save output to file



    FILE *out_fptr;
    if((out_fptr=fopen("tmp", "w")) == NULL){
        perror("Error");
        exit(EXIT_FAILURE);
    }


    assemble_binary(out_fptr, labels, processed_lines, good_lines);



    /*
    ht_hash_table* ht = ht_new();
    ht_insert(ht, "key",  "val");
    ht_delete(ht, "one");
    char* s = ht_search(ht, "one");
    printf("s: %s \n", s);
    ht_hash_table* ht = define_predefined_mem();
    */
    return 0;
}



void assemble_binary(FILE *out_fptr, ht_hash_table *labels, char **lines, int n_lines){

    for(int i =0; i < n_lines; i++){
        fprintf (out_fptr, "This is line: %s\n", assemble_line(labels, lines[i]));
    }

    // Todo:
    // change assemble_line to return a string
    // take output from assemble_line and writ it to file


}



char* assemble_line(ht_hash_table *labels, char *line){

    // TODO:
    // identify instruction type (A|C)
    // if A call function process_a_instructino
    // if C call function process_c_instructino

    printf("goodline: %s \n", line);
    char* s = ht_search(labels, "loop");
    // printf("%s", s);
    return s;
}





void get_number_lines(FILE *fptr, size_t *n){
    int lines = 0;
    char *line = NULL;
    while ((getline(&line, n, fptr)) != -1) { lines++; }
    *n = lines;
    rewind(fptr);
}


void read_lines(FILE *fptr, char** arr){
    size_t n = 0;
    arr[0] = NULL;
    int i = 0;

    while ((getline(&arr[i], &n, fptr)) != -1) { i++; }
}


char** process_lines(
    char** lines,
    int num_of_lines,
    int* line_count,
    ht_hash_table* labels,
    char** processed_lines
    ){

    for(int i = 0; i < num_of_lines; i++){

        if(strncmp(lines[i], "//", 2) != 0 && strcmp(lines[i], "\r\n") != 0){
            size_t length = strlen(lines[i]);

            if(strncmp(lines[i], "(", 1) == 0){
                char buf[length];
                strncpy(buf, lines[i]+1, length-4);
                buf[length-1] = '\0';
                char *line_num = (char*) malloc(4 * sizeof(int)+1);

                sprintf(line_num, "%d", (*line_count)+1);
                ht_insert(labels, buf, line_num);
            }
            else {
                processed_lines[(*line_count)++] = strdup(lines[i]);
            }
        }
    }
}
