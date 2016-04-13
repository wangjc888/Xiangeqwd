	$(function(){

		var myscroll;
        function loaded(){
           setTimeout(function(){
                myscroll=new iScroll("wrapper");
             },100 );
        }
        
        window.addEventListener("load",loaded,false);

	});