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
            dataStatus: false,
            data: null,
        };
    },
    props: {
        repo: null
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
            this.myChart = echarts.init(document.getElementById('commitSizeLine'))
        },
        run() {
            this.myChart.setOption(this.option());
        },
        getData() {
            let status;
            $.ajax({
                type: "post",
                url: 'http://192.168.31.11:173/check',
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
                    url: 'http://192.168.31.11:173/chartdata',
                    data: {
                        type: 'commit_line',
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
                    text: this.repo
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6A7985',
                            // formatter: "{value}"
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
                    data: this.data,
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
                series: this.data
            };
        }
    }
}
</script>
 
<style>
</style>