<?php
include_once("include/config.php");
include_once("include/auth.lib.php");

list($status, $user) = auth_get_status();

if($status == AUTH_LOGGED & auth_get_option("TRANSICTION METHOD") == AUTH_USE_LINK){
	$link = "?uid=".$_GET['uid'];
}else	$link = '';
?>
<html>
	<head>
		<title>Home Page</title>
	</head>
	<body>
	<h2>Benvenuto in OpenPursuit</h2>
	<div align="center">
	<p>Se non sai di cosa si parla vai sulla pagina di spiegazione, altrimenti fai login.
	Se non hai un account puoi creartelo andando su registrati.
	Una volta loggato potrai aggiungere nuove domande al database o consultarlo</p>
		<table cellspacing="2">
			<tr>
				<td><a href="home.php<?=$link?>">Home Page</a></td>
				<td><a href="rationale.html<?=$link?>">Spiegazione (pubblica)</a></td>
				<td><a href="addQuestionForm.php<?=$link?>">Aggiungi Domanda (solo registrati)</a></td>
				<td><a href="searchQuestionForm.php<?=$link?>">Cerca Quiz (solo registrati)</a></td>
				<td><a href="playForm.php<?=$link?>">Gioca!</a></td>
				<td><a href="registerUserForm.php">Registrati</a></td>
			</tr>
		</table>
		<?php
		switch($status){
			case AUTH_LOGGED:
			?>
		<b>Sei loggato con il nome di <?=$user["name"];?> <a href="logout.php<?=$link?>">Logout</a></b>
			<?php
			break;
			case AUTH_NOT_LOGGED:
			?>
		<form action="login.php<?=$link?>" method="post">
			<table cellspacing="2">
				<tr>
					<td>Nome Utente:</td>
					<td><input type="text" name="uname"></td>
				</tr>
				<tr>
					<td>Password:</td>
					<td><input type="password" name="passw"></td>
				</tr>
				<tr>
					<td colspan="2"><input type="submit" name="action" value="login"></td>
				</tr>
			</table>
		</form>
		<?php
			break;
		}
		?>
	</div>
	</body>
</html>
