<?php
function reg_register($data){
	//registro l'utente
	global $_CONFIG;
	
//	$id = reg_get_unique_id();
	echo "
	        INSERT INTO ".$_CONFIG['op_members']."
		        (memberName, dateRegistered, emailAddress, realName, location, password, gender, birthdate, websiteUrl, personalText, personalIcon,active)
			        VALUES
				        ('".$data['memberName']."', '".gmdate("Y-m-d H:i:s", time())."','".$data['emailAddress']."','".$data['realName']."','".$data['location']."',MD5('".$data['password']."'),'".$data['gender']."','".$data['birthdate']."','".$data['websiteUrl']."','".$data['perso
					nalText']."','".$data['personalIcon']."','1' )";
	mysql_query("
	INSERT INTO ".$_CONFIG['op_members']."
	(memberName, dateRegistered, emailAddress, realName, location, password, gender, birthdate, websiteUrl, personalText, personalIcon,active)
	VALUES
	('".$data['memberName']."', '".gmdate("Y-m-d H:i:s", time())."','".$data['emailAddress']."',
'".$data['realName']."','".$data['location']."',MD5('".$data['password']."'),'".$data['gender']."','".$data['birthdate']."','".$data['websiteUrl']."','".$data['personalText']."','".$data['personalIcon']."','1' )");
	//Decommentate la riga seguente per testare lo script in locale
	//echo "<a href=\"http://localhost/Articoli/autenticazione/2/scripts/confirm.php?id=".$id."\">Conferma</a>";
	if(mysql_insert_id()){
		//return reg_send_confirmation_mail($data['emailAddress'], "test@localhost", $id);
		return REG_SUCCESS;
	}else return REG_FAILED;
}

function reg_send_confirmation_mail($to, $from, $id){
	//invio la mail di conferma
	$msg = "Per confermare l'avvenuta registrazione, clicckate il link seguente:
	http://localhost/Articoli/autenticazione/1/scripts/confirm.php?id=".$ID_MEMBER."
	";
	return (mail($to, "Conferma la registrazione", $msg, "From: ".$from)) ? REG_SUCCESS : REG_FAILED;
}

function reg_clean_expired(){
	global $_CONFIG;
	
	$query = mysql_query("
	DELETE FROM ".$_CONFIG['os_members']."
	WHERE (regdate + ".($_CONFIG['regexpire'] * 60 * 60).") <= ".time()." and active='0'");
}

function reg_get_unique_id(){
	//restituisce un ID univoco per gestire la registrazione
	list($usec, $sec) = explode(' ', microtime());
	mt_srand((float) $sec + ((float) $usec * 100000));
	return md5(uniqid(mt_rand(), true));
}

function reg_check_data(&$data){
	global $_CONFIG;
	
	$errors = array();
	
	foreach($data as $field_name => $value){
		$func = $_CONFIG['check_table'][$field_name];
		if(!is_null($func)){
			$ret = $func($value);
			if($ret !== true)
				$errors[] = array($field_name, $ret);
		}
	}
	
	return count($errors) > 0 ? $errors : true;
}

function reg_confirm($id){
	global $_CONFIG;
	
	$query = mysql_query("
	UPDATE ".$_CONFIG['os_members']."
	SET active='1'
	WHERE ID_MEMBER='".$id."'");
	
	return (mysql_affected_rows () != 0) ? REG_SUCCESS : REG_FAILED;
}
?>
