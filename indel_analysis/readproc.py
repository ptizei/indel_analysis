# AUTOGENERATED! DO NOT EDIT! File to edit: 00_readproc.ipynb (unless otherwise specified).

__all__ = ['trim_cterm', 'fasta_to_counts', 'increment_seq_counts', 'dict_to_df']

# Cell
import re
from pathlib import Path
import pandas as pd


def trim_cterm(inputFile, outputFile, motifToTrim):
    with open(inputFile, 'r') as inputFH:
        with open(outputFile,'w') as outputFH:
            i = 0
            for line in inputFH:
                i += 1
                if i%2 ==1: outputFH.write(line)
                else:
                    line = re.sub(motifToTrim, '', line)
                    #line += '\n'
                    outputFH.write(line)


def fasta_to_counts(inputFile):


    df_seq_counts = pd.DataFrame()
    cur_name = ''
    cur_seq = ''
    dict_temp_seqs = {}
    i = 0
    #make a temporary dict for counting seqs
    with open(inputFile, 'r') as inputFH:
        for line in inputFH:
            #print(i)
            if line[0] == '>': # lines starting with '>' are seq names
                if cur_name != '': #add previous seq to dict, if it exists
                    dict_temp_seqs = increment_seq_counts(dict_temp_seqs, cur_name, cur_seq)
                    #if cur_name in dict_temp_seqs.keys():
                    #    dict_temp_seqs[cur_name][1] += 1 # add 1 to count for cur_seq
                    #else:
                    #    dict_temp_seqs[cur_name] = [cur_seq, 1]
                cur_name = line.rstrip()[1:] # strip newline and '>'
                cur_seq = ''
                i += 1
            else: # odd lines are the actual sequences, concatenate until a new sequence starts
                cur_seq += line.rstrip()
               # print(cur_seq)
        dict_temp_seqs = increment_seq_counts(dict_temp_seqs, cur_name,cur_seq)
        #if cur_name in dict_temp_seqs.keys(): #add the last seq to the dict
        #    dict_temp_seqs[cur_name][1] += 1
        #else:
        #    dict_temp_seqs[cur_name] =  [cur_seq, 1]


    return dict_temp_seqs

def increment_seq_counts(seq_dict, cur_seq_name, cur_seq):
    if cur_seq_name in seq_dict.keys():
        seq_dict[cur_seq_name][0] +=1
    else:
        seq_dict[cur_seq_name] = [1, cur_seq]
    return seq_dict


def dict_to_df(seq_dict) -> pd.core.frame.DataFrame:
    dict_for_df={}
    for i, cur_name in enumerate(seq_dict):
        cur_count = seq_dict[cur_name][0]
        cur_seq = seq_dict[cur_name][1]
        cur_seqZ = 'Z' + cur_seq + 'Z'
        dict_for_df[i] = [cur_name, seq_dict[cur_name][0],cur_seq, cur_seqZ]
    df_seqs = pd.DataFrame.from_dict(dict_for_df, orient='index', columns=['seq_name', 'count', 'seq', 'seqZ'])
    return df_seqs






    #make a second dic with the final counts and also the sequences with terminal Zs, to build the DF

