<?php
include_once("include/config.php");
include_once("include/auth.lib.php");

list($status, $user) = auth_get_status();

if($status == AUTH_NOT_LOGGED){
	$uname = strtolower(trim($_POST['uname']));
	$passw = strtolower(trim($_POST['passw']));

	if($uname == "" or $passw == ""){
		$status = AUTH_INVALID_PARAMS;
	}else{
		list($status, $user) = auth_login($uname, $passw);
		if(!is_null($user)){
			list($status, $uid) = auth_register_session($user);
		}
	}
}

switch($status){
	case AUTH_LOGGED:
		header("Refresh: 5;URL=home.php");
		echo '<div align="center">Sei gia connesso ... attendi il reindirizzamento</div>';
	break;
	case AUTH_INVALID_PARAMS:
		header("Refresh: 5;URL=home.php");
		echo '<div align="center">Hai inserito dati non corretti ... attendi il reindirizzamento</div>';
	break;
	case AUTH_LOGEDD_IN:
		switch(auth_get_option("TRANSICTION METHOD")){
			case AUTH_USE_LINK:
				header("Refresh: 5;URL=home.php?uid=".$uid);
			break;
			case AUTH_USE_COOKIE:
				header("Refresh: 5;URL=home.php");
				setcookie('uid', $uid, time()+3600*365);
			break;
			case AUTH_USE_SESSION:
				header("Refresh: 5;URL=home.php");
				$_SESSION['uid'] = $uid;
			break;
		}
		echo '<div align="center">Ciao '.$user['name'].' ... attendi il reindirizzamento</div>';
	break;
	case AUTH_FAILED:
		header("Refresh: 5;URL=home.php");
		echo '<div align="center">Fallimento durante il tentativo di connessione ... attendi il reindirizzamento</div>';
	break;
}
?>
