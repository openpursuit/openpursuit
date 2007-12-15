# Create your views here.
from django.http import HttpResponse


#FIXME
#questa index va totalmente cambiata

def index(request):

	output = "  \
<html> \
<head>\
 <title>Aggiungi nuova domanda</title>\
</head>\
<body>\
<b><font color=\"red\" size=\"5\"><?=$msg;?></font></b>\
<form action=\"addQuestionDo.php\" method=\"post\">\
<div align=\"center\"><table align=\"left\" border=\"0\" cellspacing=\"0\" cellpadding=\"3\"> \
Question:<input type=\"text\" size=\"30\" maxlength=\"36\" name=\"question\">:<br />Right Answer:<input type=\"text\" size=\"30\" maxlength=\"36\" name=\"right1\">:<br />\
	Wrong Answer1:<input type=\"text\" size=\"30\" maxlength=\"36\" name=\"wrong1\">:<br />\
	Wrong Answer2:<input type=\"text\" size=\"30\" maxlength=\"36\" name=\"wrong2\">:<br />\
	Wrong Answer3:<input type=\"text\" size=\"30\" maxlength=\"36\" name=\"wrong3\">:<br />\
	Difficulty:<input type=\"text\" size=\"12\" maxlength=\"36\" name=\"difficulty\">:<br />\
	Tags (separati da virgole)<input type=\"text\" size=\"12\" maxlength=\"36\" name=\"tags\">:<br />\
<tr><td colspan=\"2\" align=\"right\"><input type=\"submit\" name=\"action\" value=\"addquestion\"></td></tr></table>\
</div>\
</form>\
</body>\
</html>\
	";
return HttpResponse(output)


#FIXME
#questo Ã¨ solo uno scheletro per aggiungere una domanda passata tramite POST

def addQuestion(request):

from djangoOp.OpenPursuit_Base.models import Tags
from djangoOp.OpenPursuit_Base.models import Question 
from djangoOp.OpenPursuit_Base.models import Answers

#TODO
#Check se il tag specificato non esiste gia

#Se il tag non esiste lo aggiungo

#FIXME: "musica" va cambiato con il TAG passato via POST
t = Tags.objects.create(tag="musica")
t.save()

q = Question(question = 'x', difficulty = ' ', score = ' ', date = ' ');
q.tag.add(t)
q.save()

p = Answers(question = q, right1='sdfds' , wrong1='sdfsdf', wrong2='cdsfs', wrong3='xx')
p.save()


