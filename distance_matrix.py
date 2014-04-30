from GamTools import corr
import numpy as np
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Calculate coverage over different window sizes for a list of bam files.')
parser.add_argument('npz_frequencies_file', help='An npz file containing co-segregation frequencies to convert to correlations')

args = parser.parse_args()

correlation_file = args.npz_frequencies_file.split('.')
correlation_file[correlation_file.index('chrom')] = "corr"
correlation_file = '.'.join(correlation_file)

if os.path.exists(correlation_file):
    sys.exit('File exists already, not overwriting')

freqs = np.load(args.npz_frequencies_file)['freqs']

def flatten_freqs(freqs):
        
    freqs_shape = freqs.shape
    flat_shape = ( freqs_shape[0] * freqs_shape[1], freqs_shape[2], freqs_shape[3])
    return freqs.reshape(flat_shape)

distances = np.array(map(corr, flatten_freqs(freqs))).reshape(freqs.shape[:2])

np.savez_compressed(correlation_file, corr=distances)