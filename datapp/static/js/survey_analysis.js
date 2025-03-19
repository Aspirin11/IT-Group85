document.addEventListener("DOMContentLoaded", function () {
    // Survey Response Chart
    var surveyChart = echarts.init(document.getElementById("surveyResponseChart"));
    var surveyOption = {
        tooltip: {
            trigger: "axis",
            axisPointer: { type: "shadow" }
        },
        grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
        },
        xAxis: {
            type: "category",
            data: surveyData.map(item => item.title),
            axisLabel: { interval: 0, rotate: 30 }
        },
        yAxis: { type: "value", name: "Responses" },
        series: [{
            name: "Responses",
            type: "bar",
            data: surveyData.map(item => item.response_count),
            itemStyle: { color: "#4e73df" }
        }]
    };
    surveyChart.setOption(surveyOption);

    // Question Type Chart
    var questionChart = echarts.init(document.getElementById("questionTypeChart"));
    var questionOption = {
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: "vertical",
            left: 10,
            data: questionTypeData.map(item => item.type)
        },
        series: [{
            name: "Question Types",
            type: "pie",
            radius: ["50%", "70%"],
            avoidLabelOverlap: false,
            label: { show: false, position: "center" },
            emphasis: {
                label: { show: true, fontSize: "16", fontWeight: "bold" }
            },
            labelLine: { show: false },
            data: questionTypeData.map(item => ({ value: item.count, name: item.type }))
        }]
    };
    questionChart.setOption(questionOption);

    // Resize charts when window is resized
    window.addEventListener("resize", function () {
        surveyChart.resize();
        questionChart.resize();
    });
});
