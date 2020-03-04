Dim wshshell, x, s, c
q = inputbox("Temps A Attendre (Multiplier la seconde par 1000)")
if  q = ""  Then 
wscript.quit
End if
x = 2
c = 1
Set wshshell = wscript.CreateObject("WScript.Shell")
do
s = x ^ c
wscript.sleep q
wshshell.sendkeys x  
wshshell.sendkeys " puissance "
wshshell.sendkeys c & " = " &  s
wshshell.sendkeys "{ENTER}"
if c = 10 then 
        x = x + 1
        c = 1
End if
c = c + 1
loop