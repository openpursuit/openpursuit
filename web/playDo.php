<html>
<head>
<style type="text/css">
<!--
.style1 {
	color: #FF0000;
	font-weight: bold;
}
-->
</style>
</head>
<body>
<?php
include_once("include/config.php");

include_once("include/auth.lib.php");

include_once("include/play.lib.php");



list($status, $user) = auth_get_status();
//$status = AUTH_LOGGED;

if($status == AUTH_LOGGED){

if(isset($_POST['action']) and $_POST['action'] == 'play'){
	//$ret = question_check_data($_POST);
	$status = check_right_answer($_POST['id_answer'], $_POST['response']) ;
	//$status = ($ret === true) ? question_register($_POST) : REG_ERRORS;
	
	switch($status){
		case FAILED:
			echo "Richiesta Fallita a causa di un errore interno.";
		break;
		case WRONG:
			//echo "Registrazione avvenuta con successo.<br>
			//Vi è stata inviata una email contente le istruzioni per confermare la registrazione.";
			echo  "Hai sbagliato! Consulta wikipedia!";
		break;
		case RIGHT:
			//echo "Registrazione avvenuta con successo.<br>
			//Vi è stata inviata una email contente le istruzioni per confermare la registrazione.";
			echo  "Bravo! avevi ragine!";
		break;
	}
}

}else	echo 'Non hai i diritti per visualizzare la pagina';

?>
</body>
</html>
