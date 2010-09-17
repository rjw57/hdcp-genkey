#!/usr/bin/env python

import string, random

MASTER_KEY_SRC = 'master-key.txt'

def read_key_file(filelike):
	"""Read a HDCP master key from a key file.

	The key file is formatted into 40*40 56-bit hex values separated by
	white space. The first 40 values correspond to row 1 of the matrix, the
	next 40 row 2, etc. Lines beginning with a '#' are ignored. """

	key_matrix = [ [] ]

	for line in filelike:
		if line[0] == '#':
			# This is a comment... skip
			continue

		# split the line into words and parse the hex
		for entry in map(lambda x: int(x, 16), string.split(line)):
			# do we need to start a new row?
			if len(key_matrix[-1]) >= 40:
				key_matrix.append([])

			# append this entry to the row
			key_matrix[-1].append(entry)

	# check we read the right number of entries in total
	assert( len(key_matrix) == 40 )
	assert( len(key_matrix[-1]) == 40 )

	return key_matrix

def gen_source_key(key_matrix):
	"""Generate a source key from the master key matrix passed.

	To generate a source key, take a forty-bit number that (in binary)
	consists of twenty ones and twenty zeroes; this is the source KSV.  Add
	together those twenty rows of the matrix that correspond to the ones in
	the KSV (with the lowest bit in the KSV corresponding to the first
	row), taking all elements modulo two to the power of fifty-six; this is
	the source private key."""

	# generate KSV - 20 1s and 20 0s
	ksv = (['1'] * 20) + (['0'] * 20)

	# permute KSV
	random.shuffle(ksv)

	# convert the binary to int
	ksv_val = int(string.join(ksv, ''), 2)

	# zip the master key matrix and the ksv s.t. the LSB of KSV is associated with
	# the first row, etc. Then filter to only select those rows where the
	# appropriate bit of the KSV is 1.
	ksv.reverse()
	master_rows = map(lambda x: x[1], filter(lambda x: x[0] == '1', zip(ksv, key_matrix)))

	# now generate the key
	key = [0] * 40

	for row in master_rows:
		# add row to key
		key = map(lambda x: (x[0] + x[1]) & 0xffffffffffffff, zip(key, row))

	return (ksv_val, key)

def output_human_readable(ksv, key):
	"""Print a human readable version of the KSV and key.

	The KSV is a single integer. The key is a list of 40 integers."""

	# output the ksv
	print 'KSV:'
	print '%010x' % ksv

	# output the key
	key_strs = map(lambda x: '%014x' % x, key)
	print '\nKey:'
	print string.join(map(lambda x: string.join(x, ' '), zip(*[key_strs]*5)), '\n')

# read the master key file
key_matrix = read_key_file(open(MASTER_KEY_SRC))

# generate a source key and output it
output_human_readable(*gen_source_key(key_matrix))
