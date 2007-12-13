<?php
function question_register($data,$user){
	//registro l'utente
	global $_CONFIG;
	
//	$id = reg_get_unique_id();
	
//
	mysql_query("
	INSERT INTO ".$_CONFIG['op_questions']."
	(question, creationDate, ID_MEMBER, difficulty)
	VALUES
	('".$data['question']."', '".gmdate("Y-m-d H:i:s", time())."','".$user['id_member']."','".$data['difficulty']."' )");
	
	$id = mysql_insert_id();
	if ($id == 0)
		return ADD_FAILED;
	
	mysql_query("
	INSERT INTO ".$_CONFIG['op_answers']."
	(ID_QUESTION, right1 , wrong1, wrong2, wrong3)
	VALUES
	('".$id."','".$data['right1']."' ,'".$data['wrong1']."','".$data['wrong2']."','".$data['wrong3']."' )");


	if (mysql_insert_id() == 0)
		return ADD_FAILED;
	
	
		$tagsar = split(',',$data['tags']);
	
	foreach($tagsar as $singletag)	{
				if($singletag != '')		{
			$singletag = rtrim(ltrim(strtolower($singletag)));
			$query = "SELECT * FROM ".$_CONFIG['op_tags']." WHERE `tag` = '".$singletag."' ";			$result = mysql_query($query); 
			$tagid = '0';
						if(mysql_num_rows($result)  < 1)  {
				// die (" ".$data['singletag']." row");
				mysql_query("
				INSERT INTO ".$_CONFIG['op_tags']."
				(tag)
				VALUES
				('".$singletag."')
				");
				$tagid =  mysql_insert_id();
				if ($tagid == 0)
					//return ADD_FAILED;
					die ("died for tag");
			} else {
				$query = "UPDATE ".$_CONFIG['op_tags']." SET `count` = `count`+1 WHERE `tag` = '".$singletag."' "; 
				$result3 = mysql_query($query);
				
				$oldtag = mysql_fetch_array($result);
				$tagid = $oldtag['ID_TAG'];
			//	die (" ".$data['ID_TAG']." row");
			}
			
			mysql_query("
			INSERT INTO ".$_CONFIG['op_tags_links']."
			(ID_TAG, ID_QUESTION)
			VALUES
			('".$tagid."', '".$id."') ");
			mysql_insert_id();
			if (mysql_insert_id() == 0)
				//return ADD_FAILED;
				die("died for tag links");
					}	}
	
	
	if(mysql_insert_id()){
		//return reg_send_confirmation_mail($data['emailAddress'], "test@localhost", $id);
		return ADD_SUCCESS;
	}else return ADD_FAILED;
}

?>
