function pieo(judgeCount)
{
  //  console.log('judgeCount:', judgeCount)
	// 路径配置
	require.config({
		paths: {
			echarts: 'http://echarts.baidu.com/build/dist'
		}
	});
	// 使用
	require(
		[
			'echarts',
			'echarts/chart/pie' // 使用柱状图就加载bar模块，按需加载
		],
		function (ec) {
			// 基于准备好的dom，初始化echarts图表
			var myChart = ec.init(document.getElementById('echartsmap-pie')); 
			
			var option = {
    title : {
        text: '用户评价分布',
        subtext: '菜品评价',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient : 'vertical',
        x : 'left',
        data:['一星','二星','三星','四星','五星']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true, 
                type: ['pie'],
                option: {
                    funnel: {
                        x: '25%',
                        width: '50%',
                        funnelAlign: 'left',
                        max: 1548
                    }
                }
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'访问来源',
            type:'pie',
            radius : '55%',
            center: ['50%', '50%'],
            data:[
                {value:judgeCount.judge_service[0], name:'一星'},
                {value:judgeCount.judge_service[1], name:'二星'},
                {value:judgeCount.judge_service[2], name:'三星'},
                {value:judgeCount.judge_service[3], name:'四星'},
                {value:judgeCount.judge_service[4], name:'五星'}
                ]
            /*data:[
                {value:335, name:'一星'},
                {value:310, name:'二星'},
                {value:234, name:'三星'},
                {value:135, name:'四星'},
                {value:157, name:'五星'}
            ]*/
        }
    ]
};
                    
                    
			// 为echarts对象加载数据 
			myChart.setOption(option); 
			window.onresize=myChart.resize;
		}
	);
}