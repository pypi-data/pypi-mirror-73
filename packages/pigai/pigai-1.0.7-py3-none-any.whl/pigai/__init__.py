# pigai, 20-7-7
from ipywidgets import widgets,interact, interactive, fixed, interact_manual,Button, Layout,Dropdown,RadioButtons
from IPython.display import display, clear_output
from IPython.core.display import HTML,display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy,json,re,os, platform,builtins,requests
import pygtrie, random, json
from functools import reduce
from urllib.parse import quote

builtins.interact	= interact
builtins.nlp		= spacy.load('en_core_web_sm')
builtins.merge_nps	= nlp.create_pipe("merge_noun_chunks")
builtins.postag		= lambda snt: pd.DataFrame([ (t.text, t.tag_) for t in nlp(snt)], columns=['word','pos'])
builtins.tokenize	= lambda snt: " ".join([t.text for t in nlp(snt) if len(t.text.strip())]).strip()

api_url = "http://rest.wrask.com"	
builtins.rows		= lambda sql, corpus='dic', columns=[]: requests.get(f"{api_url}/kpfts/query/{corpus}", params={'sql':sql}).json() if not columns else pd.DataFrame(rows(sql, corpus, columns=[]), columns=columns)
builtins.mapk		= lambda sql, corpus='dic', columns=[]: {row[0]:row for row in requests.get(f"{api_url}/kpfts/query/{corpus}", params={'sql':sql}).json()}
builtins.select		= lambda sql, corpus='dic', columns=['kp','mf','arr']:  pd.DataFrame(rows(sql, corpus), columns=columns)
builtins.kwic		= lambda kw, corpus='dic', start=0, end=10:requests.get(f"{api_url}/kpfts/kwic/{corpus}", params={'kw':kw, 'start':start, 'end':end}).json() #http://dev.werror.com:7090/kwic/dic?kw=considering
builtins.getmf		= lambda kp, corpus='dic': requests.get(f"{api_url}/kpfts/mf", params={'kps':kp,'corpus':corpus}).json().get(corpus, {}).get(kp, 0.0)
builtins.getmfs		= lambda kps, corpus='dic': pd.read_json(f"{api_url}/kpfts/mf?kps={quote(kps)}&corpus={corpus}")
builtins.getsnt		= lambda kps, corpus='dic': requests.get(f"{api_url}/kpfts/snt/{corpus}", params={'kps':kps}).json() 
builtins.trpstar	= lambda kp, corpus='dic',start=0,end=10: pd.read_json(f"{api_url}/kpfts/trpstar/{corpus}?kp={quote(kp)}&start={start}&end={end}")
builtins.getarr		= lambda kp, corpus='dic', start=0, end= 10, vs='', columns=['word','prob']: pd.read_json(f"{api_url}/kpfts/arr/{corpus}?kp={quote(kp)}&start={start}&end={end}&vs={vs}&columns={','.join(columns)}")
	
def subset(kp, cp1='gaokao', cp2='clec',columns=['#','word','num']):
	dct = { row['word']:row['prob'] for index, row in getarr(kp,cp2,end=0).iterrows()}
	df = pd.DataFrame([ (index,row['word'],row['prob']) for index, row in getarr(kp,cp1,end=0).iterrows() if not row['word'] in dct], columns=columns)
	return df.set_index(columns[0])
builtins.subset		= subset
#print(subset('open */von'))

def parse(snt, merge_np= False):
	doc = nlp(snt)
	if merge_np : merge_nps(doc)
	return pd.DataFrame({'word': [t.text for t in doc], 'tag': [t.tag_ for t in doc],'pos': [t.pos_ for t in doc],'head': [t.head.orth_ for t in doc],'dep': [t.dep_ for t in doc], 'lemma': [t.text.lower() if t.lemma_ == '-PRON-' else t.lemma_ for t in doc],
	'lefts': [ list(t.lefts) for t in doc], 'rights': [ list(t.rights) for t in doc], 'subtree': [ list(t.subtree) for t in doc],'children': [ list(t.children) for t in doc],})

def highlight(snt, merge_np= False,  colors={'ROOT':'red', 'VERB':'orange','ADJ':'green'}, font_size=0):
	doc = nlp(snt)
	if merge_np : merge_nps(doc)
	arr = [ f"<span pos='{t.tag_}'>{t.text.replace(' ','_')}</span>" for t in doc]
	for i, t in enumerate(doc): 
		if t.dep_ == 'ROOT': arr[i] = f"<b><font color='red'>{arr[i]}</font></b>"
		if t.pos_ in colors: arr[i] = f"<font color='{colors[t.pos_]}'>{arr[i]}</font>"
	html =  " ".join(arr) 
	return HTML(html if font_size <=0 else f"<div style='font-size:{font_size}px'>{html}</div>")

builtins.parse = parse
builtins.wordlist	= lambda: {w for w, in requests.get(f"{api_url}/kpfts/query/wordlist", params={'sql':'select kp from vocab'}).json()}
builtins.wordidf	= lambda: {w:f for w,f in requests.get(f"{api_url}/kpfts/query/wordidf", params={'sql':'select kp,mf from vocab'}).json()}
builtins.spellerr		= lambda w, topk=10: getarr(w, 'spellerr', end=topk)
builtins.spellerrper	= lambda w: getmf(w, 'spellerr')
builtins.random_one		= lambda arr: arr[ int( len(arr) * random.random() )]
builtins.random_word	= lambda c: random_one(letter_words[c])
builtins.nextword_if	= lambda snt_prefix, c , topk= 1000: [ row for row in nextword(snt_prefix, topk= topk) if c in row[0] and row[0].isalpha() and row[0] in wordlist and len(row[0]) > 1]

def word_to_sent( word, topk = 300  ) :   #sentord, wordence
	snt = random_word(word[0])
	for i in range(1, len(word)):
		cands = nextword_if(snt, word[i], topk)
		if len(cands) > 0 : 
			snt = snt + " " + cands[0][0]
		else:
			return f"Failed: {snt} , i = {i} | {word}"
	return snt
builtins.word_to_sent = word_to_sent

def subwords(w = 'knowledge', minlen=1, editdis=0):
	if subwords.counter <= 0: 
		subwords.counter = 1
		subwords.trie = pygtrie.CharTrie()
		for w in wordlist(): subwords.trie[w] = len(w)
	res =[]
	for i in range(len(w)): res.extend(subwords.trie.prefixes(w[i:]))
	res.sort(key =lambda ar: ar[1], reverse=True)
	return list(filter(lambda pair: pair[1] > minlen, res))

subwords.counter = 0 

def sent_to_word(snt):
	wlist = wordlist()
	return {w for w in reduce(lambda x,y:[ i+j for i in x for j in y], [ [a for a in word] for word in snt.split(" ")]) if w in wlist }

builtins.subwords		= subwords
builtins.sent_to_word	= sent_to_word
builtins.ecdic			= lambda pattern='con*ate', wlen=0,limit=10:  pd.DataFrame(rows(
f"select kp,arr from vocab where kp like '{pattern.replace('*','%')}' and length(kp) = {wlen} limit {limit} " if wlen > 0 else 
f"select kp,arr from vocab where kp like '{pattern.replace('*','%')}' limit {limit} ",corpus='ecdic'), columns=['word','trans'])
#print(ecdic(wlen=10))

builtins.parasent	= lambda snt, topk=10,nprobe=10,corpus='dic': pd.DataFrame(requests.get(f'{api_url}/sntvec/search/{corpus}', params={'snt':snt, 'topk':topk,'nprobe':nprobe}).json(), columns=['sid','snt','semdis'])
builtins.cola		= lambda snt: pd.DataFrame(requests.get(f'{api_url}/cola/{snt}').json(), columns=['word','prob']) #http://cluesay.com:7095/cola/I%20love%20you%7CI%20live%20you |[["I love you",0.973],["I live you",0.2679]]
builtins.nextword	= lambda snt, topk=10: requests.get(f'{api_url}/auto/nextword', params={'snt': snt, 'topk':int(topk)}).json()
builtins.autowrite	= lambda snt, maxlen=30: requests.get(f'{api_url}/auto/autowrite', params={'snt': snt, 'maxlen':maxlen}).text
builtins.paraphrase	= lambda snt0, snt1: requests.get(f'{api_url}/auto/paraphrase', params={'snt0': snt0, 'snt1': snt1}).json()
builtins.nsp		= lambda snt0, snt1: requests.get(f'{api_url}/auto/nsp', params={'snt0': snt0, 'snt1': snt1}).json()
builtins.flue		= lambda snt, midx=0: requests.get(f'{api_url}/kenlm/flue/{snt}',params={'midx':midx}).json() #http://cluesay.com:7098/flue/I%20love%20you%7CI%20like%20you?midx=0
builtins.ppl		= lambda snt, midx=0: requests.get(f'{api_url}/kenlm/ppl/{snt}',params={'midx':midx}).json()
builtins.flueadd	= lambda snt, widx, word, midx=0: requests.get(f'{api_url}/kenlm/flueadd/{snt}/widx/word',params={'midx':midx}).json()
builtins.fluerep	= lambda snt, widx, word, midx=0: requests.get(f'{api_url}/kenlm/fluerep/{snt}/widx/word',params={'midx':midx}).json()
builtins.fluedel	= lambda snt, widx, midx=0: requests.get(f'{api_url}/kenlm/fluedel/{snt}/widx',params={'midx':midx}).json()
builtins.cloze		= lambda snt, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/cloze', params={'snt':snt, 'topk':topk}).json(), columns=['word','prob'])
builtins.addone		= lambda snt, index=0, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/addone', params={'snt':snt, 'index':index, 'topk':topk}).json(), columns=['word','prob'])
builtins.repone		= lambda snt, index=0, topk=10: pd.DataFrame(requests.get(f'{api_url}/mask/repone', params={'snt':snt, 'index':index, 'topk':topk}).json(), columns=['word','prob'])
builtins.nldp	= lambda snt : requests.get(f'{api_url}/nldpkp/', params={'q': snt, 'trpx': 0,'trp':0, 'ske':0}).json()
def restate(snt='John opened the window.', tense=0, option=[False, False, True, False, False, False]): # 0:unchanged 1:pres 2:past 3:futr | 0..5:  
	try:
		query = f"q={snt.replace(' ','+')}&tenseOpt={tense}" + "".join([ f"&Options%24{i}=on" for i,opt in enumerate(option) if opt])  #html.escape("hello world")
		res = requests.post(f'{api_url}/nldprestate/', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=f'__VIEWSTATE=%2FwEPDwUKLTcwMTczNTk3NmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgcFCU9wdGlvbnMkMAUJT3B0aW9ucyQxBQlPcHRpb25zJDIFCU9wdGlvbnMkMwUJT3B0aW9ucyQ0BQlPcHRpb25zJDUFCU9wdGlvbnMkNVB%2F2Xl4E6Vc7Gl%2FWXYSYKbZ3OO4&{query}&Button1=%E5%8F%A5%E5%BC%8F%E6%94%B9%E5%86%99&__EVENTVALIDATION=%2FwEWDgLIgLeyBwLP76ruDAKM54rGBgLHr9K5CQLYr9K5CQLZr9K5CQLar9K5CQLXwPjXBQLx9MPdAQLw9MPdAQLv9MPdAQLu9MPdAQLt9MPdAQLs9MPdARuWtZztNkJEFeswt2Z1Y6i4m27E').text
		start = res.index('<span id="Label2"><font size="7">') + len('<span id="Label2"><font size="7">')
		end = res.index('</font></span>', start ) #<span id="Label2"><font size="7">The door was opened by Tom.</font></span>
		return res[start:end]
	except Exception as e:
		print("restate ex:", e, snt)
		return f"failed: {snt} tense={tense} option={option}" + e

builtins.restate = restate 

from spacy.attrs import LOWER
def learn(essay = "The quick fox jumped over the lazy dog. I have learned a lot of knowledges."): 
	if learn.counter <= 0: 
		learn.counter = 1
		learn.widf = wordidf()
	doc = nlp(essay)
	wc = doc.count_by(LOWER) #nlp.vocab[8566208034543834098].text
	d = {} 
	for t in doc: 
		if not t.text.lower() in df.index and not t.pos_ in ('PUNCT'):
			d[t.text.lower()] = {'word': t.text, 'lemma':t.lemma_, 'tag': t.tag_, 'pos': t.pos_, 'count': wc.get(nlp.vocab[t.text.lower()].orth,0), 'diff': learn.widf.get(t.text.lower(),0.0), 'isstop':t.is_stop}
	return d

learn.counter = 0 

if __name__ == '__main__': 
	print(subwords())