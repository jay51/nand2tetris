#!/usr/bin/env python3

import os
import subprocess

# todo:
#   find all dirs and files to test
#   run assembler on *.vm file in test folder and place the result file in same dir
#   run CPUEmulator on gnerated *.asm file in test dir


if __name__ == "__main__":

    pathto_07 = os.path.abspath("..")
    pathto_emulator = "/home/jay/Downloads/nand2tetris/tools/CPUEmulator.sh"
    # pathto_assembler = "/home/jay/Downloads/nand2tetris/tools/Assembler.sh"
    pathto_assembler = "/home/jay/dev/clang/nand2tetris/06/assembler/passembler/assembler.py"
    pathto_vm_translator = "/home/jay/dev/clang/nand2tetris/07/vm-translator/python-vm-translator/vm-translator.py"

    for root, dirs, files in os.walk(pathto_07):
        if("vm-translator" not in root and files):
            vm_file = root + "/" + [f for f in files if f.endswith("vm")][0]
            tst_file = root + "/" + [f for f in files if "VM" not in f and f.endswith("tst")][0]

            try:
                stdout = subprocess.check_output([pathto_vm_translator, vm_file])
                # print(stdout)
            except subprocess.CalledProcessError as e:
                # print(e)
                print("ASSEMBLER FAILD: file %s" %vm_file)


            try:
                stdout = subprocess.check_output([pathto_emulator, tst_file])
                print(stdout.decode())
            except subprocess.CalledProcessError as e:
                # print(e)
                print("EMULATOR FAILD: file %s\n" %tst_file)




