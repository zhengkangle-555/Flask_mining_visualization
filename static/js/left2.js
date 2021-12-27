var left2 = echarts.init(document.getElementById("l2"),"dark");


var left2_option;



left2_option = {
    title: {
        text: '人数和经验',
        subtext: '数据来自51job',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            // restore: {show: true}
            // saveAsImage: {show: False}
        }
    },
    legend: {
        data: ['人数','平均经验'],
        left: 'left'
    },
    xAxis: [
        {
            type: 'category',
            // data: ['高中', '中专', '大专', '本科', '硕士', '博士'],
            data: [],
            axisPointer: {
                type: 'shadow'
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '人数',
            // min: 0,
            // max: 12000,
            // interval: 1000,
            axisLabel: {
                formatter: '{value}'
            }
        },
        {
            type: 'value',
            name: '平均经验',
            // min: 0,
            // max: 3,
            // interval: 0.5,
            axisLabel: {
                formatter: '{value}'
            }
        }
    ],
    series: [
        {
            name: '人数',
            type: 'bar',
            // data: [217, 89, 8980, 11367, 1279, 115]
            data: []
        },
        {
            name: '平均经验',
            type: 'line',
            yAxisIndex: 1,
            // data: [0.43, 0.71, 1.14, 2.87, 2.24, 1.78]
            data: []
        }
    ]
};

left2.setOption(left2_option);
