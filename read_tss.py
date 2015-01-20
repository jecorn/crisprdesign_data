#!/usr/bin/env python
class GenomicLocation:
	def __init__(self, chr, start, end, strand):
		#instance variables
		self.chr = chr
		self.start = start # start and end are 1-indexed (as per UCSC)
		self.end = end
		self.strand = strand
	def __eq__( self, other):
		return( (self.chr,self.start,self.end,self.strand) == (other.chr,other.start,other.end,other.strand) )
	def __ne__( self, other):
		return not self == other
	def __hash__( self ):
		s = str(self.chr)+str(self.start)+str(self.end)+str(self.strand)
		hash = int(''.join(str(ord(c)) for c in s))
		return hash
	def __str__( self ):
		return "%s %s:%s%s" % (self.chr, self.start, self.end, self.strand)
		
class Gene:
	def __init__(self, id, transcripts):
		self.id = id
		self.transcripts = transcripts
	def get_chromosome( self ):
		chrs = set(t.get_chromosome() for t in self.transcripts)
		if len( chrs ) == 1:
			return chrs.pop()
		else:
			print "Found mixed transcript chromosomes!"
			return 0
	def get_strand( self ):
		strands = set( t.get_strand() for t in self.transcripts)
		if len( strands ) == 1:
			return strands.pop()
		else:
			print "Found mixed transcript strands!"
			return 0
	
class Transcript:
	def __init__(self, id, tss, principal_isoform, exons):
		self.id = id
		self.tss = tss
		self.prin_iso = principal_isoform
		self.exons = exons
	def get_chromosome( self ):
		chrs = set(exon.location.chr for exon in self.exons)
		if len( chrs ) == 1:
			return chrs.pop()
		else:
			print "Found mixed exon chromosomes!"
			return 0
	def get_strand( self ):
		strands = set( e.location.strand for e in self.exons )
		if len( strands ) == 1:
			return strands.pop()
		else:
			print "Found mixed exon strands!"
			return 0

class Exon:
	def __init__(self, location, constitutive):
		self.location = location
		self.constitutive = constitutive

g = Gene( "P53", [] )
t = Transcript( "ENS1234", 900, True, [] )
loc1 = GenomicLocation( "chr1", 1001, 1201, "+")
loc2 = GenomicLocation( "chr1", 1524, 1924, "+")
e1 = Exon( loc1, True )
e2 = Exon( loc2, False )

t.exons = [e1, e2]
g.transcripts = [t]

print g.get_strand()
print g.get_chromosome()