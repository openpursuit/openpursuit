<?php
include_once("include/config.php");
include_once("include/auth.lib.php");

list($status, $user) = auth_get_status();
header("Refresh: 5;URL=home.php");

if($status == AUTH_LOGGED){
	if(auth_logout()){
		echo '<div align="center">Disconnessione effettuata ... attendi il reindirizzamento</div>';
	}else{
		echo '<div align="center">Errore durante la disconnessione ... attendi il reindirizzamento</div>';
	}
}else{
	echo '<div align="center">Non sei connesso ... attendi il reindirizzamento</div>';
}
?>
