<?
	// register_globals�� off�� ���� ���� ���� ������
	@extract($HTTP_GET_VARS); 
	@extract($HTTP_POST_VARS); 
	@extract($HTTP_SERVER_VARS);
	@extract($HTTP_ENV_VARS);

	// ���κ��� ���̺귯�� ������
	$_zb_path = realpath("../../")."/";
	include $_zb_path."lib.php";

	// DB �������� ������
	$connect = dbConn();
	
	$result = mysql_query("select * from `zetyx_board_werewolf_subrule`");
	while($temp = mysql_fetch_array($result)) {
		echo $temp[no]." / ".$temp[name]."<br>";
	}

	mysql_close($connect);
?>