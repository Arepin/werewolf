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
	
	// ���̺� �߰�
	$subrule_schema = 
	"CREATE TABLE `zetyx_board_werewolf_subrule` (
	`no` int(20) unsigned NOT NULL auto_increment,
	`name` varchar(20) default NULL,
	PRIMARY KEY  (`no`)
	) ENGINE=MyISAM  DEFAULT CHARSET=euckr AUTO_INCREMENT=5 ;";
	
	@mysql_query($subrule_schema, $connect) or Error("subrule ���̺� ���� ����", "");
	
	// ������ ����
	$subrule_data = 
	"INSERT INTO `zetyx_board_werewolf_subrule` (`no`, `name`) VALUES 
	(1, '�ζ� ���� ����'),
	(2, 'NPC ���� ���� �ο�'),
	(3, '�ڷ��Ľ� ��� �Ұ�');";
	
	@mysql_query($subrule_data, $connect) or Error("subrule ������ ���� ����", "");
	
	// ������ Ȯ��
	$subrule_load = 
	"select * from `zetyx_board_werewolf_subrule`";
	
	$result = mysql_query($subrule_load, $connect);
	while($temp = mysql_fetch_array($result)) {
		echo $temp[no]." :: ".$temp[name]."<br>";
	}
	
	mysql_close($connect);
?>