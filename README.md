# HDCP Key Generation Example

This script implements a simple version of the HDCP key generation algorithm in
Python using the leaked HDCP master key (which is located in master-key.txt).

```
Usage: generate_key.py [options]

Options:
  -h, --help            show this help message and exit
  -m FILE, --master=FILE
                        load master key from FILE
  -k, --sink            generate a sink key rather than a source key
  --ksv=KSV             use a specific KSV expressed in hexadecimal
  -j, --json            output key and KSV as JSON
  -t, --test            generate source and sink keys and test they work
```

Examples:

```bash
# Generate a sink key with KSV 0x54f0af39a8 and output the result in JSON
./generate_key.py -k --ksv 54f0af39a8 -j

# Generate a source key with a random KSV and output the result in a 
# human-readable form
./generate_key.py

# Run a self-test to make sure the source a sink key generation is consistent
./generate_key.py -t
```

