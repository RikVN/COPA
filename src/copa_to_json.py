#!/usr/bin/env python
# -*- coding: utf8 -*-


'''Convert tab-separated COPA data sets to JSON, so it works with run_copa.py
   It's possible to only keep a subset of the data set (see -d arguments)
   It's also possible to add a token indicating whether an example is cause or effect
   In that case, you have to specify the language iso code with -l'''


import argparse
import json


def main():
    '''Main function of the script'''
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", required=True, help="input file (tab separated)")
    parser.add_argument("-o", "--output_file", required=True, help="output file in JSON format")
    parser.add_argument("-l", "--language", default='', 
                        help="Language, only needed when adding cause/premise token")
    parser.add_argument("-d", "--data_type", default ="all", choices=["all", "cause","effect", "token"],
                        help="Do we keep all data or only cause/premise? When using 'token' we add a token that indicates cause or effect to the premise")
    args = parser.parse_args()

    # When we add a token to indicate cause/effect, we do so in the actual language
    # That seems to make more sense than a new token, or to do it in English
    typ_dict = {}
    typ_dict["bg-cause"] = "причина"
    typ_dict["tr-cause"] = "neden"
    typ_dict["mk-cause"] = "причина"
    typ_dict["bg-effect"] = "ефект"
    typ_dict["tr-effect"] = "Efekt"
    typ_dict["mk-effect"] = "ефект"

    # Read in input file and create list of dictionaries
    data_list = []
    with open(args.input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Split line by tab character and remove newline character
            typ, label, premise, option1, option2 = line.strip().split('\t')

            # For "all" and "token" keep all data, otherwise just cause/effect
            if args.data_type in ["token", "all"] or args.data_type == typ:
                if args.data_type == "token":
                    if not args.language:
                        raise ValueError("Specify language iso code with -l when using -d token")
                    # Premise now contains cause/effect in target language
                    premise = typ_dict[args.language + "-" + typ] + ' ' + premise

                # Create dictionary with keys type, label, premise, option1, option2
                data_dict = {
                    #'type': items[0],
                    'label': int(label) - 1,
                    'premise': premise,
                    'option1': option1,
                    'option2': option2
                }
                data_list.append(data_dict)

    # Write dictionary to output file in JSON format
    with open(args.output_file, 'w', encoding='utf-8') as out_f:
        for dic in data_list:
            json.dump(dic, out_f, ensure_ascii=False)
            out_f.write('\n')


if __name__ == "__main__":
    main()
