import subprocess
def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    # print(result.stdout)
    # print(result.returncode)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False

def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

folderIn = '/home/user/tst'
folderOut = '/home/user/tstout'

hash = getout(f"crc32 {folderOut}/arh1.7z")
print(hash, type(hash))