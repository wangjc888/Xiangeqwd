	$(function(){
		
  	    var oFImg =  $("div.food-fl p.f-img");
	    var oFoodBg = $("div.food-bg");
	    var oFoodSign = $("div.food-sign");
	    var oFoodDetails = $("div.fodd-details");
	    var oFoodClose = $("div.food-close");

	    oFImg.each(function(index){

	    	$(this).on('click',function(){
	    		oFoodBg.eq(index).show();
	    		oFoodSign.eq(index).show();
	    		oFoodDetails.eq(index).show();
	    		oFoodClose.eq(index).show();
	    	});

	    	oFoodBg.each(function(i){
	    		$(this).on('click',function(){
	    			oFoodBg.eq(i).hide();
		    		oFoodSign.eq(i).hide();
		    		oFoodDetails.eq(i).hide();
		    		oFoodClose.eq(i).hide();
	    		});
	    	});

	    	oFoodClose.each(function(i){
	    		$(this).on('click',function(){
	    			oFoodBg.eq(i).hide();
		    		oFoodSign.eq(i).hide();
		    		oFoodDetails.eq(i).hide();
		    		oFoodClose.eq(i).hide();
	    		});
	    	});

	    });

	});