<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="line" class="chart"></div>
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
            var ROOT_PATH = '../../output/Uahh/Fyzhq_line.json'
            var chartDom = document.getElementById('line');
            var myChart = echarts.init(chartDom);
            var option;

            myChart.showLoading();
            $.get(
                ROOT_PATH,
                function (_rawData) {
                    myChart.hideLoading();
                    run(_rawData);
                }
            );
            function run(_rawData) {
                const countries = [
                    'Uahh/Fyzhq',
                    'Uahh/Slscq',
                ];
                const datasetWithFilters = [];
                const seriesList = [];
                echarts.util.each(countries, function (country) {
                    var datasetId = 'dataset_' + country;
                    datasetWithFilters.push({
                        id: datasetId,
                        fromDatasetId: 'dataset_raw',
                        transform: {
                            type: 'filter',
                            config: {
                                and: [
                                    { dimension: 'Day', gte: 1950 },
                                    { dimension: 'Repo', '=': country }
                                ]
                            }
                        }
                    });
                    seriesList.push({
                        type: 'line',
                        datasetId: datasetId,
                        showSymbol: false,
                        name: country,
                        endLabel: {
                            show: true,
                            formatter: function (params) {
                                return params.value[1] + ': ' + params.value[0];
                            }
                        },
                        labelLayout: {
                            moveOverlap: 'shiftY'
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        encode: {
                            x: 'Day',
                            y: 'Star',
                            label: ['Repo', 'Star'],
                            itemName: 'Day',
                            tooltip: ['Star']
                        }
                    });
                });
                option = {
                    animationDuration: 10000,
                    dataset: [
                        {
                            id: 'dataset_raw',
                            source: _rawData
                        },
                        ...datasetWithFilters
                    ],
                    title: {
                        text: 'Uahh/Fyzhq',
                    },
                    tooltip: {
                        order: 'valueDesc',
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            label: {
                                backgroundColor: '#6A7985',
                                formatter: "date: {value}"
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
                            }
                        }
                    },
                    xAxis: {
                        name: 'Date',
                        type: 'category'
                    },
                    yAxis: {
                        name: 'Star'
                    },
                    grid: {
                        right: 140
                    },
                    series: seriesList
                };
                myChart.setOption(option);
            }

            option && myChart.setOption(option);
        }
    }
}
</script>
 
<style>
</style>