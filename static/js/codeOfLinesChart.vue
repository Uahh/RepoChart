<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="codeOfLines" class="chart" style="padding: 0px;"></div>
                <el-row>
                    <el-col :span="12">
                    </el-col>
                    <el-col :span="12">
                    </el-col>
                </el-row>
            </div>
        </el-col>
    </el-row>
</template>
 
<script>
module.exports = {
    data() {
        return {
            protocol: 'http',
            url: window.location.host,
            dataStatus: false,
            data: null,
            image: 'data:image/png;base64,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'
        };
    },
    props: {
        repo: null,
    },
    mounted: function () {
        this.lineEchartsInit();
    },
    methods: {
        lineEchartsInit() {
            this.init()
            this.myChart.showLoading();
            if (this.dataStatus == false) {
                this.times = setInterval(this.getData(), 3000);
            }
        },
        init() {
            this.myChart = echarts.init(document.getElementById('codeOfLines'))
        },
        run() {
            this.myChart.setOption(this.option());
        },
        getData() {
            let status;
            $.ajax({
                type: "post",
                url: this.protocol + '://' + this.url + '/repochart/check',
                data: {
                    repo: this.repo
                },
                async: false,
                success: function (result) {
                    status = result.status;
                }
            })
            if (status == 'True') {
                this.dataStatus = true
                clearInterval(this.times);
                $.ajax({
                    type: "post",
                    url: this.protocol + '://' + this.url + '/repochart/chartdata',
                    data: {
                        type: 'code_of_lines',
                        repo: this.repo
                    },
                    async: false,
                    dataType: 'json',
                    success: (result) => {
                        this.data = result.data;
                        this.run();
                        this.myChart.hideLoading();
                    }
                })
            }
            return this.getData;
        },
        option() {
            return {
                title: {
                    text: this.repo,
                    textStyle: {
                        color: "#EEEEEE"
                    }
                },
                toolbox: {
                    show: true,
                    bottom: '1%',
                    left: '1%',
                    itemSize: 20,
                    feature: {
                        saveAsImage: {
                            show: true
                        },
                        restore: {
                            show: true
                        }
                    }
                },
                backgroundColor: '#0f375f',
                tooltip: {},
                xAxis: [
                    {
                        data: [this.repo, '', 'Uahh/RepoChart', 'tianocore/\nedk2-edkrepo', 'pallets/flask', 'vuejs/vue'],
                        axisTick: { show: false },
                        axisLine: { show: false },
                        axisLabel: {
                            margin: 20,
                            color: '#ddd',
                            fontSize: 14
                        }
                    }
                ],
                yAxis: {
                    splitLine: { show: false },
                    axisTick: { show: false },
                    axisLine: { show: false },
                    axisLabel: { show: false }
                },
                markLine: {
                    z: -1
                },
                animationEasing: 'elasticOut',
                legend: {
                    show: false
                },
                series: [
                    {
                        type: 'pictorialBar',
                        name: 'All',
                        emphasis: {
                            scale: true
                        },
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c} lines',
                            fontSize: 16,
                            color: '#EEEEEE'
                        },
                        data: [
                            {
                                value: this.data,
                                symbol: 'image://' + this.image,
                                symbolRepeat: true,
                                symbolSize: ['100%', '20%'],
                                symbolMargin: '-30%',
                                animationDelay: function (dataIndex, params) {
                                    return params.index * 30;
                                }
                            },
                            {
                                value: '-',
                                symbol: 'none'
                            },
                            {
                                value: 7984,
                                symbol: 'image://' + this.image,
                                symbolRepeat: true,
                                symbolSize: ['50%', '20%'],
                                symbolOffset: [0, 10],
                                symbolMargin: '-30%',
                                animationDelay: function (dataIndex, params) {
                                    return params.index * 30;
                                }
                            },
                            {
                                value: 45208,
                                symbol: 'image://' + this.image,
                                symbolRepeat: true,
                                symbolSize: ['50%', '20%'],
                                symbolOffset: [0, 10],
                                symbolMargin: '-30%',
                                animationDelay: function (dataIndex, params) {
                                    return params.index * 30;
                                }
                            },
                            {
                                value: 71654,
                                symbol: 'image://' + this.image,
                                symbolRepeat: true,
                                symbolSize: ['50%', '20%'],
                                symbolOffset: [0, 10],
                                symbolMargin: '-30%',
                                animationDelay: function (dataIndex, params) {
                                    return params.index * 30;
                                }
                            },
                            {
                                value: 165112,
                                symbol: 'image://' + this.image,
                                symbolRepeat: true,
                                symbolSize: ['50%', '20%'],
                                symbolOffset: [0, 10],
                                symbolMargin: '-30%',
                                animationDelay: function (dataIndex, params) {
                                    return params.index * 30;
                                }
                            }
                        ],
                        markLine: {
                            symbol: ['none', 'none'],
                            label: {
                                show: false
                            },
                            lineStyle: {
                                color: '#e54035',
                                width: 2
                            },
                            data: [
                                {
                                    yAxis: this.data
                                }
                            ]
                        }
                    },
                    {
                        name: 'All',
                        type: 'pictorialBar',
                        barGap: '-100%',
                        symbol: 'circle',
                        itemStyle: {
                            color: '#185491'
                        },
                        silent: true,
                        symbolOffset: [0, '50%'],
                        z: -10,
                        data: [
                            {
                                value: 1,
                                symbolSize: ['100%', 50]
                            },
                            {
                                value: '-'
                            },
                            {
                                value: 1,
                                symbolSize: ['100%', 50]
                            },
                            {
                                value: 1,
                                symbolSize: ['100%', 50]
                            },
                            {
                                value: 1,
                                symbolSize: ['100%', 50]
                            },
                            {
                                value: 1,
                                symbolSize: ['100%', 50]
                            }
                        ]
                    }
                ]
            };
        }
    }
}
</script>
 
<style>
</style>