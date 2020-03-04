Dim wshshell, s 
s = 1
Set wshshell = wscript.CreateObject("WScript.Shell")
p = inputbox("Temps A Attendre (Multiplier la seconde par 1000)")
if  p = ""  Then 
wscript.quit
End if
do
wscript.sleep p
wshshell.sendkeys s 
wshshell.sendkeys " " & "{+}" & " "
wshshell.sendkeys s  & " = " &  s + s
wshshell.sendkeys "{ENTER}"
s = s + 1
loop