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
	
	$no = 2753;

	// �������� ������
	$s_data=mysql_fetch_array(mysql_query("select * from $t_board"."_$id where no='$no'"));

   mysql_query("delete from $t_board"."_$id where no='$no'") or Error(mysql_error()); // �ۻ���

   // ���ϻ���
   @z_unlink("./".$s_data[file_name1]);
   @z_unlink("./".$s_data[file_name2]);

   minus_division($s_data[division]);

   if($s_data[depth]==0)
   {
    if($s_data[prev_no]) mysql_query("update $t_board"."_$id set next_no='$s_data[next_no]' where next_no='$s_data[no]'"); // �������� ������ ���ڸ� �޲�;;;
    if($s_data[next_no]) mysql_query("update $t_board"."_$id set prev_no='$s_data[prev_no]' where prev_no='$s_data[no]'"); // �������� ������ ���ڸ� �޲�;;;
   }
   else
   { 
    $temp=mysql_fetch_array(mysql_query("select count(*) from $t_board"."_$id where father='$s_data[father]'"));
    if(!$temp[0]) mysql_query("update $t_board"."_$id set child='0' where no='$s_data[father]'"); // �������� ������ �������� �ڽı��� ����;;;
   }

   // ������ ��� ����
   mysql_query("delete from $t_comment"."_$id where parent='$s_data[no]'");

	// ���� ��� ���� - ����
	$DB_gameinfo=$t_board."_".$id."_gameinfo";
	$DB_entry=$t_board."_".$id."_entry";
	$DB_comment_type=$t_comment."_$id"."_commentType";
	$DB_record = $t_board."_".$id."_record";

   mysql_query("delete from $DB_gameinfo where game='$s_data[no]'");
   mysql_query("delete from $DB_entry where game='$s_data[no]'");
   mysql_query("delete from $DB_comment_type where game='$s_data[no]'");
	// ���� ��� ���� - ��


   $total=mysql_fetch_array(mysql_query("select count(*) from $t_board"."_$id "));
   mysql_query("update $admin_table set total_article='$total[0]' where name='$id'");

   // ī�װ� �ʵ� ����
   mysql_query("update $t_category"."_$id set num=num-1 where no='$s_data[category]'",$connect);

   // ȸ���� ��� �ش� �ؿ��� ���� �ֱ�
   if($member[no]==$s_data[ismember]) @mysql_query("update $member_table set point1=point1-1 where no='$member[no]'",$connect) or error(mysql_error());
	
	
	mysql_close($connect);
?>