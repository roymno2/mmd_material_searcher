# -*-coding:gbk-*-
import os
import subprocess
import sys
import commands

default_path_7z_cmd='c:\\Program Files\\7-Zip\\7z.exe'

def walk_in_dir(root_path):
    
    for root, dirs, files in os.walk(root_path, True):
        for name in files:
            if len(name)>0:
                if name[0]!="$":
                    front_name,ext_name=os.path.splitext(name)
                    if ext_name.lower() in [".rar",".7z",".zip"]:
                        zipfilepath=root+os.path.sep+name
                        cmd = '"'+default_path_7z_cmd+'" l "'+ windows_cmd_sep_copy(zipfilepath)+'"'
                 
                        run_result=run_in_subprocesspopen(cmd)
                        if run_result is not None:
                            if run_result["model"]!=[]:
                                print root+os.path.sep+name+" find model"
                                print "\n".join(run_result["model"])+"\n"
                            if run_result["motion"]!=[]:
                                print root+os.path.sep+name+" find motion"
                                print "\n".join(run_result["motion"])+"\n"
                        else:
                            print "unzip error "+root+os.path.sep+name
                            
                    if ext_name.lower() in [".pmd",".mpo",".pmx",".x"]:
                        print root+os.path.sep+name+" find model"
                        print ""
                    if ext_name.lower() in [".vmd"]:
                        print root+os.path.sep+name+" find motion"
                        print ""
                        
                
            

def which_platform():
    # 判定是 windows 还是 linux
    import platform
    pythonVersion = platform.python_version()
    uname = platform.uname()
    if len(uname)>0:
        return uname[0]
        

def run_in_subprocesspopen(cmd):
    try:
        flag_mmd_cell={}
        flag_mmd_cell["model"]=[]
        flag_mmd_cell["motion"]=[]
       

        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT) 
        k=0
        result = res.stdout.readlines()

        for i in result:
            line_c=i.strip()
            

            if len(line_c)>6:   
                line_array=line_c.split( )
                if line_c[0:5]=="-----" and len(line_array)==5:
                    if k==0:
                        k=1
                        first_part=" ".join(line_array[0:4])+" "
                        file_part_len=len(first_part)
                    else:
                        k+=1
                else:
                    if k==1:
                        if len(line_c)>(file_part_len+2):
                            part_line_c=line_c[file_part_len+1:]     
                            front_name,ext_name=os.path.splitext(part_line_c)
                            if ext_name.lower() in [".pmd",".mpo",".pmx",".x"]:
                                
                                flag_mmd_cell["model"].append(part_line_c)
                            if ext_name.lower() in [".vmd"]:
                                flag_mmd_cell["motion"].append(part_line_c)
                                
        return flag_mmd_cell
    except:
        s=sys.exc_info()
        print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
        return None



                
def windows_cmd_sep_copy(org_path):
    path=org_path.replace('\\','\\\\')
    return path
       
        

if len(sys.argv)==2:
    walk_in_dir(sys.argv[1])
else:
    print "Usage:search_run.py {dir path}"
