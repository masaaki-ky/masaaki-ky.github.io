#!/usr/local/bin/perl

# Copyright (C) 2001-2003 All right reserved by Shinya Kondo ( CGI KON )

	require "cgi-lib.pl";

	&ReadParse;

	$yy = $in{'yy'};
	$mm = $in{'mm'};
	$dd = $in{'dd'};
	$note = $in{'note'};

	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;

# メインプログラム

	if($in{'edit'}) {
		if(open(OFILE,">>history_1.log")) {
			$date = sprintf("%02d/%02d/%04d",$mm,$dd,$yy);
			$note =~ s/\x0D\x0A|\x0D|\x0A/<BR>/g;
			print OFILE $date."\t".$note."\n";
			close(OFILE);
			require "history_1_v.inc";
			exit;
		} else {
			$error = "登録できませんでした。";
			require "history_1_i.inc";
			exit;
		}
	}

	if($in{'insert'}) {
		$yy = $year;
		$mm = $mon + 1;
		$dd = $mday;
		require "history_1_i.inc";
		exit;
	}

	require "history_1_v.inc";
	exit;


