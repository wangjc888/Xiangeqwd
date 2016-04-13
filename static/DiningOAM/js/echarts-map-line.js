function lineo(show_count_info)
//function lineo(userCount)
//function lineo()
{
    // 路径配置
    //console.log('===================')
    //console.log('lineo:',userCount,'type:', typeof userCount);
    //console.log('lineo:',show_count_info,'type:', typeof show_count_info);
    //console.log('data2:',show_count_info.show_date_list,'data3:',show_count_info.daliy_cnt_list)
	require.config({
		paths: {
			echarts: 'http://echarts.baidu.com/build/dist'
		}
	});
	
	// 使用
	require(
		[
			'echarts',
			'echarts/chart/line' // 使用柱状图就加载bar模块，按需加载
		],
		function (ec) {
			// 基于准备好的dom，初始化echarts图表
			var myChart = ec.init(document.getElementById('echartsmap-line')); 
			
			var option = {
    //title : { 			//标题
    //    text: '用户走势图',
    //    subtext: '折线图'
    //},
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        //data:['最高气温','最低气温','哈喽','哈喽123']
        data:['每日用户量', '总的用户量']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            //data : ['周一','周二','周三','周四','周五','周六','周日']
            //data : userCount.show_date_list     //显示时间间隔，每日用户量，和用户总量应该放一起，
            data : show_count_info.show_date_list    //显示时间间隔，每日用户量，和用户总量应该放一起，
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value}'
            }
        }
    ],
    series : [

        {
            name:'每日用户量',
            type:'line',
            data: show_count_info.daliy_cnt_list,
            //data: data3,
            //data : userCount.daliy_cnt_list,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
        {
            name:'总的用户量',
            type:'line',
            //data:userCount.total_cnt_list,
            data : show_count_info.total_cnt_list,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        }
        /*
        {
            name:'最高气温',
            type:'line',
            data:[11, 11, 15, 13, 12, 13, 10],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
        {
            name:'最低气温',
            type:'line',
            data:[1, -2, 2, 5, 3, 2, 0],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        },
        {
            name:'哈喽',
            type:'line',
            data:[3, 2, 1, 0, 2, 3, 4],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        },
        {
            name:'哈喽123',
            type:'line',
            data:[6,5,3,1,-2,5,2],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        }*/

    ]
};
                    
	
			// 为echarts对象加载数据 
			myChart.setOption(option); 
			window.onresize=myChart.resize;
		}
	);
}