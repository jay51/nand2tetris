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

char** process_lines(char** lines, int num_of_lines, int* line_count, char** processed_lines);
void assemble_binary(FILE *out_fptr, char **lines, int n_lines);

char* process_a_instruction(char *instruction);
char* process_c_instruction(char *instruction);

char* convert_to_bin(char* a);

ht_hash_table *predefined_mem; 
ht_hash_table* labels;
ht_hash_table *comp_table;
ht_hash_table *dest_table;
ht_hash_table *jump_table;
ht_hash_table *variables;

int good_lines = 0;
size_t num_of_lines = 0;
int current_free_addr = 16;



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

    predefined_mem = define_predefined_mem();
    comp_table = define_comp();
    dest_table = define_dest();
    jump_table = define_jump();
    variables = ht_new();
    labels = ht_new();
    
    // get line numbers before malloc
    get_number_lines(fptr, &num_of_lines);
    char **lines = (char**) malloc(num_of_lines * sizeof(char*));
    read_lines(fptr, lines);

    char **processed_lines =(char**) malloc(num_of_lines * sizeof(char*)); 
    process_lines(lines, num_of_lines, &good_lines, processed_lines);


    FILE *out_fptr;
    if((out_fptr=fopen("out", "wb")) == NULL){
        perror("Error");
        exit(EXIT_FAILURE);
    }

    assemble_binary(out_fptr, processed_lines, good_lines);

    // CLEAN UP
    for(int i = 0; i < num_of_lines; i++)
        free(lines[i]);

    for(int i = 0; i < good_lines; i++)
        free(processed_lines[i]);

    free(lines);
    free(processed_lines);
    ht_del_hash_table(labels);
    ht_del_hash_table(variables);

    ht_del_hash_table(comp_table);
    ht_del_hash_table(dest_table);
    ht_del_hash_table(jump_table);
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


void assemble_binary(FILE *out_fptr, char **lines, int n_lines){

    for(int i =0; i < n_lines; i++){
        char* opcode;
        if(strncmp(lines[i], "@", 1) == 0){
            opcode = process_a_instruction(lines[i]);
            fprintf (out_fptr, "0%s\n", opcode);
        } else {
            opcode = process_c_instruction(lines[i]);
            printf("instruction: %s \n", lines[i]);
            fprintf (out_fptr, "%s\n", opcode);
        }
        free(opcode);
    }
}


// DON'T START A VARIABLE WITH A NUMBER! 
char* process_a_instruction(char *instruction){

    if(!isdigit(instruction[1])){

        if(ht_search(labels, instruction+1)){
            return convert_to_bin(ht_search(labels, instruction+1));
        } else if(ht_search(predefined_mem, instruction+1)){
            return convert_to_bin(ht_search(predefined_mem, instruction+1));
        } else{
            // this is a variable, in that case we store it in the next avaliable memory addr
            if(ht_search(variables, instruction+1)){
                return convert_to_bin(ht_search(variables, instruction+1));
            }
            else {
                char *addr = (char*) malloc(6 * sizeof(char)+1);
                sprintf(addr, "%d", current_free_addr++);
                ht_insert(variables, instruction+1, addr);
                return convert_to_bin(addr);
            }
        }
        
    } else
        return convert_to_bin(instruction+1);
}


char* process_c_instruction(char *instruction){

    char comp[5];
    char dest[2];
    char jump[4];
    char* opcode = malloc(16 * sizeof(char) + 1);
    memset(comp, '\0', sizeof(comp));
    memset(dest, '\0', sizeof(dest));
    memset(jump, '\0', sizeof(jump));

    memset(opcode, '1', sizeof(char) * 3);
    opcode[3] = '\0';

    if(instruction[1] == '='){
        strncpy(dest, instruction, 1); 
        strncpy(comp, instruction+2, 3); 

        strcat(opcode, ht_search(comp_table, comp));
        strcat(opcode, ht_search(dest_table, dest));
        strcat(opcode, ht_search(jump_table, ""));
    } else {
        strncpy(comp, instruction, 1); 
        strncpy(jump, instruction+2, 3); 

        strcat(opcode, ht_search(comp_table, comp));
        strcat(opcode, ht_search(dest_table, ""));
        strcat(opcode, ht_search(jump_table, jump));
    }

    return opcode;
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


char** process_lines( char** lines, int num_of_lines, int* line_count, char** processed_lines){

    for(int i = 0; i < num_of_lines; i++){
        if(strncmp(lines[i], "//", 2) != 0 && strcmp(lines[i], "\n") != 0){
            size_t length = strlen(lines[i]);

            if(strncmp(lines[i], "(", 1) == 0){
                char *buf = malloc(sizeof(char) * length);
                memset(buf, '\0', sizeof(buf));
                strncpy(buf, lines[i]+1, length-3);

                char *line_num = (char*) malloc(6 * sizeof(char)+1);
                memset(buf, '\0', sizeof(line_num));
                sprintf(line_num, "%d", (*line_count)+1);
                ht_insert(labels, buf, line_num);

            } else {
                char *cpy = malloc(sizeof(char) * length);
                strncpy(cpy, lines[i], length-1);
                processed_lines[(*line_count)++] = cpy;

            }
        }
    }
}
