Dim wshshell, x
x = 2
q = inputbox("Temps A Attendre (Multiplier la seconde par 1000)")
if  q = ""  Then 
wscript.quit
End if
Set wshshell = wscript.CreateObject("WScript.Shell")
do
x = x + 1
s = x ^ 2
wscript.sleep q
wshshell.sendkeys x  
wshshell.sendkeys " au carre "
wshshell.sendkeys " = " &  s
wshshell.sendkeys "{ENTER}"
loop