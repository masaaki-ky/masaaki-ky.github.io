function showCurrentPage(){

	try{
		var thisURL = window.location.pathname.match("([^\/]+?)([\?#].*)?$")[0];
	} catch(e){
		// If thisURL is Slash stop path, Match "index" is thisChild.
		var thisURL = "";
		var indexMatch = true;
	}

	localnavi = document.getElementById("localNavigation");
	localnavilists = localnavi.getElementsByTagName("li");
	for ( i=0; i<localnavilists.length; i++){
		var linkURL = localnavilists[i].getElementsByTagName("a")[0].getAttribute("href");
		// for IE6 ( get plain href attribute) 
		if ( linkURL.match("\/") == "\/" ){
			var linkURL = localnavilists[i].getElementsByTagName("a")[0].getAttribute("href").match("([^\/]+?)([\?#].*)?$")[0];
		}
		if ( (indexMatch == true ) && (linkURL.match("index.") == "index.") ){
			localnavilists[i].className += " thisChild";
		}
		// Get variable parentMatch ( Match "index" is thisChild ).
		try{
			if ( (parentMatch == true ) && (linkURL.match("index.") == "index.") ){
				localnavilists[i].className += " thisChild";
			}
		} catch(e) { }
		if ( thisURL == linkURL ){ 
			localnavilists[i].className += " thisChild";
		}
	}

}

if(window.addEventListener) {
	window.addEventListener("load", showCurrentPage, false);
}
else if(window.attachEvent) {
	window.attachEvent("onload", showCurrentPage);
}