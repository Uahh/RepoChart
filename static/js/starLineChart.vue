<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="starLine" class="chart"></div>
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
            dataStatus: false,
            data: null,
        };
    },
    props: {
        repo: null,
        server: null,
        protocol: null
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
            this.myChart = echarts.init(document.getElementById('starLine'))
        },
        run() {
            this.myChart.setOption(this.option());
        },
        getData() {
            let status;
            $.ajax({
                type: "post",
                url: this.protocol + '://' + this.server + '/repochart/check',
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
                    url: this.protocol + '://' + this.server + '/repochart/chartdata',
                    data: {
                        type: 'star_line',
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
        },
        option() {
            let repoName = this.repo.split('/')[1]
            const countries = [
                repoName,
            ];
            const datasetWithFilters = [];
            const seriesList = [];
            echarts.util.each(countries, (repoName) => {
                var datasetId = 'dataset_' + repoName;
                datasetWithFilters.push({
                    id: datasetId,
                    fromDatasetId: 'dataset_raw',
                    transform: {
                        type: 'filter',
                        config: {
                            and: [
                                { dimension: 'Day', gte: 1950 },
                                { dimension: 'Repo', '=': repoName }
                            ]
                        }
                    }
                });
                seriesList.push({
                    type: 'line',
                    datasetId: datasetId,
                    showSymbol: false,
                    name: repoName,
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
            return {
                animationDuration: 10000,
                dataset: [
                    {
                        id: 'dataset_raw',
                        source: this.data
                    },
                    ...datasetWithFilters
                ],
                title: {
                    text: this.repo,
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
        }
    }
}
</script>
 
<style>
</style>