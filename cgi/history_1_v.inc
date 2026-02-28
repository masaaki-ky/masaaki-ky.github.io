

# 更新履歴の表示

	if(open(IFILE,"history_1.log")) {
		while($line = <IFILE>) {
			chomp($line);
			($date,$note) = split("\t",$line);
			$Hash_Data{$date} = $note;
		}
		close(IFILE);
	}

	while(($date,$note) = each(%Hash_Data)) {
		$Hash_Note{$date} = $note if($note);
	}

print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
	<TITLE>更新履歴</TITLE>
	<META Http-Equiv="Content-Type" Content="text/html;charset=UTF-8">
</HEAD>
<BODY>
<CENTER>
	<TABLE WIDTH="80%">
		<TR>
			<TD WIDTH="33%">　</TD>
			<TD WIDTH="33%" ALIGN="center" NOWRAP>
				<FONT SIZE="4"><B>更新履歴</B></FONT>　
			</TD>
			<TD ALIGN="right" NOWRAP>
				<A HREF="">
					<FONT SIZE="2" COLOR="green"><B></B></FONT>
				</A>
			</TD>
		</TR>
	</TABLE>
<P>
	<TABLE BORDER=1 WIDTH="80%" CELLPADDING="2" CELLSPACING="0">
		<TR BGCOLOR="#CCF2FF" ALIGN="center">
			<TD><FONT SIZE="2">更新日</FONT></TD>
			<TD><FONT SIZE="2">タイトル</FONT></TD>
		</TR>
!;

	foreach $date (sort {$b cmp $a} keys %Hash_Note) {
		$note = $Hash_Note{$date};
		print qq!
		<TR>
			<TD WIDTH=5% VALIGN="top" NOWRAP>
				<FONT SIZE="2">$date</FONT>
			</TD>
			<TD>
				<FONT SIZE="2">$note</FONT>
			</TD>
		</TR>
		!;
	}

print qq!
	</TABLE>
	<P>
</CENTER>
</BODY>
</HTML>
!;


