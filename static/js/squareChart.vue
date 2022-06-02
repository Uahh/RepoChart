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
                            <el-radio v-model="radio" label="square" border size="medium"
                                @change="squareEchartsInit(radio)">
                                Square
                            </el-radio>
                            <el-radio v-model="radio" label="sunset" border size="medium"
                                @change="squareEchartsInit(radio)">
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
            title: "",
            path: "",
            radio: "square",
        };
    },
    mounted: function () {
        this.squareEchartsInit(this.radio);
    },
    methods: {
        squareEchartsInit(radio) {
            var ROOT_PATH = '../../output/Uahh/Fyzhq_square.json';
            var chartDom = document.getElementById('square');
            var myChart = echarts.init(chartDom);
            console.log(radio)
            myChart.showLoading();
            $.get(ROOT_PATH, function (diskData) {
                myChart.hideLoading();
                function getLevelOption() {
                    return [
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
                    ];
                }
                function getSunsetLevelOption() {
                    return [
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
                }
                var sunsetOption = {
                    title: {
                        text: 'Uahh/Fyzhq',
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
                            id: 'echarts-package-size',
                            radius: ['0%', '95%'],
                            animationDurationUpdate: 1000,
                            // nodeClick: undefined,
                            data: diskData,
                            universalTransition: true,
                            itemStyle: {
                                borderWidth: 1,
                                borderColor: 'rgba(255,255,255,.5)'
                            },
                            levels: getSunsetLevelOption(),
                        }
                    ]
                }
                var squareOption = {
                    title: {
                        text: 'Uahh/Fyzhq',
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
                            name: 'Uahh/Fyzhq',
                            type: 'treemap',
                            visibleMin: 300,
                            // leafDepth: 5,
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
                            levels: getLevelOption(),
                            data: diskData
                        }
                    ]
                }
                var curOption;
                if (radio == "square") {
                    curOption = squareOption
                    console.log(1)
                }
                else {
                    curOption = sunsetOption
                    console.log(2)
                }
                myChart.setOption(curOption, true);
            })
        },
    }
}
</script>
 
<style>
</style>