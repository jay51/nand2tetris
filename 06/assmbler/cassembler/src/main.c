#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<errno.h>
#include<assert.h>
#include<ctype.h>

#include "hash_table.h"
#include "const.h"

void read_lines(FILE* fptr, char** arr);
void get_number_lines(FILE* fptr, size_t* n);
char** process_lines(char** lines,
    int num_of_lines,
    int* line_count,
    ht_hash_table* labels,
    char** processed_lines);

void assemble_binary(FILE *out_fptr,
    ht_hash_table *labels,
    ht_hash_table *predefined_mem,
    char **lines,
    int n_lines);

char* process_a_instruction(ht_hash_table *labels,
    ht_hash_table *predefined_mem,
    char *instruction);

char* process_c_instruction(ht_hash_table *labels, char *instruction);

char* convert_to_bin(char* a);


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

    ht_hash_table *predefined_mem = define_predefined_mem();
    // define_comp();
    // define_dest();
    // define_jump();
    

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
    process_lines(
        lines, 
        num_of_lines,
        &good_lines,
        labels,
        processed_lines);



    // TODO:
    // file reading and parseing is. DONE
    // write the assemble_line function
    // define instruction type and translate instruction
    // put output inside array and save output to file



    FILE *out_fptr;
    if((out_fptr=fopen("tmp", "wb")) == NULL){
        perror("Error");
        exit(EXIT_FAILURE);
    }


    assemble_binary(
        out_fptr,
        labels,
        predefined_mem,
        processed_lines,
        good_lines);



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


char* convert_to_bin(char* a) {
    int n = atoi(a);
    // OPCODE SIZE 16 BIT
    int binary[16];
    int i = 0;

    while (n > 0) { 
        binary[i] = n % 2; 
        n = n / 2; 
        i++; 
    }

    char* buf = malloc(i * sizeof(char) +1);
    int index = 0;

    // LOOPING BACKWARD
    for (int j = 14; j >= 0; j--){
        if(j > i-1)
            index += sprintf(&buf[index], "%d", 0);
        else
            index += sprintf(&buf[index], "%d", binary[j]);
    }

    return buf;
}



void assemble_binary(
    FILE *out_fptr,
    ht_hash_table *labels,
    ht_hash_table *predefined_mem,
    char **lines,
    int n_lines
    ){

    char* s = ht_search(labels, "loop");
    // printf("%s", s);

    for(int i =0; i < n_lines; i++){
        // TODO:
        // if C call function process_c_instructino
        if(strncmp(lines[i], "@", 1) == 0)
            fprintf (out_fptr, "0%s\n", process_a_instruction(labels, predefined_mem, lines[i]));
        // else
            // fprintf (out_fptr, "This is line: %s\n", process_c_instruction(labels, lines[i]));

    }
}


// DON'T START A LABEL WITH A NUMBER! 
char* process_a_instruction(
    ht_hash_table *labels,
    ht_hash_table *predefined_mem,
    char *instruction
    ){

    if(!isdigit(instruction[1])){

        if(ht_search(labels, instruction+1)){
            return convert_to_bin(ht_search(labels, instruction+1));
        } else if(ht_search(predefined_mem, instruction+1)){
            return convert_to_bin(ht_search(predefined_mem, instruction+1));
        } else{
            // this is a variable, in that case we store it in the next avaliable memory addr
            return "fuck you";
        }
        
    } else
        return convert_to_bin(instruction+1);
}


char* process_c_instruction(ht_hash_table *labels, char *instruction){

    if(!isdigit(*instruction))
        return "label";
    else
        return "not a label";
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

                char *buf = malloc(sizeof(char) * length);
                strncpy(buf, lines[i]+1, length-4);

                char *line_num = (char*) malloc(4 * sizeof(int)+1);
                sprintf(line_num, "%d", (*line_count)+1);
                ht_insert(labels, buf, line_num);

            } else {
                // processed_lines[(*line_count)++] = strdup(lines[i]);
                char *cpy = malloc(sizeof(char) * length);
                strncpy(cpy, lines[i], length-2);
                processed_lines[(*line_count)++] = cpy;
            }
        }
    }
}
