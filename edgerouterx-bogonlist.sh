#!/bin/bash

runcmd="/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper"
networkgrp="Bogon_list"
networkgrptest="Test"

curl https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt  --output fullbogonlist.txt
mapfile -t arr < fullbogonlist.txt

sleep 1

#mapfile -t arr < bogoniplist.txt

$runcmd begin
$runcmd delete firewall group network-group "$networkgrp"
#printf "Network-Group $networkgrptest Deleted\n"
$runcmd commit

sleep 2

for ip in "${arr[@]}"

        do
                $runcmd set firewall group network-group "$networkgrp" network "$ip"
                #printf "Adding $ip\n"

done

$runcmd commit
$runcmd save

exit
