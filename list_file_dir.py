import os 
import sys 

def main():
    reqPath=input("Enter your path to get list of files & Dir's: ")
    # if not os.path.exists(reqPath) :
    #     print(f'Given Path {reqPath} Not Exist')
    #     sys.exit(1)
    # if os.path.isfile(reqPath) :
    #     print(f'Given Path {reqPath} is for file, so cant get list of files & dirs ')
    #     sys.exit(2)
    try: 
        allFD=os.listdir(reqPath)
    except FileNotFoundError:
        print(f'Given Path {reqPath} Not Exist')
        sys.exit(1)
    except NotADirectoryError :
        print(f'Given Path {reqPath} is for file, so cant get list of files & dirs ')
        sys.exit(2)
    except PermissionError :
        print(f'We dont have the read acces for the given path: {reqPath}')
        sys.exit(3)
    except Exception as e :
        print(e)
        sys.exit(4)

    if len(allFD) == 0 :
        print(f"There are no file/dirs in a given path : {reqPath}")
        # sys.exit(0)          
        return None 
    for eachFD in allFD:
        # print(os.path.join(reqPath,eachFD))
        if os.path.join(reqPath,eachFD).endswith('.py') :
            print(os.path.join(reqPath,eachFD))
    # FileNotFoundError
    # NotADirectoryError
    return None 

if __name__ == "__main__":
    main()
    sys.exit(0)