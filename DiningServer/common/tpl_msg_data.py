'''微信模板消息数据'''
(red, green, gold, black) = ("#FF0000", "#008000", "#C4C400", "#173177")


'''ID: X-1HSV69BTa03E5gj-ySu7sao7_N9Cx9EuLIlZzIYDI'''
welcom_data = {
			 "first": {
				 "value":"欢迎光临，请尽情选购各种美食！",
				 "color":green
			 },
			 "keyword1":{
				 "value":"家家长沙米粉",
				 "color":black
			 },
			 "keyword2": {
				 "value":"各种优惠活动正在制定中，敬请期待！",
				 "color":black
			 },	
			 "remark":{
				 "value":"温馨提示：请首先填写送餐信息以便准确的推送最近店面！",
				 "color":red
			 }
		  }

'''ID: HRECa6Gb9oRqcHS-G7krnT5_bqBsOgYJsKwga52O0xE'''
accept_data = {
			 "first": {
				 "value":"恭喜，店家已经接受订单！",
				 "color":green
			 },
			 "keyword1":{
				 "value":"餐厅",
				 "color":black
			 },
			 "keyword2": {
				 "value":"下单时间",
				 "color":black
			 },
			 "keyword3": {
				 "value":"菜品",
				 "color":black
			 },

			 "keyword4": {
				 "value":"金额",
				 "color":gold
			 },
			 "remark":{
				 "value":"小店正在玩命备餐中，请耐心等候送餐小哥(づ￣ 3￣)づ",
				 "color":green
			 }
		  }


'''ID: 6E5y5UZsExW45VywamzEzk7eyf8eOM1KXKSzJyU5NHQ'''
deny_data = {
			 "first": {
				 "value":"抱歉，请另选其她菜品o(^▽^)o",
				 "color":red
			 },
			 "keyword1":{
				 "value":"订单编号",
				 "color":black
			 },
			 "keyword2": {
				 "value":"下单时间",
				 "color":black
			 },
			 "keyword3": {
				 "value":"拒绝时间",
				 "color":black
			 },

			 "keyword4": {
				 "value":"所选菜品已经售完",
				 "color":red
			 },
			 "remark":{
				 "value":"已通过微信平台退款。退款有一定延时，零钱支付的退款20分钟内到账，银行卡支付的退款3个工作日后到账",
				 "color":green
			 }
		  }
