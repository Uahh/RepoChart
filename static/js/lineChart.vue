<template>
    <div id="line" class="lineChart"></div>
</template>
 
<script>
module.exports = {
    data() {
        return {
        };
    },
    mounted: function () {
        this.lineEchartsInit();
    },
    methods: {
        lineEchartsInit() {
            var ROOT_PATH = '../../output/itorr/imouto_line.json'
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
                    'itorr/imouto',
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
                        text: 'Star of Germany and France since 1950'
                    },
                    tooltip: {
                        order: 'valueDesc',
                        trigger: 'axis'
                    },
                    xAxis: {
                        type: 'category',
                        nameLocation: 'middle'
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
.lineChart {
    width: 100%;
    height: 800px;
}
</style>