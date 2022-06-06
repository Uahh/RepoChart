<template>
    <el-row>
        <el-col :span="24">
            <div class="chart-region">
                <div id="square" class="chart"></div>
                <el-row>
                    <el-col :span="12">
                    </el-col>
                    <el-col :span="12">
                        <div class="radio">
                            <a style="padding: 10px">Style:</a>
                            <el-radio v-model="radio" label="square" border size="medium" @change="run()">
                                Square
                            </el-radio>
                            <el-radio v-model="radio" label="sunset" border size="medium" @change="run()">
                                Sunset
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
            radio: "square",
            dataStatus: false,
            data: null,
            // myChart: null,
            getLevelOption: [
                {
                    itemStyle: {
                        borderColor: '#333',
                        borderWidth: 0,
                        gapWidth: 1,
                    },
                    upperLabel: {
                        show: false
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#444',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#555',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#666',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#777',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#888',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#999',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#AAA',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#BBB',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    itemStyle: {
                        borderColor: '#CCC',
                        borderWidth: 5,
                        gapWidth: 1
                    },
                    emphasis: {
                        itemStyle: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    colorSaturation: [0.35, 1],
                    itemStyle: {
                        borderWidth: 5,
                        gapWidth: 1,
                        borderColorSaturation: 0.6
                    }
                }
            ],
            getSunsetLevelOption: [
                {},
                {
                    itemStyle: {
                        borderWidth: 2
                    },
                    label: {
                        minAngle: 360,
                        rotate: 'tangential',
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
                {
                    label: {
                        minAngle: 360,
                        position: 'outside',
                        padding: 3,
                        silent: false
                    },
                    itemStyle: {
                        borderWidth: 3
                    }
                },
            ]
        };
    },
    props: {
        repo: null
    },
    mounted: function () {
        this.squareEchartsInit();
    },
    methods: {
        squareEchartsInit() {
            this.init()
            this.myChart.showLoading();
            if (this.dataStatus == false) {
                this.times = setInterval(this.getData(), 3000);
            }
        },
        init() {
            this.myChart = echarts.init(document.getElementById('square'))
        },
        run() {
            if (this.radio == "square") {
                this.myChart.setOption(this.squareOption());
            }
            else {
                this.myChart.setOption(this.sunsetOption());
            }
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
                        type: 'square',
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
        squareOption() {
            return {
                title: {
                    text: this.repo,
                },
                tooltip: {
                    formatter: function (info) {
                        var value = info.value;
                        var treePathInfo = info.treePathInfo;
                        var treePath = [];
                        for (var i = 1; i < treePathInfo.length; i++) {
                            treePath.push(treePathInfo[i].name);
                        }
                        return [
                            '<div class="tooltip-title">' +
                            echarts.format.encodeHTML(treePath.join('/')) +
                            '</div>',
                            echarts.format.addCommas(value) + ' KB'
                        ].join('');
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
                series: [
                    {
                        type: 'treemap',
                        visibleMin: 300,
                        animationDurationUpdate: 1000,
                        universalTransition: true,
                        label: {
                            show: true,
                            formatter: '{b}'
                        },
                        upperLabel: {
                            show: true,
                            height: 30
                        },
                        itemStyle: {
                            borderWidth: 5
                        },
                        levels: this.getLevelOption,
                        data: this.data
                    }
                ]
            }
        },
        sunsetOption() {
            return {
                title: {
                    text: this.repo,
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
                series: [
                    {
                        type: 'sunburst',
                        radius: ['0%', '95%'],
                        animationDurationUpdate: 1000,
                        universalTransition: true,
                        itemStyle: {
                            borderWidth: 1,
                            borderColor: 'rgba(255,255,255,.5)'
                        },
                        levels: this.getSunsetLevelOption,
                        data: this.data,
                    }
                ]
            }
        },
    }
}
</script>
 
<style>
</style>