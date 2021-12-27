var left1 = echarts.init(document.getElementById("l1"),"dark");

var left1_option;


left1_option = {
    title: {
        text: '公司数和薪资',
        subtext: '数据来自51job',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false
        }
    },
    legend: {
        data: ['公司数', '薪资'],
        left: 'left'
    },
    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            // restore: {}
        }
    },
    axisPointer: {
        link: {xAxisIndex: 'all'}
    },
    dataZoom: [
        {
            show: true,
            realtime: true,
            start: 30,
            end: 70,
            xAxisIndex: [0, 1]
        },
        {
            type: 'inside',
            realtime: true,
            start: 30,
            end: 70,
            xAxisIndex: [0, 1]
        }
    ],
    grid: [{
        left: 50,
        right: 50,
        height: '35%'
    }, {
        left: 50,
        right: 50,
        top: '55%',
        height: '35%'
    }],
    xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            axisLine: {onZero: true},
            // data: ['高中', '中专', '大专', '本科', '硕士', '博士'],
            data: []
        },
        {
            gridIndex: 1,
            type: 'category',
            boundaryGap: false,
            axisLine: {onZero: true},
            data: [],
            position: 'top'
        }
    ],
    yAxis: [
        {
            name: '公司数',
            type: 'value',
            // max: 5500
        },
        {
            gridIndex: 1,
            name: '薪资',
            type: 'value',
            inverse: true,
            // max: 30,
            // min: 5
        }
    ],
    series: [
        {
            name: '公司数',
            type: 'line',
            symbolSize: 8,
            hoverAnimation: false,
            // data: [65, 42, 3394, 5493, 693, 68],
            data: []
        },
        {
            name: '薪资',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            symbolSize: 8,
            hoverAnimation: false,
            // data: [8.37, 8.6, 10.32, 16.7, 20.03, 28.59],
            data: []
        }
    ]
};

left1.setOption(left1_option)
