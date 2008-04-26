from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import Quiz
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch ,cm
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus.tables import Table, TableStyle
import random

def colors2(canvas): 
    from reportlab.lib.units import inch 
    
    x = 0; dx = 0.4*inch 
    for i in range(4): 
        for color in (colors.pink, colors.green, colors.brown): 
            canvas.setFillColor(color) 
            canvas.rect(x,0,dx,3*inch,stroke=0,fill=1) 
            x = x+dx 
    canvas.setFillColor(colors.white) 
    canvas.setStrokeColor(colors.white) 
    canvas.setFont("Helvetica-Bold", 85) 
    canvas.drawCentredString(2.75*inch, 1.3*inch, "OPEN") 
    return
    
    
    textobject = canvas.beginText() 
    textobject.setTextOrigin(inch, 2.5*inch) 
    textobject.setFont("Helvetica-Oblique", 14) 
    for line in lyrics: 
        textobject.textLine(line) 
    textobject.setFillGray(0.4) 
    textobject.textLines(''' 
    With many apologies to the Beach Boys 
    and anyone else who finds this objectionable 
    ''') 
    canvas.drawText(textobject) 
    
    black = colors.black 
    y = x = 0; dy=inch*3/4.0; dx=inch*5.5/5; w=h=dy/2; rdx=(dx-w)/2 
    rdy=h/5.0; texty=h+2*rdy 
    canvas.setFont("Helvetica",10) 
    for [namedcolor, name] in ( 
           [colors.lavenderblush, "lavenderblush"], 
           [colors.lawngreen, "lawngreen"], 
           [colors.lemonchiffon, "lemonchiffon"], 
           [colors.lightblue, "lightblue"], 
           [colors.lightcoral, "lightcoral"]): 
        canvas.setFillColor(namedcolor) 
        canvas.rect(x+rdx, y+rdy, w, h, fill=1) 
        canvas.setFillColor(black) 
        canvas.drawCentredString(x+dx/2, y+texty, name) 
        x = x+dx 
    y = y + dy; x = 0 
    for rgb in [(1,0,0), (0,1,0), (0,0,1), (0.5,0.3,0.1), (0.4,0.5,0.3)]: 
        r,g,b = rgb 
        canvas.setFillColorRGB(r,g,b) 
        canvas.rect(x+rdx, y+rdy, w, h, fill=1) 
        canvas.setFillColor(black) 
        canvas.drawCentredString(x+dx/2, y+texty, "r%s g%s b%s"%rgb) 
        x = x+dx 
    y = y + dy; x = 0 
    for cmyk in [(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1), (0,0,0,0)]: 
        c,m,y1,k = cmyk 
        canvas.setFillColorCMYK(c,m,y1,k) 
        canvas.rect(x+rdx, y+rdy, w, h, fill=1) 
        canvas.setFillColor(black) 
        canvas.drawCentredString(x+dx/2, y+texty, "c%s m%s y%s k%s"%cmyk) 
        x = x+dx 
    y = y + dy; x = 0 
    for gray in (0.0, 0.25, 0.50, 0.75, 1.0): 
        canvas.setFillGray(gray) 
        canvas.rect(x+rdx, y+rdy, w, h, fill=1) 
        canvas.setFillColor(black) 




def genpdf(request):
	
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    # Create the PDF object, using the response object as its "file."
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    c.translate(inch,inch)
    #colors(p)
	# Take quiz
    res = Quiz.objects.all()
	#filter(tags__tag__startswith='reti')
    data=  [['00', '01', '02', '03', '04'], 
           ['10', '11', '12', '13', '14'], 
           ['20', '21', '22', '23', '24'], 
           ['30', '31', '32', '33', '34']] 
    t=Table(data,1*cm, 2*cm) 
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'), 
                         ('TEXTCOLOR',(1,1),(-2,-2),colors.blue), 
                         ('VALIGN',(0,0),(0,-1),'TOP'), 
                         ('TEXTCOLOR',(0,0),(0,-1),colors.blue), 
                         ('ALIGN',(0,-1),(-1,-1),'CENTER'), 
                         ('VALIGN',(0,-1),(-1,-1),'MIDDLE'), 
                         ('TEXTCOLOR',(0,-1),(-1,-1),colors.green), 
                         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), 
                         ('BOX', (0,0), (-1,-1), 0.25, colors.black), 
                          ])) 


	
	
	
	
	
	
	
	
	
    quiz = res[0]
    r,g,b = (0,0.3,0.1)
    c.setFillColorRGB(r,g,b) 
    w = 7
    h = 10
    c.rect(2*cm, 2*cm, w*cm, h*cm, fill=1) 
    
   # c.setFillColor(colors.lightblue) 
    c.drawCentredString(1*cm, 1*cm, "q=%s"% quiz.question) 
	
	
	
	
	


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()
    return response

