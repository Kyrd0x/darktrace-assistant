from darktrace_api import *
import argparse





def main():

    args = parseArgs()
    print(args)

    TAG_ID = args.t or 0

    if args.l:
        list_tags(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN)
        exit(0)

    if args.list_all:
        list_tags(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, all=True)
        exit(0)

    tagname = get_tag_name_from_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, TAG_ID)
    print("Tag name: ", tagname)

    OUTPUT_FILE = args.o if args.o else (f"{tagname}_ips.txt" if tagname else "output_ips.txt")

    entities = get_entities_from_tag_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, TAG_ID)
    written = 0
    with open(OUTPUT_FILE, "w") as f:
        for entity in entities:
            entity_id = entity['entityValue']
            entity_info = get_ip_from_entity_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, entity_id)
            print(entity_info)
            entity_ip = entity_info.get("ip") or None
            if entity_ip:
                written += 1 
                f.write(entity_ip + "\n")
   
    print(written, " / ", len(entities), " IPs written to ", OUTPUT_FILE)

def parseArgs():
    ap = argparse.ArgumentParser(description='Darktrace assistant', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=50))
    ap.add_argument('-t', metavar='tagID', help='tag ID')
    ap.add_argument('-o', metavar='outputFile', help='Output file')
    ap.add_argument('-l',  action='store_true', help='List tags info for most used tags')
    ap.add_argument('--list-all', action='store_true', help='List all tags info')

    args = ap.parse_args()
    return args

if __name__ == "__main__":
    main()

"""
arguments
-t TAG_NAME
-l TAG_LIST
-o OUTPUT_FILE
-v -> VERBOSE
-h -> HELP

"""
