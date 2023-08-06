#!/usr/bin/env python
from __future__ import division
from argparse import ArgumentParser
import sys
import re
from multiprocessing import Pool
try:
    from itertools import izip as zip
except ImportError:
    pass



def argypargy():
    parser = ArgumentParser(description="callMUT -i input.mpileup -o output.mprofile")
    req_args = parser.add_argument_group('Required arguments')
    add_args = parser.add_argument_group('Additional arguments')
    req_args.add_argument("--input", "-i", help="Input mpileup or mprofile to process.")
    req_args.add_argument("--output", "-o", help="Output mprofile.")
    add_args.add_argument("--indelcut", "-ic", help="Minimum rate for an indel's sequence to be reported, default=1, If 'NA', no cutoff will be applied.", nargs='?', default=1)
    add_args.add_argument("--control", "-c", help="mpileup/mprofile to normalise to (e.g. untreated).")
    add_args.add_argument("--preproc", "-pp", help="Specifies input files are mprofiles, not mpileups (requires --control to be set).", action='store_true')
    add_args.add_argument("--quiet", "-q", help="Removes all messages.")
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()
    if args.input is None and args.read1 is None:
        print("\ncallMUT ERROR: Please provide an input file with --input (-i).\n")
        sys.exit()
    if args.output is None:
        print("\ncallMUT ERROR: Please provide an output file with --output (-o).\n")
        sys.exit()
    if args.preproc == True and args.control is None:
        print("\ncallMUT ERROR: --preproc (-pp) also needs --control (-c) to calculate a differential to the --input (-i) sample.\n")
        sys.exit()
    if args.indelcut != "NA":
        try:
            args.indelcut=float(args.indelcut)
        except ValueError:
            print("\nIndel cutoff is not a valid number, running without a cutoff.\n")
            args.indelcut = "NA"
    return(args)
def de_indel(argues):
    mpileup_base = argues[0]
    cutoff = argues[1]
    columns = mpileup_base.split("\t")
    chr = columns[0]
    coordinate = columns[1]
    base = columns[2]
    readcount = int(columns[3])
    reads = re.sub('\\^.', "", columns[4])
    startlocations = list()
    endlocations = list()
    length_diff = 0
    indel_sequences = ""
    # indels must first be extracted from the mpileup mutation calls, as it reports indel sequences which interferes with point mutation counting. 
    # use regex to find and extract the string of the indel number (findall) as well as the match object for the indel (finditer).
    if readcount>0:
        indels = re.findall(r'\d+', reads)
        # use the match objects to create a list of locations for each match.
        for match in re.finditer(r'\d+', reads):
            startlocations.append(int(match.start()))
            endlocations.append(int(match.end()))
        # iterate over the list of indel strings and their locations simultaneously to remove the sequences and generate a new string containing just the indels (indel_sequences).
        # the length difference is calculated to account for the removal of each indel shortening the sequence and therefore altering the position of the indels.
        for startlocation, endlocation, indel in zip(startlocations, endlocations, indels):
            if indel != '':
                indel_sequences = indel_sequences+(reads[(startlocation-1-length_diff):(endlocation+int(indel)-length_diff)]).upper()+","
                oldlength = len(reads)
                reads = reads[:(endlocation-length_diff)] + reads[(endlocation + int(indel) - length_diff):]
                newlength = len(reads)
                length_diff = length_diff + (oldlength - newlength)
        # calculate the mutation rates.
        formatted_indels = ""
        for indel in set(indel_sequences.split(",")):
            if indel != '':
                rate = (indel_sequences.count(indel)/readcount)*100
                if cutoff.upper() != "NA":
                    if rate > float(cutoff):
                        formatted_indels = formatted_indels+(indel+":"+str(rate)+",")
                else:
                    formatted_indels = formatted_indels+(indel+":"+str(rate)+",")
        a_rate = (reads.upper().count("A")/readcount)*100
        t_rate = (reads.upper().count("T")/readcount)*100
        g_rate = (reads.upper().count("G")/readcount)*100
        c_rate = (reads.upper().count("C")/readcount)*100
        in_rate = (reads.count("+")/readcount)*100
        del_rate = (reads.count("-")/readcount)*100
        snv_rate = a_rate + t_rate + g_rate + c_rate
        if base == "G":
            transition = a_rate
            transversion = t_rate + c_rate
        elif base == "C":
            transition = t_rate
            transversion = a_rate + g_rate
        elif base == "T":
            transition = c_rate
            transversion = a_rate + g_rate
        elif base == "A":
            transition = g_rate
            transversion = t_rate + c_rate
    else:
        a_rate = 0
        t_rate = 0
        g_rate = 0
        c_rate = 0
        transition=0
        transversion=0
        snv_rate=0
        in_rate = 0
        del_rate = 0
        formatted_indels = ""
    # return a string of the mutation rates that is ready for writing to an output file.
    return(('\t'.join([chr, coordinate, base, str(readcount), str(a_rate), str(t_rate), str(g_rate), str(c_rate), str(transition), str(transversion), str(snv_rate), str(in_rate), str(del_rate), formatted_indels]))+"\n")
def mutDIFF(ctrl_mprofile, treated_mprofile, cutoff="NA"):
    ctrl_columns = ctrl_mprofile.split("\t")
    treat_columns = treated_mprofile.split("\t")
    # take the minimum of the two readcoutns as this dictates the resolution of the mutation calling.
    readcount = min(int(treat_columns[3]), int(ctrl_columns[3]))
    # calculate the differential in the mtuation rates betwee the two samples. 
    a_rate = float(treat_columns[4])-float(ctrl_columns[4])
    t_rate = float(treat_columns[5])-float(ctrl_columns[5])
    g_rate = float(treat_columns[6])-float(ctrl_columns[6])
    c_rate = float(treat_columns[7])-float(ctrl_columns[7])
    transitions = float(treat_columns[8])-float(ctrl_columns[8])
    transversions = float(treat_columns[9])-float(ctrl_columns[9])
    snv_rate = float(treat_columns[10])-float(ctrl_columns[10])
    in_rate = float(treat_columns[11])-float(ctrl_columns[11])
    del_rate = float(treat_columns[12])-float(ctrl_columns[12])
    # for common indel sequences, first create a dictionary of the control indels (key=indel sequence, value=rate).
    ctrl_indels = {indel.split(":")[0]:indel.split(":")[1] for indel in ctrl_columns[13].split(",") if indel != "\n"}
    formatted_indels = ""
    # for each indel in the treated sample, see if the same indel is in the control and if it is, calculate the rate differential between the two samples.
    # if it is in the treated, but not the control, then the treated rate is kept as it is.
    for indel in treat_columns[13].split(","):
        if indel.split(":")[0] in ctrl_indels.keys():
            rate = float(indel.split(":")[1]) - float(ctrl_indels[indel.split(":")[0]])
            new_indel = indel.split(":")[0]+":"+str(rate)
        else:
            new_indel = indel.strip(",")
        if new_indel != "\n":
            if str(cutoff).upper() != "NA":
                if float(new_indel.split(":")[1]) > float(cutoff):
                    formatted_indels = formatted_indels+new_indel+","
            elif str(cutoff).upper() == "NA":
                formatted_indels = formatted_indels+new_indel+","
    # return a string of the mutation rates that is ready for writing to an output file.
    return(('\t'.join([ctrl_columns[0], ctrl_columns[1], ctrl_columns[2], str(readcount), str(a_rate), str(t_rate), str(g_rate), str(c_rate), str(transitions), str(transversions), str(snv_rate), str(in_rate), str(del_rate), formatted_indels]))+"\n")
def main(args=argypargy()):
    with open(args.output, 'w') as outputfile:
        outputfile.write("Chromosome\tCoordinate\tRef.Base\tReadcount\tA.Mutations\tT.Mutations\tG.Mutations\tC.Mutations\tTransitions\tTransversions\tTotal.SNVs\tInsertions\tDeletions\tCommon.Indels\n")
        if args.preproc == False:
            if args.control is None:
                if args.quiet is not None:
                    print("\nProcessing mpileup into mprofile...\n")
                with open(args.input) as mpileup_file:
                    for mpileup_base in mpileup_file:
                        outputfile.write(de_indel([mpileup_base, args.indelcut]))
            elif args.control is not None:
                if args.quiet is not None:
                    print("\nProcessing mpileups into mprofiles and calculating input-control differential...\n")
                with open(args.control) as ctrl_mpileup, open(args.input) as treat_mpileup:
                    p=Pool(2)
                    for ctrl, treated in zip(ctrl_mpileup, treat_mpileup):
                        both_lines=p.map(de_indel, [[ctrl, "NA"], [treated, "NA"]])
                        outputfile.write(mutDIFF(both_lines[0], both_lines[1], cutoff=args.indelcut))
                    p.close()
        elif args.preproc == True:
            if args.quiet is not None:
                print("\nCalculating input-control differential...\n")
            with open(args.control) as ctrl_mprofile, open(args.input) as treat_mprofile:
                next(ctrl_mprofile)
                next(treat_mprofile)
                for ctrl, treated in zip(ctrl_mprofile, treat_mprofile):
                    outputfile.write(mutDIFF(ctrl, treated, cutoff=args.indelcut))

