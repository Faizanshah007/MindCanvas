from Data import *
from math import *

f = open('Summary.html','w')


# Creating content for HTML document

html1 = """
<!DOCTYPE html>
<html>

<head>
<title>Anaglink</title>
</head>

<style>
p  { margin-bottom: 10px }
h1 { margin-bottom: 40px }
</style>

<body bgcolor = "#7FFFD4">

<h1 style = "font-size:35px"><u>Game Summary</u></h1>
<p style = "font-size:20px"><b>The words given to you were :</b></p>

<table>
<col width = "70" >
<col width = "70">
<col width = "70">
<col width = "70">
<col width = "70">
"""

html2 = str()
for i in range(5):
    html2 = html2 + """<tr>"""
    for j in range(5):
        html2 = html2 + """<td height = "30"><a href = "https://en.wiktionary.org/wiki/""" + str(anagselec[(i * 5 + j)]) + """" target="_blank"">""" + str(anagselec[(i * 5 + j)]) + """</a></td>"""
    html2 = html2 + """</tr>"""

html3 = """
</table>

<br>
<p style="font-size:20px"><b>Following anaglinks were present :</b></p>

<p>

"""

html4 = str()
for lnk in ans_copy:
    for anag in lnk:
        html4 = html4 + """ - """ + anag
    html4 = html4 + """ <br><br>\n """

html5 = """
</p>

<p style="font-size:20px">
<b>Your current status : 
"""
html5 = html5 + stat + """. <br></b> \n</p> \n\n """

if( stat == "Won" ):
    html5 = html5 + """
<p style="font-size:15px">
You scored : """ + str(Score) + """,  Which includes a time bonus : """ + str(floor((60 - timer) * 0.5)) + """ \n.</p> """

html5 = html5 + """

</body>

</html>

"""
    
f.write(html1+html2+html3+html4+html5)
f.close()


# Executing HTML file in browser

import webbrowser

def runweb():
    ie = webbrowser.get(webbrowser.iexplore)
    ie.open(os.path.join(os.path.dirname(sys.argv[0]), "Summary.html"))
