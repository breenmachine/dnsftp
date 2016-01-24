#!/bin/bash
error=';; connection timed out; no servers could be reached'
i=0
echo ''> output.b64
while :
do
  RESP=`dig +short $i.$1 TXT | cut -d'"' -f 2`
  if [ "$RESP" = "$error" ];
  then
    echo "Timeout - done"
    break
  fi
  echo -ne $RESP >> output.b64
  echo $RESP
  i=$((i+1))
done
cat output.b64 | base64 -d > output