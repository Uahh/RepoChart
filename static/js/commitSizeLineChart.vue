<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="commitSizeLine" class="chart"></div>
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
            title: "",
            path: ""
        };
    },
    mounted: function () {
        this.lineEchartsInit();
    },
    methods: {
        lineEchartsInit() {
            var ROOT_PATH = '../../output/Uahh/ToastFish_commit_line.json';
            var chartDom = document.getElementById('commitSizeLine');
            var myChart = echarts.init(chartDom);
            $.get(ROOT_PATH, (diskData) => {
                var option = {
                    title: {
                        text: 'Uahh/ToastFish'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            label: {
                                backgroundColor: '#6A7985',
                                formatter: "commits order: {value}"
                            },
                        },
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
                    legend: {
                        data: diskData,
                        top: '3%'
                    },
                    xAxis: [
                        {
                            name: 'commit',
                            type: 'category'
                        }
                    ],
                    yAxis: [
                        {
                            name: 'byte',
                            type: 'value'
                        }
                    ],
                    dataZoom: [
                        {
                            type: 'inside'
                        },
                        {
                            type: 'slider',
                            xAxisIndex: [0],
                            filterMode: 'filter'
                        }
                    ],
                    series: diskData
                };
                myChart.setOption(option);
            })
        }
    }
}
</script>
 
<style>
</style>