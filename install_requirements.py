import subprocess as sub

def checkInstallations(requirement):
    """Check the reqiored libraries are installed or not, if not install them"""
    for line in requirement:
        print("Checking {} library ".format(line))
        sub.run("pip install {}".format(line))


def checkRequiremnets():
    """Check Requirements of installed library"""
    library=input("Enter the library name: ")
    response=sub.check_output("pip show {}".format(library))
    response=response.decode('utf-8')
    for line in response.split('\n'):
        line=line.split(":")
        if(line[0]=='Requires'):
            requirement=line[1].strip().split(", ")
    return requirement
    

def main():
    requirement=checkRequiremnets()
    checkInstallations(requirement)


if __name__=="__main__":
    main()
