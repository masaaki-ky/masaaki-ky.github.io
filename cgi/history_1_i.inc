

# 更新履歴フォームの表示

	$chk_y[$yy] = " SELECTED";
	$chk_m[$mm] = " SELECTED";
	$chk_d[$dd] = " SELECTED";

print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
	<TITLE>更新履歴登録</TITLE>
	<META Http-Equiv="Content-Type" Content="text/html;charset=UTF-8">
</HEAD>
<BODY>
<FORM ACTION="history_1.cgi" METHOD="post">
<CENTER>
<P>
<TABLE BORDER="0" BGCOLOR="#EEEEEE" CELLPADDING="10">
	<TR>
		<TD ALIGN="right" WIDTH="65%">
			<FONT SIZE="4"><B>更新履歴登録</B></FONT>　　
		</TD>
		<TD ALIGN="right">
			<A HREF="">
				<FONT SIZE="2" COLOR="green"><B></B></FONT>
			</A>
		</TD>
	</TR>
	<TR>
		<TD COLSPAN="2">
			<TABLE BORDER="0" CELLPADDING="3">
				<TR>
					<TD NOWRAP><FONT SIZE="2">日付</FONT></TD>
					<TD>
						<SELECT NAME="yy">
!;

					for($yy = $year;$yy >= $year - 5;$yy--) {
						print '
							<OPTION VALUE="'.$yy.'"'.$chk_y[$yy].'>'.$yy;
					}

print qq!
						</SELECT>年
						<SELECT NAME="mm">
!;

					for($mm = 1;$mm <= 12;$mm++) {
						print '
							<OPTION VALUE="'.$mm.'"'.$chk_m[$mm].'>'.$mm;
					}


print qq!
						</SELECT>月
						<SELECT NAME="dd">
!;

					for($dd = 1;$dd <= 31;$dd++) {
						print '
							<OPTION VALUE="'.$dd.'"'.$chk_d[$dd].'>'.$dd;
					}

print qq!
						</SELECT>日
						<FONT COLOR="#FF0000">$error</FONT>
					</TD>
				</TR>
				<TR>
					<TD NOWRAP><FONT SIZE="2">内容</FONT></TD>
					<TD><TEXTAREA NAME="note" COLS="50" rows="12">$note</TEXTAREA></TD>
				</TR>
				<TR>
					<TD ALIGN="center" COLSPAN="2">
						<INPUT TYPE="submit" NAME="edit" VALUE="登録する">　
					</TD>
				</TR>
			</TABLE>
		</TD>
	</TR>
</TABLE>
<BR>
</CENTER>
</FORM>
</BODY>
</HTML>
!;


