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
	
	$query = 
	"update `zetyx_board_werewolf_gameinfo` set state='���ӳ�' where game=2753;";
	
	@mysql_query($query, $connect) or Error("���� ���� ����", "");
	
	mysql_close($connect);
?>