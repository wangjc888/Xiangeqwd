function baro(stateSheet)
{
	// 路径配置
    console.log('stateSheet', stateSheet);
	require.config({
		paths:{
			echarts:'http://echarts.baidu.com/build/dist'
		}
	});
	// 使用
	require(
		[
			'echarts',
			'echarts/chart/bar' // 使用柱状图就加载bar模块，按需加载
		],
		function (ec) {
			// 基于准备好的dom，初始化echarts图表
			var myChart = ec.init(document.getElementById('echartsmap-report'));
			
			var option = {
                tooltip : {
                    show: true,
                    trigger: 'item'
                },
                legend: {
                    //data:['邮件营销','联盟广告','直接访问','搜索引擎']
                    data:['销售总金额(单位：元)','销售菜品总数(单位：份)']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        //data : ['周一','周二','周三','周四','周五','周六','周日']
                        data:stateSheet.house_name
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'销售总金额(单位：元)',
                        type:'bar',
                        barWidth: 40,                   // 系列级个性化，柱形宽度
                        itemStyle: {
                            normal: {                   // 系列级个性化，横向渐变填充
                                borderRadius: 5,
                                color : (function (){
                                    var zrColor = require('zrender/tool/color');
                                    return zrColor.getLinearGradient(
                                        0, 0, 1000, 0,
                                        [[0, 'rgba(30,144,255,0.8)'],[1, 'rgba(138,43,226,0.8)']]
                                    )
                                })(),
                                label : {
                                    show : true,
                                    textStyle : {
                                        fontSize : '14',
                                        fontFamily : '微软雅黑',
                                        fontWeight : 'bold'
                                    }
                                }
                            }
                        },
                        data:stateSheet.total_amount,
                        /*
                        data:[
                            620, 732,
                            {
                                value: 701,
                                itemStyle : { normal: {label : {position: 'top'}}}
                            },
                            734, 890, 930, 820
                        ],*/
                        markLine : {
                            data : [
                                {type : 'average', name : '平均值'},
                                {type : 'max'},
                                {type : 'min'}
                            ]
                        }
                    },
                    {
                        name:'销售菜品总数(单位：份)',
                        type:'bar',
                        barWidth: 40,//add by ljz
                        stack: '总量',
                        itemStyle: {// 系列级个性化
                            normal: {
                                barBorderWidth: 6,
                                barBorderColor:'tomato',
                                color: 'red',
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle : {
                                        fontSize : '14',
                                        fontFamily : '微软雅黑',
                                        fontWeight : 'bold'
                                    }
                                }
                            },
                            emphasis: {
                                barBorderColor:'red',
                                color: 'blue'
                            }
                        },
                        data:stateSheet.total_sold_cnt
                        /*
                        data:[
                            320, 332, 100, 334,
                            {
                                value: 390,
                                symbolSize : 10,   // 数据级个性化
                                itemStyle: {
                                    normal: {
                                        color :'lime'
                                    },
                                    emphasis: {
                                        color: 'skyBlue'
                                    }
                                }
                            },
                            330, 320
                        ]*/
                    }
                    /*,
                    {
                        name:'最受欢迎菜品',
                        type:'bar',
                        itemStyle: {        // 系列级个性化样式，纵向渐变填充
                            normal: {
                                barBorderColor:'red',
                                barBorderWidth: 5,
                                color : (function (){
                                    var zrColor = require('zrender/tool/color');
                                    return zrColor.getLinearGradient(
                                        0, 400, 0, 300,
                                        [[0, 'green'],[1, 'yellow']]
                                    )
                                })()
                            },
                            emphasis: {
                                barBorderWidth: 5,
                                barBorderColor:'green',
                                color: (function (){
                                    var zrColor = require('zrender/tool/color');
                                    return zrColor.getLinearGradient(
                                        0, 400, 0, 300,
                                        [[0, 'red'],[1, 'orange']]
                                    )
                                })(),
                                label : {
                                    show : true,
                                    position : 'top',
                                    formatter : "{a} {b} {c}",
                                    textStyle : {
                                        color: 'blue'
                                    }
                                }
                            }
                        },
                        //data:[220, 232, 101, 234, 190, 330, 210]
                        data:stateSheet.popular_meal
                    },
                    {
                        name:'整体评价',
                        type:'bar',
                        stack: '总量',
                        //data:[120, '-', 451, 134, 190, 230, 110]
                        data: stateSheet.total_judge
                    }*/
                ]
            };

			// 为echarts对象加载数据 
			myChart.setOption(option); 
			window.onresize=myChart.resize;
		}
	);
}