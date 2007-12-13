<?php
$_CONFIG['host'] = "localhost";
$_CONFIG['user'] = "pursuitplayer";
$_CONFIG['pass'] = "bzzauz";
$_CONFIG['dbname'] = "openpursuit";

$_CONFIG['op_sessions'] = "op_sessions";
$_CONFIG['op_members'] = "op_members";
$_CONFIG['op_questions'] = "op_questions";
$_CONFIG['op_answers'] = "op_answers";
$_CONFIG['op_tags'] = "op_tags";
$_CONFIG['op_tags_links'] = "op_tags_links";


$_CONFIG['expire'] = 6000;

$_CONFIG['regexpire'] = 24; //in ore

$_CONFIG['check_table'] = array(
	"username" => "check_username",
	"password" => "check_global",
	"name" => "check_global",
	"surname" => "check_global",
	"indirizzo" => "check_global",
	"occupazione" => "check_global",
	"mail" => "check_global"
);

function check_username($value){
	global $_CONFIG;
	
	$value = trim($value);
	if($value == "")
		return "Il campo non può essere lasciato vuoto";
	$query = mysql_query("
	SELECT id
	FROM ".$_CONFIG['table_utenti']."
	WHERE username='".$value."'");
	if(mysql_num_rows($query) != 0)
		return "Nome utente già utilizzato";
	
	return true;
}

function check_global($value){
	global $_CONFIG;
	
	$value = trim($value);
	if($value == "")
		return "Il campo non può essere lasciato vuoto";
	
	return true;
}

//--------------
define('AUTH_LOGGED', 99);
define('AUTH_NOT_LOGGED', 100);

define('AUTH_USE_COOKIE', 101);
define('AUTH_USE_LINK', 103);
define('AUTH_INVALID_PARAMS', 104);
define('AUTH_LOGEDD_IN', 105);
define('AUTH_FAILED', 106);

$conn = mysql_connect($_CONFIG['host'], $_CONFIG['user'], $_CONFIG['pass']) or die('Impossibile stabilire una connessione');
mysql_select_db($_CONFIG['dbname']);
?>
