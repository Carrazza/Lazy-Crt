#!/bin/bash

#--------------Corzinhas
GREEN="\e[32m"
YELLOW='\033[1;33m'
ENDCOLOR="\e[0m"
##############################################


#------------------MAIN------------------------#

#Pegando a url e checando se o moço n esqueceu de fornecer uma url
url=$1

if [[ $url = "" ]]; then

    echo "Esqueceu o url"
    exit

fi

#-----------------------------------------------


#Criando as pastas necessarias se não tiver

if [[ ! -d "$url" ]];then

    mkdir $url
fi

if [[ ! -d "$url/aquatone" ]];then

    mkdir "$url/aquatone"
fi

#-----------------------------------------------

#Caso eu precise mudar o diretório depois já fica ai
dir="$url"
final="res.txt"

echo -e "$GREEN{-} Checando o Assetfinder $ENDCOLOR"

    assetfinder $url >> $dir/final.txt
    cat $url/assetTmp.txt | grep $1 > $url/assetTmp.txt

    #rm $url/recon/assetTmp.txt 

echo -e "$GREEN{-} Checando o Sublist3r $ENDCOLOR"

    sublist3r -d $url -o $dir/sublisterTmp.txt > /dev/null

    cat $dir/sublisterTmp.txt >> $dir/final.txt


    #amass -enum -d $url >> $url/recon/amassTmp.txt 

echo -e "$GREEN{-} Checando o crt.sh $ENDCOLOR"

crtQuery="https://crt.sh/?q=%25."$1"&output=json"

curl -s $crtQuery | jq -r '.[].name_value' >> $dir/final.txt

#deixando apenas resultados únicos 
sort -u $dir/final.txt > $dir/res.txt 

rm -r $dir/final.txt
rm -r $dir/sublisterTmp.txt
rm -r $dir/assetTmp.txt

echo -e "$GREEN{-} Checando o Httprobe $ENDCOLOR"


cat $url/$final | httprobe -c 120 | sed 's/https\?:\/\///' >> $url/a.txt

sort -u $url/a.txt > $url/alive.txt

rm $url/a.txt



echo -e "$GREEN{-} Checando o Aquatone $ENDCOLOR"

cat $dir/$final | aquatone -out  $dir/aquatone/ > $dir/aquatoneAlive.txt






echo -e "$YELLOW{-} Abrindo o relatório $ENDCOLOR"

chromium $dir/aquatone/aquatone_report.html

