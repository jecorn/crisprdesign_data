*crispri/a
data from Ensembl BioMart
only well-annotated chromosomes sans MT (e.g. 1-19XY or 1-22XY)
protein_coding and known genes only -- add novel at a later date? how many are there?
export ids, name, strand, TSS, principal isoform:
Ensembl Gene ID,Ensembl Transcript ID,Associated Gene Name,Chromosome Name,Strand,Transcription Start Site (TSS),APPRIS principal isoform annotation
design guides based on transcription start site of principal isoform

*ko
data from Ensembl BioMart
only well-annotated chromosome maps sans MT (e.g. 1-19XY or 1-22XY)
protein_coding and known genes only
export ids, name, strand, tss, exon start/end, constitutive exon, exon rank:
Ensembl Gene ID,Ensembl Transcript ID,Associated Gene Name,Chromosome Name,Strand,Transcription Start Site (TSS),Exon Chr Start (bp),Exon Chr End (bp),Constitutive Exon,Exon Rank in Transcript
design guides based on first 2 constitutive exons of each transcript
Not all genes have constitutive exon annotation! E.g. ENSMUSG00000074305 = Peak1 in m38.p3 and ENSG00000104671 = DCTN6 in h38
So use APPRIS principal isoform info from crispri/a list
	Add from TSS dataset above to constitutive_exon dataset
	note not all genes have principal isoform annotation E.g. SSX5
	grep "APPRIS" from TSS dataset
	prin_iso.py script takes principal isoform data from TSS_priniso and adds boolean to end of constitutive exon data
	
Algorithm:
	For gene in genes:
		read exon data into list
		sort exons by start,end
		make exons unique
		guides_per_gene = 5
		accepted_guides = []
		disallowed_patterns = [ restriction_enzyme_sequences ]
		if no constitutive exons:
			target_ranges = [all exons ranges] according to rank
		else:
			target_ranges = [constitutive exons ranges] according to distance from TSS
		for range in target_ranges:
			seq = get_seq( range, chromosome )
			exon_guides = find_guides( seq )
			score_guides( exon_guides )
			for guide in exon_guides:
				if guide.score < threshold_score and disallowed_patterns not in guide:
					accepted_guides.append( (geneid+transcriptid, guide) )
					if accepted_guides.length >= guides_per_transcript:
						break

Are there hits in screens that match exons *not* in principal isoform?

*exon skipping
data from Ensembl BioMart
only well-annotated chromosome maps sans MT (e.g. 1-19XY or 1-22XY)
protein_coding and known genes only
export ids, name, strand, tss, exon start/end, constitutive exon, exon rank:
Ensembl Gene ID,Ensembl Transcript ID,Associated Gene Name,Chromosome Name,Strand,Transcription Start Site (TSS),Exon Chr Start (bp),Exon Chr End (bp),Constitutive Exon,Exon Rank in Transcript
design guides based on NON constitutive exons - find guides that span 5' boundary of these exons
Algorithm:
	for transcript in transcripts:
		guides_per_transcript = 2
		accepted_guides = []
		disallowed_patterns = [restriction_enzyme_seqs ]
		for exon in transcript:
			if not constitutive:
				set exon_start
				seq = get_seq( (exon_start-50, exon_start+50), chromosome)
				guides = find_guides( seq )
				score_guides( guides )
				for guide in guides:
					if guide.score < threshold_score and disallowed_patterns not in guide and guide not in accepted_guides:
						accepted_guides.append( (target,guide) )
						if accepted_guides.length > guides_per_exon
							break