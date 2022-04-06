""" TeX2LMS version 0.0.1

Converts an excel spreadsheet with list of questions written in LaTeX
into png images and generates a tab-separated file with html reference to the
images ready for import into LMS.

(c) 2022 David Pfefferlé, Perth, Australia
Release under GNU Public License (GPL)

"""

import pandas as pd
import sympy
import csv
import os

def make_template_spreadsheet(filename="template_mcq_database.ods",engine="odf"):
    """ create a template spreadsheet 

    Parameters:

    filename : name of output file
    engine="odf" : Pandas engine used to generate file
    """
    print("Creating new spreadsheet with minimal columns to make a pool of MCQ questions")
    data=pd.DataFrame(columns=["Question Type","Question Title","Filename prefix","Description 1","Answer 1","Status 1","Answer 2","Status 2"])
    # default row
    data.loc[0,"Question Type"]="MC"
    data.loc[0,"Question Title"]="Title of the question (ignored by LMS)"
    data.loc[0,"Filename prefix"]="prefix-without-spaces"
    data.loc[0,"Description 1"]="What is $2\times 2$?"
    data.loc[0,"Answer 1"]="$4$"
    data.loc[0,"Status 1"]="correct"
    data.loc[0,"Answer 2"]="$5$"
    data.loc[0,"Status 2"]="incorrect"
    
    data.to_excel(filename,engine=engine,index=False)
    print("Written "+filename)
    

def process_mcq_spreadsheet(filename,lms_url,image_resolution="200",engine="odf"):
    """ process a spreasheet and generate png images and tab-separated file for upload
    to LMS

    Parameters:

    filename : input file name containing database of questions written in LaTeX
    lms_url  : folder where the images are stored on the LMS, see content collection
    image_resolution="200" : resolution of output png images, must be text (not number)
    engine="odf" : Pandas engine to read spreadsheet
    """
    fin=pd.ExcelFile(filename,engine=engine)
    for i,q in enumerate(fin.sheet_names):
        print("Processing sheet "+str(i)+" "+q)
        dp=Data_Processor(pd.read_excel(fin,q),lms_url,image_resolution)
        dp.generate_mcq_lms_data()


class Data_Processor:
    """
    A class to help handling the data from a Pandas question sheet
    """

    def __init__(self,data,lms_url,image_resolution="200"):
        self.data=data
        self.lms_url=lms_url
        self.image_resolution=image_resolution
        
        self.headers=list(self.data.columns)
        self.answers = [s for s in self.headers if s.startswith("Answer")]
        self.statuses= [s for s in self.headers if s.startswith("Status")]

        self.folder=self.data['Filename prefix'][0]+'/'
        print("Creating/updating folder "+self.folder)
        os.makedirs(self.folder,exist_ok=True)
        
        self.outcols=['Question Type','LMS Description']

        self.make_full_description()
        self.initialise_lms_columns()
        
    def initialise_lms_columns(self):
        self.data['LMS Description']=""
        for i, (answer,status) in enumerate(zip(self.answers,self.statuses)):
            self.outcols.append('LMS '+answer)
            self.outcols.append('LMS '+status)
            self.data['LMS '+answer]=""
            self.data['LMS '+status]=""

            
    def make_full_description(self):
        descriptions = [s for s in self.headers if s.startswith("Description")]
        self.data['Full Description'] = self.data[descriptions].agg(' '.join, axis=1)


    def generate_mcq_lms_data(self):
        """ given a dataframe (sheet) of questions, generate png images and tab-separated file 
        for upload to LMS
        """
        
        for index, row in self.data.iterrows():
            prefix=row['Filename prefix']+'_'+str(index+1)

            self.convert(text=row["Full Description"],
                         img_name=prefix+'_desc.png',
                         column="LMS Description",
                         row=index)
                
            for i, (answer,status) in enumerate(zip(self.answers,self.statuses)):
                self.convert(text=row[answer],
                             img_name=prefix+'_ans'+str(i+1)+'_'+row[status]+'.png',
                             column="LMS "+answer,
                             row=index)
                
                self.data.loc[index,'LMS '+status]=row[status]
                
        self.save_lms_file()

    def save_lms_file(self):
        self.data[self.outcols].to_csv(self.folder+self.data['Filename prefix'][0]+'.txt',sep='\t',index=False,header=False,quoting=csv.QUOTE_NONE)
    
    def convert(self,text,img_name,column,row):
        if text.find("$")!=-1:
            sympy.preview(text,filename=self.folder+img_name,
                          viewer='file', euler=False,
                          dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D",self.image_resolution])
            self.data.loc[row,column]='<p><img src="'+self.lms_url+img_name+'"></p>'
        else:
            self.data.loc[row,column]=text

