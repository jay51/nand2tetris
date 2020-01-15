#include "hash_table.h"

ht_hash_table* define_predefined_mem(void){

    ht_hash_table* ht = ht_new();

    ht_insert(ht,"SP","0");
    ht_insert(ht, "LCL","1");
    ht_insert(ht, "ARG","2");
    ht_insert(ht, "THIS","3");
    ht_insert(ht, "THAT","4");
    ht_insert(ht, "SCREEN","16384");
    ht_insert(ht, "KBD","24576");
    ht_insert(ht, "R0","0");
    ht_insert(ht, "R1","1");
    ht_insert(ht, "R2","2");
    ht_insert(ht, "R3","3");
    ht_insert(ht, "R4","4");
    ht_insert(ht, "R5","5");
    ht_insert(ht, "R6","6");
    ht_insert(ht, "R7","7");
    ht_insert(ht, "R8","8");
    ht_insert(ht, "R9","9");
    ht_insert(ht, "R10","10");
    ht_insert(ht, "R11","11");
    ht_insert(ht, "R12","12");
    ht_insert(ht, "R13","13");
    ht_insert(ht, "R14","14");
    ht_insert(ht, "R15","15");

    return ht;
}



ht_hash_table* define_comp(void){
    ht_hash_table* ht = ht_new();

    ht_insert(ht, "0", "0101010");
    ht_insert(ht, "1", "0111111");
    ht_insert(ht, "-1", "0111010");
    ht_insert(ht, "D", "0001100");
    ht_insert(ht, "A", "0110000");
    ht_insert(ht, "M", "1110000");
    ht_insert(ht, "!D", "0001101");
    ht_insert(ht, "!A", "0110001");
    ht_insert(ht, "!M", "1110001");
    ht_insert(ht, "-D", "0001111");
    ht_insert(ht, "-A", "0110011");
    ht_insert(ht, "-M", "1110011");
    ht_insert(ht, "D+1", "0011111");
    ht_insert(ht, "A+1", "0110111");
    ht_insert(ht, "M+1", "1110111");
    ht_insert(ht, "D-1", "0001110");
    ht_insert(ht, "A-1", "0110010");
    ht_insert(ht, "M-1", "1110010");
    ht_insert(ht, "D+A", "0000010");
    ht_insert(ht, "D+M", "1000010");
    ht_insert(ht, "D-A", "0010011");
    ht_insert(ht, "D-M", "1010011");
    ht_insert(ht, "A-D", "0000111");
    ht_insert(ht, "M-D", "1000111");
    ht_insert(ht, "D&A", "0000000");
    ht_insert(ht, "D&M", "1000000");
    ht_insert(ht, "D|A", "0010101");
    ht_insert(ht, "D|M", "1010101");

    return ht;
}



ht_hash_table* define_dest(void){

    ht_hash_table* ht = ht_new();

    ht_insert(ht, "", "000");
    ht_insert(ht, "M", "001");
    ht_insert(ht, "D", "010");
    ht_insert(ht, "MD", "011");
    ht_insert(ht, "A", "100");
    ht_insert(ht, "AM", "101");
    ht_insert(ht, "AD", "110");
    ht_insert(ht, "AMD", "111");

    return ht;
}



ht_hash_table* define_jump(void){

    ht_hash_table* ht = ht_new();

    ht_insert(ht, "", "000");
    ht_insert(ht, "JGT", "001");
    ht_insert(ht, "JEQ", "010");
    ht_insert(ht, "JGE", "011");
    ht_insert(ht, "JLT", "100");
    ht_insert(ht, "JNE", "101");
    ht_insert(ht, "JLE", "110");
    ht_insert(ht, "JMP", "111");

    return ht;
}


