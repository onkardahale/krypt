import argparse
import krypt

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group();

# -e privateKey
group.add_argument("-e", action="store_true");

# -d hash privateKey
group.add_argument("-d", action="store_true");

#arguments
parser.add_argument("--privateKey", type=str, required=True)
parser.add_argument("--hash", type=str, required=False)

args = parser.parse_args();

if args.e:
    cipher = krypt.AESCipher(args.privateKey)
    print(cipher.encrypt());
elif args.d:
    cipher = krypt.AESCipher(args.privateKey)
    print(cipher.decrypt(args.hash));

#print("privateKey is: " + args.privateKey)
