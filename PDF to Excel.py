__author__ = 'Harshal Vakharia'
#===============================================
#========== Tabula Example ====================
#===============================================

import os
import tabula
import camelot
import pandas as pd

# get the current working directory of file
directory = os.path.dirname(os.path.abspath(__file__))

# list all the pdf files in the directory
all_pdf_files = [i for i in os.listdir(directory) if i.endswith(".pdf")]

# create new folder output if not exist
if os.path.exists(directory+'/output'):
    print("path already exist")
else:
    os.mkdir(directory+'/output')

# convert to csv by tabula and camelot
print("There are "+str(len(all_pdf_files))+" files to be processed")
counter=0
filesNotProcessed=0
for pdf in all_pdf_files:
    counter=counter+1
    print("="*130+"\n")
    print("No of files processed ---",counter,"and Total files processed ----",(counter/len(all_pdf_files)*100),"\n")
    print("="*130+"\n")
    try:

        inputFile = directory+"/"+pdf
        outputFile = (directory+'/output/'+pdf.replace('.pdf','_tabula.csv'))

        tabula.convert_into(inputFile, outputFile, output_format='csv', pages="all")
        tables = camelot.read_pdf(inputFile, pages='all')
        pdf_pages = len(tables)
        list_of_df = []
        for no_of_page in range(0, pdf_pages):
            list_of_df.append(pd.DataFrame(tables[no_of_page].df))
        finalCSV = pd.concat(list_of_df)
        outputFile = (directory + '/output/' + pdf.replace('.pdf', '_camelot.csv'))
        finalCSV.to_csv(outputFile)
    except:
        filesNotProcessed=filesNotProcessed+1
        print("Not able to convert pdf to csv either by tabula or camelot the reason might be pdf is password protected or scanned one")
        pass
print("Total Files Not Processed ------ ",filesNotProcessed)
print("Total Files Processed ------ ",len(all_pdf_files)-filesNotProcessed)