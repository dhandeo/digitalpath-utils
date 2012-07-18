import subprocess
#shell is set to false so we don't get the black command line window
#stdout=subprocess.PIPE shortly is the magic line
#that allows us to read back the information that is outputted on the command line window
proc = subprocess.Popen('python child.py',
                        shell=False ,
                        stdout=subprocess.PIPE,
                        )

while True:
    output = proc.stdout.readline()
 
    if "%" in output:
        print output.rstrip()
 
    if output is "":
        print "DONE!"
        break
