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
	
	$subrule_data = 
	"INSERT INTO `zetyx_board_werewolf_subrule` (`name`) VALUES 
	('��� ��ǥ');";
	
	@mysql_query($subrule_data, $connect) or Error("subrule ������ ���� ����", "");
	
	mysql_close($connect);
?>