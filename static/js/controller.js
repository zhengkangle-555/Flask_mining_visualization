// 使用ajax来动态获取时间
function get_time() {
    $.ajax({
        url: '/time',
        timeout: 1000,
        success: function (data) {
            $('#time').html(data)
        },
        error: function (xhr, type, errorThrown) {
        }
    })
}

function get_title() {
    $.ajax({
        url: '/title',
        success: function (data) {
            $('title').html('全国' + data + '岗位就业可视化系统')
            $('#title').html('全国' + data + '岗位就业可视化系统')
        },
        error: function (xhr, type, errorThrown) {
        }
    })
}

function get_c1_data() {
    $.ajax({
        url: '/c1',
        // timeout: 10000,
        success: function (data) {
//          eq表示选择第几个h1下面的标签
            $('.num h1').eq(0).text(data.employ),
            $('.num h1').eq(1).text(data.avg_salary),
            $('.num h1').eq(2).text(data.province),
            $('.num h1').eq(3).text(data.edu)
        },
        error: function (xhr, type, errorThrown) {
        }
    })
}

// 下面的逻辑其实都差不多，都是使用ajax获取从数据库中的数据，再对每张图的js中的echarts对象中的data赋值
function get_c2_data() {
    $.ajax({
        url:"/c2",
        // timeout: 10000,
        success: function(data) {
            optionMap.series[0].data = data.data,
            center.setOption(optionMap)
        },
        error: function(xhr, type, errorThrown) {
        }
    })
}

// function get_l1_data() {
//     $.ajax({
//         url:"/l1",
//         success: function(data) {
//             option_left1.xAxis.data = data.edu,
//             option_left1.series[0].data = data.avg_salary,
//             left1.setOption(option_left1)
//         },
//         error: function(xhr, type, errorThrown) {
//         }
//     })
// }

function get_l1_data() {
    $.ajax({
        url:"/l1",
        success: function(data) {
            left1_option.xAxis[0].data = data.edu;
            left1_option.xAxis[1].data = data.edu;
            left1_option.series[0].data = data.sum_company,
            left1_option.series[1].data = data.avg_salary,
            left1.setOption(left1_option)
        },
        error: function(xhr, type, errorThrown) {
        }
    })
}

function get_l2_data() {
	$.ajax({
		url:"/l2",
		success: function(data) {
			left2_option.xAxis[0].data = data.edu,
            left2_option.series[0].data = data.num,
            left2_option.series[1].data = data.exp,
			left2.setOption(left2_option)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function get_r1_data() {
    $.ajax({
        url:"/r1",
        // timeout: 10000,
        success: function(data) {
            right1_option.series[0].data = data.data,
            ec_right1.setOption(right1_option)
        },
        error: function(xhr, type, errorThrown) {
        }
    })
}

function get_r2_data() {
	$.ajax({
		url:"/r2",
		success: function(data) {
			option_right2.series[0].data = data.kws,
			right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

// 注意定义完函数之后要调用才会生效
get_time()
get_title()
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()
setInterval(get_time, 1000)
// 设置词云每隔10s钟从数据库更新一次
setInterval(get_r2_data, 1000 * 10)

