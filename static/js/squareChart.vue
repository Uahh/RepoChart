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
                            <a style="padding: 10px">Order by:</a>
                            <el-radio v-model="radio" label="$commits" border size="medium">
                                commits
                            </el-radio>
                            <el-radio v-model="radio" label="$lines" border size="medium">
                                lines
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
            path: ""
        };
    },
    mounted: function () {
        this.squareEchartsInit();
    },
    methods: {
        squareEchartsInit() {
            var ROOT_PATH = '../../output/vuejs/vue_square.json';
            var chartDom = document.getElementById('square');
            var myChart = echarts.init(chartDom);
            var option;

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
                // myChart.setOption(option = {
                //     series: [
                //         {
                //             title: {
                //                 text: 'Disk Usage',
                //             },
                //             tooltip: {
                //                 formatter: function (info) {
                //                     var value = info.value;
                //                     var treePathInfo = info.treePathInfo;
                //                     var treePath = [];
                //                     for (var i = 1; i < treePathInfo.length; i++) {
                //                         treePath.push(treePathInfo[i].name);
                //                     }
                //                     console.log(echarts.format.addCommas(value))
                //                     return [
                //                         '<div class="tooltip-title">' +
                //                         echarts.format.encodeHTML(treePath.join('/')) +
                //                         '</div>',
                //                         'Disk Usage: ' + echarts.format.addCommas(value) + ' KB'
                //                     ].join('');
                //                 }
                //             },
                //             type: 'sunburst',
                //             id: 'echarts-package-size',
                //             radius: ['20%', '90%'],
                //             animationDurationUpdate: 1000,
                //             nodeClick: undefined,
                //             data: diskData,
                //             universalTransition: true,
                //             itemStyle: {
                //                 borderWidth: 1,
                //                 borderColor: 'rgba(255,255,255,.5)'
                //             },
                //             label: {
                //                 show: false
                //             }
                //         }
                //     ]
                // })
                myChart.setOption(
                    (option = {
                        title: {
                            text: 'Disk Usage',
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
                                    'Disk Usage: ' + echarts.format.addCommas(value) + ' KB'
                                ].join('');
                            }
                        },
                        series: [
                            {
                                name: 'Disk Usage',
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
                    })
                );
            });

            option && myChart.setOption(option);
        },
    }
}
</script>
 
<style>
</style>