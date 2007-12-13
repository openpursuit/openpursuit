<?php


function search_question_and_answers($tagsar){
	//registro l'utente
	global $_CONFIG;
	//	$tagsar = split(',',$data['tags']);
	
	foreach($tagsar as $singletag)	{
				if($singletag != '')		{
			$singletag = rtrim(ltrim(strtolower($singletag)));
			$query = "SELECT * FROM ".$_CONFIG['op_tags']." WHERE `tag` = '".$singletag."'";			$result = mysql_query($query); 
						if(mysql_num_rows($result)  > 0)  {
				$result = mysql_fetch_array($result);
				$query = "SELECT * FROM ".$_CONFIG['op_tags_links']." WHERE `ID_TAG` = '".$result['ID_TAG']."'";
				$result = mysql_query($query); 
				
				if(mysql_num_rows($result)  < 1) 
					return array(SEARCH_FAILED, NULL); 
				$result = mysql_fetch_array($result);
				$query = "SELECT * FROM ".$_CONFIG['op_questions']." WHERE `ID_QUESTION` = '".$result['ID_QUESTION']."' ORDER BY RAND( ) LIMIT 1 ";
				
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



function check_right_answer($id_answer, $response){
	global $_CONFIG;
	$query = "SELECT * FROM " .$_CONFIG['op_answers']. " WHERE `ID_ANSWER` = '" .$id_answer. "'" ;
	//$query = "SELECT * FROM " .$_CONFIG['op_answers']. " WHERE `ID_ANSWER`=32";
	$result = mysql_query($query); 
	if(mysql_num_rows($result)  < 1) 
		return FAILED; 
	$result = mysql_fetch_array($result);
	if ($result['right1'] == $response) 
		return RIGHT;
	else 
		return WRONG;

}

?>
