import os

file_name='SocialList.txt'

f=open(file_name,'r')


counter=0
i=1
for line in f:

    if counter==1:
        counter=0
        i+=1

    splitfilename=os.path.splitext(file_name)[0]+str(i)+'.txt'
    sf=open(splitfilename,'a')
    sf.write(line.strip('\n'))
    sf.close()
    counter+=1

f.close()
