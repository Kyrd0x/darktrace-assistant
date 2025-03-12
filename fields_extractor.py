from darktrace_api import *
import argparse

def main():
    args = parse_arguments()
    print(args)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse arguments for the app")
    
    parser.add_argument("--model", type=str, required=True, help="Model name (mandatory)")
    parser.add_argument("--field", type=lambda s: s.split(","), default=None, help="Fields to process, comma-separated (default: all)")
    parser.add_argument("--status", type=str, choices=["check", "uncheck", "all"], default="all", help="Status filter (default: all)")
    parser.add_argument("--type", type=str, choices=["csv", "txt", "json"], default="csv", help="Output type (default: csv)")
    parser.add_argument("--output", type=str, default="output.csv", help="Output filename (default: output.csv)")
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()


"""

--model="Domain Fluxing" (mandatory)
--field=x1,x2,x3 (default all) 
--aknl -unaknl --all (default all)
--type=csv,txt,json (default csv)
--output=filename (default output.csv)

"""