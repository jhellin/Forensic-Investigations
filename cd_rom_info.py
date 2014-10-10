import time
import os
import subprocess 
import csv

def insert_char(string, char, index):
    return string[:index] + char + string[index:]
	
blocksize='isoinfo -d -i /dev/cdrom | grep "^Logical block size is:" | cut -d " " -f 5'
blockcount= 'isoinfo -d -i /dev/cdrom | grep "^Volume size is:" | cut -d " " -f 4'

ts = int(time.time())

print "-----------------------------------------------------"
print "Script para Calcular MD5 y extrater fecha de creacion"
print "Media: CD-ROM, DVD"
print "-----------------------------------------------------"

print 'Creating report file: '+'report-'+str(ts)+'.csv'

with open('report-'+str(ts)+'.csv', 'w') as fp:
	a = csv.writer(fp, delimiter=',')
	while True:
		#label
		labelVar = raw_input("Etiqueta (-1 para salir): ")
		if labelVar == '-1':
			break

		#md5
		blocksizeOut = subprocess.check_output(blocksize, shell=True)
		blockcountOut = subprocess.check_output(blockcount, shell=True)

		cmd = 'dd if=/dev/cdrom bs='+blocksizeOut.rstrip('\n')+' count='+blockcountOut.rstrip('\n')+' conv=notrunc,noerror | md5sum'	
		md5Out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) 
		output = md5Out.communicate()[0]
	
		#md5Out = subprocess.check_output(cmd, shell=True)

		#date created
		disk = file('/dev/cdrom','rb')
		disk.seek(33581)
		sDate = disk.read(16)
		sDateFormat = insert_char(sDate, '-', 4) #Year
		sDateFormat = insert_char(sDateFormat, '-', 7) #Month
		sDateFormat = insert_char(sDateFormat, ' ', 10) #Space
		sDateFormat = insert_char(sDateFormat, ':', 13) #Hour
		sDateFormat = insert_char(sDateFormat, ':', 16) #Minute
		sDateFormat = insert_char(sDateFormat, '.', 19) #Sec

		print labelVar+','+output.rstrip('\n').rstrip('-').replace(" ", "")+','+sDateFormat
  		data = [labelVar, output.rstrip('\n').rstrip('-').replace(" ", ""), sDateFormat]
		a.writerow(data)
		print "Inserta otro CD ROM..."

print "Good bye!"
