$(function() {

	_tab($("#menu li.menu-li"),$("#food li.index-food"));
   	_tab($("#jump li.jump-li"),$("#paging li.box-index"));
   	_tab($("#order-box p.order-p"),$("#order-cont li.cont-li"));
   	_tab($("#see-li li.eveat"),$("#dom-li li.see-cont"));

    function _tab(obj,name){
    	obj.on('click',function(){
            obj.eq($(this).index()).addClass("on").siblings().removeClass('on');
            name.hide().eq($(this).index()).show();
        });
    }
 });