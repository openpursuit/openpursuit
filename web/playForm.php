<?php
include_once("include/config.php");
include_once("include/auth.lib.php");
include_once("include/play.lib.php");

list($status, $user) = auth_get_status();

if($status == AUTH_LOGGED){
	$msg = 'Contenuto della pagina';
	
}else	$msg = 'Non hai i diritti per visualizzare la pagina';
?>
<html>
	<head>
		<title>Gioca</title>
	<style type="text/css">
	<!--
	.tag5 { font-size: 7pt; }	.tag4 { font-size: 8pt; }	.tag3 { font-size: 9pt; }	.tag2 { font-size: 11pt; }	.tag1 { font-size: 14pt; }
	}
	-->
	</style>
	<SCRIPT>function scrivi(str){ 	document.frm.tags.value=str;}</SCRIPT>
	</head>
	<body>
	<b><font color="red" size="5"><?=$msg;?></font></b><br><br>
	<?php 
	if(isset($_POST['action']) and $_POST['action'] == 'searchtag') {
		list($status, $result) = search_question_and_answers(split(',',$_POST['tags']));
		if ($status != SEARCH_SUCCESS) die("");
		echo  "Domanda: " . $result['question'] . "<br>";
		
		echo "<form name='play' action='playDo.php' method='POST'";		echo "<div align=\"center\"><br>";			
		$array_dati=array('right1','wrong1','wrong2','wrong3');
		shuffle($array_dati);		for($a=0;$a<count($array_dati);$a++){			echo "<input type=\"radio\" name=\"response\" value=\"" .$result[$array_dati[$a]]. "\"> ".$result[$array_dati[$a]]."<br>";		}		
		echo "<input type=\"hidden\" name=\"id_answer\" value=\"".$result['ID_ANSWER']."\">";
		
		echo "<input type=\"submit\" name=\"action\" value=\"play\">";		echo "</div>";		echo "</form>";
			
		} else {
			?>
			<form action="playForm.php" name="frm" method="post">
				<div align="center">				<table align="left" border="0" cellspacing="0" cellpadding="3">
				Inserisci dei tag su cui basare la ricerca separati da virgole:<input type="text" size="30" maxlength="36" name="tags" id="tags">:<br />				<tr><td colspan="2" align="right"><input type="submit" name="action" value="searchtag"></td></tr>				</table>
				</div>
			</form>
			<br>
			<h2>Tags Cloud</h2>
			<?php
			  $query = "SELECT Min(count) as val_min, Max(count) as val_max FROM op_tags";		      $rs = mysql_query($query,$conn) or die("Errore nella query:" . mysql_error());		      while ($riga=mysql_fetch_array($rs)) {		           $vmin = $riga['val_min'];		           $vmax = $riga['val_max'];		      }

			$query = "SELECT tag, count FROM op_tags";      		$rs = mysql_query($query,$conn) or die("Errore nella query:" . mysql_error());      		while ($riga=mysql_fetch_array($rs)) {                $dim = ceil(5*($vmax-$riga['count'])/($vmax-$vmin));
                                print "<a href=\"JavaScript:scrivi('".$riga['tag']."');\" ><span class='tag".($dim)."'>".$riga['tag']."</span> .</a>";      		}
			
			

			
			}
		?> 
		
	</body>
</html>
