#!/usr/bin/env python
import sys

fname1 = sys.argv[1]
fname2 = sys.argv[2]

f1 = open( fname1, mode="rU") # file with principal isoform data. crispria
f2 = open( fname2, mode="rU").readlines() # file with exon data. ko

print f2[0].rstrip()+","+"APPRIS principal isoform"
txids = set()
for line1 in f1:
	if line1[0] == "#":
		continue
	linesplit1 = line1.rstrip().split(",")
	txids.add(linesplit1[1])
f1.close()

for line2 in f2:
	if line2[0] == "#":
		continue
	linesplit2 = line2.rstrip().split(",")
	txid2 = linesplit2[1]
	if txid2 in txids:
		print line2.rstrip()+",1"
	else:
		print line2.rstrip()+",0"