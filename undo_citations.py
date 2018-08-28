from __future__ import print_function
from panflute import *
from functools import partial
import sys

# holds all the citations we wrote out during the isolate_citations filter
citation_stack = None

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#converts the citation pre and suffix to string, drops all formatting.
def to_string(elem):
	prefix = []
	for s in elem:
		if hasattr(s, 'text'):
			prefix.append(s.text)

	prefix = ' '.join(prefix)
	return prefix

def undo_citation(elem,doc):

#find an emph section
	if isinstance(elem,Emph):
		
		# determine if this is a reference within an emph section
		ref=[]
		f = partial(isCitation, ref=ref)
		elem.walk(f)

		elem_str = stringify(elem)

		#if it starts with a ( and ends with a ), we can determine if this is inline or bracketed. 
		#Likely needs to be expanded for non author-year cls
		isNormalCitation = None
		if citation_stack is None:
			isNormalCitation = elem_str[0] == "(" and elem_str[-1] == ")"

		citation = None
		if len(ref) >= 1: # if we found a citation
			citation = Cite()

		for r in ref:

			#build our citation
			c = Citation(id=r)


			i = 0
			#look for the found citation in the citation stack
			#now some citations might be reordered, but since this a list of every citation, we should needed to go more than a few past the head (as we pop off it)
			#to find what we are looking for.
			for s in citation_stack:
				if r in s: # the reference is in this citation
					values = s.split(';')

					# eprint(r,values[1],values[2].rstrip())
					#set the citation prefix and suffix to what we have stored
					c.prefix = ListContainer(Str(values[1]))
					c.suffix = ListContainer(Str(values[2])) # remove new line


					#if isNormalCitation is none, then we are using it form citation.txt
					if isNormalCitation is None:
						c.mode = values[3].rstrip()
						# eprint(c.mode)
					elif not isNormalCitation: #otherwise guess it from '(' and ')' surrounding as per above
						c.mode = "AuthorInText"
					
					break

				i = i +1

			#remove the index of the one we found
			if len(citation_stack) >0 :

				del citation_stack[i] # remove the one we found
				# eprint(citation_stack)


			#append the citations
			citation.citations.append(c)
		
		#Replace the emph section with the newly build citation
		return citation

#determines if this is a citation
def isCitation(elem,doc,ref):
	
	if isinstance(elem,Link):
	 	link = elem.url
	 	if "#ref-" in link:
	 	 	link = elem.url[5:]
		ref.append(link)

def main(doc=None):
	global citation_stack

	try:
		with open('citations.txt','r') as f:
			citation_stack = f.readlines()
	except:
		eprint('citation.txt not found, not looking to replace suffix and prefix')

	return run_filter(undo_citation, doc=doc)

if __name__ == "__main__":
	main()
	
