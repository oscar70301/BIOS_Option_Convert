import re
import time
import sys
import os


def main(argv):
    
    #Remove old output file
    try:
        os.remove("output.txt")
        print("Remove old output file")
    except:
        pass

    #Read Scelnx file
    try:
        filename = sys.argv[1]
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        print("convert.py <Scelnx file>")
        sys.exit(2)

    buf = []
    buf.clear()
    cnt = 0
    size = len(lines)
    IsNum = 0

    for cur in lines:
    
        #Print convert status.
        cnt = cnt + 1
        sys.stdout.write('\r')
        sys.stdout.flush()
        print("Converting ",end ='')
        print(cnt,end ='')
        print('/',end='')
        print(size,end='')

        if re.search(r'Setup Question\t=\s*(.+)', cur) != None:
        
            #If find the "Setup Question" String, output the buf to the output file.
            with open("output.txt", "a") as fp1:
            
                #Normal option
                if IsNum == 0:
                    try:
                        fp1.write(buf[0]+' '+'(')
                        fp1.write(buf[3])
                        for i in buf[4:]:
                            fp1.write('/'+i)
                        fp1.write(')['+buf[2]+']'+'\n')
                        fp1.write(buf[1]+'\n')
                    except:
                        fp1.write('\n')
                    buf.clear()
                    
                #Numerical option
                else:           
                    try:
                        fp1.write(buf[0]+' '+'['+buf[2]+']'+'\n')
                        fp1.write(buf[1]+'\n')
                    except:
                        pass
                    buf.clear()
            
            #Add the Setup Question to buf[0].
            Q = re.search(r'Setup Question\t=\s*(.+)', cur)
            buf.append(Q.group(1))
            
        if re.search(r'Help String\t=\s*(.+)', cur) != None:
        
            #Add the help string to buf[1].
            H = re.search(r'Help String\t=\s*(.+)', cur)
            buf.append(H.group(1))

#------------------------------------------------------------------------------------------        
#There are two modes of BIOS options, which will be separated here and identified by IsNum.|
#------------------------------------------------------------------------------------------   
       
        #Normal option
        if re.search(r'BIOS Default=\[[A-F0-9]{2}\](.*?)(\n|\t)', cur) != None:
        
            #Add the Default setting to buf[2].
            Def = re.search(r'BIOS Default=\[[A-F0-9]{2}\](.*?)(\n|\t)', cur)
            buf.append(Def.group(1))
            
            #Is Normal option
            IsNum = 0
            
        #Numerical option
        elif re.search(r'Value\t=*(.+)', cur) != None:
            #Add the default value to buf[2].
            Val = re.search(r'[A-F0-9]', cur)
            try:
                buf.append(Val.group())
            except:
                pass
                
            #Is numerical option
            IsNum = 1
        
        #If it is a Normal option, store other options in buf[3:]
        elif re.search(r'\[[A-F0-9]{2}\](.*?)(\n|\t)', cur) != None:
            Opt = re.search(r'\[[A-F0-9]{2}\](.*?)(\n|\t)', cur)
            buf.append(Opt.group(1))
    
    #Convert complete
    print("\nConvert complete")
    print("Result is saved in output.txt")

if __name__ == "__main__":
   main(sys.argv[1:]) 