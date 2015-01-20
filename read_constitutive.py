#!/usr/bin/env python
import sys

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
	def __init__(self, id, start, end, transcripts):
		self.id = id
		self.start = start
		self.end = end
		self.transcripts = transcripts
	def __str__( self ):
		return "Gene %s %s %s %s" % (self.id, self.start, self.end, self.transcripts)
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
	def __init__(self, id, start, end, tss, principal_isoform, exons):
		self.id = id
		self.start = start
		self.end = end
		self.tss = tss
		self.prin_iso = principal_isoform
		self.exons = exons
	def __str__( self ):
		return "Transcript %s %s %s" % (self.id, self.start, self.end, self.tss, self.prin_iso, self.exons)
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
	def __str__( self ):
		return "Exon %s %s" % (self.location, self.constitutive)


fname = sys.argv[1]
f = open( fname, mode="rU")
prev_geneid = ""
prev_txid = ""
for line in f:
	if line[0] == "#":
		continue
	geneid, txid, genename, chr, tss, strand, start, end, constitutive, rank = line.rstrip().split(",")
	chr = "chr"+chr
	tss = int(tss)
	start = int(start)
	end = int(end)
	if strand == "1":
		strand = "+"
	elif strand == "-1":
		strand = "-"
	if constitutive == 1:
		constitutive = True
	elif constitutive == 0:
		constitutive = False
	rank = int(rank)
	
	e = Exon( GenomicLocation( chr, start, end, strand ), constitutive )

	fake_start = 0
	fake_end = 0
	if prev_txid == txid:
		t.exons.append( e )
		for e in t.exons:
	else:
		t = Transcript( txid, fake_start, fake_end, tss, True, [e] )
	if prev_geneid == geneid:
		g.transcripts.append( t )
	else:
		g = Gene( geneid+"_"+genename, fake_start, fake_end, [t] )
	
	prev_geneid = geneid
	prev_txid = txid