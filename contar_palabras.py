"""
Cañete Tomás, Lino
Jarilla Romo, Victor
"""

import re
import sys

def eliminarsws(text,language):
	"""
	Esta función recibe un texto en forma de lista de lineas y devuelve el mismo texto
	sin las stopwords del idioma que se le pase como argumento
	"""
	swfile = open('stopwords_'+language+'.txt','r')
	swlist = swfile.read().split('\n')
	res=[]
	for i in range(len(text)):
		line=''
		linea = mi_er.sub(' ',text[i]).strip().split()
		for palabra in linea:
			if palabra not in swlist:
				line+=palabra+' '
		res.append(line)
	return res
		

def analizar(text,lower,stopwords,language):
	"""
	Esta función recibe un texto en forma de lista de lineas y las señales de control para pasarlo a
	minusculas 	y/o eliminar las stopwords del idioma especificado y lo analiza devolviendo un informe
	con los datos relevantes.
	"""
	swfile = open('stopwords_'+language+'.txt','r')
	swlist = swfile.read().split('\n')
	modificar = ['1','yes','True']
	lines = 0
	words = 0
	sws = 0
	hashwords = {}
	symbols = 0
	hashsymbols = {}
	report = ''
	
	for i in range(len(text)):
		lines=lines+1
		linea = mi_er.sub(' ',text[i]).strip().split(' ')
		
		for j in range(len(linea)):
			words = words+1
			if stopwords not in modificar or linea[j].lower() not in swlist:
				if lower in modificar:
					palabra = linea[j].lower()
						
				else:
					palabra = linea[j]
				if palabra in hashwords:
					hashwords[palabra] = hashwords.get(palabra)+1
				else:
					hashwords[palabra] = 1
				simbolos = list(linea[j])			
			
				for k in range(len(simbolos)):
					symbols = symbols+1
					if lower in modificar:
						simbolo = simbolos[k].lower()
					else:
						simbolo = simbolos[k]
					if simbolo in hashsymbols:
						hashsymbols[simbolo] = hashsymbols.get(simbolo)+1
					else:
						hashsymbols[simbolo] = 1
			else:
				sws+=1
	report+='Lines: '+str(lines)+'\n'
	report+='Number words (with stopwords): '+str(words)+'\n'
	if stopwords in modificar:	
		report+='Number words (without stopwords): '+str(words-sws)+'\n'
	report+='Vocabulary size: '+str(len(hashwords))+'\n'
	report+='Number of symbols: '+str(symbols)+'\n'
	report+='Number of different symbols: '+str(len(hashsymbols))+'\n'
	report+='Words (alphabetical order):\n'
	for key in sorted(hashwords):
		report+='\t'+key+': '+str(hashwords.get(key))+'\n'
	report+='Words (by frequency):\n'
	for key in sorted(hashwords.items(), key=lambda x:x[1], reverse=True):
		report+='\t'+key[0]+': '+str(key[1])+'\n'
	report+='Symbols (alphabetical order):\n'
	for key in sorted(hashsymbols.items(), key=lambda x:x[0]):
		report+='\t'+key[0]+': '+str(key[1])+'\n'
	report+='Symbols (by frequency):\n'
	for key in sorted(hashsymbols.items(), key=lambda x:x[1], reverse=True):
		report+='\t'+key[0]+': '+str(key[1])+'\n'
	return report

"""
Ampliación
"""
def ampliar(text,lower):
	"""
	Esta función recibe como parámetro un texto y devuelve un informe con los pares de palabras y de simbolos 
	ordenados alfabéticamente y por frecuencia.
	"""
	report = ''
	modificar = ['1','yes','True']
	hashbigrams={}
	hashbisymbols={}
	for i in range(len(text)):
		bigrams=[]
		bisymbols=[]
		if lower in modificar:
			linea = mi_er.sub(' ',text[i].lower()).strip().split(' ')
		else:
			linea = mi_er.sub(' ',text[i]).strip().split(' ')
		linea.append('$')
		linea.insert(0,'$')
		for j in range(len(linea)-1):
			bigrams.append((linea[j],linea[j+1]))
		for b in bigrams:
			if b in hashbigrams:
				hashbigrams[b] = hashbigrams.get(b)+1
			else:
				hashbigrams[b] = 1
		if lower in modificar:
			linea = mi_er.sub(' ',text[i].lower()).strip().split(' ')
		else:
			linea = mi_er.sub(' ',text[i]).strip().split(' ')
		for palabra in linea:
			bisymbols=[]
			for k in range(len(palabra)-1):
				bisymbols.append(palabra[k]+palabra[k+1])
			for n in bisymbols:
				if n in hashbisymbols:
					hashbisymbols[n] = hashbisymbols.get(n)+1
				else:
					hashbisymbols[n] = 1				
			
	report+='Word pairs (alphabetical order):\n'
	for key in sorted(hashbigrams):
		report+='\t'+key[0]+' '+key[1]+': '+str(hashbigrams.get(key))+'\n'
	report+='Word pairs (by frequency):\n'
	for key in sorted(hashbigrams.items(), key=lambda x:x[1], reverse=True):
		report+='\t'+key[0][0]+' '+key[0][1]+': '+str(hashbigrams.get(key[0]))+'\n'
	report+='Symbol pairs (alphabetical order):\n'
	for key in sorted(hashbisymbols):
		report+='\t'+key+': '+str(hashbisymbols.get(key))+'\n'
	report+='Symbol pairs (by frequency):\n'
	for key in sorted(hashbisymbols.items(), key=lambda x:x[1], reverse=True):
		report+='\t'+key[0]+': '+str(key[1])+'\n'
	return report	
			

if __name__ == "__main__":
	if len(sys.argv) == 2:
		sys.argv.append('no')
		sys.argv.append('no')
		sys.argv.append('en')
	if len(sys.argv) == 3:
		sys.argv.append('no')
		sys.argv.append('en')
	if len(sys.argv) == 4:
		sys.argv.append('en')
	entrada = open(sys.argv[1],'r', encoding="utf-8")	
	salida = open(sys.argv[1][:len(sys.argv[1])-4]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.txt','w')
	mi_er = re.compile('\W+')
	texto = entrada.read().split('\n')[:-1]
	control = ['yes','no','1','0','True','False']
	languages = ['en','ca','es','fr','gr']
	
	if len(sys.argv) < 2 or len(sys.argv) > 5 or sys.argv[4] not in languages:
		print('Numero o valor incorrecto de argumentos')
	else:
		salida.write(analizar(texto,sys.argv[2],sys.argv[3],sys.argv[4]))
		if sys.argv[3] in ['yes','True','1']:
			texto = eliminarsws(texto,sys.argv[4])
		salida.write(ampliar(texto,sys.argv[2]))
