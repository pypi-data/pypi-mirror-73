import sys
import argparse
from pancli.commands.package import PackageCommand

def main(argv = None):
    if argv is None:
        argv = sys.argv
    
    parser = argparse.ArgumentParser('')
    parser.add_argument('command', help='available commands: package')
    args = parser.parse_args()
    print(args.command)
    command = None
    if args.command == 'package':
        command = PackageCommand()
    else:
        print(f"Invalid command {args.command}")
    
    if command:
        command.run(argv)
    else:
        parser.print_help()
        

