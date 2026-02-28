#!/usr/local/bin/perl


###############################################
#   sche38.cgi
#      V1.5 (2020.12.30)
#                     Copyright(C) CGI-design
###############################################

$script = 'sche38.cgi';
$base = './schedata';				#データ格納ディレクトリ
$opfile = "$base/option.txt";

@week = ('日','月','火','水','木','金','土');
@mdays = (31,28,31,30,31,30,31,31,30,31,30,31);

open (IN,"$opfile") || &error("OPEN ERROR");	$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	open(OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "$pass<>#fafaf5,#000000,#ffffff,#c9e0de,#f0f8ff,#ffd700,#ff0000,#0000ff,#000000";
	close OUT;
}

### メイン処理 ###
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN,$in,$ENV{'CONTENT_LENGTH'});} else {$in = $ENV{'QUERY_STRING'};}
%in = ();
foreach (split(/&/,$in)) {
	($n,$val) = split(/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$val =~ s/&/&amp;/g;	$val =~ s/</&lt;/g;		$val =~ s/>/&gt;/g;		$val =~ s/"/&quot;/g;	$val =~ s/\r\n|\r|\n/<br>/g;
	if (defined($in{$n})) {$in{$n} .= "\0$val";} else {$in{$n} = $val;}
}
$mode = $in{'mode'};
$logyear = $in{'year'};
$logmon = $in{'mon'};

open (IN,"$opfile") || &error("OPEN ERROR");
($pass,$colors) = split(/<>/,<IN>);
close IN;
($bg_color,$text_color,$cbg_color,$frame_color,$subbg_color,$dsp_color,$sun_color,$sat_color,$day_color) = split(/,/,$colors);
@wcolor = ($sun_color,$day_color,$day_color,$day_color,$day_color,$day_color,$sat_color);

($sec,$min,$hour,$nowday,$nowmon,$nowyear) = localtime;
$nowyear += 1900;
$nowmon++;

if (!$logyear) {$logyear = $nowyear; $logmon = $nowmon;}
$logfile = "$base/$logyear$logmon.txt";

$mdays = $mdays[$logmon - 1];
if ($logmon == 2 && $logyear % 4 == 0) {$mdays = 29;}

if ($mode eq 'admin') {&admin;} else {&main;}

print "</center></body></html>\n";
exit;

###
sub header {
	print "Content-type: text/html\n\n";
	print "<html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>Calendar</title><link rel=\"stylesheet\" type=\"text/css\" href=\"$base/style.css\"></head>\n";
	$head = 1;
}

###
sub main {
	&header;
	print "<body bgcolor=\"$bg_color\" text=\"$text_color\" leftmargin=0 topmargin=0 marginwidth=0 marginheight=0><center>\n";
	print "<table width=100%><tr><td width=34>$logyear</td><td align=center>";
	$mon = $logmon - 1;
	if ($mon < 1) {$mon = 12; $year = $logyear - 1;} else {$year = $logyear;}
	print "<a href=\"$script?year=$year&mon=$mon\">&lt;&lt;</a> <b>$logmon月</b> ";
	$mon = $logmon + 1;
	if (12 < $mon) {$mon = 1; $year = $logyear + 1;} else {$year = $logyear;}
	print "<a href=\"$script?year=$year&mon=$mon\">&gt;&gt;</a></td><td width=16></td></tr></table>\n";
	&dsp_cal;
	# 次の行は著作権表示ですので削除しないで下さい。#
	print "<br><br>CGI-design\n";
}

###
sub dsp_cal {
	@dsp = ();
	if (-e $logfile) {
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($day,$dsp) = split(/<>/);
			$dsp[$day] = $dsp;
		}
		close IN;
	}
	print "<table width=100% bgcolor=\"$frame_color\" cellspacing=1 cellpadding=1><tr bgcolor=\"$subbg_color\" align=center>\n";
	for (0 .. 6) {print "<td width=14%><font color=\"$wcolor[$_]\">$week[$_]</font></td>\n";}
	print "</tr>\n";
	&set_holiday;
	&get_wday($logyear,$logmon,1);
	$w = $n = 0;
	$k = 1;
	for (0 .. 41) {
		if (!$w) {print "<tr bgcolor=\"$cbg_color\" align=center>";}
		if ($wday <= $_ && $k <= $mdays) {
			if ($w == 1) {$n++;}
			$wcolor = $wcolor[$w];
			if (2019 <= $logyear) {
				&get_holiday;
				if ($holiday) {$wcolor = $wcolor[0];}
			}
			if ($dsp[$k]) {$bc = " bgcolor=\"$dsp_color\"";	$chk = ' checked';} else {$bc = $chk = '';}
			if ($logyear eq $nowyear && $logmon eq $nowmon && $k eq $nowday) {$day = "<b>$k</b>";} else {$day = $k;}

			print "<td height=20$bc><font color=\"$wcolor\">$day</font>";
			if ($mode eq 'admin') {print "<br><input type=checkbox name=dsp$k value=\"1\"$chk>";}
			print "</td>\n";
			$k++;
		} else {
			print "<td></td>";
		}
		$w++;
		if ($w == 7) {
			print "</tr>\n";
			if ($mdays < $k) {last;}
			$w = 0;
		}
	}
	print "</table>\n";
}

###
sub set_holiday {
	$def = 0.242194*($logyear-1980)-int(($logyear-1980)/4);
	$spr = int(20.8431+$def);
	$aut = int(23.2488+$def);
	if ($logyear eq '2019') {
		%hod = ('0101','元日','0211','建国記念の日',"03$spr",'春分の日','0429','昭和の日','0430','国民の休日','0501','即位の日','0502','国民の休日','0503','憲法記念日','0504','みどりの日','0505','こどもの日','0811','山の日',"09$aut",'秋分の日','1022','即位礼正殿の儀','1103','文化の日','1123','勤労感謝の日');
		%how = ('12','成人の日','73','海の日','93','敬老の日','102','体育の日');
	} elsif ($logyear eq '2020') {
		%hod = ('0101','元日','0211','建国記念の日','0223','天皇誕生日',"03$spr",'春分の日','0429','昭和の日','0503','憲法記念日','0504','みどりの日','0505','こどもの日','0723','海の日','0724','スポーツの日','0810','山の日',"09$aut",'秋分の日','1103','文化の日','1123','勤労感謝の日');
		%how = ('12','成人の日','93','敬老の日');
	} elsif ($logyear eq '2021') {
		%hod = ('0101','元日','0211','建国記念の日','0223','天皇誕生日',"03$spr",'春分の日','0429','昭和の日','0503','憲法記念日','0504','みどりの日','0505','こどもの日','0722','海の日','0723','スポーツの日','0808','山の日',"09$aut",'秋分の日','1103','文化の日','1123','勤労感謝の日');
		%how = ('12','成人の日','93','敬老の日');
	} else {
		%hod = ('0101','元日','0211','建国記念の日','0223','天皇誕生日',"03$spr",'春分の日','0429','昭和の日','0503','憲法記念日','0504','みどりの日','0505','こどもの日','0811','山の日',"09$aut",'秋分の日','1103','文化の日','1123','勤労感謝の日');
		%how = ('12','成人の日','73','海の日','93','敬老の日','102','スポーツの日');
	}
}

###
sub get_holiday {
	$sm = sprintf("%02d%02d",$logmon,$k);
	$holiday = $hod{$sm};
	if ($holiday && !$w) {$hflag = 1;}
	if (!$holiday && $w == 1) {$holiday = $how{"$logmon$n"};}
	if (!$holiday && $hflag) {$holiday = '振替休日'; $hflag = 0;}
	if (($logyear eq '2026' && $sm eq '0922') || ($logyear eq '2032' && $sm eq '0921')) {$holiday = '国民の休日';}
}

###
sub get_wday {
	($y,$m,$d) = @_;
	if ($m < 3) {$y--; $m+=12;}
	$wday = ($y+int($y/4)-int($y/100)+int($y/400)+int((13*$m+8)/5)+$d)%7;
}

###
sub admin {
	&header;
	print "<body><center>\n";
	$inpass = $in{'pass'};
	if ($inpass eq '') {
		print "<br><br><br><br><h4>パスワードを入力して下さい</h4>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=password size=10 maxlength=8 name=pass>\n";
		print "<input type=submit value=\" 認証 \"></form>\n";
		print "</center></body></html>\n";
		exit;
	}
	$mat = &decrypt($inpass,$pass);
	if (!$mat) {&error("パスワードが違います");}

	print "<table width=100% bgcolor=\"#8c4600\"><tr><td>　<a href=\"$script?mode=admin\"><font color=\"#ffffff\"><b>ログアウト</b></font></a></td>\n";
	print "<form action=\"$script\" method=POST><td align=right>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=submit value=\"カレンダー設定\">\n";
	print "<input type=submit name=set value=\"基本設定\"></td></form><td width=10></td></tr></table><br>\n";

	if ($in{'set'}) {&setup;} else {&edtin;}
}

###
sub edtin {
	if ($in{'wrt'}) {
		open (OUT,">$logfile") || &error("OPEN ERROR");
		for (1 .. $mdays) {print OUT "$_<>$in{\"dsp$_\"}<>\n";}
		close OUT;
		chmod(0666,$logfile);
	}
	print "特定日にチェックを入れ、「設定する」を押して下さい。<br><br>\n";
	$mon = $logmon - 1;
	if ($mon < 1) {$mon = 12; $year = $logyear - 1;} else {$year = $logyear;}
	print "<table width=280><tr><form action=\"$script\" method=POST><td>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=submit value=\"前月\"></td></form>\n";
	print "<td align=center><font size=\"+1\"><b>$logyear年$logmon月</b></font></td>\n";
	$mon = $logmon + 1;
	if (12 < $mon) {$mon = 1; $year = $logyear + 1;} else {$year = $logyear;}
	print "<form action=\"$script\" method=POST><td align=right>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=submit value=\"次月\"></td></form></tr>\n";

	print "<tr><form action=\"$script\" method=POST><td colspan=3>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$logyear\">\n";
	print "<input type=hidden name=mon value=\"$logmon\">\n";
	&dsp_cal;
	print "</td></tr></table><br><input type=submit name=wrt value=\"設定する\">\n";
	print "</form>\n";
}

###
sub setup {
	if ($in{'wrt'}) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$colors = $in{'colors'};	$colors =~ s/\0/,/g;
		open (OUT,">$opfile") || &error("OPEN ERROR");		print OUT "$pass<>$colors";		close OUT;
	}
	print "下記に入力後、「設定する」を押して下さい。<br><br>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=set value=\"1\">\n";
	print "<input type=submit name=wrt value=\"設定する\"><br><br>\n";

	print "<table bgcolor=\"#dddddd\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td></td><td><a href=\"$base/color.htm\" target=\"_blank\">カラーコード</a></td></tr>\n";
	@name = ('基本背景色','基本文字色','カレンダー背景色','枠色','曜日背景色','特定日背景色','日曜日','土曜日','平日');
	@colors = split(/,/,$colors);
	for (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text name=colors size=10 value=\"$colors[$_]\" style=\"ime-mode:inactive;\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$colors[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>パスワード変更</b></td><td><input type=password size=10 maxlength=8 name=newpass> （英数8文字以内）</td></tr>\n";
	print "</table></td></tr></table></form>\n";
}

###
sub crypt {
	@salt = ('a' .. 'z','A' .. 'Z','0' .. '9');
	srand;
	$salt = "$salt[int(rand($#salt))]$salt[int(rand($#salt))]";
	return crypt($_[0],$salt);
}

###
sub decrypt {
	$salt = $_[1] =~ /^\$1\$(.*)\$/ && $1 || substr($_[1],0,2);
	if (crypt($_[0],$salt) eq $_[1] || crypt($_[0],'$1$' . $salt) eq $_[1]) {return 1;}
	return 0;
}

###
sub error {
	if (!$head) {&header; print "<body><center>\n";}
	print "<br><br><br><br><h3>ERROR !!</h3><font color=red><b>$_[0]</b></font>\n";
	print "</center></body></html>\n";
	exit;
}
