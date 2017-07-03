# -*- coding: utf-8 -*-

'''
Created on 21 Jun 2017

@author: Kalle Olumets
'''

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.classify.megam import _write_megam_features

def send2morfanalyzer(inp_txt):
    
    res = None
    data1 = ""
    
    inp_payl = {
        'doc': inp_txt,
        'guess': 'on'
        }
    
    try:
        res  = requests.post('http://www.filosoft.ee/html_morf_et/html_morf.cgi', data = inp_payl)
        data1 = res.text
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
        data1 = {'has_error':True, 'error_message':e.message}
        return data1
    
    if res.ok:
        return data1
    else:
        return res.status_code
    
    
def parse_answer(inp_answer,inp_target):
    soup = BeautifulSoup(inp_answer, 'html.parser')
    #print(soup.title)
    
    sentence = ""
    for link in soup.table.find_all('td'):
        line = link.text.split()
        #print line[0],line[2] 
        sentence +=  line[0] + " "+ line[2]  + " "
            
    print sentence + ";;" +str(inp_target)
    return sentence + ";;" +str(inp_target)
    
def read_pos_line(inp_posline):
    print inp_posline
    
def person_features(inp_posline):
    
    line = inp_posline.split(';;')
        
    pos_line = line[0].split('_ ')
    #print pos_line
    pn_indx = int(line[1]) 
    #indx_arr = line[1].lstrip('(').rstrip(')').split(',')
    #print indx_line[0]
    
    print pn_indx
    
    feat = {}
    
    feat['pos']         = pos_line[pn_indx].split('//')[1]
    feat['prefix_pos']  = pos_line[pn_indx-1].split('//')[1]
    feat['sufffix_pos'] = pos_line[pn_indx+1].split('//')[1]
    feat['size']        = len(pos_line[pn_indx])
    feat['prefix_size'] = len(pos_line[pn_indx-1])
    feat['suffix_size'] = len(pos_line[pn_indx+1])
    
    target = (pos_line[pn_indx].split('//')[0]).strip()
    feat['last_letter'] = target[-1]
    
    prefix = (pos_line[pn_indx-1].split('//')[0]).strip()
    feat['prefix_last_letter'] = prefix[-1]
    
    suffix = (pos_line[pn_indx+1].split('//')[0]).strip()
    feat['suffix_last_letter'] = suffix[-1]
    
    return feat
      
    

def person_name_ftrs(inp_name,inp_prev,inp_post):
    '''
    Personal name features
    '''
    features = {}
    features["first_letter"] = inp_name[0].lower()
    features["last_letter"] = inp_name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = inp_name.lower().count(letter)
        features["has({})".format(letter)] = (letter in inp_name.lower())
        
    return features


if __name__ == '__main__':
    pass
    inp_txt1 = '''
    Lasnamäe linnaosavanem Maria Jufereva tegi linnaosa koolidele õppeaasta lõpu puhul videopöördumise,
     mille kujunduses paistis Venemaa lippu meenutav sümbol, 
    Jufereva enda sõnul on tegemist kujundaja apsakaga ja kellelgi polnud plaanis idanaabri riiklikke sümboleid kujutada.
    '''
    inp_txt2 = '''
    sõi musta leiba
    '''
    
    inp_txt3 = "Aadu Must sõi musta leiba ja söömise käigus rääkis  oma õe Kadi Mustaga Ungarist"
    
    inp_txt4 = "osaleb läbirääkimistes Yana Toomiga erakonna esimees Jüri Ratas"
    
    res    = send2morfanalyzer(inp_txt4)
    postxt = parse_answer(res,3)
    
    #test_pos = 'Aadu //_H_ Must //_P_ sõi //_V_ musta //_A_ leiba //_S_ ;;1'
    feat   = person_features(postxt)
    print feat



