import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Generate equally spaced bins from the set provided in the stdin')
    parser.add_argument('-d','--dest', metavar='N', type=str, help='path to save the result')
    args = parser.parse_args()
    return args