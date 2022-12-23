<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="commitSizePie" class="chart"></div>
                <el-row>
                    <el-col :span="12">
                    </el-col>
                    <el-col :span="12">
                        <div class="radio">
                            <a style="padding: 10px">Order by:</a>
                            <el-radio v-model="radio" label="ring" border size="medium" @change="run()">
                                Ring
                            </el-radio>
                            <el-radio v-model="radio" label="pie" border size="medium" @change="run()">
                                Pie
                            </el-radio>
                        </div>
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
            radio: "ring",
            dataStatus: false,
            data: null,
        };
    },
    props: {
        repo: null,
    },
    mounted: function () {
        this.pieEchartsInit();
    },
    methods: {
        pieEchartsInit() {
            this.init()
            this.myChart.showLoading();
            if (this.dataStatus == false) {
                this.times = setInterval(this.getData(), 3000);
            }
        },
        init() {
            this.myChart = echarts.init(document.getElementById('commitSizePie'))
        },
        run() {
            if (this.radio == "ring") {
                this.myChart.setOption(this.ringOption());
            }
            else {
                this.myChart.setOption(this.pieOption());
            }
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
                        type: 'commit_pie',
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
        ringOption() {
            return {
                title: {
                    text: this.repo,
                },
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '3%',
                    left: 'center'
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
                series: [
                    {
                        name: this.repo,
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: '{a} <br/>{b} : {c} ({d}%)'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '40',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: this.data
                    }
                ]
            }
        },
        pieOption() {
            return {
                title: {
                    text: this.repo,
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                legend: {
                    top: '3%',
                    left: 'center'
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
                series: [
                    {
                        name: this.repo,
                        type: 'pie',
                        radius: '65%',
                        itemStyle: {
                            borderRadius: 8
                        },
                        data: this.data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
        }
    }
}
</script>
 
<style>
</style>