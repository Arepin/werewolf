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

	mysql_query("update `zetyx_member_table` set level='9' where no='1650'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1651'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1652'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1653'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1654'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1655'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1656'");
	mysql_query("update `zetyx_member_table` set level='9' where no='1657'");
	
	mysql_close($connect);
?>