from os.path import expanduser
from os.path import sep as separator

def read_token_file():
    tokfile = expanduser("~") + separator + '.infinstor' + separator + '/token'
    fclient_id = None
    ftoken = None
    frefresh_token = None
    ftoken_time = None
    fservice = None
    with (open(tokfile)) as fp:
        for count, line in enumerate(fp):
            if (line.startswith('ClientId=')):
                fclient_id = line[len('ClientId='):].rstrip()
            if (line.startswith('Token=')):
                ftoken = line[len('Token='):].rstrip()
            if (line.startswith('RefreshToken=')):
                frefresh_token = line[len('RefreshToken='):].rstrip()
            if (line.startswith('TokenTimeEpochSeconds=')):
                ftoken_time = int(line[len('TokenTimeEpochSeconds='):].rstrip())
            if (line.startswith('Service=')):
                fservice = line[len('Service='):].rstrip()
    return ftoken, frefresh_token, ftoken_time, fclient_id, fservice

def write_token_file(token_time, token, refresh_token, client_id, service):
    home = expanduser("~")
    tokfile = expanduser("~") + separator + '.infinstor' + separator + '/token'
    with open(tokfile, 'w') as wfile:
        wfile.write("Token=" + token + "\n")
        wfile.write("RefreshToken=" + refresh_token + "\n")
        wfile.write("ClientId=" + client_id + "\n")
        wfile.write("TokenTimeEpochSeconds=" + str(token_time) + "\n")
        wfile.write("Service=" + service + "\n")
        wfile.close()
