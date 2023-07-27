#!/bin/bash

ccm_log=$(ps -fea | grep ccm_log.py | grep -v grep | wc -l)

if [[ $ccm_log == 0 ]]; then
 python3 /path/al/script/main.py /var/log/lugar_donde_se_guarda_el_Log_local.log &
 echo " $(date) \| Se reinicio el logeo del archivo" >> ./info.out
fi


#crontab [cada minuto]
# * * * * * /path/al/script/script.sh
