#!/usr/bin/env python 

import requests as r 
import json 
import argparse
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


def create_parser():

    #Creating a argument parser
    parser = argparse.ArgumentParser(description="Preguiça de acessar o crt.sh então eu criei isso pra pegar tudo de lá pra mim!")

    #argumento do domínio/link 
    parser.add_argument("-d","--domain",type=str ,metavar=" ", required=True, help="Domínio que vamos dar uma olhada")
    parser.add_argument("-o","--output",type=str,metavar=" ",required=False , help="Manda o output para um arquivo cujo nome vem depois do -o")

    return parser.parse_args()




def print_logo():

    print(Fore.YELLOW+ Style.BRIGHT + """ 
        ---------------------------------------------------------------
        db       .d8b.  d88888D db    db       .o88b. d8888b. d888888b 
        88      d8' `8b YP  d8' `8b  d8'      d8P  Y8 88  `8D `~~88~~' 
        88      88ooo88    d8'   `8bd8'       8P      88oobY'    88    
        88      88~~~88   d8'      88         8b      88`8b      88    
        88booo. 88   88  d8' db    88         Y8b  d8 88 `88.    88    
        Y88888P YP   YP d88888P    YP          `Y88P' 88   YD    YP    
        ---------------------------------------------------------------
        -by bruno_carrazza https://github.com/Carrazza?tab=repositories
        ---------------------------------------------------------------
    """)



def crtsh(args):

    #Gets the json response from crt.sh
    json_request = r.get("https://crt.sh/?q=%25."+args.domain+"&output=json")

    #Transforms the response in valid json to be interpreted by python
    json_py = json.loads(json_request.text)

    crtsh_set = set()

    for dictionary in json_py:
        
        #print(type(stuff))
        
        #getting the address names 
        addrs_list = dictionary['name_value'].split('\n')
        
        for addrs in addrs_list:

            if addrs not in crtsh_set:
                crtsh_set.add(addrs)

    return crtsh_set


def sublist3r(args):

    sublister = "/home/carrazza/Desktop/hack/Scripts/Sublist3r/sublist3r.py -d " + args.domain + " -o ./sublister.txt > /dev/null"


    os.system(sublister)

    sublister_set = set()

    #Pegando os domínios do sublister 
    with open("/home/carrazza/hack/Scripts/lazycrt/sublister.txt","r") as f:

        for result in f.readlines():
            
            #quando pegamos o output do sublist3r ele vem com \n, vamos tirar eles
            result = result.replace('\n','')

            if result not in sublister_set:
                sublister_set.add(result)
    
    return sublister_set



def unir_resultados(crtsh_set,sublister_set):

    return crtsh_set.union(sublister_set)




def lista_final(list_of_addr):

    print(Fore.BLUE+"-"*50+"Resultados Finais das buscas:"+"-"*50)

    list_of_addr = list(list_of_addr)
    list_of_addr.sort()

    #printa a lista
    for addr in list_of_addr:
        print(Fore.YELLOW + Style.BRIGHT + addr,end="\n")


def print_arquivo(list_of_addr,args):

    #Printando para um arquivo
    print(Fore.BLUE + "-"*46 + "--->Printando os resultados em " + Fore.CYAN + args.output + Fore.BLUE + "<---"+"-"*46)

    with open(args.output,"w") as f:

        string = "\n".join(list_of_addr)        
        string = string + "\n"
        f.write(string)


def main():

    args = create_parser()

    #remove trequinhos desnecessários para fazer a request 
    args.domain = args.domain.replace("https://","")
    args.domain = args.domain.replace("www.","")
    args.domain = args.domain.replace("http://","")

    print_logo()

    #list with all addr
    list_of_addr = set()

    #achados do Crt.sh
    print(Fore.GREEN+"[-] Pesquisando no crt.sh")
    crtsh_set = crtsh(args)

    #achados do Sublist3r
    print(Fore.GREEN+'[-] Pesquisando no Sublist3r')
    sublister_set = sublist3r(args)



    #unindo tudo
    list_of_addr = unir_resultados(crtsh_set,sublister_set)



    lista_final(list_of_addr)

    if (args.output != None): print_arquivo(list_of_addr,args)

#LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOL


main()





















