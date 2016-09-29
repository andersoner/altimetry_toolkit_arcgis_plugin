import arcpy
import pythonaddins
from datetime import datetime,timedelta
from collections import defaultdict
import csv
import fnmatch
import ftplib
import os,glob
import sys
import zipfile
import ctypes
import ftplib
global new_v1
global new_v2

class Compute(object):
    """Implementation for Template_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        if (DataSource.x1=="JASON2" and len(Location1.TC1)==1):
            date2cycle()
            JASON_Script(a=sd1,b=ed1)
            TC1=[]
        if (DataSource.x1=="ALTIKA" and len(Location1.TC1)==1):
            date2cycle()
            ALTIKA_Script(a=sd1,b=ed1)
            Location1.TC1=[]
            filelist = glob.glob("*.zip")
            for f in filelist:
                os.remove(f)
        arcpy.SelectLayerByAttribute_management(r"Jason2_Ground_Track","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management(r"SARAL_Ground_Track","CLEAR_SELECTION")
        arcpy.RefreshActiveView()
        print "Mission Accomplished"

class DataSource(object):
    """Implementation for Template_addin.combobox (ComboBox)"""
    def __init__(self):
        self.items = ["JASON2", "ALTIKA"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        DataSource.x1=selection
        datevalue1()
        file1=arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(file1)
        if selection=="JASON2":
            arcpy.SelectLayerByAttribute_management(r"Jason2_Ground_Track","CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(r"SARAL_Ground_Track","CLEAR_SELECTION")
            combobox_2.value="2008/07/12"
            combobox_2.refresh()
            for layer in layers:
                if layer.name=="Jason2_Ground_Track":
                    layer.visible=True
                if layer.name=="SARAL_Ground_Track":
                    layer.visible=False
        if selection=="ALTIKA":
            arcpy.SelectLayerByAttribute_management(r"Jason2_Ground_Track","CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(r"SARAL_Ground_Track","CLEAR_SELECTION")
            combobox_2.value="2013/03/14"
            combobox_2.refresh()  
            for layer in layers:
                if layer.name=="Jason2_Ground_Track":
                    layer.visible=False
                if layer.name=="SARAL_Ground_Track":
                    layer.visible=True
        combobox_3.value=datevalue1.out1
        combobox_3.refresh()
        new_v1=str(combobox_2.value)
        new_v2=str(combobox_3.value)
        #print new_v1, new_v2, "success"
        arcpy.RefreshActiveView()


class StartDate_CB(object):
    """Implementation for Template_addin.combobox_2 (ComboBox)"""
    def __init__(self):
        self.items = [""]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        pass
    def onFocus(self, focused):
        pass
    def onEditChange(self, text):
        new_v1=text
    def onEnter(self):
        pass
    def refresh(self):
        new_v1=combobox_2.value
        #print "Step2," + new_v1
        pass

class EndDate_CB(object):
    """Implementation for Template_addin.combobox_3 (ComboBox)"""
    def __init__(self):
        self.items=[]
        self.editable = True
        self.enabled = True
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        pass
    def onFocus(self, focused):
        pass
    def onEditChange(self, text):
        new_v2=text
    def onEnter(self):
        pass
    def refresh(self):
        new_v2=combobox_3.value
        #print "Step3," + new_v2
        pass

class GroundTrack(object):
    """Implementation for Template_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    
class GroundTrack_B(object):
    """Implementation for Template_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class Location1(object):
    """Implementation for Template_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 3
    def onMouseDownMap(self, x, y, button, shift):
        Location1.x1 = x
        Location1.y1 = y
        print "Location 1: " + str(x) + ", " + str(y)
        for row in arcpy.SearchCursor('Jason2_Ground_Track'):
            track=row.getValue('Name')
            Location1.TC1=[]
            (Location1.TC1).append(int(track.split()[2]))
        for row in arcpy.SearchCursor('SARAL_Ground_Track'):
            track=row.getValue('Name')
            Location1.TC1=[]
            (Location1.TC1).append(int(track.split()[2]))
        #print len(Location1.TC1)

class Location2(object):
    """Implementation for Template_addin.tool_1 (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 3
    def onMouseDownMap(self, x, y, button, shift):
        Location2.x2 = x
        Location2.y2 = y
        print "Location 2: " + str(x) + ", " + str(y)

def JASON_Script(a,b):
    product_='gdr_d/'
    xx1 = float(Location1.x1)
    yy1 = float(Location1.y1)
    xx2 = float(Location2.x2)
    yy2 = float(Location2.y2)
    lat1=(yy1+yy2)/2
    lon1=(xx1+xx2)/2
##        print yy1,yy2
    for row in arcpy.SearchCursor('Jason2_Ground_Track'):
##        print row.getValue('Name')
        track=row.getValue('Name')

    if len(Location1.TC1)==1:

        Path_Number = track.split()[2] 
        ftp = ftplib.FTP('avisoftp.cnes.fr',"anonymous", 'doluokeowo@yahoo.com')
        ftp.cwd('/Niveau0/AVISO/pub/jason-2/'+product_)

        PassNum= str(Path_Number)

        pathfolder='C:\Altimetry_Toolkit\JASON2\Data'+'\\'
        test1='C:/Altimetry_Toolkit/JASON2/Data/'
        f1=open(test1 + 'variables.txt',"w")
        f1.write(str(PassNum) +'\n')
        f1.write(str(lat1) +'\n')
        f1.write(str(lon1) +'\n')
        f1.write(str(yy1) +'\n')
        f1.write(str(yy2) +'\n')
        f1.close()
        # Start Code

        if not os.path.exists(os.path.dirname(pathfolder)):
            os.makedirs(os.path.dirname(pathfolder))
        #os.makedirs(pathfolder)
        dirs1=os.listdir(test1)
        tcycle=[]
        for tfile in dirs1:
            if '.nc' in tfile:
                tcycle.append(str(tfile[16:19])+','+str(tfile[12:15]))
        for cycleNum in range(int(a),int(b+1)):
            ttest1=str(PassNum)+','+str(cycleNum).zfill(3)
            if ttest1 in tcycle:
                print "Skipping downlink for PassNum:" + str(PassNum),"Cycle:"+str(cycleNum).zfill(3)
            else:
                print "Downlinking PassNum:" + str(PassNum),"Cycle:"+str(cycleNum).zfill(3)
                cycle_='cycle_'+str(cycleNum).zfill(3)
                ftp.cwd('./'+cycle_) # relative
                ff =ftp.nlst('*_'+ PassNum + '_*')
                if len(ff) == 1:
                    ftp.retrbinary('RETR {}'.format(ff[0]),open( pathfolder + ff[0],"wb").write)
                ftp.cwd('..') # Move up one directory
        print "Data downlink completed"
        ftp.close()    
        os.chdir(test1)
        print "Now processing data in Matlab"
        os.system('"C:/Altimetry_Toolkit/JASON2/Data/JASON2_Script.exe"')
##        os.system('matlab -r JASON2_Script')

def ALTIKA_Script(a,b):
    product_='gdr_t/'
    xx1 = float(Location1.x1)
    yy1 = float(Location1.y1)
    xx2 = float(Location2.x2)
    yy2 = float(Location2.y2)
    lat1=(yy1+yy2)/2
    lon1=(xx1+xx2)/2
##        print yy1,yy2
    for row in arcpy.SearchCursor('SARAL_Ground_Track'):
##        print row.getValue('Name')
        track=row.getValue('Name')

    if len(Location1.TC1)==1:
        Path_Number = track.split()[2] 
        ftp = ftplib.FTP('avisoftp.cnes.fr',"anonymous", 'doluokeowo@yahoo.com')
        ftp.cwd('/Niveau0/AVISO/pub/saral/'+product_)

        PassNum= str(Path_Number)

        pathfolder='C:\Altimetry_Toolkit\SARAL\Data'+'\\'
        test1='C:/Altimetry_Toolkit/SARAL/Data/'
        f1=open(test1 + 'variables.txt',"w")
        f1.write(str(PassNum) +'\n')
        f1.write(str(lat1) +'\n')
        f1.write(str(lon1) +'\n')
        f1.write(str(yy1) +'\n')
        f1.write(str(yy2) +'\n')
        f1.close()
        if not os.path.exists(os.path.dirname(pathfolder)):
            os.makedirs(os.path.dirname(pathfolder))
        dirs1=os.listdir(test1)
        tcycle=[]
        for tfile in dirs1:
            if '.nc' in tfile:
                tcycle.append(str(tfile[16:20])+','+str(tfile[12:15]))
        for cycleNum in range(int(a),int(b+1)):
            ttest1=str(PassNum)+','+str(cycleNum).zfill(3)
            if ttest1 in tcycle:
                print "Skipping downlink for PassNum:" + str(PassNum),"Cycle:"+str(cycleNum).zfill(3)
            else:
                print "Downlinking PassNum:" + str(PassNum),"Cycle:"+str(cycleNum).zfill(3)
                cycle_='cycle_'+str(cycleNum).zfill(3)
                ftp.cwd('./'+cycle_) # relative
                ff =ftp.nlst('*_'+ PassNum + '_*')
                if len(ff) == 1:
                    ftp.retrbinary('RETR {}'.format(ff[0]),open( pathfolder + ff[0],"wb").write)
                ftp.cwd('..') # Move up one directory
        print "Data downlink completed"
        
        ftp.close()
        print "Processing data in Matlab"
        os.chdir(pathfolder)
        for filename in os.listdir(os.getcwd()):
            if filename.endswith('.zip'):
                    with zipfile.ZipFile(filename,"r") as zh:
                            zh.extractall()

##        os.system('matlab -r ALTIKA_Script')
        os.system('"C:/Altimetry_Toolkit/SARAL/Data/ALTIKA_Script.exe"')
        
def date2cycle():
    global sd1,ed1
    columns = defaultdict(list) 

    ##Reading the CSV and creating a list for columns
    if DataSource.x1=="JASON2":        
        with open('C:\Altimetry_Toolkit\Template\Jason2_Cycle.csv') as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items(): 
                    columns[k].append(v)

    if DataSource.x1=="ALTIKA":        
        with open('C:\Altimetry_Toolkit\Template\SARAL_Cycle.csv') as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items(): 
                    columns[k].append(v)

    dates=columns['Date']
    cycle=columns['Cycle']

    ##Changing the dateformat from string to date
    DTlist = [datetime.strptime(date,'%Y/%m/%d').date() for date in dates]

    dt=datetime.strptime(combobox_2.value,"%Y/%m/%d").date()

    ##Searching the given date within the list. If not found, pick the previous closest date
    out1=min(DTlist,key=lambda date:abs(dt-date))
    #print out1

    ##Get the index number for the matched date and find the cycle number
    index1=DTlist.index(out1)
    sd1=int(cycle[index1])

    dt=datetime.strptime(combobox_3.value,"%Y/%m/%d").date()

    out1=min(DTlist,key=lambda date:abs(dt-date))
    #print out1
    index1=DTlist.index(out1)
    ed1=int(cycle[index1])     

def datevalue1():
    #current date
    d1 = datetime.today()
    d2=d1-timedelta(days=60)
    d3=datetime.strftime(d2,"%Y/%m/%d")
    #print d3
    columns = defaultdict(list) 

    ##Reading the CSV and creating a list for columns
    if DataSource.x1=="JASON2":        
        with open('C:\Altimetry_Toolkit\Template\Jason2_Cycle.csv') as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items(): 
                    columns[k].append(v)

    if DataSource.x1=="ALTIKA":        
        with open('C:\Altimetry_Toolkit\Template\SARAL_Cycle.csv') as f:
            reader = csv.DictReader(f) 
            for row in reader: 
                for (k,v) in row.items(): 
                    columns[k].append(v)

    dates=columns['Date']
    cycle=columns['Cycle']

    ##Changing the dateformat from string to date
    DTlist = [datetime.strptime(date,'%Y/%m/%d').date() for date in dates]

    dt=datetime.strptime(str(d3),"%Y/%m/%d").date()

    ##Searching the given date within the list. If not found, pick the previous closest date
    out=min(DTlist,key=lambda date:abs(dt-date))
    datevalue1.out1=datetime.strftime(out,"%Y/%m/%d")
    #print datevalue1.out1


