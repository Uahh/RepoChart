<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="activeLine" class="chart"></div>
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
            max: -1,
            min: 0xffffff
        };
    },
    props: {
        repo: null,
        server: null
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
            this.myChart = echarts.init(document.getElementById('activeLine'))
        },
        run() {
            this.myChart.setOption(this.option());
        },
        getData() {
            let status;
            $.ajax({
                type: "post",
                url: 'http://' + this.server + '/repochart/check',
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
                    url: 'http://' + this.server + '/repochart/chartdata',
                    data: {
                        type: 'active_line',
                        repo: this.repo
                    },
                    async: false,
                    dataType: 'json',
                    success: (result) => {
                        this.data = result.data;
                        for (let i = 0; i < this.data.length; i++) {
                            if (this.data[i][1] > this.max)
                                this.max = this.data[i][1]
                            if (this.data[i][1] < this.min)
                                this.min = this.data[i][1]
                        }
                        console.log(this.max)
                        console.log(this.min)
                        console.log(this.data)
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
                visualMap: [
                    {
                        show: false,
                        type: 'continuous',
                        seriesIndex: 0,
                        min: this.min,
                        max: this.max
                    }
                ],
                tooltip: {
                    trigger: 'axis'
                },
                xAxis: [
                    {
                        name: 'date',
                        data: this.dataList()
                    }
                ],
                yAxis: [
                    {
                        name: 'commits',
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
                series: [
                    {
                        type: 'line',
                        showSymbol: false,
                        data: this.valueList()
                    }
                ]
            };
        },
        dataList() {
            return this.data.map((item) => {
                return item[0];
            });
        },
        valueList() {
            return this.data.map((item) => {
                return item[1];
            });
        }
    }
}
</script>
 
<style>
</style>