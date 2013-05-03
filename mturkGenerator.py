#!/usr/bin/python
#^DO NOT MOVE^
#Original by David Landy
#Modified by Gage Holden Spring 2013 to support the mturkTemplate model of doing things, and incorporate
#file processing, etc.

#This is designed to take tab delimited files and turn them into wonderful online things
#Hopefully this goes well

#Goal: take a properly formatted text file and turn it into a series of forms presented to the participant
#Format as follows (TABS MUST SEPERATE EACH ELEMENT ON EACH LINE):
#ItemNumber Condition   0  Type    -1   Stimuli

#First line of each file is stored as a header variable and should show up in the final data

# Any defining variables are globalized here
experimentCode = None
exclusionList = None
folderName = None
skipAtStart = 0
skipAtEnd = 0

#Import the CGI module
import cgi
import cgitb
cgitb.enable()
from datetime import date
from mturkSupport import *

import os
import csv

needsMouse = []

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

consent_boilerplate = """<b>Statement of research:</b> Your responses to this HIT will be used in a study conducted by Dr. David Landy, \
                        and may be included (anonymously) in scientific publications.  By submitting this \
                        HIT, you agree that you are at least 18 years old, and that we may include your \
                        responses. If you have any questions about your role as a research participant, \
                        please see this <a href="http://davidlandy.net/consents/statement_of_consent.html">statement of consent</a>, or contact The University of \
                        Richmond Institutional Review Board at rjonas at richmond dot edu."""

def print_jquery_mouse_detect(lbl = "1"):
    continueButton = "cont" + str(int(lbl[4:])+1) + "stim"
    return """
               $("#pointer_div""" + lbl + """").click(function(e){
                   var offset = $("#pointer_div""" + lbl + """").offset();
                   var x = e.pageX - offset.left;
                   var y = e.pageY - offset.top;
                  $('#form_x""" + lbl + """').val(x);
                  $('#form_y""" + lbl + """').val(y);
                  $('.follow').css(
                                 'left', (x));
                enableElement('""" + continueButton + """');
                                 
                  $('.follow').css('visibility','visible');
               });





    """

def heading(title):
    return """<HTML>
            <HEAD>
            <TITLE>""" + title + """</TITLE>
            <style>
            body{

            }
            .page{
                    position: absolute;
                    top: 10;
                    left: 100;
                    right: 50;
                    visibility: hidden;
            }
            </style>
            </HEAD>


            <BODY BGCOLOR = white>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
           
            <form id="mturk_form" method="GET" action="http://www.mturk.com/mturk/externalSubmit">

            """

mouse_scripts = """"""

def numberFill(stimuli, number):
    print stimuli[0] + """<input onClick="enableElement('""" + "cont" + str(int(number)+1) +"stim" + """')" name='"""+ number +"""number' type="number" value="">"""
    #onClick="submitForm()"
    
def wordFill(stimuli, number):
    print stimuli[0] + """<input onClick="enableElement('""" + "cont" + str(int(number)+1) +"stim" + """')" name=""" + number + """text type="text" value="">"""
    
def multipleChoice(stimuli, number):
    print "<p>\n" + stimuli[0] + "</br>"
    for option in stimuli[1:]:
        if not option == '':
            print """ <input type='radio' onClick="enableElement('""" + "cont" + str(int(number)+1) +"stim" + """')" name = '"""+number+"""radio' value ='"""+option+"""'>"""+option+"""<br/>"""
    print "\n</p>"
    
def instruction(stimuli):
    print "<p>\n" + stimuli[0] + "</br>"
    print "\n</p>"

def numberline(stimuli, number):
    global needsMouse
    needsMouse.append("stim" + number)
    print_number_line_task(stimuli[0],stimuli[1],stimuli[2], number)
    print

def printFooter():
    global needsMouse
    print """
    <script type="text/javascript">
    jQuery(document).ready(function(){
    """ + " ".join([print_jquery_mouse_detect(x) for x in needsMouse]) +\
    """

    })
    </script>
    """


def picture(stimuli):
    #import Image
    image = "../../images/TML30/"+stimuli[0]
    
    #width,height = (Image.open(image)).size
    #print "<p>\n"
    #print image
    print "<p>\n"
    print """ <img src=\""""+ image +"""\" id="Training">"""#,width,height)
    print "\n</p>"

def print_preview_condition():
    print """ """


# Define function to generate HTML form.
def generate_HIT(active=True, condition=0, assignmentId="0", workerId="0", stimRows = []):
    if not active:
        condition = 0
    else:
        condition = int(condition)

    print multiform_scripts
    print mouse_scripts
    
    print '<input type="hidden" name="assignmentId" value="' + assignmentId + '">' 
    print '<input type="hidden" name="workerId" value="' + str(workerId) + '">'     
    print '<input type="hidden" name="condition" value="' + str(condition) + '">'
    
    print heading("Questionnaire")
    
    print """<div id="page1" class="page" style="visibility:visible;">"""

    print consent_boilerplate
    print_instructions()
    
    number = -1
    
    disableContinue = False
    element = -1
    value = -1
    global skipAtEnd
    global skipAtStart
    startRow = skipAtStart+1
    for element in stimRows[startRow:]:
        element['Stimuli'][0] = element['Stimuli'][0].replace('&NL','</br>')
        #element['Stimuli'][0] = element['Stimuli'][0].replace("'","\\'")
        #element['Stimuli'][0] = element['Stimuli'][0].replace('"','\\"')

        if(int(element['ItemNumber'])>skipAtEnd):
            break
        print_diff_continuation(str(int(element['ItemNumber']))+"stim", disableContinue)
        print_diff_head(element['ItemNumber']+"stim")
        disableContinue = True
        if(element['Type']=='numberFill'):
            numberFill(element['Stimuli'],element['ItemNumber'])
        elif(element['Type']=='multipleChoice'):
            multipleChoice(element['Stimuli'],element['ItemNumber'])
        elif(element['Type']=='wordFill'):
            wordFill(element['Stimuli'],element['ItemNumber'])
        elif(element['Type']=='instruction'):
            instruction(element['Stimuli'])
            disableContinue = False
        elif(element['Type']=='numberline'):
            numberline(element['Stimuli'],element['ItemNumber'])
        elif(element['Type']=='picture'):
            picture(element['Stimuli'])
            disableContinue = False
        value = int(element['ItemNumber'])
    
    print_diff_continuation(str(int(element['ItemNumber']))+"stim", disableContinue)
    print_diff_head(str(int(element['ItemNumber']))+"stim")

    print """Thanks for your help!"""
    
    if active:
        print """<center><input id="submitButton" type="button" name="Submit" value="Submit" onClick="submitForm()"></center>"""
    else:
        print """<center><input id="submitButton" type="button" name="Submit" disabled="True" value="You must ACCEPT the HIT before you can submit the results."></center>"""
    
    print '<input type="hidden" name="assignmentId" value="' + assignmentId + '">' 
    print '<input type="hidden" name="workerId" value="' + str(workerId) + '">'     
    print '<input type="hidden" name="condition" value="' + str(condition) + '">'

    print """
    </div>
    </form>
    """
    print """
        <script language="Javascript">
         var form = document.getElementById('mturk_form');
        if (document.referrer && ( document.referrer.indexOf('workersandbox') != -1) ) {
            form.action = "http://workersandbox.mturk.com/mturk/externalSubmit";
        }
         </script>
    """

    print """
        
        <script type="text/javascript">
        function submitForm()
        {
        script = document.createElement('script'); // Create an element """
    global experimentCode
    print "script.src = 'http://davidlandy.net/cgi-bin/update_worker_file.cgi?workerId=" + str(workerId) + "&experiment=" + experimentCode + "';" 
    print """
        script.type = "text/javascript"
        document.getElementsByTagName("head")[0].appendChild(script);
        """
    print """
        }
        </script>
        
    """
    
    
    print "</BODY>\n"
    print "</HTML>\n"

# Call main function.
   
def generateTurk(definingBits={}):
    global exclusionList
    global experimentCode
    global skipAtStart
    global skipAtEnd
    global folderName
    exclusionList = definingBits['exclusionList']
    experimentCode = definingBits['experimentCode']
    folderName = definingBits['folderName']
    skipAtStart = definingBits['skipAtStart']
    skipAtEnd = definingBits['skipAtEnd']
    
    dictIn = {}
    stimRows = []
    global workerId
    form = cgi.FieldStorage()
    
    if form.has_key("condition"):
        condition = form["condition"].value
        int(condition)
        filename=""
        
        for name in os.listdir("../../stimuli/"+ folderName + "/"):
            if name[0] == condition:
                filename=name
        fileIn = open("../../stimuli/"+folderName +"/" + filename, 'rU')

        i = 0
        for line in fileIn:
            i += 1
        fileIn.seek(0)
        
        dictIn = csv.DictReader(fileIn,dialect="excel-tab", fieldnames = ['ItemNumber','Condition','Zero','Type','NegOne'], restkey = "Stimuli", quoting = csv.QUOTE_NONE)
        for i in range(i):
            stimRows.append(dictIn.next())
            
        skipAtEnd = i - skipAtEnd
        
        #print stimRows
        #ARGH NO
        #condition = "0"
    else:
        condition = "0"
        # Check whether worker is previewing, and generate the appropriate HIT for them.
    
    # Check whether this worker appears on the participation list
    if not form.has_key("workerId"):
        workerId = "0"
        condition = "0"
        generate_error("NO_WORKER_ID")

    else:
        workerId = form["workerId"].value
        old_workers = {}
        try:
             inp = open("../../workers.txt", "r")
             for line in inp.readlines():
                line_split = line.split()
                if len(line_split)>=2:
                    old_workers[line_split[0]+":"+line_split[1]] = line_split[1]
             inp.close()

                        
        except: # If there's an error, just leave old_workers empty and move on
            pass

        for item in exclusionList:
            if old_workers.has_key(workerId+":"+item):
                generate_reparticipation_error()
                return 0

        if (form.has_key("assignmentId")):
            if form["assignmentId"].value == "ASSIGNMENT_ID_NOT_AVAILABLE" or condition=="0":
                generate_HIT(False, condition, form["assignmentId"].value, workerId, stimRows)
            else:
            	generate_HIT(True, condition, form["assignmentId"].value, workerId, stimRows)
        else:
            generate_error("NO_ASSIGNMENT_ID")
        
    printFooter()


#main(exclusionList)
