#!/usr/bin/python
#Some necessary support methods
#Original by David Landy
#Modified by Gage Holden Spring 2013

import re
import cgi
import cgitb
cgitb.enable()
from datetime import date

def print_likert_scale(name, values, labels=[], vertical=True):
    if labels==[]:
        labels = values
    print """
    <table align=center>
    """
    if vertical:
        for i in range(len(values)):
            print """
            <tr >
            <td align=center> <input name=""" + '"' + name + '"' +   """ type="radio" value=""" + '"' + str(values[i]) + '"' + """ ></td>
            <td > <p style="font-size:100%">""" + str(labels[i]) +"""</p> </td>

                </tr>
            """
    else:
        print "<tr>"
        for i in range(len(values)):
            print """
            
            <td align=center style="width:200px;"> <input name=""" + '"' + name + '"' +   """ type="radio" value=""" + '"' + str(values[i]) + '"' + """ ></td>
            <td > <p style="font-size:100%">""" + str(labels[i]) +"""</p> </td>
            """
        print "</tr>"

    print """

    </table>
    """


def print_hybrid_to_numeral(active=True, lst=[]):
    print "<br/><br/>"
    if active:
        for i in range(len(lst)):
            print "Please write " + lst[i] + " as a numeral:"
            print """<input name="hybridtonum"""+str(i)+"""" type="text" value="">"""
            print "<br/><br/>"
    else:
        print "A few questions about your understanding of numbers during mathematics will be put here once you ACCEPT the HIT"
        

def print_number_scale(name, values):

    print """
    <table align=center>
    <tr align=center>
    """
    for i in range(len(values)):
        print """
        <td align=center> <input name=""" + '"' + name + '"' +   """ type="radio" value=""" + '"' + str(values[i]) + '"' + """ ></td>

        """
    print """     
    </tr>
    <tr align=center>
    """

    print """
    </tr>
    </table>
    """

def print_number_line_task(pick, start, end, itemNumber, active = True,):
    if('Thousand' in start):
        #formName = ''.join(re.split(' |,',pick+start+end))
        print_number_line(active, pick, "stim" + itemNumber, "../../images/TML30/tablineTH_BIL_WORD.png")

def print_number_line_tasks(active, numbers=[], tasks=[], withContinuation=False, image='../../images/numline.png'):
    if withContinuation and len(tasks)>0:
        print_diff_continuation('numberlinetask' + tasks[0])
    for i in range(len(tasks)-1):
        print_diff_head('numberlinetask' + tasks[i])
        print_number_line(active, numbers[i], tasks[i], image)
        print_diff_continuation('numberlinetask' + tasks[i+1])
    print_diff_head('numberlinetask' + tasks[len(tasks)-1])
    print_number_line(active, numbers[len(tasks)-1], tasks[len(tasks)-1], image)

    
    
def print_instructions():
    print """
<h4> Instructions: Please read the instructions for each task, and follow them. 
Please don't write anything down.</h4>
    """

def print_number_line_instructions(active=True):
    print """ <h4> Instructions: Please read these instructions about your next task.  Click continue when you are ready for the
              task itself.</h4>
            """

    print """ <img src="../../images/TML-5-Instructions.png" width=610 height=322  id="Instructions">"""

def print_number_line(active=True, number="1 million", formIndex="1", image='../../images/numline.png'):
    #import re
    #formIndex = re.sub(r'[^\w]', '', formIndex)
    if active:    
        print """
        <div id="pointer_div"""+formIndex+""""  style = "background-image:url("""+image+""");width:508;height:178px;">
        <img src="../../images/vertical_line.png" id="vertical_line"""+formIndex+""".png" class="follow" style="height:70;position:absolute;visibility:hidden;z-index:2;">
        </div>
        

        <input type="hidden" id="form_x"""+formIndex+"""\" name="form_x"""+formIndex+"""" size="4" />
        <input type="hidden" id="form_y"""+formIndex+"""\" name="form_y"""+formIndex+"""" size="4" />
        

        <p></p>



    """
   
        print """  <h4>""" + number + """: Please choose a place on this number line that corresponds to the value """ + number + """.
                    Mark your choice by clicking on the line.
                    You may not be able to see the mark you place--That's okay!  We'll record it.
                    If click multiple times, we'll get your last click.</h4>

    """
    else:
        print """        <img src="../../images/vertical_line.png" id="vertical_line"""+formIndex+""".png" style="height:70;position:relative;visibility:visible;z-index:2;">
"""
        print """<p><em>: Once you accept this hit, you will be asked to select a place corresponding to a number, on a line that will appear above</em></p>"""


# Turk code


def submit_scripts(workerId, experimentCode):
        return   """    
        <script language="Javascript">
         var form = document.getElementById('mturk_form');
        if (document.referrer && ( document.referrer.indexOf('workersandbox') != -1) ) {
            form.action = "http://workersandbox.mturk.com/mturk/externalSubmit";
        }
         </script>

      <script type="text/javascript">
        function submitForm()
        {
        script = document.createElement('script'); // Create an element 

    script.src = 'http://davidlandy.net/cgi-bin/update_worker_file.cgi?workerId=""" + str(workerId) + """&experiment=""" + experimentCode + """';
    script.type = "text/javascript"
    document.getElementsByTagName("head")[0].appendChild(script);
    }
    </script>
        
    """


def generate_error(error = 0):
    print """
     <HTML>
     <HEAD>
     \t<TITLE>Error rocessing HIT</TITLE>
     </HEAD>
     <BODY BGCOLOR = white>
      Thank you for your interest in our HIT! Because this is a research study, we can't show you a full preview of the hit. 
      We think it will take about 5-10 minutes, and you'll answer several multiple choice and fill-in-the-blank style questions,
      and some questions about numbers. 
    <p> 
    """
    
    #     Thank you for your interest in our HIT!  Unfortunately, something has gone wrong processing this request.
    #  Sorry about that; we'll try to get this sorted out as soon as possible.
    #  Please feel free to let us know you got this message, so we can diagnose the error more quickly.
    # print "The error code was " + str(error)
    print "</BODY>\n"
    print "</HTML>\n"

def generate_reparticipation_error():
    print """
     <HTML>
     <HEAD>
     \t<TITLE>Error Processing HIT</TITLE>
     </HEAD>
     <BODY BGCOLOR = white>
     Thank you for your interest in our HIT! Our HIT is part of a study, and we need unique participants in each condition. \
     Our records indicate that you have already participated in some part of this experiment (possibly in a different HIT with a \
     very similar title/description), so we can't use your help on this part.  We appreciate your previous work, \
     and hope you continue to try our HITs in the future!
     <p>
     If you think you got this message in error, please feel free to let us know, so we can figure out what went wrong.
    <p>
    """

    print "</BODY>\n"
    print "</HTML>\n"

 
# multiform scripts
multiform_scripts = """
                <script language="JavaScript">
            var currentLayer = 'page1';
            function showLayer(lyr){
                    hideLayer(currentLayer);
                    document.getElementById(lyr).style.visibility = 'visible';
                    currentLayer = lyr;
                    $('.follow').css('visibility','hidden');
                    
                    $('html,body').scrollTop(0);
                    
            }
            
            function enableElement(element)
            {
                 document.getElementById(element).disabled = false;
            }

            function hideLayer(lyr){
                    document.getElementById(lyr).style.visibility = 'hidden';
            }
            function showValues(form){
                    var values = '';

                    var len = form.length - 1; //Leave off Submit Button
                    for(i=0; i<len; i++){
                            if(form[i].id.indexOf("C")!=-1||form[i].id.indexOf("B")!=-1)//Skip Continue and Back Buttons
                                    continue;
                            values += form[i].id;
                            values += ': ';
                            values += form[i].value;
                            values += '\\n';
                    }
                    alert(values);
            }
            </script>



            <SCRIPT LANGUAGE="JavaScript">
    function enableSubmit (button){
        button.disabled=false
        return
    }
    </SCRIPT>


    """


def print_diff_head(thisTask="thisTask"):
    print """<div id=\""""+thisTask+"""\" class="page">"""
    

def print_diff_continuation(nextTask="nextTask",startDisabled = True):
    if startDisabled:
        print '''<p><input type="button" id="cont'''+nextTask+"""" disabled = true value="Continue" onClick="showLayer('"""+nextTask+"""')"></p>"""
    else:
        print '''<p><input type="button" id="cont'''+nextTask+"""" value="Continue" onClick="showLayer('"""+nextTask+"""')"></p>"""
    print """</div>"""

