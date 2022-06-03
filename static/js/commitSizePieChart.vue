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
                            <el-radio v-model="radio" label="ring" border size="medium" @change="pieEchartsInit(radio)">
                                Ring
                            </el-radio>
                            <el-radio v-model="radio" label="pie" border size="medium" @change="pieEchartsInit(radio)">
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
            title: "",
            path: "",
            radio: "ring"
        };
    },
    mounted: function () {
        this.pieEchartsInit(this.radio);
    },
    methods: {
        pieEchartsInit(radio) {
            var ROOT_PATH = '../../output/Uahh/ToastFish_commit_pie.json';
            var chartDom = document.getElementById('commitSizePie');
            var myChart = echarts.init(chartDom);
            $.get(ROOT_PATH, (data) => {
                var option1 = {
                    title: {
                        text: 'Uahh/ToastFish',
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
                            name: 'Uahh/ToastFish',
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
                            data: data
                        }
                    ]
                };
                var option2 = {
                    title: {
                        text: 'Uahh/ToastFish',
                        // subtext: 'Fake Data',
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
                            name: 'Uahh/ToastFish',
                            type: 'pie',
                            radius: '50%',
                            itemStyle: {
                                borderRadius: 8
                            },
                            data: data,
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
                var curOption;
                if (radio == "ring") {
                    curOption = option1
                }
                else {
                    curOption = option2
                }
                myChart.setOption(curOption, true);
            })
        }
    }
}
</script>
 
<style>
</style>