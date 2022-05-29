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
            var ROOT_PATH = '../../output/vuejs/vue_suffix_line.json';
            var chartDom = document.getElementById('commitSizeLine');
            var myChart = echarts.init(chartDom);
            $.get(ROOT_PATH, function (diskData) {
                var option = {
                    title: {
                        text: 'vuejs/vue'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            label: {
                                backgroundColor: '#6a7985'
                            }
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
                            }
                        }
                    },
                    legend: {
                        data: diskData,
                        top: '3%'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: 'category'
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
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