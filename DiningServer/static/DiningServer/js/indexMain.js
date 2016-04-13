$(function() {

        //数据存储
    var json = {};
    
    // var savedMeals = window.sessionStorage['JJCS'];
    // if(savedMeals != undefined || savedMeals != null){
    //     savedMeals = JSON.parse(savedMeals);
    //     for(var meal in savedMeals){
    //         var oParentId = meal.parentId;
    //         var ddname = meal.name;
    //         var tval = meal.tval;

    //         var oLi = $('#shop-ul').find('.js-'+oParentId);

    //         if (oLi.length==0) {
    //             oLi = "<li class=js-"+oParentId+"><span><i class='ul-i'></i><i class='ul-meal'>"+ddname+"</i></span><div class='shop-div'><input type='button' class='minus-a' value='-'><input type='text' class='result-a' value="+"'"+tval+"'"+" disabled='true'><input type='button' class='add-a' value='+'></div></li>";

    //             $('#shop-ul').append(oLi);
    //         }else{
    //             oLi.find(".result-a").val(tval);

    //         }
    //         var a =$('.shop-ul li').length;

    //         // 超出5个多出滚动条
    //         if ( a >= 6 ) {
    //             $('.shop-ul').css('height','2.75rem');
    //             $('.shop-ul').css('overflow-y','scroll');
    //         }
    //     }
    // }




    // 获取session 这是商品详情的取。暂时不用
    // var section = window.sessionStorage['JJCS'];
    // section = section?JSON.parse(section):{};
    // // 赋值
    // for(var name in section){
    //     $('#'+name).find('.result').val(section[name]);
    //     console.log(section[name],name);
    // }


    $(".add").click(function () {
        var t = $(this).parent().find('input[class*=result]');
        var oParentId = $(this).parents(".prt-lt").attr("id");
        t.val(parseInt(t.val()) + 1);
        setTotal();
        
        var ddname = $(this).parent().find('.di-name').text();
        var tval = t.val();

        var oLi = $('#shop-ul').find('.js-'+oParentId);

        if (oLi.length==0) {
            oLi = "<li class=js-"+oParentId+"><span><i class='ul-i'></i><i class='ul-meal'>"+ddname+"</i></span><div class='shop-div'><input type='button' class='minus-a' value='-'><input type='text' class='result-a' value="+"'"+tval+"'"+" disabled='true'><input type='button' class='add-a' value='+'></div></li>";

            $('#shop-ul').append(oLi);
        }else{
            oLi.find(".result-a").val(tval);

        }

        var a =$('.shop-ul li').length;


        // 超出5个多出滚动条
        if ( a >= 6 ) {
            $('.shop-ul').css('height','2.75rem');
            $('.shop-ul').css('overflow-y','scroll');
        }

        // 存
        var data = getSession('JJCS') || {};
        data[oParentId] = tval;
        saveSession('JJCS',data);
    });
    // 显示
    var data = getSession('JJCS');
    if (data) {
        for (var name in data) {
            $('#'+name).find('.result').val(data[name]);
            var ddname = $('#'+name).find('.di-name').text();
            var oLi = "<li class=js-"+name+"><span><i class='ul-i'></i><i class='ul-meal'>"+ddname+"</i></span><div class='shop-div'><input type='button' class='minus-a' value='-'><input type='text' class='result-a' value="+"'"+data[name]+"'"+" disabled='true'><input type='button' class='add-a' value='+'></div></li>";

            $('#shop-ul').append(oLi);
        };
    };



    $('#shop-ul').on('click','.add-a',function (){
        var oRt1 = $(this).parent().find('.result-a');
        oRt1.val(parseInt(oRt1.val())+1);

        var str1 = $(this).parents("li").attr("class").substring(3);

        $('div.prt-lt').each(function(index){
            var str2 = $('div.prt-lt').eq(index).attr('id');

            if (str1===str2) {
                var oRt2 = $(this).find('.result');
                oRt2.val(parseInt(oRt2.val())+1);
            }
        });
        setTotal();
        
    });

    $('#shop-ul').on('click','.minus-a',function (){
        var oRt1 = $(this).parent().find('.result-a');
        oRt1.val(parseInt(oRt1.val())-1);
        if (oRt1.val()==0) {
            oRt1.val(0);
            $(this).parents("li").remove();
        }

        var str1 = $(this).parents("li").attr("class").substring(3);

        $('div.prt-lt').each(function(index){
            var str2 = $('div.prt-lt').eq(index).attr('id');

            if (str1===str2) {
                var oRt2 = $(this).find('.result');
                oRt2.val(parseInt(oRt2.val())-1);
                if (oRt2.val()==0) {
                    oRt2.val(0);
                }
            }
        });
        setTotal();

    });


    $(".minus").click(function () {
        var t = $(this).parent().find('input[class*=result]');
        var oParentId = $(this).parents(".prt-lt").attr("id");
        var ddname = $(this).parent().find('.di-name').text();
        var tval = t.val();
        tval--;
        if (tval<0) {tval=0};
        
        t.val(tval);

        setTotal();

        var oLi = $('#shop-ul').find('.js-'+oParentId);
        if (oLi.length>0) {
        	if (tval != 0) {
        		oLi.find(".result-a").val(tval);
        	}else{
        		// 移除
        		oLi.remove();
        	};
            
        }

    });


    var $changeBtn = $("#change-success")
            , url = '/DiningServer/gotoOrderPage/'
            ;
            
    $changeBtn.on("click", function () {

        // getChoosedMeals();

        var oTr = $('.share').text();
        if ( oTr > 0 ) {
            var $item = $('#container .prt-lt');
            $item.each(function (index,ele){
                var _id = $(ele).attr('id');
                var num = $(ele).find('.result').val();
                if (num > 0) {
                    json[_id] = num;
                };
            });


            StandardPost(url, json);
        }else{
            alert('请您先选择菜品！');
            return false;
        }


    });

    function StandardPost(url,args) {
        var body = $(document.body),
            form = $("<form method='post'></form>"),
            input;
        form.attr({"action":url});
        $.each(args,function(key,value){
            input = $("<input type='hidden'>");
            input.attr({"name":key});
            input.val(value);
            form.append(input);
        });

        form.appendTo(document.body);
        form.submit();
        document.body.removeChild(form[0]);
    }

    function setTotal() {
        var sum = 0;
        var meal_count = 0;
        var category_count = 0;
        //计算总额
        $(".lt-rt").each(function () {
            sum += parseInt($(this).find('input[class*=result]').val()) * parseFloat($(this).siblings().find('span[class*=price]').text());
        });

        //计算菜种-
        var nIn = $("li.current a").attr("href");
        $(nIn + " input[type='text']").each(function () {
            if ($(this).val() != 0) {
                category_count++;
            }
        });

        //计算总份数
        $(".result").each(function () {

            meal_count += parseInt($(this).val());
        });
        if (category_count > 0) {
            $(".current b").html(category_count).show();
        } else {
            $(".current b").hide();
        }
        $(".share").html(meal_count);
        $("#total").html(sum.toFixed(2));
    }
        setTotal();



        // function fnSave(meals){
        //     window.sessionStorage['JJCS'] = meals;
        // }

        // function createMeal(parentId, name, tval){
        //     var meal = new Object();
        //     meal.parentId = parentId;
        //     meal.name = name;
        //     meal.tval;
        //     return meal;
        // }

        // function getChoosedMeals(){
        //     var meals = new Array();
        //     var count = 0;
        //     $(".prt-lt").each(function () {
        //         if($(this).find('.result').val() > 0){
        //             meals[count] = createMeal(
        //                 $(this).attr('id'),
        //                 $(this).find('.di-name').text(),
        //                 $(this).find('.result').val()
        //             );
        //             count ++;
        //         }
        //     });
        //     fnSave(meals);
        // }




        // 存
        function saveSession(name,value){
            var json2 = {};
            json2.data = value;
            window.sessionStorage[name] = JSON.stringify(json2);
        }

        // 取
        function getSession(name){
            var value = window.sessionStorage[name];
            var data = '';
            if (value) {
                data = JSON.parse(value).data;
            };
            return data;
        }
 });



