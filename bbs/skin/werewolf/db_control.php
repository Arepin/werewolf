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
	
	// Į�� Ȯ��
	$gameinfo_show_subrule = 
	"SHOW COLUMNS FROM `zetyx_board_werewolf_gameinfo`;";
	$gameinfo_show_delay = 
	"SHOW COLUMNS FROM `zetyx_board_werewolf_gameinfo`;";
	
	$result1 = mysql_query($gameinfo_show_subrule, $connect);
	$result2 = mysql_query($gameinfo_show_delay, $connect);
	
	if (!$result1) {
		echo 'Could not run query: ' . mysql_error();
		exit;
	}
	if (mysql_num_rows($result1) > 0) {
		while ($row = mysql_fetch_assoc($result1)) {
			print_r($row);
		}
	}

	if (!$result2) {
		echo 'Could not run query: ' . mysql_error();
		exit;
	}
	if (mysql_num_rows($result2) > 0) {
		while ($row = mysql_fetch_assoc($result2)) {
			print_r($row);
		}
	}
	
	mysql_close($connect);
?>