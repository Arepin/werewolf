<?
	// register_globals�� off�� ���� ���� ���� ������
	@extract($HTTP_SERVER_VARS);
	@extract($HTTP_ENV_VARS);

	// ���κ��� ���̺귯�� ������
	$_zb_path = realpath("../../")."/";
	include $_zb_path."lib.php";

	// DB �������� ������
	$connect = dbConn();
	
	
	// Į�� �߰�
	$gameinfo_add_delayAfter = 
	"ALTER TABLE `zetyx_board_werewolf_gameinfo` CHANGE `delay` `delayAfter` MEDIUMINT(13) UNSIGNED NOT NULL DEFAULT '0';";
	$gameinfo_add_delayBefore = 
	"ALTER TABLE `zetyx_board_werewolf_gameinfo` ADD `delayBefore` MEDIUMINT(13) UNSIGNED NOT NULL DEFAULT '0';";
	$gameinfo_add_delayAfterUsed = 
	"ALTER TABLE `zetyx_board_werewolf_gameinfo` ADD `delayAfterUsed` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0';";
	$gameinfo_add_delayBeforeUsed = 
	"ALTER TABLE `zetyx_board_werewolf_gameinfo` ADD `delayBeforeUsed` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0';";
	
	@mysql_query($gameinfo_add_delayAfter, $connect) or Error("delayAfter Į�� �߰� ����", "");
	@mysql_query($gameinfo_add_delayBefore, $connect) or Error("delayBefore Į�� �߰� ����", "");
	@mysql_query($gameinfo_add_delayAfterUsed, $connect) or Error("delayAfterUsed Į�� �߰� ����", "");
	@mysql_query($gameinfo_add_delayBeforeUsed, $connect) or Error("delayBeforeUsed Į�� �߰� ����", "");
	
	
	mysql_close($connect);
?>