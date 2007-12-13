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

include_once("include/add.lib.php");

list($status, $user) = auth_get_status();

if($status == AUTH_LOGGED){

if(isset($_POST['action']) and $_POST['action'] == 'addquestion'){
	//$ret = question_check_data($_POST);
	$status = question_register($_POST,$user) ;
	//$status = ($ret === true) ? question_register($_POST) : REG_ERRORS;
	
	switch($status){
		case ADD_ERRORS:
			?>
			<span class="style1">Sono stati rilevati i seguenti errori:</span><br>
			<?php
			foreach($ret as $error)
				printf("<b>%s</b>: %s<br>", $error[0], $error[1]);
			?>
			<br>Premere "indietro" per modificare i dati
			<?php
		break;
		case ADD_FAILED:
			echo "Registrazione Fallita a causa di un errore interno.";
		break;
		case ADD_SUCCESS:
			//echo "Registrazione avvenuta con successo.<br>
			//Vi è stata inviata una email contente le istruzioni per confermare la registrazione.";
			echo "Domanda aggiunta con successo.<br>
			Tornate alla <a href=\"home.php\">home</a>";
		break;
	}
}

}else	echo 'Non hai i diritti per visualizzare la pagina';

?>
</body>
</html>
