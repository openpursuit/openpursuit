<?php
include_once("include/config.php");
include_once("include/auth.lib.php");

list($status, $user) = auth_get_status();

if($status == AUTH_LOGGED){
	$msg = 'Contenuto della pagina';
}else	$msg = 'Non hai i diritti per visualizzare la pagina';
?>
<html>
	<head>
		<title>Aggiungi nuova domanda</title>
	</head>
	<body>
	<b><font color="red" size="5"><?=$msg;?></font></b>

<form action="addQuestionDo.php" method="post">
<div align="center"><table align="left" border="0" cellspacing="0" cellpadding="3">
Question:<input type="text" size="30" maxlength="36" name="question">:<br />Right Answer:<input type="text" size="30" maxlength="36" name="right1">:<br />
Wrong Answer1:<input type="text" size="30" maxlength="36" name="wrong1">:<br />
Wrong Answer2:<input type="text" size="30" maxlength="36" name="wrong2">:<br />
Wrong Answer3:<input type="text" size="30" maxlength="36" name="wrong3">:<br />
Difficulty:<input type="text" size="12" maxlength="36" name="difficulty">:<br />
Tags (separati da virgole)<input type="text" size="12" maxlength="36" name="tags">:<br />
<tr><td colspan="2" align="right"><input type="submit" name="action" value="addquestion"></td></tr></table>
</div>
</form>

	
	</body>
</html>

