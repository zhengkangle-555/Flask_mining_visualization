var right1 = document.getElementById("r1");
var ec_right1 = echarts.init(right1, 'dark');

var right1_option;



right1_option = {
    title: {
        text: '公司类型',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '14%',
        left: 'left',
        orient: 'vertical'
    },
    series: [
        {
            name: '公司类型',
            top: '0%',
            left: '12%',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '20',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [
//                 {value: 7036, name: '民营公司'},
//                 {value: 928, name: '上市公司'},
//                 {value: 629, name: '国企'},
//                 {value: 464, name: '合资'},
//                 {value: 308, name: '外资（非欧美）'}
            ]
        }
    ]
};

if (right1_option && typeof right1_option === 'object') {
    ec_right1.setOption(right1_option);
}