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

//include_once("include/reg.lib.php");

function search_question($data){
	//registro l'utente
	global $_CONFIG;
		$tagsar = split(',',$data['tags']);
	
	foreach($tagsar as $singletag)	{
				if($singletag != '')		{
			$singletag = rtrim(ltrim(strtolower($singletag)));
			$query = "SELECT * FROM ".$_CONFIG['op_tags']." WHERE `tag` = '".$singletag."' ORDER BY RAND( ) LIMIT 1 ";			$result = mysql_query($query); 
						if(mysql_num_rows($result)  > 0)  {
				$result = mysql_fetch_array($result);
				$query = "SELECT * FROM ".$_CONFIG['op_tags_links']." WHERE `ID_TAG` = '".$result['ID_TAG']."'";
				$result = mysql_query($query); 
				
				if(mysql_num_rows($result)  < 1) 
					return array(SEARCH_FAILED, NULL); 
				$result = mysql_fetch_array($result);
				$query = "SELECT * FROM ".$_CONFIG['op_questions']." WHERE `ID_QUESTION` = '".$result['ID_QUESTION']."'";
				
				$result = mysql_query($query); 
				if(mysql_num_rows($result)  < 1) 
					return array(SEARCH_FAILED, NULL); 
				$result = mysql_fetch_array($result);	
				
				$query = "SELECT * FROM ".$_CONFIG['op_answers']." WHERE `ID_QUESTION` = '".$result['ID_QUESTION']."'";
				$result2 = mysql_query($query); 
				if(mysql_num_rows($result2)  < 1) 
					return array(SEARCH_FAILED, NULL); 
				$result2 = mysql_fetch_array($result2);
				
				return array(SEARCH_SUCCESS, array_merge($result,$result2) );
			} else {
				return NO_RESULTS;
				return array(NO_RESULTS, NULL); 
			//	die (" ".$data['ID_TAG']." row");
			}
			
								}	}
	
	
	if(mysql_insert_id()){
		//return reg_send_confirmation_mail($data['emailAddress'], "test@localhost", $id);
		return ADD_SUCCESS;
	}else return ADD_FAILED;
}


list($status, $user) = auth_get_status();
//$status = AUTH_LOGGED;

if($status == AUTH_LOGGED){

if(isset($_POST['action']) and $_POST['action'] == 'searchquestion'){
	//$ret = question_check_data($_POST);
	list($status, $result) = search_question($_POST) ;
	//$status = ($ret === true) ? question_register($_POST) : REG_ERRORS;
	
	switch($status){
		case NO_RESULTS:
			?>
			<span class="style1">Nessuna domanda disponibile per quel tag</span><br>
			<br>Premere "indietro" per modificare i dati
			<?php
		break;
		case SEARCH_FAILED:
			echo "Richiesta Fallita a causa di un errore interno.";
		break;
		case SEARCH_SUCCESS:
			//echo "Registrazione avvenuta con successo.<br>
			//Vi è stata inviata una email contente le istruzioni per confermare la registrazione.";
			echo  "Domanda: " . $result['question'] . "<br>";
			echo  "Risposta giusta: " . $result['right1'] . "<br>";
			echo  "Risposta sbagliata: " . $result['wrong1'] . "<br>";
			echo  "Risposta sbagliata: " . $result['wrong2'] . "<br>";
			echo  "Risposta sbagliata: " . $result['wrong3'] . "<br>";
			//echo "Domanda aggiunta con successo.<br> Tornate alla <a href=\"home.php\">home</a>";
		break;
	}
}

}else	echo 'Non hai i diritti per visualizzare la pagina';

?>
</body>
</html>
