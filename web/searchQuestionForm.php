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
		<title>Cerca un quiz</title>
	</head>
	<body>
	<b><font color="red" size="5"><?=$msg;?></font></b>
	<form action="searchQuestionDo.php" method="post">
		<div align="center">		<table align="left" border="0" cellspacing="0" cellpadding="3">
		Inserisci dei tag su cui basare la ricerca separati da virgole:<input type="text" size="30" maxlength="36" name="tags">:<br />		<tr><td colspan="2" align="right"><input type="submit" name="action" value="searchquestion"></td></tr>		</table>
		</div>
	</form>
	</body>
</html>
