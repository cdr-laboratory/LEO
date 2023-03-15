from shutil import copyfile
import sys 

def main():

    workdir = '../../LEO/genie-userconfigs/'
    src         =workdir+sys.argv[1]
    dst         =workdir+sys.argv[2]
    inlist      =int(sys.argv[3])
    replacelist =sys.argv[4]
    
    # print(src,dst)
    # print(inlist,replacelist)
    
    if dst!=src:copyfile(src, dst)

    file_name = dst
    
    with open(file_name, mode="r") as f:
        # data_lines = f.read()
        data_lines = f.readlines()
        
    # data_lines = data_lines.replace(str(inlist), str(replacelist))
    # print(data_lines)
    data_lines.insert(inlist, replacelist+"\n")
    # print(data_lines)
    
    with open(file_name, mode="w") as f:
        data_lines="".join(data_lines)
        # print(data_lines)
        f.write(data_lines)
    
if __name__=='__main__':
    main()