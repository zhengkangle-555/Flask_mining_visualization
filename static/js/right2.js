var right2 = echarts3.init(document.getElementById("r2"), "dark");

var datamessage = [];
var option_right2 = {
	title: {
		text: "数据挖掘岗位词云图",
		textStyle: {
			color: 'white'
		},
		left: 'left'
	},
	tooltip: {
		show: false
	},
	series: [{
		type: 'wordCloud',
		shape: 'diamond',
		left: 'center',
		top: 'center',
		right: null,
		bottom: null,
		width: '100%',
		height: '100%',
		sizeRange: [12, 60],
		rotationRange: [-90, 90],
		rotationStep: 45,
		gridSize: 8,
		drawOutOfBound: false,
		textStyle: {
			normal: {
				fontFamily: 'sans-serif',
				fontWeight: 'normal',
				color: function () {
					return 'rgb(' + [
                    Math.round(Math.random() * 256),
                    Math.round(Math.random() * 256),
                    Math.round(Math.random() * 256)
                ].join(',') + ')';
				}
				},
			emphasis: {
				shadowBlur: 12,
				shadowColor: '#333'
			}
		},
		data: datamessage
	}]

};
//使用制定的配置项和数据显示图表
right2.setOption(option_right2);
